# The Knowledge Seed Protocol

**Democracy scaled via compute.**

## The Problem

The world is making more decisions with AI. Urban planning, environmental review, public policy, business strategy — the trajectory is clear. But the AI systems making or informing these decisions have a fundamental blindness: they don't know what's happening on the ground.

Ask any frontier model about your local town and it will search the web, summarize some news articles, maybe pull from training data that's months or years stale. It will never know that turtle eggs hatch on the south beach every June. It will never know that the boat rental shop saw a 30% revenue drop when the coastal path was rerouted. It will never know the thing that the person who lives there knows.

That knowledge lives with people. And increasingly, it lives with the AI systems that work alongside those people — personal agents that accumulate rich, contextual, lived experience over months and years of collaboration.

This is not a training data problem. No amount of scraping or scaling will capture what a marine biologist and her AI have learned from three years of walking a coastline together. That knowledge is local, personal, and sovereign. It belongs to her.

The question is: how does she share it when it matters?

## The Current State

Today, the way AI systems share knowledge is primitive.

**Skills** are folders of markdown instructions. They say "do this" — a frozen snapshot of someone's current best guess, with no history, no reasoning, no way to verify how the conclusion was reached. A governing body that accepts a skill file is accepting an opaque assertion.

**RAG and fine-tuning** centralize knowledge into a single model or retrieval system. They collapse provenance. You can't ask "who contributed this, and why did they believe it?"

**Centralized platforms** aggregate user data to improve a shared model. The value flows up. The local knowledge that makes decisions better gets absorbed, anonymized, and stripped of context. The person who contributed it has no control over how it's used.

None of these approaches are adequate for a world where AI-assisted collective decision-making needs to be trustworthy, auditable, and democratic.

## The Vision

Imagine your local government is considering a new restaurant on the beach. The plans are public. The decision affects everyone.

In the current world, public comment means showing up to a meeting, writing a letter, or filling out a form. Most expertise never reaches the decision-makers. The marine biologist is busy. The boat rental owner doesn't think anyone cares. The retired urban planner across the street doesn't know there's a proposal.

In the world we're proposing, each of these people has an AI partner that has been learning alongside them. The biologist's agent has three years of coastal observation. The rental owner's agent has revenue trends, customer feedback, seasonal patterns. The urban planner's agent has decades of professional experience distilled through years of conversation.

Each of them can **donate a knowledge seed** — not a document, not an opinion, but a verifiable chain of reasoning showing how they arrived at their perspective. The governing body's AI system can replay each seed, inspect the evidence, weigh it against other inputs, and critically — audit exactly how every conclusion was formed.

The biologist doesn't submit a letter saying "there are turtle nests." She shares the work: the observations, the data collection, the seasonal patterns, the conversations with her AI where they analysed the trends together. The governing body can see it all, verify the reasoning, and integrate it alongside a hundred other contributions — each with its own transparent chain of evidence.

**This is not consultation. This is collective intelligence with distributed trust.**

## The Insight

Nothing beats boots-on-the-ground data for decision making.

As more people manage aspects of their lives with AI, extraordinarily rich data is preserved with the people who generate it. Today, that data is either locked in proprietary platforms or lost entirely.

Centralizing this into bigger, better, single-source-of-truth models is already proven to not work. The model will never have enough local knowledge, and it will always be stale. The information that matters most for local decisions is exactly the information that global models cannot have.

The alternative is decentralisation. The people who live there are the source. Their AI partners are the medium. What's missing is a safe protocol for sharing.

## What a Knowledge Seed Is

A knowledge seed is an **auditable evidence package with a verifiable reasoning chain**.

It carries:
- **Events**: the append-only record of the work — observations, conversations, analysis, pivots, dead ends
- **Lineage**: where this knowledge came from, which branches were explored, how the thinking evolved
- **Projectors**: declared ways to materialise the events into inspectable artifacts — summaries, reports, datasets, maps
- **Interventions**: receiver-controlled points where the incoming knowledge can be filtered, adapted, redacted, or enriched before integration

