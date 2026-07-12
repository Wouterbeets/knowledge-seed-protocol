# The account format — v0

An account is a directory of plain text. It is the one wire format of the
Account Protocol: everything that moves between instances moves as one of
these, and every operation it supports — inspection, curation, redaction,
translation — is a text editor. This spec is deliberately small enough to be
held whole; its first readers are the brains that must honor it.

```
account/
  intent.md      the telling      required
  record.jsonl   the evidence     optional
  manifest.json  the attestation  optional
```

A directory with only `intent.md` is a **lesson** (tier 1). Add a structured
provenance trail to the telling and it is tier 2. Add the full record and it
is tier 3 — shown work, replayable.

## intent.md — the telling

Plain Markdown, written to be read by the human who audits first and the
brain that learns second. It says who this is from, what it means, and what
the giver hopes it becomes. For a capability account it fixes the public
surface (names, arguments, behavior) and leaves the implementation to the
learner. The telling is the only part of an account that is *meant* to
persuade; that is why it is read before anything is integrated.

## record.jsonl — the evidence

One JSON object per line:

```json
{"id":"…","seq":12,"name":"note.taken","occurred_at":"2024-03-09T12:30:00Z","payload":{…}}
```

Rules, all mechanical:

1. **Verbatim out.** A giver writes selected events exactly as they appear in
   its log. Curation is deleting lines, never editing them.
2. **Moments preserved.** A learner re-mints `id` and `seq` (they are local)
   but MUST keep `occurred_at`. A record arriving is history, not news.
3. **Never through the model.** Planted events land byte-identical in the
   receiver's log. The receiving brain reads the record; it never rewrites
   it. Translation into local vocabulary happens in the receiver's
   projections — the planted events stay foreign and honest.
4. **Reserved vocabulary.** Every runtime has lifecycle events its kernel
   acts on (in `self`: `command.declared`, `projector.declared`,
   `script.compiled`, `capability.retired`, `intent.declared`,
   `lesson.learned`, `account.given`, `learn.orchestrated`,
   `self.reflected`, `kernel.initialized`, `capability.revision.requested`).
   A giver MUST rename its own lifecycle events to `lineage.<name>` on the
   way out; a learner MUST refuse a record that carries the learner's
   lifecycle names raw. Consequence: an account can carry its whole history
   as evidence, but it cannot speak in the receiving kernel's voice — a
   hostile account cannot install anything.
5. **Lineage is inert by type.** `lineage.*` events are another instance's
   history: reference material for the learning brain and for provenance,
   never operative. A capability account is exactly this — the giver's
   declarations and signed receipts as `lineage.*`, from which the learner's
   brain derives its own declaration, compiled and signed locally.

## manifest.json — the attestation

```json
{
  "events": 12,
  "record_sha256": "<sha256 hex of record.jsonl, exact bytes>",
  "prefix": "note.",
  "capability": "command/note",
  "signer": "wouter",
  "signature": "record.jsonl.sig"
}
```

- `events`, `record_sha256` — what was given. Required when a record is present.
- `prefix` *or* `capability` — the selector that produced the record (flavor marker).
- `signer`, `signature` — optional identity. `signature` names a detached
  signature file over `record.jsonl`, made with standard tools
  (`ssh-keygen -Y sign -n account -f <key> record.jsonl`); `signer` is a name
  the receiver may look up in its own allowed-signers list
  (`ssh-keygen -Y verify`). The protocol adds no key distribution: a
  signature answers *who to blame*, never *what the contents do to the brain
  that reads them*. Identity narrows provenance; inspection remains the gate.

## Receipts — both sides remember

- The giver appends **`account.given`** `{selector, events, dir,
  record_sha256}` to its own log at the moment of giving.
- The learner appends **`lesson.learned`** `{lesson, capabilities, events,
  record_sha256, manifest_sha256}` — where `record_sha256` is the digest of
  the record file it *actually* read, beside the manifest's claim.

A mismatch between the two digests is not an error. It means the account was
edited between giving and learning — a curation, a redaction, an
intervention. All of those are legitimate, receiver-sovereign moves; the
format's job is only to make them **visible, forever, in both ledgers**.

## Conformance

A runtime speaks the Account Protocol when:

1. its *give* writes this directory with a truthful manifest and renames its
   own lifecycle events to `lineage.*`;
2. its *learn* refuses raw lifecycle vocabulary, preserves `occurred_at`,
   plants the record verbatim without routing it through a model, derives
   any capability locally under a local key, and records both digests in its
   receipt;
3. nothing carried by an account is ever executed or installed as received.

Everything else — how the brain reads a telling, how projections translate a
foreign record, what a nursery or study page looks like — is the runtime's
own character, not the protocol's business.
