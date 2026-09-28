# Engineering standards

## TL;DR

- Build capability-oriented hexagonal boundaries and keep domain policy free of
  frameworks, transports, persistence, vendors, and model providers.
- Treat all external and model-produced data as untrusted; convert it into typed
  proposals and validate independently.
- Prefer explicit identities, states, units, ownership, failure classes, and
  bounded behavior over generic frameworks.
- Separate investigator, approver, executor, and verifier authority in code,
  credentials, and tests.
- Apply language-specific best practices after the runtime ADR selects a
  language; do not add a toolchain speculatively.

## Architecture and ownership

Organize code around capabilities such as intake, evidence, investigation,
action policy, approval, execution, verification, and evaluation. Each
application capability owns the ports it consumes. Driving adapters translate
untrusted requests into application commands; outbound adapters implement
application-owned ports.

Domain code MUST NOT import HTTP, SQL, Kubernetes, observability, SCM, model,
queue, or sibling-product types. Transport DTOs, database records, events,
model output, and domain values remain distinct where their invariants or
lifecycles differ. A module owns its writes; other modules use a public use case
or versioned fact, never its tables.

Use SOLID as reasoning, not ceremony. Prefer cohesive packages, composition,
small consumer-owned interfaces, validated value objects, explicit state
machines, and ordinary functions. Avoid generic repositories, service locators,
ambient global state, boolean state machines, and speculative extension points.

## Identity, time, and evidence

Model identifiers, revisions, hashes, confidence, risk, durations, timestamps,
byte sizes, and units explicitly. Distinguish alert event time, telemetry
observation time, ingestion time, decision time, approval time, execution time,
and verification time.

Every decision that must be explained pins source, contract, policy, prompt,
model, tool, adapter, environment, deployment, and evidence revisions as
applicable. Evidence references include integrity, producer, scope, tenant,
redaction, retention, and availability semantics. Missing is never zero.

Inject clocks, identifier generators, randomness, and external clients where
policy or deterministic testing depends on them. Prefer immutable values and
closed outcomes over combinations of flags.

## Errors, bounds, and asynchronous work

Distinguish invalid input, unauthorized, forbidden, absent, conflict, stale,
unsupported, unavailable, timeout, cancellation, rate or budget exhaustion,
unsafe proposal, inconclusive verification, and internal defect. Public errors
must not expose credentials, provider internals, prompts, or sensitive evidence.

Bound input, output, time range, cardinality, bytes, concurrency, retries,
execution time, model context, tool calls, and cost. Remote calls stay outside
database transactions. Idempotency compares stable identity and immutable
content, not a key alone.

Use structured concurrency. Child work belongs to an investigation, action, or
service lifecycle and is cancelled with it. Background work defines claim,
lease, fencing, retry classification, terminal failure, recovery, and operator
visibility before it is deployed.

## Model and tool boundaries

Prompts, model output, retrieved text, alerts, logs, traces, repository content,
incident notes, and tool descriptions are untrusted. Runtime schema validation
is necessary but does not establish factual correctness, authorization, or
safety.

A model can request a server-owned tool and return a typed proposal. It cannot:

- define or expand its available tools;
- supply credentials or authorization through output;
- bypass target, tenant, time, or result bounds;
- approve its own proposal;
- convert confidence into permission;
- invoke a write tool through a read-only investigation session; or
- decide that its own action resolved the incident.

Tool adapters use deny-by-default allowlists, least privilege, explicit egress,
timeouts, cancellation, redaction, safe error classes, and audit evidence.
Shell-like search may operate only inside a bounded read-only evidence workspace,
never as ambient host or production shell access.

## Security and privacy

Authentication establishes identity; authorization is enforced at the use case
and protected resource. Credentials are isolated by source, tenant,
environment, and authority. Investigators cannot acquire executor credentials.

Classify telemetry and artifacts before storage or model use. Minimize and
redact sensitive fields, encrypt in transit and at rest, constrain regions and
providers where required, and define retention and deletion. Never commit
customer evidence or use it in tests without approved anonymization.

Approval is immutable, audience-bound, short-lived, replay-protected, and tied
to exact action bytes and current-state preconditions. Executor and verifier
audit records are append-only evidence.

## Contracts and compatibility

Published HTTP schemas, events, artifacts, tool schemas, model outputs,
configuration, persisted payloads, prompts used by replay, and CLI behavior are
compatibility boundaries. Version semantics rather than filenames. Breaking
changes require a new version or an explicit expand, migrate, and contract plan.

Commands request intent. Events report completed facts in past tense. Generated
artifacts are deterministic and checked for drift. Add language bindings only
for real producers or consumers and keep wire types out of domain policy.

## Testing and evaluation

Test at the lowest convincing boundary: pure domain behavior, application use
cases with fakes, adapter integration against real protocols, contract fixtures,
and a small number of end-to-end paths. Tests cover success and important
rejection, duplicate, stale, authorization, timeout, retry, cancellation,
partial-failure, restart, rollback, and recovery behavior.

Do not use sleeps for coordination. Use controlled clocks, barriers, channels,
events, and observable state. Use a real disposable database or protocol when a
mock cannot reproduce constraints, transactions, locking, or encoding.

Incident evaluation uses temporal holdouts. Deterministic scorers own citation,
chronology, policy, identity, and action-safety gates. Versioned semantic judges
may assess explanation quality but cannot override deterministic safety.
Regression fixes begin with a failing test or replay case.

## Language guidance

The runtime and contract languages remain deferred until their ADRs. Once a
language enters the repository, its compiler, formatter, linter, type checker,
tests, dependency resolution, vulnerability checks, and relevant race or fuzz
checks MUST be pinned and included in `make validate`.

### Go

- Follow standard Go naming, package, context, error wrapping, resource closing,
  documentation, and concurrency guidance.
- Define interfaces near consumers; accept interfaces and return concrete types.
- Use `context.Context` first for request-scoped cancellation and never store it.
- Use `errors.Is` or `errors.As` compatible classifications for public errors.
- Keep goroutine ownership visible and run ordinary, race, static, vulnerability,
  and parser fuzz checks where applicable.

### Python

- Use a locked project configuration, formatter, linter, and strict type checker.
- Normalize untyped libraries at adapters and isolate any unavoidable `Any`.
- Keep imports side-effect-free and load configuration at composition boundaries.
- Use async only for real asynchronous I/O with owned tasks and cancellation.
- Prefer frozen values, precise exceptions, context managers, `pathlib`, and
  standard-library facilities before dependencies.

### TypeScript

- Enable strict mode and consider unchecked-index, exact-optional, and unknown-
  catch protections according to runtime compatibility.
- Treat external values as `unknown` and decode them at adapters.
- Prefer readonly values, discriminated unions, exhaustive switches, owned
  promises, `AbortSignal`, and explicit timeouts.
- Avoid `any`, floating promises, accidental ESM/CommonJS mixing, and broad
  barrel exports.

## Documentation and operations

Public APIs document purpose, invariants, units, ownership, side effects,
concurrency, security, and actionable failures. Comments explain decisions and
constraints rather than syntax. Operational behavior includes healthy signals,
failure classes, recovery, rollout, and rollback in the same change.
