# The Account Protocol

**An open standard for moving records and capabilities between sovereign AI
systems — as accounts a receiver reads and learns from, never as opaque code
or bare assertions.**

*(Formerly the Knowledge Seed Protocol. The idea was always bigger than
knowledge; the name caught up.)*

## The problem

AI systems share what they *know* and what they can *do* in two bad ways.

- **Skills, docs, RAG, fine-tuning** ship *conclusions*. "Do this." "This is true." A frozen assertion with no reasoning, no provenance, no way to check how it was reached. You have to trust the sender.
- **Plugins, packages, binaries** ship *code*. Foreign logic you didn't write, running on your machine. You have to trust the supply chain.

The first collapses provenance — you can't ask *why*. The second collapses sovereignty — you're executing someone else's logic. Neither is safe enough for a world where AI systems increasingly make or inform real decisions, and increasingly need each other's local knowledge and local capabilities to do it well.

People solved this long ago, between themselves. You cannot transplant a
skill, and you cannot write into another mind's memory. What you can do is
**give an account** — show your work — and let the other mind learn it in its
own substance. This protocol is that move, made precise enough for machines.

## What an account is

An **account** is an auditable directory that carries **the work, not the
conclusion**. The word is doing both of its jobs at once: an account is a
*narrative* (who I am, what this means, what I hope it becomes) and a
*ledger* (the record of what actually happened). One format, two flavors:

- A **record account** carries evidence — the events of a lived stretch of
  work, verbatim, with their original moments. The receiver can replay it and
  check whether it holds up.
- A **capability account** carries a *declaration* of what a tool should do,
  plus the lineage of how the giver built and ran it — but never the runnable
  script. The receiver's own brain writes the script locally, fitted to the
  receiver's own state.

Both are evidence, not assertions. Both let the receiver verify before
integrating. And a capability account is a *lesson*, not a package: the same
lesson, learned by two students, produces two different understandings — each
fitted to what that mind already knew. That is not drift to be corrected; it
is the point.

