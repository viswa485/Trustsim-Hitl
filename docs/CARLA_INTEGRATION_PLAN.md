CARLA integration plan
======================

CARLA is a candidate simulator for autonomous-driving scenarios, sensors and traffic actors. It is not currently integrated.

Select a version and record matching engine, Python API and operating-system compatibility. Define adapter methods for reset, observation, action, event logging and teardown. Map controlled scenarios to simulator actors and sensors. Validate one scenario manually before automation. Add ScenarioRunner / OpenSCENARIO only after version checks. Consider ROS 2 only for a concrete autonomy-stack requirement.

Keep the Python toy environment as the CI baseline. Do not commit simulator binaries, maps or licensed assets. No CARLA server, map, actor, sensor, ScenarioRunner or ROS 2 integration is present.
