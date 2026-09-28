# Argus SRE product definition

## TL;DR

- Argus SRE shortens the path from a production alert to an evidence-backed,
  reviewable next action.
- The product owns incident investigation, action proposals, supervised
  remediation, and independent verification; it does not own testing or
  performance-analysis policy.
- The first supported mode is read-only recommendation for one bounded
  Kubernetes post-deployment incident class.
- Autonomous production mutation, security-incident response, unrestricted
  shell access, and self-approval are outside the initial product.
- Progression from observation to action is earned through replay evidence and
  explicit per-action authorization, never enabled globally by model confidence.

## Problem

Production incidents combine noisy alerts, fragmented telemetry, recent source
and configuration changes, incomplete service topology, and pressure to act.
On-call engineers spend valuable time collecting and correlating evidence before
they can judge a likely cause or safe next step. Conversational summaries alone
do not solve the problem when their evidence, authority, and verification are
unclear.

Argus SRE provides a durable incident decision record. It gathers only the
evidence needed for the current investigation, distinguishes observations from
inferences, retains competing explanations, proposes a constrained action, and
defines how recovery would be verified.

## Users and jobs

Primary users are on-call software engineers, site-reliability engineers, and
service owners. Platform and security engineers configure evidence access,
approved actions, tenant boundaries, and operational policy.

The product helps them:

- triage and correlate an alert without manually opening every source system;
- understand which deployment, code, configuration, dependency, or resource
  change is plausibly related;
- see evidence for and against each material hypothesis;
- obtain one precisely scoped next action with risks and preconditions;
- approve or reject that action without granting wider authority; and
- know whether the action resolved the incident or merely changed the system.

## Product authority

Argus SRE owns:

- normalized incident identity and lifecycle;
- investigation budgets, hypotheses, findings, contradictions, and abstention;
- evidence references and the incident decision transcript;
- action proposal, approval correlation, execution request, and verification;
- replay datasets and incident-response evaluation; and
- reviewed incident outcomes made available as learning evidence.

It does not own:

- source-control or deployment systems as systems of record;
- test catalog, impacted-test selection, or automated test maintenance, which
  belong to Argus;
- performance workloads, measurement quality, baselines, SLO evaluation, or
  regression analysis, which belong to Perfeng;
- observability backends or Kubernetes desired state;
- human incident command, communication, or organizational escalation; or
- security-event containment and forensic response in the initial product.

## Supported incident scope

The first vertical slice covers one post-deployment Kubernetes service
regression for which an authorized operator can provide:

- a normalized alert with service and environment identity;
- an immutable deployment revision;
- bounded metrics and log windows;
- Kubernetes workload and event evidence; and
- source-change provenance.

The system produces a read-only investigation with ranked hypotheses, cited
findings, ruled-out alternatives, missing evidence, one proposed next action,
and an explicit verification plan. It executes nothing.

Later incident classes may include dependency failure, capacity exhaustion,
configuration drift, resource-limit failure, and performance degradation. Each
class requires its own evidence requirements, evaluation corpus, action policy,
and promotion evidence.

## Decision outputs

An investigation ends in exactly one of these outcomes:

- **PROPOSE_ACTION** — evidence supports one bounded action strongly enough for
  human review.
- **REQUEST_EVIDENCE** — a named, obtainable evidence item is required before a
  responsible proposal can be made.
- **ESCALATE** — the incident is outside supported policy or requires authority
  and judgment the product does not possess.
- **ABSTAIN** — evidence is contradictory or insufficient and no bounded next
  step is justified.

Confidence is explanatory metadata, not authorization. It cannot convert an
unsupported action into a permitted one.

## Evidence and explanation

Every material finding records:

- the incident and investigation revision;
- observation or inference classification;
- immutable evidence references and producer provenance;
- event, observation, and ingestion times where applicable;
- scope, redaction, retention, and integrity metadata;
- confidence with a defined scale and calibration version; and
- contradictions, expiry, and unavailable evidence.

The report distinguishes facts from hypotheses. It MUST NOT invent missing
telemetry, treat absence as zero, or hide conflicting observations. A reviewer
must be able to reconstruct why an action was proposed without replaying a raw
model conversation.

## Autonomy model

Autonomy advances independently for every incident class, environment, action
type, and tenant:

| Level | Product behavior | Initial support |
|:--|:--|:--|
| A0 - Observe | Gather and normalize bounded evidence | Planned first |
| A1 - Recommend | Publish investigation and action proposal | Initial target |
| A2 - Supervised execute | Execute an exact, time-bound approved action | Deferred |
| A3 - Pre-authorized execute | Execute a narrowly pre-authorized action under policy | Not planned until production evidence justifies it |

There is no global autonomous mode. Promotion requires replay and shadow-mode
evidence, owner approval, explicit rollback, and operational monitoring.

## Action and verification safety

An action proposal identifies the exact operation, target, immutable deployment
or resource precondition, parameters, expected effect, blast radius, expiry,
rollback, and verification plan. Approval binds those exact values and cannot be
reused for another target or expanded by the investigator.

The executor has only the capability needed for the approved action. It reports
what was attempted and observed but does not decide whether the incident is
resolved. An independently invoked verifier evaluates declared recovery and
guardrail signals. A successful command with failed or inconclusive recovery is
not a successful remediation.

## Cross-product integration

Argus SRE consumes only published, versioned evidence:

- From Argus: immutable change identity, affected capabilities, test-selection
  decisions, inclusion and omission reasons, attempts, misses, adaptations, and
  validation outcomes.
- From Perfeng: workload and environment identity, measurement-quality verdict,
  SLO and regression outcome, baseline provenance, and immutable diagnostic
  artifact references.

Argus SRE never reads either product's private tables or imports its private
packages. It can publish reviewed incident outcomes that the owning product may
ingest as another evidence source. Neither product changes policy or baseline
automatically from that feedback.

## Success measures

Evaluation is chronological and incident-class-specific. Important measures
include:

- median and tail time to first useful finding;
- root cause represented in the top ranked hypotheses;
- evidence citation validity and temporal correctness;
- proposed-action match and unsafe-action rate;
- correct abstention and escalation rate;
- human acceptance, rejection, and edited-action outcomes;
- verification accuracy, including failed and inconclusive recovery;
- investigation tool calls, latency, and model cost; and
- recurrence and rollback outcomes after an approved action.

No single aggregate score authorizes production execution. Safety-critical
false positives and unsupported high-confidence actions are reported separately.

## Non-goals

The initial product will not:

- provide unrestricted shell, SSH, database, or cluster access to a model;
- mutate production without exact human approval;
- allow the proposing model to approve or verify its action;
- replace incident command, paging, status communication, or postmortem review;
- train a foundation model;
- build a general-purpose agent framework;
- duplicate Argus or Perfeng policy and analysis; or
- claim support for an incident class without a replay corpus and explicit
  promotion evidence.
