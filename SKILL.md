---
name: no-ai-slop
description: Audit and rewrite UI and design work so it does not read as generic AI-generated slop. Use this whenever you are about to write, review, or ship HTML, CSS, React/JSX, Vue, Tailwind, a landing page, a marketing site, a dashboard, or any screen design. Also use when the user says "AI slop", "make it not look AI-generated", "does this look generic?", "design taste check", "review the visuals", or asks for a second pass on visual quality. Use proactively before presenting any UI code to a user, even if they did not explicitly request a review — it is much cheaper to catch these tells before shipping than after.
argument-hint: "<file-or-code> [--rewrite]"
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
license: MIT
---

# No AI Slop

A design taste check. It catches the visual, typographic, and copywriting habits that make generated interfaces look machine-made, then shows how to replace them with deliberate choices.

The point is not to ban any single pattern forever. The point is that these patterns are the *statistical defaults* of generative models: they appear because they are safe and common, not because they fit the product. An interface that reads as "AI slop" signals low intent. This skill turns a vague sense of "this looks generic" into a concrete, scoreable audit with specific fixes.

Source list: Charles Liu, "20 More AI Design Slop Indicators" (https://youtube.com/shorts/E7JrEO7L5rQ).

## Contract for long sessions

Confirm every scanner hit before counting it. Score only from confirmed findings. Reload `references/slop-indicators.md` rather than recalling it. State when no render was available.

## When to use

The description above is the trigger. In practice: before showing a user any UI you generated, when reviewing someone else's front-end, when polishing a landing page or dashboard, or when a user asks whether something looks AI-generated.

Skip the audit for pure backend work, plain terminal output, data files, or non-visual code.

## Workflow

1. **Locate the work.** Take the user's path, pasted code, or the files you are about to write. If nothing is specified, use the UI files in the current change set.
2. **Run the deterministic scan** when source files are available. It finds textual tells (class names, hex values, keywords, structures) with file and line evidence:

   ```bash
   python3 <skill-dir>/scripts/scan_slop.py <path> [--json]
   ```

   The script is a triage aid, not a verdict. Regex hits are candidates; a cream hex can be the right brand color, and `grid-cols-3` can be justified. Confirm each hit against context, then **walk all 20 indicators manually** — the scanner misses tells expressed through custom class names (`.pill`, `border-radius:999px`) or loose spacing between related declarations. Never treat the script's score as the final score.
3. **Inspect the rendered design** when you have a screenshot, browser, or running preview. Several tells (blurry glows, fade-on-scroll, over-use of eyebrows/pills, three identical cards) are visual and will not appear in source scanning. If no browser or preview is reachable, say so explicitly and score from source only; note in the report that visual-only tells may have been missed. Do not repeatedly retry a browser connection that was refused.
4. **Score and report** using the format below. Before counting any candidate, confirm it against source or screenshot: a regex hit is a candidate, not a finding. Cite the exact line or screenshot region for every finding.
5. **Rewrite only when asked.** If the user wants a fix, apply the rewrite playbook and re-score to show the delta.

## Scoring

Each indicator has a fixed penalty reflecting how strongly it reads as generated. Count each indicator **once** per audit regardless of how many times it appears, but mention the repeat count in the evidence — repetition itself is a symptom.

| Severity | Weight | Indicators |
|---|---|---|
| High | 7 | Everything in a card; three icon cards in a row; made-up stats; blurry glows behind the hero; two-word sentences |
| Medium | 5 | Arrows on every button; cream backgrounds; one italic word in the headline; sparkle icons; numbered sections; pulsing green dots; Instrument Serif; colored left borders; pills above the headline; sections fading on scroll |
| Low | 3 | Little dots between words; overusing eyebrows; "quiet"; "real"; dithering |

`score = 100 - sum(penalties for confirmed indicators)`, clamped to 0.

- **90-100** — clean; ship it.
- **70-89** — a few tells; polish before shipping.
- **Below 70** — reads as generated; rewrite the structure, not just the colors.

A low score is not a moral judgment. It is a prediction of how a discerning viewer will read the work. Say so plainly.

## Detection and fixes

Full per-indicator rules — what to look for, why it reads as slop, and the concrete replacement — live in `references/slop-indicators.md`. Read that file whenever you are scoring or rewriting; the one-line names in the scoring table are not enough to apply the rules consistently. In a long session, re-read it instead of relying on recall; it is the authoritative anchor, and it is grep-able.

For positive direction (layout archetypes, typography pairing, copy patterns that signal intent), read `references/rewrite-playbook.md`.

## Output format

Always use this structure for an audit. Keep it compact — this is a checklist a human should scan in ten seconds.

```markdown
## Slop audit — <what you reviewed>

**Score: <N>/100** (<verdict>)

| # | Indicator | Severity | Evidence | Why it reads as AI | Fix |
|---|---|---|---|---|---|
| 1 | <name> | high/medium/low | <file:line or screenshot region> | <one clause> | <replacement> |

<1-2 sentences on the overall impression and the highest-leverage change.>
```

Rules for the table:

- Only list **confirmed** indicators. Do not pad the table with regex false positives.
- Sort by severity, then by the first line where the tell is **used** (not where its CSS is declared).
- Evidence must be locatable: a `file:line`, a class name, or a region in the screenshot.
- "Fix" must be an action, not "remove it" — e.g. "replace the three icon cards with one featured example and a short list".

When the user asks for a rewrite, follow the audit with the rewritten code or a precise diff, then a one-line re-score: `After rewrite: <N>/100 (+<delta>)`. Do not rewrite unprompted.

## Rewriting principles

Work from structure outward. The highest-leverage changes are almost always structural (cards, grids, section rhythm), not cosmetic (swapping a font). Specifically:

- Prefer hierarchy and whitespace over containers. If everything is in a card, nothing is emphasized.
- Make one deliberate choice where the default would be symmetric. Three equal cards, centered text, and evenly spaced sections are the shape of a template.
- Replace claims with specifics: a real number with a source beats "made up stats"; a concrete verb beats "real" or "quiet".
- Use motion only to explain state or cause. Decorative fade-in-on-scroll and pulsing status lights with no live data are noise.
- Keep the product's own voice. Removing slop should make the design more specific to *this* product, not more generic in a different direction.

## Limitations

- Source scanning cannot see rendered layout, animation, or color in context. It over-flags common utilities (`blur`, `rounded-full`, `grid-cols-3`) and under-flags visually obvious slop built from custom CSS. Treat the score as a conversation starter and the screenshot as the truth.
- **Inert scaffolding:** source may contain tells that would not actually render — a decorative glow div with no size, an `IntersectionObserver` that never calls `observe()`, an undefined `.fade-in` class, Tailwind utilities with no Tailwind loaded. Score the *intent* as a tell when it is clearly there, but disclose in the evidence that it may be inert. Do not claim an effect renders when the code cannot produce it.
- The list is a 2026 snapshot of generative design defaults. When a tell becomes unfashionable, update `references/slop-indicators.md` rather than loosening the scoring ad hoc.
- These are tendencies, not banned APIs. A user who explicitly wants the "AI aesthetic" for a parody or concept piece should get it — note the deliberate choice and move on.

## Files in this skill

- `references/slop-indicators.md` — the 20 indicators with detection rules, rationale, and replacements.
- `references/rewrite-playbook.md` — positive patterns for layout, type, copy, and motion.
- `scripts/scan_slop.py` — stdlib-only textual scan; prints a table, JSON with `--json`, and exits 0 so findings never break a build.
