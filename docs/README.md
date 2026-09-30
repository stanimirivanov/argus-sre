# Argus SRE documentation map

## TL;DR

- Start with [CONTRIBUTING.md](../CONTRIBUTING.md), then read only the sources
  routed to the work you are doing.
- Product behavior belongs in the product definition, current boundaries in the
  architecture overview, and durable choices in ADRs.
- The harness guide maps repository guidance to executable feedback and explains
  how later runtime tooling must join the stable command surface.
- Update this map whenever a canonical document moves or a recurring task lacks
  a clear route.

## Route by task

| Task or changed area | Read before changing it | Verify or consult as needed |
|:--|:--|:--|
| Product scope, autonomy, incident outcomes, or safety | [Product definition](product/product-definition.md) | [Architecture overview](architecture/overview.md), relevant [ADRs](decisions/README.md) |
| Capability, authority, trust, or cross-product boundaries | [Architecture overview](architecture/overview.md), [engineering standards](development/engineering-standards.md) | [ADR index](decisions/README.md), [security policy](../SECURITY.md) |
| Repository policy, CI, tooling, or contributor experience | [Harness guide](development/harness.md), [developer quickstart](development/developer-quickstart.md) | `make docs-check`, `make verify`, `make validate` |
| Runtime or contract-toolchain selection | [Engineering standards](development/engineering-standards.md), [dependency policy](development/dependency-policy.md) | [M01 roadmap](roadmap/milestones.md#m01---trusted-product-foundation), a new ADR |
| Persistence or SQL migration design | [SQL migration criteria](development/sql-migrations.md) | Architecture and security guidance, a technology ADR before implementation |
| Dependency admission, update, licensing, or vulnerability response | [Dependency policy](development/dependency-policy.md) | [Security policy](../SECURITY.md) |
| Milestone or issue planning | [Implementation milestones](roadmap/milestones.md), [CONTRIBUTING.md](../CONTRIBUTING.md) | Relevant product, architecture, and decision sources |
| Vulnerability reporting or security-sensitive behavior | [Security policy](../SECURITY.md) | Product safety rules and relevant ADRs |

## Canonical collections

- [Product](product/product-definition.md) owns users, scope, outcomes, autonomy,
  success measures, and non-goals.
- [Architecture](architecture/overview.md) owns logical capabilities, evidence
  flow, authority, and cross-product boundaries.
- [Development](development/harness.md) owns engineering, environment,
  dependency, migration, and harness guidance.
- [Decisions](decisions/README.md) records durable choices and supersession.
- [Roadmap](roadmap/milestones.md) owns delivery order and promotion gates.
- [Security](../SECURITY.md) owns private reporting and security expectations.

## Keeping the map useful

A change MUST update this page when it adds, renames, moves, or removes a
canonical source or creates a recurring task that lacks a route. Avoid copying
normative detail into this map. `make docs-check` validates mechanical structure
and repository-local links; semantic accuracy remains a review responsibility.
