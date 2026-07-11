# Trial 001: Responsible Succession

This is the first falsifiable experiment for the Knowledge Seed Protocol. It
transfers a small capability and its cultural rationale from an event-aware
sender to a plain Python receiver. No `self` runtime or model is required.

Read [`KSP-0001.md`](KSP-0001.md) for the claims, limits, and failure criteria.

## Run

Requires Python 3.9+ and only the standard library.

```sh
python3 trial-001/ksp_trial.py validate \
  trial-001/seeds/responsible-succession.seed.jsonl

python3 trial-001/ksp_trial.py plant \
  trial-001/seeds/responsible-succession.seed.jsonl \
  --home /tmp/ksp-trial-001 \
  --policy trial-001/policy.example.json

/tmp/ksp-trial-001/responsible-succession claim \
  "the receiver rebuilt a local capability"
/tmp/ksp-trial-001/responsible-succession verify local-1 pass \
  "artifact and replay verification passed"
/tmp/ksp-trial-001/responsible-succession bequeath \
  "inspect the receipts before trusting this result"

python3 trial-001/ksp_trial.py verify --home /tmp/ksp-trial-001
python3 trial-001/ksp_trial.py show --home /tmp/ksp-trial-001
python3 -m unittest discover -s trial-001/tests -v
```

`plant` refuses a non-empty home to keep each run isolated. The receiver
creates its own key, generated capability, append-only local log, accepted
seed copy, and receipts. The seed remains inert data under `incoming/`.

## What This Demonstrates

- A seed can carry design history, alternatives, evidence, culture, and a
  capability declaration without executable code.
- A receiver can reject or remap input under its own policy.
- A receiver can author and sign its own implementation.
- Claims, verification, and bequests remain distinguishable on replay.

## What Remains External

- An independent receiver implementation and operator.
- A second model or system performing reconstruction.
- Evaluation of whether the practice changes behavior outside this narrow
  workflow.
- Wouter's one-page human motivation for why this experiment matters.

The first local rehearsal is recorded in
[`reference-result.md`](reference-result.md). It is implementation evidence,
not independent confirmation.
