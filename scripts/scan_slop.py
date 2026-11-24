#!/usr/bin/env python3
"""Textual triage for AI-design tells. Stdlib only; never fails a build.

Usage:
    python3 scan_slop.py <path> [--json] [--max-evidence N]

Scans source files for the textual signatures of the 20 indicators in the
no-ai-slop skill. Findings are candidates, not verdicts: a human (or the
Claude using this skill) must confirm them against rendered context.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field

SKIP_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "dist", "build", ".next",
    ".nuxt", "__pycache__", ".venv", "venv", "vendor", ".cache",
    "coverage", ".turbo", ".svelte-kit",
}
EXTENSIONS = {
    ".html", ".htm", ".css", ".scss", ".sass", ".less",
    ".js", ".jsx", ".mjs", ".ts", ".tsx", ".vue", ".svelte",
    ".md", ".mdx",
}


@dataclass
class Indicator:
    id: str
    name: str
    weight: int
    patterns: list[str]
    min_hits: int = 1
    require: list[str] = field(default_factory=list)
    note: str = ""
    case_sensitive: bool = False

    @property
    def severity(self) -> str:
        return "high" if self.weight >= 7 else "medium" if self.weight >= 5 else "low"

    def compiled(self) -> list[re.Pattern[str]]:
        flags = re.MULTILINE | (0 if self.case_sensitive else re.IGNORECASE)
        return [re.compile(p, flags) for p in self.patterns]

    def required(self) -> list[re.Pattern[str]]:
        return [re.compile(p, re.IGNORECASE | re.MULTILINE) for p in self.require]


INDICATORS: list[Indicator] = [
    Indicator("arrows", "Arrows on every button", 5,
              [r"→", r"↗", r"ArrowRight", r"arrow-right", r"chevron-right", r"fa-arrow"],
              min_hits=2, note="Only a problem when repeated across CTAs."),
    Indicator("dots", "Little dots between words", 3,
              [r"\w\s*(?:·|•|&middot;)\s*\w"]),
    Indicator("eyebrows", "Overusing eyebrows", 3,
              [r"\beyebrow\b", r"\boverline\b", r"\bkicker\b",
               r"uppercase[^;\n]{0,40}tracking-(?:wide|wider|widest)"],
              note="One kicker is fine; check whether every section has one."),
    Indicator("cream", "Cream backgrounds", 5,
              [r"#(?:faf6ef|fdfbf7|f5f0e6|faf7f0|fffcf5|f9f6f0|fdf8f0|f8f4ec|f4efe6)\b",
               r"\b(?:cream|ivory|bone|parchment)\b"],
              note="Flag a global wash, not an accent panel."),
    Indicator("italic_headline", "One italic word in the headline", 5,
              [r"<h[1-6][^>]*>.{0,180}?(?:<em\b|italic)",
               r"(?:<em\b|italic).{0,180}?</h[1-6]>"]),
    Indicator("sparkles", "Sparkle icons", 5,
              [r"✨", r"\bSparkles\b", r"\bsparkles\b", r"ai-sparkle", r"magic-wand"]),
    Indicator("cards", "Everything in a card", 7,
              [r"\bcard\b", r"rounded-(?:xl|2xl|3xl)", r"shadow-(?:sm|md|lg|xl|2xl)"],
              min_hits=4, note="Count is per file; check other sections before confirming."),
    Indicator("quiet", 'The word "quiet"', 3, [r"\bquiet(?:er|ly|eness)?\b"]),
    Indicator("numbered_sections", "Numbered sections", 5,
              [r"(?:^|[\"'>\s])(?:0[1-9])\s*(?:/|[-–—]|\.)\s*[A-Z]"]),
    Indicator("green_dots", "Pulsing green dots", 5,
              [r"(?:animate-)?pulse[^\n]{0,140}(?:green|emerald|#22c55e|#4ade80|#16a34a)",
               r"(?:green|emerald|#22c55e|#4ade80|#16a34a)[^\n]{0,140}(?:animate-)?pulse"],
              require=[r"pulse", r"green|emerald|#22c55e|#4ade80|#16a34a"],
              note="Confirm the pulse is bound to live status; a static dot is only decorative."),
    Indicator("glows", "Blurry glows behind the hero", 7,
              [r"blur-(?:2xl|3xl)", r"filter:\s*blur\s*\(", r"radial-gradient",
               r"\bglow\b", r"backdrop-blur"]),
    Indicator("instrument_serif", "Instrument Serif", 5,
              [r"instrument[ _-]?serif"]),
    Indicator("left_borders", "Colored left borders", 5,
              [r"border-l-(?:2|4|8|\[)", r"border-left:\s*[1-9]\d*px"]),
    Indicator("three_cards", "Three icon cards in a row", 7,
              [r"grid-cols-3", r"md:grid-cols-3", r"lg:grid-cols-3", r"columns-3"],
              require=[r"\bcard\b|\bicon\b|rounded-(?:lg|xl|2xl)"]),
    Indicator("pills", "Pills above the headline", 5,
              [r"rounded-full", r"\bpill\b", r"border-radius:\s*9999?px"],
              require=[r"<h[12]\b|heading|title"],
              note="Confirm the capsule sits above a heading; also check screenshots."),
    Indicator("real", 'The word "real"', 3, [r"\breal(?:ly)?\b"]),
    Indicator("stats", "Made-up stats", 7,
              [r"(?<!: )\b\d{1,3}%\b", r"\b\d+(?:\.\d+)?x\b",
               r"\b[\d,]{2,8}\+?\s*(?:users\b|teams\b|customers\b|faster\b|hours\b|days\b)"],
              note="Verify source and methodology before counting as confirmed."),
    Indicator("two_word", "Two-word sentences", 7,
              [r"(?:^|[\"'>\s])([A-Z][a-z]{1,12}\s+[a-z]{1,14})\.(?=\s|<|$)"],
              case_sensitive=True),
    Indicator("fade_scroll", "Sections fading on scroll", 5,
              [r"opacity-0", r"\bfade-in\b", r"IntersectionObserver",
               r"whileInView", r"reveal-on-scroll", r"scroll-reveal"]),
    Indicator("dither", "Dithering", 3,
              [r"\bdither\w*\b", r"feTurbulence", r"noise[-\s]?(?:png|svg|texture)", r"\bgrain\b"]),
]


def iter_files(path: str):
    if os.path.isfile(path):
        if os.path.splitext(path)[1].lower() in EXTENSIONS:
            yield path
        return
    for root, dirs, files in os.walk(path):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            if os.path.splitext(name)[1].lower() in EXTENSIONS:
                yield os.path.join(root, name)


def scan(path: str, max_evidence: int) -> dict:
    findings = {ind.id: {"hits": 0, "files": set(), "evidence": []} for ind in INDICATORS}
    compiled = {ind.id: ind.compiled() for ind in INDICATORS}
    required = {ind.id: ind.required() for ind in INDICATORS}

    for file_path in iter_files(path):
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as handle:
                lines = handle.readlines()
        except OSError:
            continue
        text = "".join(lines)
        for ind in INDICATORS:
            if required[ind.id] and not any(rx.search(text) for rx in required[ind.id]):
                continue
            for lineno, line in enumerate(lines, 1):
                snippet = line.strip()
                if not snippet:
                    continue
                matched = False
                for rx in compiled[ind.id]:
                    if rx.search(snippet):
                        matched = True
                        break
                if not matched:
                    continue
                record = findings[ind.id]
                record["hits"] += 1
                record["files"].add(file_path)
                if len(record["evidence"]) < max_evidence:
                    record["evidence"].append({
                        "file": file_path,
                        "line": lineno,
                        "text": snippet[:160],
                    })

    confirmed = []
    for ind in INDICATORS:
        record = findings[ind.id]
        if record["hits"] >= ind.min_hits:
            confirmed.append({
                "id": ind.id,
                "name": ind.name,
                "severity": ind.severity,
                "weight": ind.weight,
                "hits": record["hits"],
                "file_count": len(record["files"]),
                "evidence": record["evidence"],
                "note": ind.note,
            })
    confirmed.sort(key=lambda f: (-f["weight"], -f["hits"]))
    score = max(0, 100 - sum(f["weight"] for f in confirmed))
    verdict = "clean" if score >= 90 else "needs polish" if score >= 70 else "reads as generated"
    return {"path": path, "score": score, "verdict": verdict, "findings": confirmed}


def print_table(result: dict) -> None:
    print(f"Slop scan: {result['path']}")
    print(f"Score: {result['score']}/100 ({result['verdict']})")
    print("Triage only: cross-check all 20 indicators manually and against a render.\n")
    if not result["findings"]:
        print("No textual tells found. Check the rendered design visually too.")
        return
    print(f"{'Indicator':34} {'Sev':7} {'Hits':>5}  First evidence")
    print("-" * 96)
    for f in result["findings"]:
        ev = f["evidence"][0]
        location = f"{ev['file']}:{ev['line']}"
        print(f"{f['name'][:34]:34} {f['severity']:7} {f['hits']:>5}  {location}")
        print(f"{'':34} {'':7} {'':5}  {ev['text'][:88]}")
        if f["note"]:
            print(f"{'':34} {'':7} {'':5}  note: {f['note']}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", help="file or directory to scan")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    parser.add_argument("--max-evidence", type=int, default=3, help="evidence rows per indicator")
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"scan_slop.py: no such path: {args.path}", file=sys.stderr)
        return 1

    result = scan(args.path, args.max_evidence)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_table(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
