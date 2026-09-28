# ADR-0001: Keep Argus SRE independent and integrate through evidence contracts

- Status: Accepted
- Date: 2026-09-28
- Milestone: M01 - Trusted product foundation
- Deciders: Repository owner
- Supersedes: None
- Superseded by: None

## TL;DR

- Keep Argus SRE in its own repository, deployment, state, credentials,
  authorization, and release lifecycle.
- Give it authority over incident investigation, supervised remediation, and
  verification—not test selection or performance analysis.
- Integrate with Argus and Perfeng through public, versioned, immutable evidence
  contracts; never private packages, tables, or workspace paths.
- Deliver read-only recommendation first. Add execution only behind exact human
  approval, a restricted executor, and independent verification.
- Reuse vocabulary, fixtures, and proven patterns before extracting shared code
  or services.

## Context

Three related products address different moments in the software reliability
lifecycle. Argus understands changes and decides which tests should run or be
maintained. Perfeng executes and evaluates performance evidence. Argus SRE will
investigate production incidents and propose or, under later supervision,
execute and verify remediation.

They need overlapping identities, evidence provenance, artifact references,
attempt semantics, and evaluation practices. Source proximity and similar
mechanisms do not establish identical domain meaning. Combining the products or
importing private implementations would couple authority, credentials,
persistence, releases, and failure modes. Building a universal reliability
platform before one incident path exists would create an abstraction without a
validated consumer boundary.

Production investigation adds a stronger trust distinction than the existing
products: evidence access, action proposal, human approval, mutation authority,
and recovery verification must not collapse into one model-controlled context.
The repository therefore needs an explicit product and security boundary before
runtime technology or schemas are selected.

## Decision

### Product and repository authority

Argus SRE is an independently versioned product in one initial repository. It
owns incident identity and lifecycle, investigation policy and evidence,
proposals, approval correlation, execution observations, verification outcomes,
and replay evaluation.

Argus continues to own change impact, test selection, test execution decisions,
and test adaptation. Perfeng continues to own performance workloads,
measurement quality, SLO evaluation, regression analysis, baselines, and raw
performance-evidence meaning.

Each product owns its database schema, credentials, authorization, deployment,
release, operations, and rollback. No product may read or write another's
private tables, import private packages, require sibling filesystem layout, or
assume an atomic cross-repository commit.

### Initial autonomy and security boundary

The first product slice is read-only investigation and recommendation for one
bounded incident class. It may obtain evidence through least-privilege adapters
and publish a typed action proposal. It does not execute the action.

Later supervised execution requires:

- server-owned action policy;
- authenticated human approval bound to an exact immutable proposal, target,
  parameters, preconditions, expiry, and executor audience;
- a restricted executor with credentials unavailable to the investigator;
- idempotent, auditable execution with bounded retries and cancellation;
- an independent verifier with explicit recovery and guardrail conditions; and
- a failed or inconclusive outcome when command success does not prove recovery.

A model cannot grant capability, authorize itself, widen an approved action,
receive ambient production credentials, or declare remediation successful.

### Cross-product integration

Integration uses published, versioned, language-neutral messages or immutable
artifacts. The product that owns a meaning publishes its contract and
compatibility fixtures first. Consumers pin an exact release or
content-addressed revision and validate the same positive and negative cases.

The planned sequence is:

1. establish incident, investigation, evidence-reference, and action-proposal
   semantics without depending on either sibling product;
2. deliver and evaluate a read-only investigation using observability,
   deployment, Kubernetes, and source evidence;
3. consume stable Argus change, capability, selection, and outcome evidence;
4. consume stable Perfeng quality, SLO, regression, baseline, environment, and
   artifact evidence;
5. demonstrate one correlated investigation across deployment, change, test,
   and performance evidence; and
6. only then evaluate whether any product-neutral contract, library, or service
   should be extracted.

Incident outcomes are feedback evidence. They do not automatically change
Argus selection policy, approve an adaptation, change a Perfeng baseline, or
reclassify measurement quality.

### Reuse and extraction gate

The preferred reuse order is:

1. vocabulary and documented semantics;
2. schemas, examples, and conformance fixtures;
3. a narrow library with product-neutral behavior; and
4. a shared service only when independent operation and ownership justify it.

Extraction requires at least two current production consumers with identical
meaning, validation, failure, cancellation, security, compatibility, and
support needs. It also requires an owner, release policy, migration path,
rollback, and conformance tests independent of any one product.

