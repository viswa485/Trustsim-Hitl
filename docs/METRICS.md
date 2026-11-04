# Metric definitions

The current runner reports episode-level measures:

- `collision_rate`: fraction ending in a collision event in the toy model.
- `unsafe_step_rate`: fraction of steps below the modelled required-gap heuristic.
- `episode_completion_rate`: fraction reaching the configured horizon without collision.
- `mean_speed_mps`: average ego speed.
- `braking_action_rate`: fraction of actions that brake.
- `supervisor_overrides_per_episode`: scripted-proxy overrides per episode.
- `mean_episode_return`: average sum of the toy reward.

These are software-pipeline metrics. The gap heuristic is not a validated safety envelope, a toy collision is not a real crash-risk estimate, and proxy overrides are not human interventions. Future human studies may assess intervention latency, missed / unnecessary intervention, correction quality, workload and situation awareness using supervisor-approved measures.
