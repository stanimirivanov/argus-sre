# Argus SRE coding harness

## TL;DR

- The harness combines task-routed guidance with deterministic feedback; no
  single document, formatter, or test is sufficient by itself.
- Use the [documentation map](../README.md), then run `make verify` as the fast,
  offline inner loop and `make validate` before handoff.
- The current foundation has no third-party runtime dependencies. Runtime,
  contract, architecture, and supply-chain sensors enter only with the ADR and
  delivery slice that need them.
- Repeated review findings should become clearer canonical guidance, an early
  deterministic sensor, or an explicit documented exception.

## Purpose

The coding harness makes the repository understandable and self-checking for
human contributors and coding agents. Feed-forward guides explain intent,
authority, and constraints before editing. Feedback sensors detect mechanical
policy drift after each change. The root Makefile remains the executable command
surface on every supported platform.

## Feedback tiers

| Tier | Timing | Current behavior |
|:--|:--|:--|
| T0 — route | Before editing | Use the documentation map to load only relevant canonical sources. |
| T1 — inner loop | During editing | Run focused tests and `make verify`; the current foundation is offline and standard-library only. |
| T2 — acceptance | Before handoff | Run `make fmt`, review its diff, then run `make validate`. |
| T3 — specialized | When a future boundary requires it | Add service, migration, replay, security, or deployment checks with the feature that makes them real. |

The constrained-environment protocol in
[CONTRIBUTING.md](../../CONTRIBUTING.md#verification-and-constrained-environments)
always applies. A missing future sensor is not permission to claim that property
was verified.

## Feed-forward guides

| Source | Owns |
|:--|:--|
| [AGENTS.md](../../AGENTS.md) | Concise tool-facing entry point |
| [CONTRIBUTING.md](../../CONTRIBUTING.md) | Workflow, ambiguity, issue timing, verification, and completion policy |
| [Documentation map](../README.md) | Task-to-source routing |
| [Product definition](../product/product-definition.md) | Product outcomes and safety |
| [Architecture overview](../architecture/overview.md) | Capability, evidence, trust, and authority boundaries |
| [Engineering standards](engineering-standards.md) | Design, language, testing, and operational practices |
| [Developer quickstart](developer-quickstart.md) | Supported setup and troubleshooting |
| [Dependency policy](dependency-policy.md) | Admission, pinning, licensing, and vulnerability handling |
| [ADR index](../decisions/README.md) | Durable decisions and lifecycle |
| [Roadmap](../roadmap/milestones.md) | Delivery sequence and promotion evidence |

## Current command surface

| Command | What it proves or changes |
|:--|:--|
| `make bootstrap` | Confirms the scaffold toolchain; there are currently no external packages to install. |
| `make doctor` | Reports Git, Python, and GNU Make versions without exposing the environment. |
| `make fmt` | Normalizes supported repository text; inspect the resulting diff. |
| `make docs-check` | Checks canonical text, required files, local Markdown links and anchors, TL;DR policy, ADR/index coherence, milestones, GitHub templates, and semantic-major Action references. |
| `make check` | Runs every current static repository check. |
| `make test` | Runs the documentation validator's unit tests. |
| `make verify` | Runs the complete fast, offline, non-mutating inner loop. |
| `make validate` | Runs the complete current acceptance aggregate. |

`verify` and `validate` are intentionally equal while the repository contains
only its foundation. A selected runtime MUST extend `bootstrap`, `verify`, and
`validate` in the same pull request. Add architecture, dependency, license,
vulnerability, race, integration, migration, replay, and deployment sensors only
when their corresponding code or dependency graph exists. Do not add a green
placeholder that implies an unimplemented property was checked.

## Steering loop

When a review finding or escaped defect repeats:

1. Clarify the narrow canonical guide when intent is unclear.
2. Add the cheapest deterministic sensor when the rule is mechanical.
3. Add a focused test or replay when observable behavior regressed.
4. Record an owned, reviewable exception when automation would be misleading.

Diagnostics should identify the affected location, violated rule, likely
correction, and canonical source. Sensors MUST NOT silently rewrite policy,
weaken safety, require ambient global packages, or report unavailable checks as
passed.

## Multi-PR execution plans

When one approved outcome needs multiple dependent pull requests, add a short
versioned plan under `docs/development/plans/` with the first plan-bearing
change. Record the outcome, invariants, exclusions, ordered slices,
compatibility, rollout, recovery, verification, and discoveries that change the
sequence. Each slice remains independently reviewable and leaves the repository
verifiable.

Plans do not replace GitHub issues, milestones, or ADRs. Do not create an empty
plans directory before a real multi-PR outcome needs one.
