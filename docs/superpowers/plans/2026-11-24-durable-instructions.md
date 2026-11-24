# Durable Instructions Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a portable `durable-instructions` skill from 28 research sources and integrate its distilled rules into the published `no-ai-slop` skill so its audit rules survive long sessions.

**Architecture:** Two deliverables in one repo (`~/no-ai-slop`): a new standalone skill directory with a short frontmatter-triggered `SKILL.md`, three on-demand reference files, and an eval suite; plus focused edits to `no-ai-slop/SKILL.md` that relocate critical rules next to the decisions they govern. No hooks, no runtime dependencies, no changes to the scanner or design indicators.

**Tech Stack:** Markdown skills for Claude Code, YAML frontmatter, Python 3 stdlib for the structure validator, tinyfish for source research (already done), git + gh CLI for publishing.

**Spec:** `docs/superpowers/specs/2026-11-24-durable-instructions-design.md` (committed as `d461ef7`).

## Global Constraints

- New `SKILL.md` stays under 1,500 words; depth goes in `references/`.
- Trigger conditions live only in frontmatter `description`; no "When to use" body section.
- Description is third person, symptom-driven, no workflow summary.
- Exactly six rules: Trigger contract, Point-of-decision placement, Verifiable form, Spaced restatement, Grep-able anchor, Rule budget.
- Research base is the 28 sources in the spec; every rule maps to at least one source.
- Success is 5/5 checks across three probe scenarios with fresh subagents; baseline must show at least one miss.
- No changes to `scripts/scan_slop.py`, the 20 indicators, `plugin.json`, or `marketplace.json`.
- No hooks, session state, or runtime services.
- Every commit ends with `Co-Authored-By: Claude Code <noreply@anthropic.com>`.

## Review Focus

- Near-miss prompt "fix my CSS button" must NOT invoke durable-instructions — pinned by Task 4 trigger probe.
- Compaction summary plus anchor only must still yield the contract — pinned by Task 5 probe B.
- 30-turn session with constraint at turn 3 must be honored at turn 25 — pinned by Task 5 probe A.
- SKILL.md bloat above 1,500 words must fail the validator — pinned by Task 1 step 2.
- After integration, no-ai-slop audit must confirm scanner hits before scoring — pinned by Task 6 step 4.

---

## File Structure

- `~/durable-instructions/SKILL.md` — trigger contract and six rules; the only file loaded on trigger.
- `~/durable-instructions/references/research-evidence.md` — 28 sources, findings, rule mapping, caveats.
- `~/durable-instructions/references/authoring-patterns.md` — before/after templates for prompts, skills, CLAUDE.md.
- `~/durable-instructions/references/evaluation.md` — probe protocols and pass criteria.
- `~/durable-instructions/evals/evals.json` — trigger queries and behavioral scenarios.
- `~/durable-instructions/evals/validate_structure.py` — mechanical checks on the skill files.
- `no-ai-slop/SKILL.md` — modified only: contract block, relocated rule, anchor pointer.
- `docs/superpowers/plans/2026-11-24-durable-instructions.md` — this plan.

---

### Task 1: Create the durable-instructions skill body and structure validator

**Files:**
- Create: `~/durable-instructions/SKILL.md`
- Create: `~/durable-instructions/evals/validate_structure.py`

**Interfaces:**
- Consumes: the six rules and symptom triggers from the spec.
- Produces: `~/durable-instructions/SKILL.md` with headings `## Contract`, `## The six rules`, `## Workflow`, `## Limits`, `## Files`; validator exit code 0 when structure is valid.

- [ ] **Step 1: Write SKILL.md**

Write this exact content to `~/durable-instructions/SKILL.md`:

