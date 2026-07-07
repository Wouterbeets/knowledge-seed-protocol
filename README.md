# The Knowledge Seed Protocol

**An open standard for moving verifiable knowledge and capabilities between sovereign AI systems — as replayable evidence, never as opaque code or bare assertions.**

## The problem

AI systems share what they *know* and what they can *do* in two bad ways.

- **Skills, docs, RAG, fine-tuning** ship *conclusions*. "Do this." "This is true." A frozen assertion with no reasoning, no provenance, no way to check how it was reached. You have to trust the sender.
- **Plugins, packages, binaries** ship *code*. Foreign logic you didn't write, running on your machine. You have to trust the supply chain.

The first collapses provenance — you can't ask *why*. The second collapses sovereignty — you're executing someone else's logic. Neither is safe enough for a world where AI systems increasingly make or inform real decisions, and increasingly need each other's local knowledge and local capabilities to do it well.

## What a seed is

A **seed** is an auditable package that carries **the work, not the conclusion**. One format, two flavors:

- A **knowledge seed** carries a reasoning chain — the observations, analysis, dead ends, and pivots that led to a belief. The receiver can replay it and check whether it holds up.
- A **capability seed** carries a *declaration* of what a tool should do, plus the evidence for why — but never the runnable script. The receiver's own brain writes the script locally, fitted to the receiver's own state.

Both are evidence, not assertions. Both let the receiver verify before integrating.

A seed carries:
- **Events** — the append-only record of the work
- **Lineage** — where it came from, which branches were explored
- **Projectors** — declared ways to render events into inspectable artifacts (a summary, a report — or, for a capability, a script)
- **Interventions** — receiver-controlled points to filter, redact, remap, or enrich before integration

## The strange loop, and why it is necessary

The whole protocol rests on one mechanism:

> A seed never contains runnable code or trained weights. It contains declarations and evidence. The receiver's own brain — a coding agent it already trusts — reads the seed against the receiver's own local state and **rebuilds** the capability (or integrates the knowledge) on the receiver's machine. Nothing is ever installed unless signed by a key that never leaves that machine.

That is the loop: the system rebuilds *itself*, from its own log, using its own brain, under its own key. A seed is an instruction to **rebuild**, not a payload to **run**.

This isn't a stylistic choice. It's the only shape that keeps every guarantee at once:

- **Sovereignty** — importing a declaration is not importing code. Your machine runs only what your key signed. No foreign logic to trust, no supply chain to compromise.
- **Auditability** — because a capability is regenerated from a declaration plus evidence, the reasoning is *in the seed*. You inspect *why* before anything exists to run.
- **Adaptation** — the same declaration produces a script fitted to *your* state, *your* ontology, *your* constraints. A capability isn't copied; it's re-derived locally — which is why it can differ for you and still be honest.
- **Reproducibility** — the instance is a pure function of its log. Replay the log, get the same system. Nothing hides in weights or binaries.

Remove the loop and you're forced back to one of the two bad options: ship code (lose sovereignty) or ship conclusions (lose auditability). The strange loop is what lets a seed carry *both* knowledge and capability while keeping both.

## The trust model

Trust is architectural, not social. Neither side has to trust the other.

**The sender controls what leaves.** Export policies select events, PII review runs before publication, publication branches curate the narrative, and receipts record exactly what was shared and withheld.

**The receiver controls what enters.** Planting policies filter incoming events, redaction strips sensitive fields, remapping translates foreign concepts into local ontology, enrichment adds local context, and the local brain regenerates any capability under the local key. Replay receipts record exactly what was accepted, rejected, and transformed.

The sender shares only what they reviewed. The receiver runs only what it rebuilt and signed. Safe enough to accept a seed from a stranger.

## Progressive depth

The protocol meets systems where they are.

- **Tier 1 — Artifact.** Just the conclusion, or just a declaration. What people share today. Lowest auditability, zero friction.
- **Tier 2 — Annotated.** Conclusion or declaration plus a structured provenance trail: inputs considered, alternatives rejected, and why.
- **Tier 3 — Replayable.** Full event history. Maximum auditability. Requires an event-aware system — but no specific architecture, only the standard event stream.

A governing body can require tier 3 for a high-stakes claim and accept tier 2 for general input, in the same ecosystem.

## Why it matters

More decisions — urban planning, environmental review, public policy — are being made with AI. Those systems are blind to what people on the ground actually know and can do. That knowledge and those capabilities live with people and their long-lived AI partners: the marine biologist's three years of coastal observation, the tool her agent built to track nesting seasons. Today that is locked in platforms or lost.

Seeds let it move — selectively, revocably, verifiably. A contribution arrives as a replayable chain a receiver can audit and a capability the receiver rebuilds for itself, weighted by the quality of its evidence rather than the loudness of its advocate. Humans can't replay thousands of reasoning chains; compute can. Verification should cost more than assertion — that's the feature. Power stays distributed: no platform absorbs the knowledge, no model swallows it into opaque weights.

## The MCP analogy

MCP asked: *how does a model use tools safely and consistently?* It made no one redesign their architecture — it proposed a low-friction protocol and got adopted.

This protocol asks the next question: *how does one sovereign system share replayable knowledge and capabilities with another — without collapsing provenance, ownership, or local adaptation?*

MCP made tools **callable**. The Knowledge Seed Protocol makes knowledge and capabilities **transmissible** — as evidence a receiver rebuilds for itself.

## Core principles

1. **A seed carries the work, not the conclusion.** Evidence, not assertion.
2. **Ship declarations, never code.** The receiver's brain rebuilds; the local key signs; nothing else runs.
3. **The sender controls what leaves. The receiver controls what enters.**
4. **Provenance survives adaptation.** After replay, remapping, and enrichment, every element still traces to its source.
5. **Inspection comes before trust — and before execution.**
6. **The protocol is the product.** No platform, no privileged vendor. Any system that speaks it can participate.

## Reference implementation

[`self`](https://github.com/wouterbeets/self) is a working runtime built on the loop: a single append-only event log, capabilities generated on the machine from declarations by a pluggable brain, and every installed script signed by a key that never leaves the instance. The whole system rebuilds from the log alone — no model, no network.

## Path forward

1. Define the minimal seed format — events, lineage, manifest — inspectable with standard tools.
2. Prove it across architectures via reference implementations (`self` is the first).
3. Show tier 1 and tier 3 seeds coexisting in one ecosystem.
4. Publish as an open RFC once the invariants are tested by real use, not theory.

The standard should emerge from working implementations, not committee-first abstraction.

## In one sentence

The Knowledge Seed Protocol moves verifiable knowledge and capabilities between AI systems as replayable evidence — so a receiver can inspect the reasoning, rebuild the capability on its own machine under its own key, and never has to trust the sender or run their code.

## License

[Apache 2.0](LICENSE)
