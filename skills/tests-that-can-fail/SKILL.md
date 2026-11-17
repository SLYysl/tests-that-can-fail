---
name: tests-that-can-fail
description: Checklist and procedure for when an AI model writes the thing that decides right from wrong — unit tests, property tests, contracts, assertions, benchmarks, evals, graders. Use before writing such checks, when reviewing model-written tests, when a test suite is green but you doubt it proves anything, when a "found bug" might be a broken test, or when designing a harness that asks models to propose tests. Not needed for running an existing trusted suite.
---

# Tests that can fail

A check is evidence only if it could have failed, and would have failed for the reason
you care about. Models that write tests break this in a small number of repeatable ways.
The cause is rarely lack of ability. It is that nothing in the setup forces a check to
be falsifiable, so some checks can never fail, some always fail, and some compare the
wrong two things.

The patterns below were measured in blind runs where models wrote contracts for release
pairs of real Python libraries (a known-defective version and its fix) and a mechanical
judge scored them. The full catalogue is in
[references/failure-modes.md](references/failure-modes.md).

## Three questions for every check

Ask these of each assertion before you count it as evidence.

1. **Can it fail?** Name one concrete wrong output that would make it fail. If you
   cannot, it is filler. `x == x`, `len(x) == len(x)` and "result is not null" on a
   function that always returns something are the common cases.
2. **Does it pass on behaviour you know is right?** A check that fails on every input is
   a broken check. It also hides every assertion after it if the runner stops at the
   first failure, and it looks exactly like a big find.
3. **Is it about the two things the document relates?** Reread the sentence it is based
   on. Check the scope ("for integer types…" is not "for all types"), the direction
   ("-1 means a is lower"), and the field (the type name does not belong in the text field).

## The five causes

Deduplicated over 256 recorded apparatus failures, almost all fall into five groups.

| Cause | Share | What it looks like | What to do |
| --- | --- | --- | --- |
| **Operands** — the two things compared are not the two the document relates | 34% | int compared with bool, nested list with flat list, float `12.0` with int `12`; a sign or polarity read backwards; two different calls treated as one | Check both sides have the same type and shape. Work one example by hand for any compare-style field. Derive a relation between two calls from a rule that covers every input |
| **Scope** — true on part of the domain, written as universal | 27% | a README example (`ordinal(347) → '347th'`) asserted for all inputs; a basis that says "for integer formats" on an unconditional assertion; a closed bound whose endpoint is exactly the buggy value | Write the condition into the assertion. Treat doc examples as instances. When the doc says "less than" or "avoids", use a strict bound |
| **Filler** — written to satisfy a count or a rule | 25% | tautologies; assertions whose own rationale says "weak" or "included by mistake"; a documented operation never called; only relations between calls, no absolute claim | Never require "at least N tests". Allow an empty slot with a reason. Require one absolute claim per call |
| **Judge** — the scoring itself is wrong | 8% | a defect shared by both versions blocks credit elsewhere; a fix that looks like a regression | Score per input, not per assertion. Compare against the document before calling a new-version-only failure a regression |
| **Protocol** — the feedback loop misleads the model | 6% | validation errors that cite the wrong index, so the model resubmits unchanged; errors reported one class at a time | Quote the offending line in every validation message. Report all errors in one round |

## Procedure when you write the checks

1. **Read the behaviour claim first** and note, per operation, what the operation changes.
   Models tend to assert what stays the same, which a no-op bug also satisfies. Write at
   least one "this changed" check where the operation is supposed to change something.
2. **Commit the assertions before you see any output.** In a control run, the same model
   that caught a wrong exception when it had written `error == null` in advance printed
   that exception in 12 of 12 free-form sessions and still judged the behaviour
   consistent with the docs. Do not write a check after looking at what the code returned.
3. **Cover by construction.** Call every documented operation on every input. Free
   exploration skips whole operations: in 24 self-directed sessions no model called the
   one operation that held the defect.
4. **Sanity-pass each assertion.** It must hold on at least one observation before a
   failure of it means anything. With this one gate, one model went from 4 of 6 clean
   contracts to 6 of 6; another went from 0 of 4 contracts confirming one of the two
   known defects to 4 of 4 confirming both.
5. **Run against two versions if you can** — a known-good or fixed one beside the suspect.
   Failing on both means the check is wrong (or both share a defect). Failing only on the
   suspect is a finding. Failing only on the newer one needs the document: it may be an
   assertion that was written to match the bug. In ten contracts this separation was
   exact: every real detector failed on the old version only, every wrong assertion on both.
6. **State what the green result does not show.** Passing checks cover the inputs and
   properties tried. Say which operations, input classes or failure types were not exercised.

## Reviewing checks a model wrote

Go through them with this list. Stop treating the suite as evidence until each item is settled.

- [ ] No assertion compares a value with itself or restates its own setup.
- [ ] Every assertion has been seen to pass on some input and could fail on a named wrong output.
- [ ] Both sides of each comparison have the same type and shape; numbers are normalised before equality.
- [ ] Any sign, order or boolean-polarity check has a worked example next to it.
- [ ] Constants appear only on fields that do not depend on the input.
- [ ] Each stated condition in a rationale also appears in the assertion.
- [ ] Bounds are strict where the document says "less than", and use the right base (1024 vs 1000).
- [ ] Every documented operation is called; every feature field the harness exposes is read by some assertion.
- [ ] Each call has at least one absolute claim, so "everything wrong together" is visible.
- [ ] A red test names which side is wrong — the implementation or the test.
- [ ] The person or process that judges pass/fail did not also write the result it is judging.

## If you are building the harness

Rejecting bad assertions one rule at a time, and pasting lessons into the prompt, did not
move results in two memory-arm experiments and grew the prompt to over 40 KB. Changing the
structure did: let assertions carry a `when` scope (documents are written as conditionals);
give each call a fixed set of slots where an empty slot with a reason is valid, and drop
count and coverage quotas so there is nothing to pad; address hypotheses by slot and report
all validation errors at once. Operand mistakes are not fixed by format — keep the
two-version comparison as the backstop.

Every guard needs the same care as the tests: when you add a gate, list every path that
can confirm a failure and run each through it. A replay path that skipped the gate
"to reproduce known failures" is how wrong assertions got confirmed through the side door.