Proven patterns such as immutable evidence references, checksum verification,
lease fencing, idempotent attempts, secret-safe errors, and Effect-authored
portable contracts may be adopted without copying private code. Similarity in
language or mechanism alone is not an extraction case.

### Deployment relationship

Argus SRE may run on a qualified project-neutral Kubernetes substrate. It owns
its product environment composition and cannot make an environment repository
owned by Argus or Perfeng responsible for its application identities, secrets,
state, release selection, or rollback.

The initial architecture is a capability-oriented modular monolith. Separate
processes are introduced only for demonstrated security, runtime, scaling,
failure-isolation, distribution, or ownership boundaries. The executor is the
first expected security-driven split, but this ADR does not create it.

## Alternatives considered

### Add incident response to Argus

- Benefits: direct access to change and test evidence and one control-plane
  implementation.
- Costs and risks: combines pre-deployment test intelligence with production
  credentials, incident lifecycle, remediation authority, and availability.
- Reason not selected: the products own different decisions and trust
  boundaries; public evidence integration preserves the useful relationship.

### Add incident response to Perfeng

- Benefits: access to performance evidence, orchestration, artifact storage,
  and Kubernetes experience.
- Costs and risks: makes a performance-analysis platform responsible for broad
  production diagnosis and mutation while coupling unrelated policies and
  release cadences.
- Reason not selected: Perfeng remains a specialist evidence authority that an
  incident investigator can consume.

### Create a shared reliability platform first

- Benefits: common contracts, model routing, tools, work coordination, storage,
  and deployment from the beginning.
- Costs and risks: speculative APIs, unclear ownership, synchronized releases,
  broad credentials, and lowest-common-denominator domain models.
- Reason not selected: the extraction gate allows a shared component after
  concrete consumers prove identical semantics.

### Begin with autonomous remediation

- Benefits: earlier reduction in manual recovery time and a compelling
  demonstration.
- Costs and risks: weak evidence, prompt injection, target confusion, approval
  replay, over-broad credentials, and false recovery can directly harm
  production.
- Reason not selected: recommendation and replay evaluation establish an oracle
  and safety evidence before any write authority exists.

## Consequences

### Positive

- Authority, state, credentials, releases, and operations remain explainable.
- The initial slice can deliver investigation value without production mutation.
- Argus and Perfeng can evolve independently behind explicit compatibility
  contracts.
- A third consumer provides real evidence for later product-neutral extraction.
- Security review can reason separately about reading, approving, executing,
  and verifying.

### Negative

- Cross-product capability requires coordinated releases and conformance tests.
- Some small provenance, validation, or orchestration mechanisms may initially
  be implemented more than once.
- End-to-end local development needs pinned releases rather than importing
  sibling source.
- Supervised execution requires additional identity, authorization, audit, and
  operational machinery before it can ship.

### Neutral or follow-up

- Runtime language, persistence, model provider, contract authoring tool,
  observability vendors, queue, and deployment packaging need later ADRs when a
  delivery slice requires them.
- Multi-agent execution is neither required nor prohibited. A separate agent or
  process needs a measured context, authority, or failure-isolation reason.
- Shared model routing, tool SDKs, evidence envelopes, and replay formats remain
  candidates, not approved shared components.

## Compatibility and migration

There is no runtime migration because this is the initial product boundary.
Each cross-product integration is producer-first: publish and test a compatible
contract, migrate the consumer, then update deployment selection. Breaking
changes add a version or use an explicit expand, migrate, and contract plan.

A future shared extraction keeps existing product-owned contracts available
until consumers migrate and retains a rollback path. Repository history may be
preserved, but history does not create a runtime source dependency.

## Security and operations

Evidence adapters deny by default, use separate tenant-scoped credentials, and
bound time, size, cardinality, concurrency, and egress. Retrieved content is
untrusted and cannot redefine tools or policy. Sensitive evidence is redacted
before model use and governed by explicit retention and deletion policy.

Execution remains unavailable until action authorization, isolated credentials,
replay protection, audit, rollback, and independent verification pass their
roadmap gates. Every product remains independently deployable and recoverable.

## Validation

This decision is validated when:

- the repository can be understood and checked without sibling repositories;
- the first investigation produces a replayable report using only read-only
  adapters;
- no model path can acquire action credentials or self-approve;
- Argus and Perfeng integrations use pinned public contracts and conformance
  fixtures rather than private implementation;
- one three-product investigation correlates immutable deployment, change,
  test, and performance evidence; and
- any proposed shared extraction demonstrates every gate in this ADR.
