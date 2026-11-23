# Architecture decision records

## TL;DR

- ADRs record durable choices about compatibility, authority, security, data,
  technology, topology, ownership, or cross-product behavior.
- Allocate the next number from fresh repository state and never reuse a
  published number.
- Resolve concurrent numbering collisions by refreshing and renumbering, not by
  forcing content together.
- Supersede accepted decisions instead of rewriting history.

## Rules

Use a four-digit sequence and kebab-case name. Before creating an ADR, inspect
this index and the decision directory from current branch state. A collision at
review time is a rebase-and-renumber operation.

Statuses are Proposed, Accepted, Rejected, Deprecated, or Superseded. An ADR
includes context, decision, alternatives, consequences, compatibility and
migration, security and operations, and validation.

## Index

| ADR | Decision | Status | Date |
|:--|:--|:--|:--|
| [ADR-0001](0001-keep-argus-sre-independent-and-integrate-through-evidence-contracts.md) | Keep Argus SRE independent and integrate through evidence contracts | Accepted | 2026-09-28 |
| [ADR-0002](0002-bind-incidents-to-authoritative-deployments.md) | Bind incidents to authoritative deployments | Accepted | 2026-11-23 |
| [ADR-0003](0003-preserve-performance-evidence-authority.md) | Preserve performance evidence authority | Accepted | 2026-11-23 |
| [ADR-0004](0004-revise-published-investigations-with-late-evidence.md) | Revise published investigations with late evidence | Accepted | 2026-11-23 |