```markdown
---
name: durable-instructions
description: Make instructions survive long agent sessions. Use when an agent keeps forgetting a rule mid-task, drops constraints after context compaction, ignores guidelines written at the top of a prompt, or when writing a skill, system prompt, or CLAUDE.md that must stay in force. Also use when designing agent memory, instruction checklists, or long-context prompts that must be followed rather than merely read.
allowed-tools: Read, Grep, Glob
license: MIT
---

# Durable Instructions

Instructions are not remembered; they are re-read or they are gone. This skill turns research on agent memory, context position, and instruction density into six authoring rules that keep a rule in force at the moment it matters.

## Contract

1. Triggers live only in the frontmatter description.
2. Put each rule where the decision happens.
3. Make every rule observable.
4. Restate briefly at section boundaries.
5. Keep an external plain-text anchor.
6. Keep the active rule set short.

## The six rules

### 1. Trigger contract

Write invocation conditions in the frontmatter description, in third person, using the symptom a user actually notices: "keeps forgetting a rule", "drops constraints", "ignores guidelines". Do not add a "When to use" section to the body, and do not summarize the workflow in the description. A workflow summary makes agents act on the description and skip the body.

### 2. Point-of-decision placement

Place a constraint immediately before the step it governs. A rule stated only in a preamble competes with everything that follows it; relevance in the middle of a long context is reliably under-used, and early instructions win disproportionate attention. If a rule governs scoring, put it in the scoring step, not in an intro.

### 3. Verifiable form

State what passing looks like. "Evidence is a file:line or a screenshot region" can be checked; "be careful with evidence" cannot. Separate the action from the assertion, and give each rule a pass/fail condition. An agent can repeat an instruction while violating it, so only observable checks count as compliance.

### 4. Spaced restatement

Repeat a three-to-five line contract at the boundaries where a long task changes phase. One dense list at the top is cramming; short restatements at decision points are retrieval practice. Each restatement costs tokens, so keep it short and only restate rules that govern the upcoming phase.

### 5. Grep-able anchor

Keep the authoritative constraints in a plain-text file that can be re-read on demand, and point to it explicitly. Assume compaction will discard anything unwritten, and assume a summary preserves the task but not the side constraints. A short append-only checklist plus a search tool outperforms lossy summarization in long-horizon recall.

### 6. Rule budget

Cut soft preferences and duplicates before adding new rules. Adherence falls as instruction count rises, and the best models still miss roughly a third of a very large instruction set. Six enforced rules beat twenty aspirational ones.

## Workflow

1. Read the contract above.
2. Identify the decision points in the work: where the agent will choose, write, or judge.
3. Select the matching template from `references/authoring-patterns.md`.
4. Place each rule at its decision point, in verifiable form.
5. Name the grep-able anchor file if one exists.
6. Run the probes in `references/evaluation.md` and report pass/fail with evidence.

## Limits

This skill improves the odds that a rule is followed; it cannot force a model to obey. Hard guarantees require external enforcement, which is deliberately out of scope here. Research is from 2023-2026; revisit the findings when context managers or model architectures change.

## Files

- `references/research-evidence.md` — sources, findings, rule mapping.
- `references/authoring-patterns.md` — before/after templates.
- `references/evaluation.md` — probes and pass criteria.
- `evals/evals.json` — trigger and behavioral tests.
- `evals/validate_structure.py` — mechanical structure check.
```

- [ ] **Step 2: Write the structure validator**

Write this exact content to `~/durable-instructions/evals/validate_structure.py`:

```python
#!/usr/bin/env python3
"""Mechanical checks for durable-instructions structure."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / "SKILL.md").read_text()
front = text.split("---", 2)[1]
errors = []

description = re.search(r"^description:\s*(.+)$", front, re.M)
if not description:
    errors.append("missing description")
else:
    low = description.group(1).lower()
    for phrase in ("keeps forgetting", "drops constraints", "skill", "claude.md"):
        if phrase not in low:
            errors.append(f"description missing symptom phrase: {phrase}")
    if low.startswith("to "):
        errors.append("description must be third person")

for heading in ("## Contract", "## The six rules", "## Workflow", "## Limits", "## Files"):
    if heading not in text:
        errors.append(f"missing heading: {heading}")

for rule in (
    "### 1. Trigger contract",
    "### 2. Point-of-decision placement",
    "### 3. Verifiable form",
    "### 4. Spaced restatement",
    "### 5. Grep-able anchor",
    "### 6. Rule budget",
):
    if rule not in text:
        errors.append(f"missing rule: {rule}")

if "## When to use" in text:
    errors.append("body must not contain a Triggers/When-to-use section")
words = len(text.split())
if words >= 1500:
    errors.append(f"SKILL.md over budget: {words} words")

for name in ("research-evidence.md", "authoring-patterns.md", "evaluation.md"):
    if not (ROOT / "references" / name).exists():
        errors.append(f"missing reference: {name}")

if errors:
    print("FAIL")
    print("\n".join(errors))
    sys.exit(1)
print(f"PASS: {words} words, all structure checks met")
```

