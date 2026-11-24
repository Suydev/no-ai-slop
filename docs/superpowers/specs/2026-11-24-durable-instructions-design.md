# Durable Instructions — design spec

Date: 2026-11-24
Status: design approved, awaiting spec review
Scope: architectural

## Problem

Agents forget. Instructions stated once early in a session are dropped during compaction, buried in the middle of a long context, or quietly outvoted as instruction density grows. The `no-ai-slop` skill has concrete rules that are only useful if the agent still follows them at the moment it writes or scores UI. The user wants two deliverables: a new skill that turns research on agent memory and forgetting into practical authoring rules, and integration of those rules into `no-ai-slop`.

"An agent cannot ignore it" is defined operationally, not magically: the constraint is honored in 5/5 long-context probes. No skill can literally prevent an agent from ignoring anything.

## Goals

- Produce a portable `durable-instructions` skill that teaches instruction durability without hooks or extra setup.
- Wire its distilled patterns into the published `no-ai-slop` repo so its 20-indicator rules survive long sessions.
- Ground every rule in a cited source, with a mapping from finding to rule.
- Ship evals so later edits can be regression-tested.

## Non-goals

- Hard enforcement via hooks or session state (considered, not selected).
- Changing the 20 design indicators themselves or the scanner's regex logic.
- Literally collecting 200 sources; 28 curated sources were selected instead.

## Requirements

Explicit:
- Create both the unified skill and the integration into `no-ai-slop`.
- Use tinyfish for web research; include articles/papers on agent memory and forgetting.
- Apply psychology and pattern research.
- Make the result crystal clear so an agent acts on it rather than skipping it.

Implicit:
- Keep skills small: `SKILL.md` under 1,500 words, depth in `references/`.
- Trigger conditions live only in frontmatter descriptions.
- Preserve the public plugin layout of `no-ai-slop` (plugin.json, marketplace.json, evals/).

Discovered:
- Undertriggering is a real failure mode; descriptions need symptom keywords, not workflow summaries.
- A rule that lives only in a preamble is exactly the rule that gets lost in the middle.

## Research evidence

| Finding | Source | Rule it drives |
|---|---|---|
| Relevant info at the start or end of context is used; info in the middle degrades sharply | Lost in the Middle, Liu et al., TACL 2023 — arxiv.org/abs/2307.03172 | 2 |
| Compactors retain only 17% of session constraints; an explicit extractor gets over 90% | Lost in Compaction — arxiv.org/html/2608.11242v1 | 5 |
| Append-only plain-text log + grep: 95-97% recall vs at most 21% for lossy baselines | GrepMem — arxiv.org/abs/2611.25123 | 5 |
| Best frontier models reach 68% at 500 simultaneous instructions; bias toward earlier ones; three degradation patterns | IFScale — arxiv.org/html/2507.11538v1 | 3, 6 |
| Verifiable instructions (clear pass/fail criteria) plus a restatement intervention improved long-context compliance by up to 79%; introduces VerIFY | We Are What We Repeatedly Do, Robinette et al., EACL 2026 Findings — aclanthology.org/2026.findings-eacl.254; openreview.net/forum?id=JAxS4ooL8F | 3, 4 |
| Instruction stability in dialogue degrades measurably with turns | Instruction (In)Stability — arxiv.org/html/2402.10962v2 | 2, 4 |
| Multi-turn, multilingual instruction following is a distinct benchmark problem | Multi-IF — arxiv.org/html/2410.15553 | 2 |
| Agents can repeat a rule while violating it; state integrity collapses in long dialogue | State Integrity Collapse — arxiv.org/html/2610.31314 | 3 |
| Density and placement of instructions, not just their content, determine compliance | Instruction Gap — arxiv.org/html/2601.03269v1 | 2, 6 |
| Hierarchical memory (working/episodic/long-term) is the dominant agent-memory architecture | MemGPT — arxiv.org/html/2310.08560v1 | 5 |
| Agent memory is an active survey topic with taxonomy and evaluation gaps | Agent Memory surveys — arxiv.org/abs/2602.06052, arxiv.org/pdf/2512.13564v1, arxiv.org/html/2603.07670v1, arxiv.org/html/2505.00675, arxiv.org/pdf/2606.06448v2 | 5 |
| Long-horizon failures are framed as a distinct survey area | Towards Long-Horizon Agents — long-horizon-agents.github.io | 5 |
| Context degradation and decoding suboptimality are measurable | Context Degradation — arxiv.org/pdf/2512.20662 | 6 |
| Placement bias (primacy/recency) is documented for prompts | Primacy exploitation — arxiv.org/html/2507.13949v1; position bias — intuitionlabs.ai/articles/llm-position-bias-primacy-recency-effects | 2 |
| Spacing and retrieval practice improve durable retention; massed repetition exhausts cognitive resources | Education Research — edresearch.edu.au/summaries-explainers/explainers/spacing-retrieval; Carpenter et al. — pdf.retrievalpractice.org/spacing/Carpenter_etal_2012_EDPR.pdf; desirable difficulty — link.springer.com/article/10.1007/s10648-022-09677-2; Decision Lab — thedecisionlab.com/biases/spacing-effect | 4 |
| Concise skills win; metadata triggers loading, and every loaded token competes with context | Anthropic skill authoring best practices — docs.anthropic.com/claude/docs/agents-and-tools/agent-skills/best-practices | 1, 6 |
| Skills are a first-class mechanism for equipping agents, with progressive disclosure | Equipping agents for the real world with Agent Skills — anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | 1 |
| Reference implementation of skill authoring in Claude Code | anthropics/claude-code skill-development SKILL.md — github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md | 1 |
| Practical guide to long-context instruction following | Scale — scale.com/blog/long-context-instruction-following | 2, 3 |
| Statelessness and external memory are the root of agent forgetting | Atlan — atlan.com/know/why-ai-agents-forget/ | 5 |

