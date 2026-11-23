# Argus and Argus SRE evidence handoffs

## TL;DR

- Argus owns change and test decisions. The deployment authority owns deployment provenance, and Perfeng owns performance outcomes.
- Argus SRE owns incident correlation, interpretation, and revision history. Its connectors and runtime are planned.
- First exchange Argus change evidence as a bounded, versioned artifact. Keep request correlation and original Perfeng evidence under their respective authorities.

## Ownership and contract boundaries

| Owner | Records and meaning | Source modules or planned capabilities |
|:--|:--|:--|
| Deployment authority | Scoped deployment, exact artifact and source revisions | External deployment or provenance system |
| Argus | Verified Change Set, catalog, capability impact, selection, execution attempt, adaptation, and review evidence | `internal/change`, `internal/catalog`, `internal/selection`, `internal/execution`, `internal/adaptation`, and `internal/predictive` |
| Argus performance integration | Reviewed target and request context, public Run correlation, and the protected metadata projection for one admitted request | `internal/performance`, `cmd/performance-evidence`, and `contracts/source` |
| Perfeng | Run admission and execution, measured evidence, baseline approval, and independent quality, SLO, and regression outcomes | Published Perfeng contracts and authorized provider reads |
| Argus SRE | Incident correlation, evidence citations, findings, hypotheses, and investigation revisions. Later stages also own supervised action and independent recovery verification. | Planned incident intake, investigation, approval, execution, and verification capabilities |

Read [Argus domain language](https://github.com/stanimirivanov/argus/blob/main/GLOSSARY.md), [Argus SRE domain language](../../GLOSSARY.md), and [Perfeng shared language](https://github.com/stanimirivanov/perfeng-contracts/blob/main/GLOSSARY.md) for producer-specific terms.

## From incident to evidence

1. Resolve the exact, scoped deployment and its artifact-to-source provenance. Use Argus for source-to-change and capability evidence. Retain the incident-specific binding in the investigation. A commit match can suggest a candidate, including when several deployments share a commit. [Deployment correlation ADR](../adr/0002-bind-incidents-to-authoritative-deployments.md)
2. In the planned Argus handoff, verify one exact, versioned Change Evidence Artifact before use. Retain which tests ran, were omitted or deferred, and what compatible control evidence actually showed. An omission, a coverage gap, a missed failure, and an unavailable observation have distinct meanings. [Argus artifact handoff ADR](https://github.com/stanimirivanov/argus/blob/main/docs/adr/0100-publish-artifact-first-change-evidence.md)
3. If the incident is tied to an Argus-issued performance request, use the authorized Argus projection to correlate the request and Run. Retain Perfeng's outcomes as reported and use separately authorized Perfeng reads for original evidence. Argus already has a protected performance exporter. Neither this exporter nor the planned change artifact supplies an SRE connector by itself. [Argus exporter](https://github.com/stanimirivanov/argus/blob/main/docs/integrations/performance-evidence-export.md) · [Performance evidence ADR](../adr/0003-preserve-performance-evidence-authority.md)
4. Publish the incident interpretation with citations and explicit gaps or conflicts. Material late evidence produces a new immutable revision for the same investigation scope. A changed scope or purpose produces a separate follow-up. A reviewed incident outcome can be offered back as evidence subject to the receiving product's policy. [Revision ADR](../adr/0004-revise-published-investigations-with-late-evidence.md)

## Delivery boundaries

Define the incident and evidence contracts and qualify the first read-only path before wiring integrations. Argus must publish and test its change evidence contract before SRE consumes it. Performance integrations use the exact scoped Argus and Perfeng contracts applicable to their evidence. The [roadmap](../roadmap/milestones.md#sequencing-and-cross-project-gates) records the integration gates. Supervised execution remains a separate milestone with exact approval and independent verification.