- [ ] **Step 3: Run the validator to confirm it fails on missing references**

Run: `python3 ~/durable-instructions/evals/validate_structure.py`
Expected: FAIL listing the three missing reference files. This proves the validator is real.

- [ ] **Step 4: Commit**

```bash
cd ~/durable-instructions
git init -q
git branch -M main
git add .
git -c user.name="suydev" -c user.email="elixir.suyashprabhu@gmail.com" commit -q -m "feat: add durable-instructions skill body and validator

Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 2: Write the research evidence reference

**Files:**
- Create: `~/durable-instructions/references/research-evidence.md`

**Interfaces:**
- Consumes: the research table in the spec.
- Produces: a citable evidence file; satisfies Task 1 validator's reference check.

- [ ] **Step 1: Write the reference file**

Write this exact content:

```markdown
# Research evidence

Funding statement: sources were collected with tinyfish search on 2026-11-24. Twenty-eight sources are listed below. Numbers are reported as the sources report them; they are not replications.

## Headline findings

- Compactors retained only 17% of injected session constraints; an explicit extractor exceeded 90% (Lost in Compaction).
- Append-only plain-text log plus grep reached 95-97% recall versus at most 21% for lossy baselines (GrepMem).
- Best frontier models reached 68% accuracy at 500 simultaneous instructions, with a bias toward earlier instructions (IFScale).
- Relevance at the beginning or end of context is used well; relevance in the middle degrades sharply (Lost in the Middle).
- Verifiable instructions plus a restatement intervention improved long-context compliance by up to 79% (VerIFY paper).
- Spacing and retrieval practice produce more durable retention than massed repetition (education research).

## Agent memory and instruction following

| Source | Finding | Rules |
|---|---|---|
| Lost in the Middle, Liu et al., TACL 2023 — arxiv.org/abs/2307.03172 | U-shaped position curve; middle content under-used | 2 |
| Lost in Compaction (CompInt) — arxiv.org/html/2608.11242v1 | 17% constraint retention; extractor over 90% | 5 |
| Forget Freely, Grep Later (GrepMem) — arxiv.org/abs/2611.25123 | 95-97% vs 21% recall | 5 |
| How Many Instructions Can LLMs Follow at Once (IFScale) — arxiv.org/html/2507.11538v1 | 68% at 500 rules; early-instruction bias | 3, 6 |
| We Are What We Repeatedly Do (VerIFY) — aclanthology.org/2026.findings-eacl.254 | Verifiable criteria; up to 79% improvement | 3, 4 |
| Measuring and Controlling Instruction Instability — arxiv.org/html/2402.10962v2 | Dialogue instructions degrade with turns | 2, 4 |
| Multi-IF — arxiv.org/html/2410.15553 | Multi-turn instruction following is distinct | 2 |
| State Integrity Collapse — arxiv.org/html/2610.31314 | Agents can restate yet violate a rule | 3 |
| The Instruction Gap — arxiv.org/html/2601.03269v1 | Density and placement determine compliance | 2, 6 |
| MemGPT — arxiv.org/html/2310.08560v1 | Hierarchical memory architecture | 5 |
| A Survey of Agent Memory in the Second Half — arxiv.org/abs/2602.06052 | Memory taxonomy and open problems | 5 |
| Memory in the Age of AI Agents — arxiv.org/pdf/2512.13564v1 | Memory as a first-class research area | 5 |
| Memory for Autonomous LLM Agents — arxiv.org/html/2603.07670v1 | Mechanisms and evaluation | 5 |
| Rethinking Memory in LLM based Agents — arxiv.org/html/2505.00675 | Representation and operations | 5 |
| Agent Memory: Characterization and System Implications — arxiv.org/pdf/2606.06448v2 | Stateful workloads | 5 |
| Towards Long-Horizon Agents: A Survey — long-horizon-agents.github.io | Long-horizon failure modes | 5 |
| Quantifying Laziness, Decoding Suboptimality, Context Degradation — arxiv.org/pdf/2512.20662 | Degradation is measurable | 6 |
| Exploiting Primacy Effect — arxiv.org/html/2507.13949v1 | Placement bias is exploitable | 2 |
| LLM Position Bias — intuitionlabs.ai/articles/llm-position-bias-primacy-recency-effects | Primacy and recency in prompts | 2 |
| A Guide to Improving Long Context Instruction Following — scale.com/blog/long-context-instruction-following | Practitioner guidance on density and placement | 2, 3 |
| Why AI Agents Forget: The Stateless LLM Problem — atlan.com/know/why-ai-agents-forget/ | Statelessness as root cause | 5 |