28 sources total (papers, official docs, and practitioner guides). Full titles and URLs go into `references/research-evidence.md`.

## Decisions and why

- **Approach A, no hooks.** Portability was chosen over hard enforcement; the user asked for research-backed instruction design, and hooks would tie the result to one client.
- **Six rules, not a catalogue.** IFScale's density result and Anthropic's concision guidance both say fewer instructions are followed better.
- **Verifiable over aspirational.** A rule that cannot be checked cannot be tested, so each rule's example states an observable pass/fail condition.
- **Anchor file instead of model recall.** Compaction and GrepMem results both say external, grep-able text is more reliable than internal memory.
- **Integration by relocation, not addition.** In `no-ai-slop`, the critical "confirm each scanner hit" rule moves next to the scoring step rather than becoming a seventh general instruction.

## Design

### New skill: `durable-instructions`

```
durable-instructions/
├── SKILL.md                      trigger contract + six rules + routing
├── references/
│   ├── research-evidence.md      28 sources, findings, rule mapping, caveats
│   ├── authoring-patterns.md     before/after templates for skills, prompts, CLAUDE.md
│   └── evaluation.md             long-context, compaction, and trigger probes
└── evals/
    └── evals.json                trigger queries + behavioral scenarios
```

Frontmatter description is third-person and symptom-driven: "Use when an agent keeps forgetting a rule mid-session, drops constraints after context compaction, ignores guidelines in long conversations, or when writing a skill, system prompt, or CLAUDE.md that must stay in force."

### The six rules

1. **Trigger contract.** Invocation conditions live in the frontmatter description; the body never restates "when to use". Symptom keywords beat topic labels because they match the user's actual complaint.
2. **Point-of-decision placement.** Put each constraint immediately before the step it governs. A preamble alone is a middle-of-context casualty.
3. **Verifiable form.** State what passing looks like ("evidence is `file:line` or a screenshot region"), not intent ("be careful"). Compliance must be checkable.
4. **Spaced restatement.** Repeat a 3-5 line contract at section boundaries; do not cram one long list at the top. Spacing beats cramming, but each restatement costs tokens, so keep it short.
5. **Grep-able anchor.** Keep constraints in a plain-text file that can be re-read on demand. Assume compaction will discard anything unwritten.
6. **Rule budget.** Cut soft preferences and duplicates. Adherence falls as instruction count rises; a short enforced list beats a long aspirational one.

### Flow

Trigger → load `SKILL.md` contract → select the relevant reference template → place each rule at its decision point → run probes → report pass/fail with evidence. The skill never assumes the agent will remember a rule it did not just read.

### Integration into `no-ai-slop`

- Add a four-line durability contract at the top of the body: confirm hits, score only from confirmed findings, reload the 20-rule reference on demand, state when no render was available.
- Move "confirm scanner hits" from general guidance into the scoring step.
- Change soft instructions into observable checks where they are already stated.
- Point explicitly to `references/slop-indicators.md` as the reloadable anchor for long sessions.
- No changes to the scanner, the 20 rules, the plugin manifest, or the marketplace manifest.

## Error handling

- Skill does not trigger → revise frontmatter from observed misses, add symptom keywords, re-run trigger probes.
- Rule ignored mid-session → relocate it next to the failing decision, re-run the long-context probe.
- Body exceeds 1,500 words → move detail to `references/`, keep only the contract and decision-point rules.
- Over-triggering on generic UI tasks → add near-miss queries to evals and tighten description.
- Evaluator disagreement → use behavior (did the agent apply the rule?), not self-report.

## Testing

- Trigger probes: 3 positives (agent forgets a rule, writing a CLAUDE.md, skill keeps getting skipped) and 3 near-misses (fix my CSS button, review this SQL migration, summarize this PDF).
- Behavioral scenarios, each run with and without the skill using fresh subagents:
  1. 30-turn simulated session; constraint injected at turn 3, decision at turn 25.
  2. Compaction simulation: agent receives a task summary plus the anchor file only; must still apply the contract.
  3. `no-ai-slop` audit of the existing sloppy fixture after a long preamble; must still confirm hits before scoring and reload the rule reference.
- Success criteria: across the three scenarios above, with-skill runs honor the constraint in 5/5 checks (multiple decision points per scenario); baseline runs show at least one miss; `SKILL.md` stays under 1,500 words; no placeholder markers in shipped files.

## Risks and obsolescence

- Research is dated 2023-2026; re-check compaction and position-bias findings when new model architectures or context managers ship.
- Repeated contract blocks cost tokens; if users report verbosity, shorten the block rather than removing it.
- A hook-based layer would raise compliance further but is out of scope; revisit only if probes fail.
