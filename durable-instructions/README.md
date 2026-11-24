# durable-instructions

![Durable Instructions mark](assets/durable-instructions-logo.svg)

A Claude Code skill that keeps a rule in force across a long agent session — through compaction, context drift, and hundreds of intervening tokens.

Written and maintained with Claude Code. Instructions are not remembered; they are re-read or they are gone. This skill turns research on agent memory, context position, and instruction density into six authoring rules that put a constraint where the decision actually happens.

## Install

Copy the `durable-instructions` directory into your skills folder:

```bash
cp -R durable-instructions ~/.claude/skills/
```

Restart Claude Code and confirm `durable-instructions` appears in `/skills`.

## Use

The skill activates when an agent keeps forgetting a rule mid-task, drops constraints after compaction, ignores guidelines written at the top of a prompt, or when you are authoring a skill, system prompt, or CLAUDE.md that must stay in force.

```
/durable-instructions this agent keeps dropping my evidence rule after compaction
/durable-instructions review my CLAUDE.md for durable constraints
```

Six rules: trigger contract, point-of-decision placement, verifiable form, spaced restatement, grep-able anchor, and rule budget. Each rule is stated so you can check whether it was followed, not just repeated.

## Files

```
SKILL.md                        the six rules, contract, workflow, and limits
assets/durable-instructions-logo.svg  repository mark
references/research-evidence.md sources, findings, rule mapping
references/authoring-patterns.md before/after templates
references/evaluation.md        probes and pass criteria
evals/evals.json                trigger and behavioral tests
evals/validate_structure.py     mechanical structure check
```

## Validation

`python3 evals/validate_structure.py` checks the description symptoms, required headings and rules, reference presence, and the SKILL.md word budget. It prints `PASS` with a word count or `FAIL` with the list of violations.

## License

MIT — see [LICENSE](LICENSE).