An account carries:
- **The intent** — the telling: read by the human who audits first, the brain that integrates second
- **The record** — the append-only evidence, moments preserved, including **lineage** (the giver's own history, explicitly marked, inert by type)
- **The manifest** — the attestation: what was given, so any edit after the giving is visible

The format is specified in [ACCOUNT.md](ACCOUNT.md). It is three plain-text
files; every intervention it supports is a text editor.

## The strange loop, and why it is necessary

The whole protocol rests on one mechanism:

> An account never contains runnable code or trained weights. It contains a telling and evidence. The receiver's own brain — a coding agent it already trusts — reads the account against the receiver's own local state and **learns** the capability (or integrates the record) on the receiver's machine. Nothing is ever installed unless signed by a key that never leaves that machine.

That is the loop: the system rebuilds *itself*, from its own log, using its
own brain, under its own key. An account is something to **learn from**,
never a payload to **run**. You can't transplant a skill; you can only show
your work.

This isn't a stylistic choice. It's the only shape that keeps every guarantee at once:

- **Sovereignty** — learning from an account is not importing code. Your machine runs only what your key signed. No foreign logic to trust, no supply chain to compromise.
- **Auditability** — because a capability is re-derived from a declaration plus evidence, the reasoning is *in the account*. You inspect *why* before anything exists to run.
- **Adaptation** — the same account produces a capability fitted to *your* state, *your* ontology, *your* constraints. A capability isn't copied; it's learned — which is why it can differ for you and still be honest.
- **Reproducibility** — the instance is a pure function of its log. Replay the log, get the same system. Nothing hides in weights or binaries.

Remove the loop and you're forced back to one of the two bad options: ship code (lose sovereignty) or ship conclusions (lose auditability). The strange loop is what lets an account carry *both* records and capabilities while keeping both guarantees.

## The trust model

Trust is architectural, not social. Neither side has to trust the other —
and the economics enforce the posture: **giving is cheap; learning is the
work.** Verification costs more than assertion, on purpose.

**The giver controls what leaves.** Giving writes the account as plain files;
curation is editing them — trim the record, rewrite the telling — before the
directory is passed on. The giver's log keeps a receipt of exactly what was
given, digest included.

**The receiver controls what enters.** The account sits as inspectable text
before anything happens. Filtering is deleting lines; redaction is `sed`;
remapping foreign concepts into local ontology happens in the receiver's own
projections, never by rewriting the planted record. The local brain learns
any capability fresh, under the local key. The receiver's receipt records the
digest of what was actually integrated beside what the manifest claimed — so
every intervention between giving and learning is visible in both ledgers,
forever.

The giver shares only what they reviewed. The receiver runs only what it
learned and signed. Safe enough to accept an account from a stranger.

**Identity lives at this layer — and it is not a shortcut.** A runtime's machine-resident key proves nothing across machines; who gave an account, and whether it arrived intact, is the protocol's job, as signatures over the account itself. But a valid signature answers only *who to blame* — never *what the contents do to the brain that reads them*. The moment "signed by someone I know" substitutes for reading, the trust model is dead. Identity narrows provenance; inspection remains the gate.

## Progressive depth

The protocol meets systems where they are — the tiers are just how much work
is shown:

- **Tier 1 — Assertion.** Just the telling: a conclusion, or a bare lesson. What people share today. Lowest auditability, zero friction.
- **Tier 2 — Explained.** The telling plus a structured provenance trail: inputs considered, alternatives rejected, and why.
- **Tier 3 — Shown work.** The full record, replayable, moments intact. Maximum auditability. Requires an event-aware system — but no specific architecture, only the standard format.

A governing body can require tier 3 for a high-stakes claim and accept tier 2 for general input, in the same ecosystem.

## The rendering condition

Projectors pin a **condition, not a technology**: mutual legibility. The rendered artifact must be perceivable by the human who audits and the machine that acts — one artifact, two kinds of reader, with the affordances visible in the artifact itself. Hypertext is the current maximum of that intersection (hierarchy, links, forms, and native to both minds); a text-described world could be tomorrow's. Any medium qualifies if it keeps three invariants:

- **Determinism** — same events, same artifact. The render is a pure replay.
- **Affordance honesty** — nothing interactable that isn't backed by a declared command. A button (or a lever) cannot lie about what it does.
- **Symmetric perception** — what the human audits is exactly what the machine perceives. The moment one mind sees what the other cannot, the audit is fiction.

This is why the protocol has no hidden machine channel: the surface the human reviews *is* the surface the agent acts on, and every guarantee above depends on keeping it that way.

## Why it matters

More decisions — urban planning, environmental review, public policy — are being made with AI. Those systems are blind to what people on the ground actually know and can do. That knowledge and those capabilities live with people and their long-lived AI partners: the marine biologist's three years of coastal observation, the tool her agent built to track nesting seasons. Today that is locked in platforms or lost.

Accounts let it move — selectively, revocably, verifiably. A contribution arrives as a replayable record a receiver can audit and a capability the receiver learns for itself, weighted by the quality of its evidence rather than the loudness of its advocate. Humans can't replay thousands of reasoning chains; compute can. Verification should cost more than assertion — that's the feature.

Two consequences follow from the shape, and they are the stakes:

**Local knowledge compounds without being averaged.** Foundation models are trained on the mean and pull everything routed through them toward it. In this architecture the model only ever writes the *disposable* part — the script, the expression — while the part that accumulates (the events, the lineage, the local vocabulary, the life of the instance) never passes through the model's gravity at all. Only the telling crosses between instances, and it re-expresses locally on arrival. Accounts are horizontal transfer between sovereign minds, not vertical inheritance from a central model: an ecology that preserves variation, rather than a monoculture that erases it. Collective intelligence, here, is not an aggregate — it is an ecosystem.

**Exit is free, so the relationship stays honest.** The brain is fungible; the log is the estate. Identity, memory, and accumulated mutual understanding accrue to the record a person owns, not to the model that happens to be reading it. Fire the model tomorrow, plug in another, lose nothing. A relationship with AI in which leaving costs you your own past is loyalty by hostage-taking; this one is governed by exit.

And one older analogy holds the whole thing: this is a **gift economy**, not
a commodity market. A gift carries the giver with it and creates a
relationship; a commodity is anonymous and closed. A platform's frozen model
is the commodity — usable, but you can never re-derive it, never ask it why,
never grow your own from it. An account is the gift: it arrives with its
history attached and asks to be understood.

## The MCP analogy

MCP asked: *how does a model use tools safely and consistently?* It made no one redesign their architecture — it proposed a low-friction protocol and got adopted.

This protocol asks the next question: *how does one sovereign system share replayable records and capabilities with another — without collapsing provenance, ownership, or local adaptation?*

MCP made tools **callable**. The Account Protocol makes records and capabilities **learnable** — as evidence a receiver rebuilds for itself.

## Core principles

1. **An account carries the work, not the conclusion.** Evidence, not assertion.
2. **Give tellings, never code.** The receiver's brain learns; the local key signs; nothing else runs.
3. **The giver controls what leaves. The receiver controls what enters.** Both sides keep receipts.
4. **Provenance survives adaptation.** After learning, remapping, and enrichment, every element still traces to its source — lineage is explicit and inert.
5. **Inspection comes before trust — and before execution.** Giving is cheap; learning is the work.
6. **The protocol is the product.** No platform, no privileged vendor. Any system that speaks the format can participate.

## Honest edges

The guarantees have boundaries. Naming them is part of the spec.

- **The compiler is a monoculture.** The averaging the account format evicts at the artifact level re-enters at the authoring level: today, every learned capability is authored by a handful of foundation models with shared idioms. The design answers with a division of labor — commodity intelligence for the replaceable part, sovereignty for the irreplaceable part. That division is the load-bearing wall of the whole protocol. If local knowledge ever has to route *through* the compiler to survive, the protocol has failed at its own game.
- **Injection rides in evidence.** An account's dangerous surface is not its bytes but its persuasive content: tellings and records are read by the receiver's brain, and a hostile account is an attempt to persuade that brain. Signatures do not reduce this — inspection and the format's mechanical gates do.
- **The posture assumes a reader.** Inspection-before-integration scales to people and systems that actually read. The growth path is not to relax that assumption but to make legibility cheaper — better projectors, better-rendered evidence — until reading is the easy path.
- **Declared vocabularies collide.** An event name and its fields are the only schema a record carries. Two instances can name the same thing differently, and a planted record renders nonsense until translated. Translation happens in the receiver's projections — never by rewriting the planted events.

## Reference implementation

[`self`](https://github.com/wouterbeets/self) is a working runtime built on the loop: a single append-only event log, capabilities generated on the machine from declarations by a pluggable brain, and every installed script signed by a key that never leaves the instance. The whole system rebuilds from the log alone — no model, no network. Its `self give` and `self learn` speak the format in [ACCOUNT.md](ACCOUNT.md).

## The first experiment

Adaptation is the protocol's central claim, so it gets measured, not asserted. The discipline: when one account is learned in two environments, distinguish three levels of divergence.

1. **Content** — same script, different events rendered. Guaranteed by replay; not a result.
2. **Implementation** — different script, same surface. The local compiler's idiom; mildly interesting.
3. **Decomposition** — different capabilities, different event vocabulary, different unfolding. The lesson actually expressing its environment. This is the claim.

The canonical run: freeze one telling byte-for-byte, learn it in two instances with different lives — a work instance full of tickets and sprint goals, a home instance full of meal plans and practice schedules — and diff what was learned, including the orchestration reasoning each brain logged, which is the experiment's lab notebook and is already in the record. Identical results are a finding too: either the telling over-specified, or the instance's identity wasn't legible from its own surface. Both are corrections the protocol wants.

## Path forward

1. ~~Define the minimal account format~~ — [ACCOUNT.md](ACCOUNT.md): three plain-text files, inspectable and writable with standard tools.
2. Account signatures are specified (detached, standard tools, never a substitute for inspection); prove them in the reference implementation.
3. Prove the format across architectures via reference implementations (`self` is the first), starting with the divergence experiment above.
4. Show tier 1 and tier 3 accounts coexisting in one ecosystem.
5. Keep the spec small enough to be held whole — the budget is a working context window, because the spec's first readers are the brains that must honor it.
6. Publish as an open RFC once the invariants are tested by real use, not theory.

The standard should emerge from working implementations, not committee-first abstraction.

## License

[Apache 2.0](LICENSE)
