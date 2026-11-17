# Failure modes of model-written checks

Each entry was observed in a scored run, not inferred. "Old" is the release with a
documented defect, "new" is the release that fixes it. Guards marked *implemented* were
built into the audit harness and re-scored on the recorded proposals.

## Operands — comparing the wrong two things

| # | What happened | Guard |
| --- | --- | --- |
| 1 | **Sign read backwards.** A field described as "-1 means a is lower than b" was asserted `== 1` in 3 of 6 blind contracts, so the whole contract failed on every input. Boolean polarity goes the same way (`bool(range) == is_empty`, 4 of 4). | Give one worked example for every compare, order or polarity field. A one-line definition is not enough. |
| 2 | **Different shapes on the two sides.** Integer count against boolean flag (`0 != false`); a nested chunk list tested as a permutation of a flat list. Fails on every non-trivial input, and a "pointer resolves" check lets it through. | Compare the schema types of both operands. *Implemented:* stopped 11 assertions in 10 proposals, all already known bad from replay. |
| 3 | **Float against integer equality.** The observation reports `12.0`, the input is `12`; under canonical JSON they never match. | Normalise numbers before equality, or make field types uniform. |
| 4 | **Two calls treated as one.** `plural_noun == singular_of_plural`, `plural_int == plural_noun`: true only for special words, fails on about 90% of inputs. Minimisation then lands the failure on an arbitrary input and it reads like a real catch. | A relation between two calls must follow from a rule covering all inputs. Credit only rows that fail inside the documented condition on old and never on new. |
| 5 | **Sibling fields mixed up.** The type name written into the text field: `value_text == 'int'`. Both are strings, so the shape check passes. | A constant must belong to the field it is compared with. |
| 6 | **Right implementation, wrong test.** The model's code was correct (0 failures in 300) and its own test expected the wrong value; its self-review passed the test. | A red test is not yet blame. Be able to say which side is wrong: extract the literal claim and compare with a reference. |

## Scope — partly true, written as universal

| # | What happened | Guard |
| --- | --- | --- |
| 7 | **Doc example used as a constant for all inputs.** README says `ordinal(347) → '347th'`; the model asserts `ordinal/text == '347th'` everywhere (28 assertions in 4 proposals). Variants that hold for one input (`== '1st'` when n=1) pass a "holds at least once" gate and then report on both versions. | Constants only on fields that do not depend on input. Tell the model examples are instances. |
| 8 | **Conditional rationale, unconditional assertion.** Rationale: "for integer type codes the output is int". Assertion: `value_type == 'int'` for every type code (18 assertions; fails for 6 of 11 codes on both versions). | The scope of the rationale must equal the scope of the assertion. Give the language a way to say `when`. |
| 9 | **Closed bound whose endpoint is the buggy value.** The doc says to avoid `1000`; the model writes `bounded [-1000, 1000]`; the defect prints exactly `1000.0 kB`. All three silent wrong-value defects were missed this way. Tightening to ±999.999 fails 31–58 of 360 calls on old and 0 on new. | "Less than" and "avoids" mean a strict bound. Offer exclusive bounds in the vocabulary. Use the right base: 1024 for binary units. |
| 10 | **Assertion that is only sometimes wrong.** Comparing chunk count with element count holds on about a quarter of inputs, so it passes sanity and shape checks and fails identically on both versions. | Within one version it cannot be told from a conditional real bug. Compare two versions. |
| 11 | **Property the bug satisfies.** The defect was "nothing changed"; all six contracts asserted "precision is equal", which the bug meets. Nobody asserted "the text changed". | Have `not_equals` / `changed` available, and ask what the operation is supposed to alter before writing the property. |

## Filler — nothing is really claimed

