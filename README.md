# tests-that-can-fail

[中文](README.zh-CN.md)

A skill for AI coding agents (Claude Code, Codex, and anything that reads `SKILL.md`)
for the moment a model writes the thing that decides right from wrong: unit tests,
property tests, contracts, benchmarks, evals.

Models are good at producing tests that look thorough. A fair share of those tests can
never fail, always fail, or compare the wrong two things. This skill gives the agent
three questions to ask of every check, the five causes behind the mistakes, a procedure
for writing checks, and a review list for checks a model already wrote.

## Where it comes from

The patterns were measured, not collected from opinion. In blind runs, two model families
wrote declarative contracts from the documentation of real Python libraries
(python-semver, more-itertools, humanize, inflect, num2words, parse). Each library was
present as two releases: one with a defect recorded in its changelog and the one that
fixed it. A mechanical judge ran the contracts on both. The concurrency entries come from
a separate lab of 17 ordering-defect mechanisms.

Every wrong contract was logged with a kind. Deduplicated, 256 failures fell into five causes:

| Cause | Share |
| --- | --- |
| Operands: the two things compared are not the two the document relates | 34% |
| Scope: true on part of the input domain, written as universal | 27% |
| Filler: assertions that exist to satisfy a count or a rule | 25% |
| Judge: the scoring was wrong | 8% |
| Protocol: validation feedback misled the model | 6% |

Two results shaped the skill most:

- Given the same documentation and the same two builds, a model that had written
  `error == null` beforehand caught a wrong exception. The same model, testing freely,
  printed that exception in 12 of 12 sessions and judged the behaviour consistent with the docs.
- Putting the lessons into the prompt did not help in two controlled comparisons.
  Changing the structure of what the model fills in did.

## Limits

These are six small, pure-Python libraries and two model families. The percentages
describe that record. The contracts were declarative assertions over observed call
results, which is narrower than free-form test code. The catalogue says what went wrong
and what stopped it there; it does not promise the same rates elsewhere.

## Install

```bash
git clone https://github.com/SLYysl/tests-that-can-fail.git
cp -R tests-that-can-fail/skills/tests-that-can-fail ~/.claude/skills/    # Claude Code
cp -R tests-that-can-fail/skills/tests-that-can-fail ~/.codex/skills/     # Codex
```

Then ask as usual: "write tests for this module", "review these tests", "is this
benchmark sound". The agent loads the skill when the task matches.

## Contents

- [`SKILL.md`](skills/tests-that-can-fail/SKILL.md) — the three questions, five causes, procedure and review list.
- [`references/failure-modes.md`](skills/tests-that-can-fail/references/failure-modes.md) — 30 observed failure modes with the guard for each.

## License

Apache-2.0
