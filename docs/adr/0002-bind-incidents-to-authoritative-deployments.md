# ADR-0002: Bind incidents to authoritative deployments

- Status: Accepted
- Date: 2026-11-23
- Milestone: M05 - Change intelligence integration
- Deciders: Workspace owner
- Supersedes: None
- Superseded by: None

## Context

One Git revision can be deployed through different artifacts, services, environments or rollouts. An incident must be attributable to the right operational context before upstream change and test evidence can be used as deployment-specific facts.

## Decision

The deployment authority attests the scoped deployment and its exact artifact and source revisions. Argus owns evidence linking those source identities to changes and capabilities. Argus SRE owns the incident-specific association and retains the producer identities and reviewed evidence on both sides.

A Git-only match remains a candidate relationship. Missing or contradictory evidence leaves the deployment association unresolved. A branch, display name, or mutable tag may help locate evidence but carries no attribution authority.

## Alternatives and consequences

A Git-SHA join offers a cheap search and can incorrectly attribute a symptom to another rollout, service, or environment. Exact bindings preserve provenance and support multi-repository deployments at the cost of explicitly reporting unresolved cases.

## Compatibility and verification

Use existing namespaced producer identities. This decision introduces no universal service identifier or deployment contract. Conformance must cover two deployments of one commit, mismatched scope or artifact, and incomplete or conflicting bindings.