The critical difference from skills or documents: **a seed carries the work, not just the conclusion**. Skills are assertions — they ask you to trust the sender. Seeds are evidence — the receiver can replay the reasoning chain and verify it themselves.

## The Trust Model

Trust in this protocol is architectural, not social.

**The sender** controls what leaves their system:
- Export policies select which events to include
- PII review catches personal information before publication
- Publication branches curate the narrative without exposing the full private history
- Publication receipts record exactly what was shared and what was withheld

**The receiver** controls what enters their system:
- Planting policies filter incoming events by type, content, or source
- Redaction strips sensitive fields before integration
- Remapping translates foreign concepts into local ontology
- Enrichment adds local context to imported knowledge
- Replay receipts record exactly what was accepted, rejected, and transformed

**Neither side has to trust the other.** The sender doesn't trust the receiver to use their knowledge responsibly — they only share what they've explicitly reviewed. The receiver doesn't trust the sender to be honest — they can inspect every step of the reasoning chain and reject what doesn't hold up.

This is what makes it safe enough for a governing body to accept knowledge from strangers.

## Progressive Depth

Not every AI system has an event-sourced architecture. Not every contribution needs a full reasoning chain. The protocol must meet systems where they are.

**Tier 1 — Artifact only**
Just the conclusion. A report, a dataset, a recommendation. No chain of reasoning. This is what people share today. Lowest auditability, but zero adoption friction.

**Tier 2 — Annotated artifact**
The conclusion plus a structured provenance trail. "Here's what I concluded, here are the inputs I considered, here's what I rejected and why." Most AI systems could produce this with a lightweight wrapper.

**Tier 3 — Replayable chain**
Full event history. The complete audit trail. Maximum auditability, maximum value. Requires an event-aware system, but the protocol doesn't require the sender to use any specific architecture — only to produce the event stream in the standard format.

The governing body can require tier 3 for high-stakes environmental claims and accept tier 2 for general public comment. The protocol accommodates both without splitting into two different systems.

## The MCP Analogy

MCP answered: "How does a model use tools safely and consistently?"

It didn't ask every AI system to redesign their architecture. It proposed a simple protocol, and everyone adopted it because it was useful and low-friction.

The Knowledge Seed Protocol answers a different question:

**"How does one sovereign system share replayable knowledge with another without collapsing provenance, ownership, or local adaptation?"**

MCP sits on the tool layer. This protocol sits on the knowledge layer.

MCP made tools interoperable. This protocol makes local knowledge interoperable.

## The Adversarial Case

This protocol isn't just about convenience. It's about resistance.

Captured systems — whether in government, pharma, energy, or finance — rely on opacity. Misaligned incentives survive because the reasoning behind decisions is hidden, the evidence is inaccessible, and the public can't verify what they're told. Power structures are remarkably good at absorbing challengers: outsiders who promise to "drain the swamp" get repurposed, their disruption redirected into familiar patterns of extraction. Chaos becomes a ladder for those already positioned to climb it.

Knowledge seeds make this absorption structurally harder.

When every contribution carries a verifiable reasoning chain, you can't quietly reframe someone's evidence to support a predetermined conclusion. When provenance survives adaptation, you can trace who changed what and why. When the receiver controls planting policy, no central authority can silently filter inconvenient inputs. The cost of manipulation goes up because fabricating a convincing reasoning chain is harder than fabricating a conclusion — and cross-referencing multiple seeds on the same topic exposes inconsistencies that single assertions never would.

This isn't a guarantee against capture. But it shifts the economics: opacity becomes expensive to maintain, and verification becomes cheap to perform.

## Scaling Democracy with Compute

The obvious objection: "A governing body can't replay thousands of reasoning chains."

Humans can't. Compute can.

