# Argus SRE

## TL;DR

- Argus SRE is an evidence-first incident investigation and supervised
  remediation product.
- Its first delivery path is read-only: correlate one Kubernetes alert with
  bounded telemetry and deployment evidence, then publish a reviewable
  investigation and action proposal.
- A model may propose an action but cannot authorize, execute, or verify its
  own proposal.
- Argus SRE remains independently deployable from Argus and Perfeng and
  integrates with them through versioned, language-neutral evidence contracts.
- The repository currently contains the product, architecture, governance, and
  implementation roadmap foundation. It has no production runtime yet.
- Start from the [documentation map](docs/README.md), run `make bootstrap` for
  a new checkout, `make verify` during development, and `make validate` before
  handoff.

Argus SRE helps an on-call engineer move from an alert to a defensible next
action. It gathers bounded evidence, records competing hypotheses, cites the
evidence behind its conclusions, proposes a precisely scoped action, and later
verifies approved execution against explicit recovery criteria.

The product complements, but does not absorb, the other reliability products:

- **Argus** owns change understanding, impacted-test selection, and
  evidence-backed test maintenance.
- **Perfeng** owns performance workload execution, measurement quality,
  baselines, regression analysis, and performance evidence.
- **Argus SRE** owns production-incident investigation, supervised remediation,
  and post-action verification.

## Start here

- [Documentation map](docs/README.md)
- [Product definition](docs/product/product-definition.md)
- [Architecture overview](docs/architecture/overview.md)
- [Product-boundary decision](docs/decisions/0001-keep-argus-sre-independent-and-integrate-through-evidence-contracts.md)
- [Implementation milestones](docs/roadmap/milestones.md)
- [Contributor workflow](CONTRIBUTING.md)
- [Engineering standards](docs/development/engineering-standards.md)
- [Security policy](SECURITY.md)

## Validate the foundation

Python 3.12 and GNU Make are the only scaffold-time requirements. The validator
uses only the Python standard library and does not access the network.

```sh
make bootstrap
make verify
make validate
```

`make verify` and the current `make validate` aggregate verify repository policy
files, Markdown hygiene, internal links and anchors, ADR/index coherence,
milestone naming, templates, and the validator's own tests. Runtime language,
contract tooling, persistence, and deployment dependencies enter the repository
only with the milestone that exercises them.

## Current status

M01 establishes an independently reviewable product boundary and contributor
harness. The first runtime implementation is deliberately deferred until its
incident and evidence contracts are defined in M02.