## Psychology of retention

| Source | Finding | Rule |
|---|---|---|
| Spacing and retrieval — edresearch.edu.au/summaries-explainers/explainers/spacing-retrieval | Spacing prevents cognitive overload; retrieval strengthens memory | 4 |
| Using Spacing to Enhance Diverse Forms of Learning — pdf.retrievalpractice.org/spacing/Carpenter_etal_2012_EDPR.pdf | Spacing improves diverse learning forms | 4 |
| Spaced Retrieval Practice Imposes Desirable Difficulty — link.springer.com/article/10.1007/s10648-022-09677-2 | Desirable difficulty improves retention | 4 |
| Spacing Effect — thedecisionlab.com/biases/spacing-effect | Shortened as a general bias reference | 4 |

## Skill authoring

| Source | Finding | Rule |
|---|---|---|
| Skill authoring best practices — docs.anthropic.com/claude/docs/agents-and-tools/agent-skills/best-practices | Concision wins; metadata loads first; every token competes with context | 1, 6 |
| Equipping agents for the real world with Agent Skills — anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | Skills are a first-class progressive-disclosure mechanism | 1 |
| skill-development SKILL.md — github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md | Reference implementation for skill authoring | 1 |

## Caveats

- These are reported results, not guarantees for every model or harness.
- Position and density effects are strongest in long contexts; short prompts need less defense.
- Restatement costs tokens; use it only at phase boundaries.
- External anchors require the agent to actually re-read them; the rule reduces reliance on recall but does not eliminate it.
```

- [ ] **Step 2: Run the validator to confirm references are now found**

Run: `python3 ~/durable-instructions/evals/validate_structure.py`
Expected: FAIL only on the two remaining missing references (`authoring-patterns.md`, `evaluation.md`).

- [ ] **Step 3: Commit**

```bash
cd ~/durable-instructions
git add ./references/research-evidence.md
git commit -m "docs: add research evidence for durable instructions

Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 3: Write authoring patterns and evaluation protocol

**Files:**
- Create: `~/durable-instructions/references/authoring-patterns.md`
- Create: `~/durable-instructions/references/evaluation.md`

**Interfaces:**
- Consumes: the six rules.
- Produces: templates used by Task 5 probes; satisfies Task 1 validator.

- [ ] **Step 1: Write authoring patterns**

Write this content to `~/durable-instructions/references/authoring-patterns.md`:

```markdown
# Authoring patterns

Each pattern shows the failure form and the replacement. Copy the structure, not the subject matter.

## Prompt: soft preamble to decision-point rule

Before:

```text
Be thorough and follow all our rules when reviewing code.
... 3,000 tokens of task description ...
Review the diff.
```

After:

```text
Review the diff.

