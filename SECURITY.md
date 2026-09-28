# Security policy

## TL;DR

- Do not disclose suspected vulnerabilities in public issues, discussions, or
  pull requests.
- Prefer GitHub private vulnerability reporting; otherwise request a private
  channel without sensitive details.
- The product is pre-release and only the current default branch is supported.
- Never test systems or data without explicit authorization.
- Changes to model tools, production evidence, approval, execution, or
  verification require focused security review.

## Supported versions

Argus SRE has no supported production release. Security fixes target the current
default branch. This section MUST become an explicit supported-version table
before the first supported release.

## Reporting a vulnerability

Use the repository Security page's **Report a vulnerability** action when
available. Otherwise request a private contact channel without naming the
vulnerable component, exploit, affected environment, or reproduction details.

Include the affected revision and configuration, impact, minimal reproduction,
redacted evidence, known mitigations, and prior disclosure. Do not test systems,
accounts, repositories, or data you do not own or have explicit permission to
assess.

## Product-specific security expectations

Alerts, logs, traces, repository content, previous incident text, tool output,
and model output are untrusted. A report involving prompt injection, tenant data
isolation, credential exposure, authorization confusion, approval replay,
executor escape, or false verification MUST use the private process.

The investigator and executor MUST use separate authority. A model cannot
approve an action, obtain credentials through its output, expand an approved
target, or verify its own remediation. Production actions remain prohibited
until the roadmap's supervised-remediation safety gates are implemented and
reviewed.

## Triage and disclosure

Maintainers SHOULD acknowledge reports, validate impact, agree on a private
communication path, and coordinate disclosure after a fix or effective
mitigation exists. Response targets remain best-effort until a staffed security
process is established.
