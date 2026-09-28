# SQL migration criteria

## TL;DR

- These rules activate only after an ADR selects a relational database; this
  document does not select one or create placeholder migrations.
- Migrations are immutable, forward-only, transactional where supported, and
  run by separately authorized deployment tooling rather than service startup.
- Every chain is tested from empty state and supported upgrade states, including
  drift, failure atomicity, and concurrent migrators.
- Runtime roles do not own schema objects or receive migration privileges.
- Destructive changes follow expand, migrate, verify, and contract with an
  explicit recovery plan.

## Scope and authority

Database tables are private implementation. Public compatibility belongs to
versioned APIs, events, and artifacts. A module owns its tables; another module
MUST NOT write them directly.

The persistence ADR will select the database, runner, numbering, and supported
upgrade window. Until then, contributors MUST NOT add empty migrations or
invent schema solely to satisfy this policy.

## Numbering and immutability

Use a monotonic sequence after the runner is selected. Allocate the next number
from fresh directory state immediately before creation. Resolve a concurrent
collision by refreshing and renumbering the later migration, never by combining
unrelated SQL.

A merged or applied migration is immutable. Correct it with a new migration.
Never reorder, reuse, or silently edit history. A ledger records exact identity
and checksum and rejects unknown, missing, reordered, or changed history.

## Execution boundary

Migrations run through an explicit administrative command or deployment job.
Ordinary startup verifies compatibility but does not acquire DDL privileges or
modify schema. Migrator and runtime credentials are separate and least
privileged.

The runner:

- acquires a database-scoped lock preventing concurrent chains;
- applies pending migrations in deterministic order;
- records identity, checksum, and completion atomically;
- emits secret-safe structured status; and
- fails without starting the runtime when compatibility is unsafe.

## Transaction and failure rules

Each migration is transactional when the selected database supports every
statement. A non-transactional operation requires an ADR or reviewed exception
with partial-state detection, restart behavior, and recovery instructions.

Broad `IF NOT EXISTS` clauses MUST NOT hide a wrong object shape, ownership, or
partial application. Migrations verify prerequisites and postconditions.
External calls, artifact reads, and model operations do not occur in database
transactions. Large backfills are bounded, observable, and restart-safe.

## Expand, migrate, verify, contract

Rolling or independently versioned deployments use four phases:

1. **Expand** with additive objects compatible with old and new code.
2. **Migrate** data through a bounded, restart-safe owner.
3. **Verify** completeness, consistency, and rollback assumptions.
4. **Contract** only after no supported reader or writer requires the old shape.

Dropping or rewriting incident, evidence, approval, execution, verification,
tenant, or audit data requires an explicit classification, retention decision,
backup, reconciliation query, authorization, and recovery plan. A destructive
down migration is not a rollback strategy.

## Data and security criteria

Schema changes preserve tenant isolation, immutable identity, provenance,
chronology, and append-only audit meaning. Constraints enforce invariants that
must survive every application path. Sensitive evidence has explicit
encryption, access, retention, and deletion policy.

Runtime roles receive only required DML privileges. Read-only investigation,
approval, execution, verification, and administration use distinct roles where
their authority differs. Migrations set ownership and grants explicitly rather
than relying on a developer's default role or search path.

## Required verification

Every migration change proves:

- a fresh database reaches the expected schema;
- each supported previous schema upgrades to the same result;
- an already-current database is a no-op;
- unknown, missing, reordered, or checksum-drifted history is rejected;
- concurrent migrators cannot both apply one step;
- injected failure leaves no unrecorded partial transactional state;
- runtime credentials cannot perform DDL;
- persistence behavior survives process restart; and
- reconciliation verifies transformed data before contraction.

Use an isolated disposable instance matching the supported production major
version. If one is unavailable, report the check as not run and state residual
risk; do not substitute a different embedded database and call it equivalent.