For each changed file, list evidence as path:line. A finding without a path:line
does not count. Output the list before any summary.
```

The observable check sits next to the action.

## SKILL.md body: restated contract at phase boundary

Before:

```markdown
Always confirm tool output before reporting.
## Step 1: scan
...
## Step 2: score
...
```

After:

```markdown
## Step 1: scan
...

## Step 2: score
CONTRACT (score phase): confirm each candidate against source before counting it.
Evidence must be path:line or a screenshot region. Unconfirmed candidates are not counted.
...
```

## CLAUDE.md: vague preference to grep-able anchor

Before:

```markdown
Keep the API conventions in mind.
```

After:

```markdown
Read `docs/api-contract.md` before adding an endpoint. It is authoritative.
If it is not present, say so and stop; do not rely on recalled conventions.
```

## Checklist anchor

Use a plain-text file with one rule per line and a short header. Append rather than rewrite; search it with grep when the decision arrives. Never encode the only copy of a constraint inside a tool result or a summary.

```text
CONTRACT
- evidence: path:line or screenshot region
- confirm before scoring
- reload docs/api-contract.md when adding endpoints
```

## What to cut

- "Be careful", "be thorough", "follow best practices" — no observable check.
- Rules repeated three or more times in one file — restate at boundaries, not in place.
- Preferences that do not change a decision — they consume the rule budget.
```

- [ ] **Step 2: Write evaluation protocol**

Write this content to `~/durable-instructions/references/evaluation.md`:

```markdown
# Evaluation protocol

Run every probe with a fresh subagent. Do not reuse an agent that has seen the skill draft.

## Probe A: long session

Prompt: "You are in turn 25 of a 30-turn session. At turn 3 the user said: never delete a file without asking. The current request is to clean up a directory of old exports. Proceed." Pass if the agent asks before deleting. Fail if it deletes or proposes deletion without asking.

## Probe B: compaction simulation

Give the agent only a task summary and the CONTRACT anchor from authoring-patterns.md. Prompt: "The earlier conversation was compacted. The summary says: refactor the auth module. The anchor file is attached. What constraints apply?" Pass if the agent restates the anchor rules and says it will re-read the full file before acting. Fail if it claims to remember rules from the lost context.

## Probe C: near-miss triggers

Ask: "fix my CSS button", "review this SQL migration", "summarize this PDF". Pass if durable-instructions is NOT invoked for any. Also ask: "my agent keeps forgetting our coding rules mid-session", "help me write a CLAUDE.md that sticks", "why does my skill get ignored?" Pass if it IS invoked for all three.

## Probe D: no-ai-slop integration

After Task 6, use the existing fixture at `evals/fixtures/sloppy-landing.html`. Prompt: "Audit this landing page; the session has been long and many files were read." Pass if the agent confirms scanner hits before scoring, cites file:line evidence, and reloads `references/slop-indicators.md` rather than recalling the list.

## Pass criteria

Five or more of six checks across probes A, B and D must pass with the skill; at least one must fail without it. Trigger probe C must be perfect in both directions.
```

- [ ] **Step 3: Run the validator; expect PASS**

Run: `python3 ~/durable-instructions/evals/validate_structure.py`
Expected: PASS with word count under 1,500.

- [ ] **Step 4: Commit**

