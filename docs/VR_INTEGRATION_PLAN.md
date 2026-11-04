VR integration plan
===================

Unity and Unreal Engine are future presentation / simulation clients. No engine scene, headset interface or human-participant study is implemented in v0.1.0.

Proposed loop: simulator state -> AI proposal -> human approval / correction -> action execution -> timestamped feedback record -> replay and evaluation.

Start with a desktop review interface and stable JSON message contract. Add headset interaction only after logging, safe fallback and usability checks. Potential study outcomes include intervention latency, missed / unnecessary interventions, workload, situation awareness and trust calibration. Obtain institutional ethics approval before recruiting participants.
