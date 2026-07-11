# Trial 001 Reference Result

Status: reference implementation passed; independent reproduction pending.

Date: 2026-07-11

Environment: macOS, Python 3.14, standard library only. The receiver does not
import or invoke `self`.

## Procedure

1. Validated `responsible-succession.seed.jsonl`.
2. Planted it into a fresh temporary receiver home with
   `policy.example.json`.
3. Ran the receiver-authored artifact to append one claim, one passing
   verification, and one bequest.
4. Restarted the verifier and replayed the local record.
5. Ran the hostile and malformed-seed test suite.

## Observed Result

- Seed: 10 events, SHA-256
  `2e0808f72139228ce184c1300af04c1b82d47fec07a89ab2e434f5ef32a70f08`.
- Generated artifact SHA-256:
  `17c6d2731ecc7fc7ae8ae3ab975654cdc33be04d2e53ced078332972e351aef5`.
- Replay after actions: 16 receiver-signed, hash-chained local events.
- The culture event was remapped to `local.culture.practice` by receiver
  policy and the transformation was recorded.
- The original claim remained present after verification.
- Artifact tampering, nested executable fields, event reordering, and policy
  removal of the capability declaration were refused by tests.
- Seven unit tests passed.

The artifact digest is deterministic for this receiver version. Its signature
is not: each fresh receiver creates its own key.

## Claims Not Earned Yet

- No independent person or implementation has reproduced the result.
- No second AI system performed a semantic reconstruction from intent; the
  reference receiver uses receiver-owned fixed generation logic.
- The run does not show that inherited culture changes general AI behavior.
- Local HMAC receipts do not establish cross-system identity.
- The forbidden-field check reduces accidental code transfer but cannot prove
  arbitrary prose safe.

## Next Evidence

An external receiver should implement `KSP-0001.md` without reading
`ksp_trial.py`, publish its policy and receipts, and report disagreements with
the profile. A failed independent reproduction is useful evidence and should
remain in the trial history.
