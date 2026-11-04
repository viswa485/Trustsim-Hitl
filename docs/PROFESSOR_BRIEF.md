# Supervisor discussion brief

## Working title
**TrustSim-HITL: A framework for evaluating human-supervised safety interventions in autonomous-mobility simulation.**

## Motivation
When an automated policy faces uncertainty or a high-consequence situation, a human may need to inspect, approve or correct a recommendation. A research platform should trace the context, proposal, intervention, executed action and outcome, and compare strategies under controlled scenarios.

## Initial research question
How do supervision interface and feedback strategies affect safety-related outcomes, task performance and human workload in controlled autonomous-mobility scenarios?

## Current prototype boundary
The v0.1.0 implementation is a simplified Python longitudinal-road simulation with a rule-based controller, deterministic scripted expert proxy, feedback record format, calibration baseline and paired experiment conditions. The proxy is software-generated, not a human participant. No real human feedback, VR scene, CARLA integration or validated vehicle-dynamics model is implemented.

## Proposed progression
1. Agree scope, hypotheses and evaluation criteria with the supervisor.
2. Strengthen scenario validity and software verification.
3. Add a desktop human-review interface and event provenance.
4. Obtain institutional ethics approval before any participant recruitment.
5. Integrate a version-pinned simulator such as CARLA; clarify Unity / Unreal roles.
6. Run a pilot and report uncertainty, limitations and failure cases.

## Questions for discussion
- Should the domain be autonomous driving, mobility logistics or general autonomous agents?
- Which simulator and engine stack are available in the lab?
- Which safety and assurance methods should structure requirements and evidence?
- Is a human-participant study feasible, and what is the ethics review route?
- Which baselines and statistical methods are expected?

## Potential contribution
A modular, reproducible framework for tracing and comparing automated decisions, software safeguards and genuine human-supervised intervention workflows. This is a proposed contribution, not a completed finding.
