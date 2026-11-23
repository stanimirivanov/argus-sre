# Argus SRE domain language

Terms for incident investigation, evidence, and supervised remediation. These terms describe the approved design for the planned runtime.

## Language

### Incident and evidence

**Alert Delivery**
One provider delivery carrying a source alert. A retried delivery and an incident have separate identities.

**Incident**
The durable identity of an operational problem being investigated or tracked through recovery.

**Deployment Correlation**
An incident-scoped association with an exact deployment, supported by scoped deployment and source evidence. A matching Git revision alone is a candidate relationship.

**Evidence Reference**
A scoped reference to a producer's observation or immutable artifact, retaining source, time, provenance, and integrity information.

**Finding**
A material, evidence-linked statement in an investigation, classified as observation or inference.

**Hypothesis**
A possible explanation of the incident, with supporting, contradicting, or missing evidence.

**Reviewed Incident Outcome**
A reviewed incident conclusion that another product may consume as evidence under its own policy.

### Investigation lifecycle

**Investigation Revision**
An immutable published investigation result for an incident, retaining the scope and evidence used. Same-scope material late evidence can produce a later revision.

**Follow-up Investigation**
A separately identified investigation linked to the same incident when its scope or purpose changes.

**Investigation Outcome**
The declared result of an investigation revision: propose action, request evidence, escalate, or abstain.

**Abstention**
The explicit outcome when contradictory or insufficient evidence leaves no justified bounded next step.

### Action and recovery

**Action Proposal**
A typed recommendation for an exact operation and target, with preconditions, expiry, expected effect, and a verification plan.

**Approval**
An authenticated human decision bound to one exact action proposal, target, parameters, expiry, and permitted executor.

**Execution Observation**
The attributable record of what the restricted executor attempted and observed.

**Verification Plan**
The recovery conditions and guardrails that an independent verifier evaluates after execution.

**Verification Verdict**
The independent passed, failed, or inconclusive determination of whether recovery and guardrails held.
