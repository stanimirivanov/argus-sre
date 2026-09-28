# Dependency policy

## TL;DR

- Add a dependency only for behavior needed by the current delivery slice.
- Pin reproducible resolution and use major-only GitHub Action references.
- Review maintenance, security, license, transitive cost, data handling, and a
  replacement boundary before admission.
- Automated updates may propose changes but never bypass normal review or tests.
- Repository-hosted dependency review is deferred until M08 and must not be a
  required check without verified repository support.

## Admission

Before adding a runtime or development dependency, record its current use,
alternatives, maintained status, license, known security posture, transitive
surface, platform support, data and network behavior, and replacement path.
Prefer standard-library functionality when it remains clear and maintainable.

Lock files and language manifests are committed together. Runtime code MUST NOT
resolve floating versions, branches, `latest`, or mutable deployment tags.
GitHub Actions use semantic major tags such as `actions/checkout@v7`; do not pin
opaque commit hashes in this repository.

## Updates and vulnerability handling

Dependency changes remain focused and include release-note review, compatibility
effects, generated lock changes, relevant tests, and rollback. Automated update
pull requests are inputs to review, not evidence of safety.

Known vulnerabilities are assessed for reachability, exposure, affected data,
fixed versions, mitigations, and disclosure needs. Scanner severity alone does
not establish product risk. Sensitive or novel findings follow SECURITY.md.

## Licensing

Every distributed dependency requires a license compatible with the repository
license and intended distribution. Tool-only dependencies remain classified
separately. Unknown, custom, source-available, copyleft, or dual-license terms
require explicit owner review before admission.

License and vulnerability checks enter `make validate` with the first ecosystem
that needs them. A check MUST NOT depend on a repository-hosted feature until
that feature is enabled and its ownership is established.
