# Contributing to Argus SRE

## TL;DR

- Deliver one coherent, verified capability per issue and pull request.
- Proceed on documented, reversible assumptions; stop for choices that change
  behavior, safety, compatibility, scope, cost, or external state materially.
- Use a supplied issue. When none is supplied, complete the smallest coherent
  scope and print a complete proposed issue in the completion report.
- Run exact repository checks. Never claim an unavailable check passed.
- Name milestones `MNN - Outcome`, beginning with M01, and include the exact
  milestone in every issue.
- Preserve the investigator, approver, executor, and verifier trust boundaries.
- Group acceptance ingredients into substantial delivery slices rather than
  creating artifact-sized pull requests.

## Policy language and sources of truth

**MUST** and **MUST NOT** are requirements. **SHOULD** and **SHOULD NOT** are
strong defaults whose exceptions need an explicit reason. **MAY** identifies an
optional choice. Lowercase wording is explanatory guidance.

| Concern | Canonical source |
|:--|:--|
| Workflow, escalation, issue timing, verification, completion | This document |
| Concise agent entry point | [AGENTS.md](AGENTS.md) |
| Progressive task-to-document routing | [Documentation map](docs/README.md) |
| Product scope and autonomy | [Product definition](docs/product/product-definition.md) |
| Logical and trust boundaries | [Architecture overview](docs/architecture/overview.md) |
| Engineering practices | [Engineering standards](docs/development/engineering-standards.md) |
| Coding harness and feedback tiers | [Harness guide](docs/development/harness.md) |
| Database migration policy | [SQL migration criteria](docs/development/sql-migrations.md) |
| Durable decisions | [Architecture decisions](docs/decisions/README.md) |
| Delivery sequence | [Implementation milestones](docs/roadmap/milestones.md) |
| Exact commands | [README](README.md) and [Makefile](Makefile) |

An accepted ADR governs its decision until superseded. A contributor MUST
surface a conflict rather than silently selecting the convenient source.

## Before starting

A contributor MUST inspect the current branch and working tree, preserve
unrelated changes, use the [documentation map](docs/README.md) to read the
relevant sources of truth, identify one observable outcome, and review contract,
security, persistence, documentation, and operational effects.

An ADR is required for a durable choice about compatibility, persisted meaning,
security or authority, deployment topology, foundational technology, ownership,
or cross-product behavior. Cheap, local implementation choices do not require
an ADR.

## Ambiguity and escalation

A contributor MAY proceed with a documented assumption when it stays inside the
requested outcome, is reversible and inexpensive, does not affect public or
persisted meaning, security, external state, destructive behavior, or required
verification, and would not materially change what a reviewer believes they
are approving.

A contributor MUST stop and request a decision when ambiguity could materially
change:

- observable behavior, acceptance criteria, milestone, or scope;
- compatibility, evidence meaning, authorization, privacy, or security;
- an irreversible, destructive, production, or third-party action;
- cost, operational ownership, or deployment topology; or
- a choice between credible designs with meaningfully different consequences.

Before escalating, inspect code, tests, fixtures, documentation, ADRs, and safe
read-only evidence. State the exact decision, alternatives, consequences, and
what work can continue safely.

## Issue timing and milestones

Issue-first is preferred. If an issue number is supplied, follow that issue and
link the pull request. If no issue is supplied, implement the smallest coherent
scope and print the issue afterward. Creating an external issue, milestone,
pull request, or release requires explicit authorization.

Milestones use `MNN - Short outcome`, beginning with M01. Published numbers are
never reused or renumbered. Refresh external milestone state immediately before
allocating a new number; resolve a collision by selecting the next number.

Every implementation issue uses this body:

```markdown
**Milestone:** MNN - Outcome

## Goal

Describe the problem and observable result.

## Scope

- Included behavior and boundaries.

## Design decisions

- Important choices, assumptions, compatibility effects, and ADR links.

## Acceptance criteria

- [ ] Observable success and verification evidence.
- [ ] Relevant rejection or failure behavior.
- [ ] Documentation and operational effects.

## Out of scope

- Explicit exclusions and deferred work.
```

## Pull-request-sized work

A pull request MUST solve one coherent problem, leave the repository verifiable,
include the relevant implementation, tests, docs, contracts, and migrations,
and demonstrate important failure behavior. A default delivery slice is larger
than one schema, interface, adapter, or documentation fragment.

Split a planned slice only when its parts have independently useful outcomes and
materially different risk, ownership, rollout, or review needs. Do not mix
unrelated refactoring, dependency updates, generated churn, or formatting.

When one approved outcome requires multiple dependent pull requests, follow the
[execution-plan guidance](docs/development/harness.md#multi-pr-execution-plans).

## Architecture and security review

Review every change for these invariants:

- Domain and application policy do not depend on vendors, transports,
  persistence, model providers, or sibling repositories.
- Interfaces are owned by their consumers and exist for demonstrated variation.
- Transport, persisted, model-output, and domain values remain distinct where
  their invariants differ.
- Inputs and outputs are bounded; timeouts, cancellation, retries,
  idempotency, concurrency, and partial failure are explicit.
- Evidence retains immutable identity, producer, observation time, provenance,
  and integrity information.
- The read-only investigator cannot acquire write authority.
- Approval binds an exact action, target, parameters, expiry, and permitted
  executor; approval is not a reusable bearer capability.
- Execution success is not remediation success. Independent verification owns
  the recovery verdict.
- Customer data, secrets, raw prompts, and unrestricted telemetry are not
  committed or logged.

## Verification and constrained environments

Run `make bootstrap` once for a new checkout, use `make verify` as the fast
offline inner loop, and run `make fmt` plus `make validate` before handoff.
`make validate` is the aggregate foundation check. A contributor MUST run the
most complete relevant checks available and report exact commands and outcomes.

`make docs-check` verifies mechanical documentation and repository-policy
structure. Semantic accuracy remains a review responsibility. When a runtime,
dependency graph, database, or deployment boundary enters the repository, its
checks MUST join the stable `make verify` and `make validate` surface rather than
becoming hidden commands.

When a required check cannot run because of missing network, credentials,
services, platform support, or sandbox capabilities:

1. do not invent a weaker substitute and call it equivalent;
2. run unaffected checks;
3. report the check as **not run**, with the concrete reason;
4. describe residual risk and where the authoritative check runs; and
5. never report it as passed.

A failure MUST be diagnosed. Do not weaken assertions, silently skip coverage,
or lengthen timeouts merely to obtain a green result.

## Documentation

Documents of at least 80 lines MUST contain a `## TL;DR` near the beginning.
The summary states the outcome, key constraints, and reader action. It does not
replace detailed design or operational guidance.

Public contracts, configuration, migrations, security behavior, runbooks, and
troubleshooting MUST change with the behavior they describe. Do not commit
credentials, customer evidence, production telemetry, machine-specific paths,
or vendor marketing research.

## Completion report

After every completed work item, print:

1. the exact milestone in `MNN - Outcome` form;
2. a proposed imperative GitHub issue title;
3. the complete issue body using the required structure;
4. assumptions, unresolved questions, and limitations; and
5. verification commands and outcomes, distinguished as **passed**,
   **failed**, or **not run**.

The report describes the work actually performed. It does not claim that an
issue or pull request was created.
