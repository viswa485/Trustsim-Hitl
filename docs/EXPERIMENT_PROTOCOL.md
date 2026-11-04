# Experiment protocol — draft

**Status:** outline for supervisor review; not preregistered, not ethics-approved and not ready for recruitment.

## Current software conditions
- autonomous_baseline: rule-based policy.
- scripted_safety_shield: baseline plus deterministic software proxy override.
- feedback_calibrated: baseline calibrated on synthetic proxy labels.

These are software conditions, not human-interaction conditions.

## Proposed future human conditions
C1 automation-only; C2 decision support with approve / override controls; C3 decision support plus structured corrections used in a separate learning stage. Counterbalance order, control practice effects and balance scenario difficulty.

## Unit of analysis
Current tests use a scenario episode. A future human study uses participant-by-scenario trials and accounts for repeated measures and participant variability.

## Planned logging
Scenario ID, pseudonymous trial ID, timestamp, policy proposal, displayed context, participant choice, executed action, intervention latency and optional rationale. Keep linkage keys separately protected; do not record names in event logs.

## Analysis and ethics
Predefine outcomes and exclusions. Report effect sizes, confidence intervals, missingness and adverse events. Select repeated-measures / mixed-effects methods after design and sample-size planning with a statistician or supervisor. Obtain institutional approval before recruiting participants and define consent, withdrawal and retention procedures.