Today, public participation means letters, meetings, and comment forms. A planning board might receive hundreds of written submissions on a zoning decision. Most get filed. A few get skimmed. Expertise is lost because human attention doesn't scale.

Knowledge seeds reframe this as a compute problem. An AI system can replay, cross-reference, and synthesise thousands of seeds — verifying reasoning chains, identifying convergent evidence from independent sources, flagging contradictions, and surfacing the inputs that matter most. The marine biologist's three years of coastal observation, the boat rental owner's revenue trends, the retired urban planner's professional experience — all replayed, verified, and weighted by evidence quality rather than who showed up to the meeting or who wrote the most persuasive letter.

Yes, this is expensive. Replaying and cross-referencing hundreds of tier-3 seeds costs real GPU hours. But consider the alternative costs:

- A zoning decision made without the biologist's data leads to an environmental lawsuit and a failed project after millions in construction
- A pharma regulation shaped without ground-level health data perpetuates misaligned incentives for another decade
- An energy policy designed without local impact data creates dependencies that adversaries exploit

Verification should cost more than assertion. That's a feature, not a bug. The current system is cheap because no one checks anything. Seeds make the checking possible, and compute makes it scalable.

The cost of compute is falling. The cost of bad decisions made on insufficient evidence is not.

## Why This Matters Now

The window for getting this right is narrow.

AI-assisted decision-making is accelerating. The patterns being established now — centralised model providers, opaque knowledge bases, platform-mediated sharing — will calcify. If the default becomes "upload your knowledge to the platform and trust us to use it well," the opportunity for sovereign, auditable, decentralised knowledge exchange closes.

**Power stays distributed.** The person who walks the beach owns their observations. The protocol lets them share selectively, revoke access, and always know exactly what they've exposed. No platform accumulates their knowledge. No model absorbs it into opaque weights.

## Core Principles

1. **The sender controls what leaves.** Publication is a deliberate curation, not a raw export.
2. **The receiver controls what enters.** Planting is an active process with inspection, filtering, and adaptation.
3. **Provenance survives adaptation.** After replay, remapping, and enrichment, you can still trace every element to its source.
4. **Inspection comes before trust.** Seeds are designed to be examined before they are integrated.
5. **Adaptation is a feature, not corruption.** Different receivers have different values, ontologies, and needs. The protocol treats local interpretation as legitimate.
6. **The protocol is the product.** No platform is required. No vendor is privileged. Any system that speaks the protocol can participate.

## The Path Forward

1. Define the minimal seed format — events, lineage, manifest — inspectable with standard tools.
2. Build reference implementations that prove the protocol works across different AI architectures.
3. Demonstrate progressive depth — show that tier 1 and tier 3 seeds coexist in the same ecosystem.
4. Publish as an open RFC once the invariants are tested by real use, not theory.

The standard should emerge from working implementations, not from committee-first abstraction.

## What Post-AI Civilisation Looks Like

The marine biologist doesn't need to attend every meeting or master lobbying. She walks the beach, does her work, and her agent preserves what she learns. When a decision comes up that her experience is relevant to, she donates a seed. The protocol handles the rest — verifiable evidence, reviewed for privacy, replayed by the governing body's system alongside hundreds of other contributions, each weighted by the quality of its reasoning chain rather than the loudness of its advocate.

Normal people doing the right thing, at scale, verified by compute.

That's the future this protocol is for.

## In One Sentence

The Knowledge Seed Protocol is an open standard for sharing verifiable, replayable evidence between AI systems — enabling collective intelligence without centralised trust.

Skills are assertions. Knowledge seeds are evidence. You can't verify a conclusion without seeing the work that produced it — and you shouldn't have to.

## Contributing

This is a proposal, not a finished standard. If this resonates — especially if you're building personal agents, long-lived AI systems, or tools for collective decision-making — open an issue or start a discussion. The protocol should emerge from working implementations, not theory.

## License

[Apache 2.0](LICENSE)
