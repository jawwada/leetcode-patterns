# Q007. Design an agent evaluation pipeline

## Scope and success

Gate releases of a CX support agent on conversation, retrieval, tool-use, and business correctness. Define critical invariants separately from average quality. Success is a reproducible decision that a candidate release meets the customer's criteria and does not regress important cohorts.

## Architecture and request path

A versioned dataset contains user turns, trusted test identities, fixture documents, expected actions, and rubrics. A runner drives the candidate CX environment against isolated backend fixtures. It captures page/playbook paths, tool arguments, evidence, responses, latency, and authoritative operation outcomes.

Deterministic assertions check ownership and action count. Retrieval metrics assess whether relevant sources appeared. Human reviewers and calibrated model judges assess supported explanations and conversation quality. An aggregator compares candidate and baseline, producing a signed release report.

## Data and contracts

An evaluation run records release manifest, dataset version, seed where applicable, repeated trial, rubric version, judge configuration, and individual results. Keep development examples separate from held-out cases. Store restricted evaluation content under the same access discipline as production data.

## Failure, security, and scale

No test call may reach a real payment or customer mutation endpoint. Use sandbox adapters and denied-access identities. Retry runner infrastructure separately from the tested behavior so failures are not concealed. Parallelize independent sessions while preserving turn order within each session.

## Trade-off and validation

Exact matching is reliable for action fields but brittle for valid paraphrases. Model judges scale semantic review but need human calibration and uncertainty analysis. Report distributions and cohort results, not only one mean. A critical invariant failure blocks promotion even if overall fluency improves.

## Interview follow-up answered

**The new version passes offline but fails in production.** Compare production distribution to dataset coverage, inspect release/data differences, roll back affected cohorts, and turn the incident into a held-out regression case. Offline evaluation reduces risk; it does not eliminate the need for controlled rollout and live outcome monitoring.
