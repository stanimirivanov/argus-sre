# ADR-0003: Preserve performance evidence authority

- Status: Accepted
- Date: 2026-11-23
- Milestone: M06 - Performance evidence integration
- Deciders: Workspace owner
- Supersedes: None
- Superseded by: None

## Context

An Argus-issued performance request has Argus-owned request context and Perfeng-owned execution and analysis evidence. Investigators sometimes need both the correlation and the original report or diagnostic artifacts.

## Decision

For an Argus-issued request, use the authorized Argus Performance Decision Projection to bind the exact request and its public Run. Preserve Perfeng's measurement-quality, SLO, and regression outcomes verbatim as separate observations. When the investigation needs original evidence, request it from Perfeng using independently granted scoped read authority and the exact retained identifiers. Argus SRE owns the incident inference and evidence citation.

A missing or unavailable projection leaves Argus request correlation unestablished. A permitted Perfeng read can still supply Perfeng evidence with its own provenance. Conflict, lack of evidence, and inconclusive outcomes remain visible.

## Alternatives and consequences

Using only direct reads loses the historical Argus request binding. Using only the projection limits the evidence available for investigation. Combining the two by authority provides traceable conclusions and requires separate permission and integrity checks at each boundary.

## Compatibility and verification

The projection's published format carries no grant to fetch other data. This record ships no new adapter or access path. Verify cross-request and cross-Run refusal, distinct unavailable and inconclusive outcomes, and that projection access never substitutes for authority to read originals.
