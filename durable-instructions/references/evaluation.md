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

All five checks (A:1, B:1, D:3) plus at least one baseline miss must pass with the skill. Trigger probe C must be perfect in both directions.
