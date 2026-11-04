# Research plan

## Working title
TrustSim-HITL: Human-supervised safety evaluation for autonomous mobility systems.

## Research questions
1. How do autonomous, supervisory and human-supervised conditions compare on safety and task metrics?
2. How do interface information and automation level affect intervention latency and correction quality?
3. Does feedback from human reviewers improve later policy behaviour on held-out scenarios?
4. How robust are effects across scenario difficulty and distribution shift?

## Method
Use versioned scenarios, paired conditions, disclosed seeds, held-out evaluation and repeated runs. Predefine primary outcomes and exclusions. Report effect sizes and uncertainty, not only point estimates. Select statistical models appropriate to the final participant / scenario design with supervisor review.

## Planned conditions
A: autonomous baseline. B: human advisory with approve / reject / correct. C: structured human corrections used in a separately evaluated learning stage. The current software proxy only tests the data pipeline and is not human evidence.

## Validity limits
The toy model omits steering, road geometry, tyre dynamics, sensor noise, complex traffic and human factors. It tests software plumbing only. Human-subject conclusions require institutional approval and real participant data.
