# ADR-0004: Revise published investigations with late evidence

- Status: Accepted
- Date: 2026-11-23
- Milestone: M02 - Incident and evidence contracts
- Deciders: Workspace owner
- Supersedes: None
- Superseded by: None

## Context

Material late evidence can change a hypothesis or invalidate a finding after an investigation has been published or acted on. Readers and reviewers still need the original record and its evidence cut.

## Decision

For the same incident and investigation scope, publish a new immutable investigation revision when material late evidence changes the assessment. Link its predecessor and identify the new evidence and its effect. Preserve original findings, evidence references, proposal identities, and published outcomes in the earlier revision.

When the investigation's purpose or scope changes, open a separately identified follow-up linked to the incident and its predecessor. An amended proposal requires approval bound to that exact proposal and its current preconditions.

## Alternatives and consequences

In-place updates would disconnect prior reviews and approvals from what they assessed. A new follow-up for every update would fragment the same investigation. Immutable revisions preserve one coherent lineage and require clear revision-aware queries and replay.

## Compatibility and verification

This decision selects a history model for the future contracts. It introduces no storage implementation. Verify that late evidence changes only the new revision, a scope change creates a distinct follow-up, and prior approvals confer no authority to execute amended proposals.
