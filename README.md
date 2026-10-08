# Missile Mk I
A Python simulator that models the flight of a missile, built as a learning project stage by stage from vacuum point flight mass, to drag, atmosphere and thrust.
Each stage is validated against analytic results and numerical convergence is checked.

## Status
Stage 1 done: shows the flight path of a missile-style projectile, uses Euler integration with an interpolated landing spot to calculate a landing range within 0.069% of the analytic result.

## Roadmap
- drag
- standard atmosphere
- RK4
- thrust