| # | What happened | Guard |
| --- | --- | --- |
| 12 | **Tautologies.** `x == x`, `length(x) == length(x)`. Often written to satisfy a rule that every field be read (16 of 20 self-comparisons in one run). | Reject identical operands. *Implemented:* 10 hits in 1,976 historical assertions, all junk. |
| 13 | **The rationale disowns the assertion.** "This assertion is intentionally invalid… included to test schema budget", "weak", "included by mistake" — and the assertion is emitted anyway to reach a count. | No minimum count. Scan the rationale for stance (disowns it; admits exceptions), not a fixed phrase list. |
| 14 | **A documented operation never exercised.** 24 free-form test sessions, none called the one operation with the defect. | The harness calls every documented operation on every input. |
| 15 | **Invariant too weak.** "Returned in the `lost` list" counted as "handled". | Tie the invariant to a consequence a user can see. |
| 16 | **A feature field nobody reads.** The harness exposed a `double_space` boolean; one model asserted on it in 22 of 22 proposals and caught the defect, the other ignored it in 19 of 24. Prompt lessons did not change this. | Return a proposal that leaves an exposed feature field unread, and name the field. |
| 17 | **Relations only.** `plain == signed == padded` stays true when every call raises the same error. 11 of 24 proposals earned no credit this way. | At least one absolute claim per call. |
| 18 | **An expressible probe nobody wrote.** A round-trip check (`singular(plural(w)) == w`) was expressible and would have caught the defect; none of 24 proposals used it. | Name round-trip and equal-to-input forms in the vocabulary examples. Record beforehand what is expressible so you can measure what was not tried. |

## Judge — the scoring is wrong

| # | What happened | Guard |
| --- | --- | --- |
| 19 | **One always-failing assertion eats the budget.** With stop-at-first-failure, it hides everything after it and looks like a large bug. | Sanity pass: an assertion must hold on some observation before its failure counts. |
| 20 | **Self-judging explains evidence away.** The model printed the wrong exception and then recorded the behaviour as consistent with the docs (12 of 12 and at least 5 of 6 sessions for two models). Given the same task with assertions written first, both caught it. | Assertions are committed before results. A mechanical judge decides. |
| 21 | **A shared residual defect blocks credit.** Both versions mishandle `+nan`; scored per assertion, 22 contracts that caught the documented defect got 0 of 33. | Score per input: version-difference inputs inside the documented condition, with shared-defect inputs separated by the two-version comparison. |
| 22 | **A fix that looks like a regression.** An assertion written to match the buggy behaviour passes on old and fails on new. | A failure only on the new version goes to the document before it is called a regression. |
| 23 | **The gate guards the front door only.** A replay path was exempted from the sanity gate so known failures could be reproduced; always-failing assertions were confirmed through it. | Exempt by property signature, not by path. When adding a gate, enumerate every path that can confirm a failure. |

## Protocol — the feedback loop misleads

| # | What happened | Guard |
| --- | --- | --- |
| 24 | **Validation message with two index systems.** "assertion 9: operands of assertion 10…" — the model fixed the wrong line and resubmitted the same one. | One index system, and quote the assertion text. |
| 25 | **Hypothesis points to an assertion that does not exist.** Almost always off by one. | State the total and valid range in the error. |
| 26 | **Rules squeeze each other.** A coverage rule, a cap of 24 assertions and two attempts together pushed models to write junk to satisfy coverage; errors reported one class per round meant some proposals first heard of a problem on their last attempt. | Report every class of error in one round, and say how many slots remain. |
| 27 | **Citation off by one line.** The same model cited line 28 for line 29 four times. | Keep citation checking exact but allow a repair round. It is a slip, not a misunderstanding. |

## Benchmarks for concurrency

| # | What happened | Guard |
| --- | --- | --- |
| 28 | **The benchmark parks itself.** The main thread calls into a parked scheduling point, waits for the timeout, nothing happens, and the benchmark "passes" on the defective version. | Document that behaviour in the harness; count "passes on the defective version" as a miss. |
| 29 | **A gate name that does not exist.** The benchmark parks on a point the mechanism never reaches; both versions time out. | Validate gate names at design time. |
| 30 | **The injected defect ranks second.** Top suspicion pointed to the right code region in 15 of 16 cases, but the injected defect was often second, behind another real weakness nearby. | Write a benchmark for each of the top two suspicions and score them separately. |