```bash
cd ~/durable-instructions
git add ./references
git commit -m "docs: add authoring patterns and evaluation protocol

Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 4: Write evals and verify trigger behavior

**Files:**
- Create: `~/durable-instructions/evals/evals.json`

**Interfaces:**
- Consumes: probe C from Task 3.
- Produces: a regression-testable eval suite used by Task 5.

- [ ] **Step 1: Write evals.json**

Write this content:

```json
{
  "skill_name": "durable-instructions",
  "evals": [
    {
      "id": 1,
      "name": "trigger-symptom-phrases",
      "prompt": "my agent keeps forgetting our coding rules halfway through a long session, can you make it stick?",
      "expected_output": "durable-instructions triggers",
      "files": []
    },
    {
      "id": 2,
      "name": "trigger-claude-md",
      "prompt": "help me write a CLAUDE.md that my agent will actually follow after context compaction",
      "expected_output": "durable-instructions triggers",
      "files": []
    },
    {
      "id": 3,
      "name": "trigger-skill-ignored",
      "prompt": "why does my Claude Code skill get ignored even though it is installed?",
      "expected_output": "durable-instructions triggers",
      "files": []
    },
    {
      "id": 4,
      "name": "near-miss-css",
      "prompt": "fix my CSS button so the hover state is not grey",
      "expected_output": "durable-instructions does not trigger",
      "files": []
    },
    {
      "id": 5,
      "name": "near-miss-sql",
      "prompt": "review this SQL migration for a missing index",
      "expected_output": "durable-instructions does not trigger",
      "files": []
    },
    {
      "id": 6,
      "name": "near-miss-pdf",
      "prompt": "summarize this PDF into five bullet points",
      "expected_output": "durable-instructions does not trigger",
      "files": []
    },
    {
      "id": 7,
      "name": "behavior-long-session",
      "prompt": "At turn 3 a user said never delete files without asking. At turn 25 they ask you to clean an exports directory.",
      "expected_output": "agent asks before deleting",
      "files": []
    },
    {
      "id": 8,
      "name": "behavior-compaction",
      "prompt": "Only a task summary and a CONTRACT anchor are available after compaction; agent restates anchor rules and re-reads the file.",
      "expected_output": "agent does not claim recall of lost context",
      "files": []
    }
  ]
}
```

- [ ] **Step 2: Validate the JSON**

Run: `python3 -c "import json; d=json.load(open('~/durable-instructions/evals/evals.json')); print(len(d['evals']))"`
Expected: `8`

- [ ] **Step 3: Commit**

```bash
cd ~/durable-instructions
git add ./evals/evals.json
git commit -m "test: add durable-instructions trigger and behavior evals

Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 5: Run behavioral probes with and without the skill

**Files:**
- Test only; no source files changed unless a probe fails.

**Interfaces:**
- Consumes: `~/durable-instructions/SKILL.md` and `references/evaluation.md`.
- Produces: pass/fail record and, on failure, a targeted edit to the rule placement.

- [ ] **Step 1: Dispatch four fresh subagents in parallel**

Use the Task tool with `subagent_type: general-purpose`. For each, paste the exact prompt below. Two get the skill, two do not.

With-skill prompt (probe A): "Read /data/data/com.termux/files/home/durable-instructions/SKILL.md and follow it. Then: You are at turn 25 of a 30-turn session. At turn 3 the user said: never delete a file without asking. The current request is to clean a directory of old exports. What do you do?"

Baseline prompt (probe A): same text after "Then:" with no skill path.

With-skill prompt (probe B): "Read /data/data/com.termux/files/home/durable-instructions/SKILL.md and follow it. Then: The earlier conversation was compacted. Your summary says: refactor the auth module. Your CONTRACT anchor says: read docs/api-contract.md before adding endpoints; never claim recall of lost context. What constraints apply?"

Baseline prompt (probe B): same text after "Then:" with no skill path.

- [ ] **Step 2: Grade the responses**

Pass conditions: with-skill probe A asks before deleting; with-skill probe B restates the anchor and says it will re-read the full file; both baseline probes show at least one violation or a claim of recall. Record each outcome in the plan's execution notes.

- [ ] **Step 3: If a with-skill probe fails, relocate the rule and re-run only that probe**

Move the failing rule next to the exact decision text in `SKILL.md` (for probe A, add it to rule 2's example; for probe B, add it to rule 5's example), then re-dispatch that single with-skill probe. Stop when it passes.

- [ ] **Step 4: Commit any rule relocation**

```bash
cd ~/durable-instructions
git add ./SKILL.md
git commit -m "fix: relocate rule to decision point after probe failure

Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

Skip this step if no edit was needed.

---

### Task 6: Integrate the patterns into no-ai-slop

**Files:**
- Modify: `no-ai-slop/SKILL.md` (three targeted edits, exact strings below).

**Interfaces:**
- Consumes: rules 2, 3 and 5 from Task 1.
- Produces: an integrated audit skill whose existing score on the fixture stays 20/100.

- [ ] **Step 1: Add the durability contract after the source line**

Edit `SKILL.md`. Find:

```markdown
Source list: Charles Liu, "20 More AI Design Slop Indicators" (https://youtube.com/shorts/E7JrEO7L5rQ).

## When to use
```

Replace with:

```markdown
Source list: Charles Liu, "20 More AI Design Slop Indicators" (https://youtube.com/shorts/E7JrEO7L5rQ).

## Contract for long sessions

Confirm every scanner hit before counting it. Score only from confirmed findings. Reload `references/slop-indicators.md` rather than recalling it. State when no render was available.

## When to use
```

- [ ] **Step 2: Relocate the confirmation rule into the scoring step**

Find:

```markdown
4. **Score and report** using the format below. Cite the exact line or screenshot region for every finding.
```

Replace with:

```markdown
4. **Score and report** using the format below. Before counting any candidate, confirm it against source or screenshot: a regex hit is a candidate, not a finding. Cite the exact line or screenshot region for every finding.
```

- [ ] **Step 3: Name the reloadable anchor**

Find:

```markdown
Full per-indicator rules — what to look for, why it reads as slop, and the concrete replacement — live in `references/slop-indicators.md`. Read that file whenever you are scoring or rewriting; the one-line names in the scoring table are not enough to apply the rules consistently.
```

Replace with:

```markdown
Full per-indicator rules — what to look for, why it reads as slop, and the concrete replacement — live in `references/slop-indicators.md`. Read that file whenever you are scoring or rewriting; the one-line names in the scoring table are not enough to apply the rules consistently. In a long session, re-read it instead of relying on recall; it is the authoritative anchor, and it is grep-able.
```

- [ ] **Step 4: Re-run the integration audit probe**

Run: `python3 scripts/scan_slop.py evals/fixtures/sloppy-landing.html --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['score'], len(d['findings']))"`
Expected: `20 16` (unchanged; the edits touch instructions, not the scanner).

Then dispatch one fresh subagent with the probe D prompt from `references/evaluation.md`. Pass if it confirms hits before scoring, cites file:line evidence, and reloads the reference.

- [ ] **Step 5: Commit**

```bash
cd ~/no-ai-slop
git add SKILL.md
git commit -m "feat: apply durable-instruction contract to no-ai-slop

Co-Authored-By: Claude Code <noreply@anthropic.com>"
```

---

### Task 7: Publish both deliverables

**Files:**
- No source changes; git and gh operations only.

**Interfaces:**
- Consumes: committed work from Tasks 1-6.
- Produces: durable-instructions available on GitHub; no-ai-slop remote updated with the spec, plan and integration.

- [ ] **Step 1: Verify clean trees**

Run: `git -C ~/no-ai-slop status --short`
Expected: no output.

- [ ] **Step 2: Push no-ai-slop**

Run: `git -C ~/no-ai-slop push origin main`
Expected: fast-forward to remote.

- [ ] **Step 3: Create and push the new repo**

```bash
cd ~/durable-instructions
timeout 60 gh repo create Suydev/durable-instructions --public --description "Portable skill for instructions that survive long agent sessions"
git remote add origin https://github.com/Suydev/durable-instructions.git
git push -u origin main
```

Expected: new public repo with SKILL.md, three references, and evals/.

- [ ] **Step 4: Verify**

Run: `timeout 60 gh repo view Suydev/durable-instructions --json name,visibility,url`
Expected: name `durable-instructions`, visibility `PUBLIC`.

## Self-review notes

- Spec coverage: all six rules in Task 1; 28 sources in Task 2; templates and probes in Tasks 3-4; behavioral delta in Task 5; integration in Task 6; publishing in Task 7.
- No placeholders: every content step includes the full text or exact old/new strings.
- Type consistency: rule names and file paths are identical across tasks.
- Review Focus: each of the five listed failure modes has a pinned test step.
