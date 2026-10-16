# CParticleEngine

The physics engine: it holds the particles, the wheels and the spring constraints, and steps them in fixed time slices. One instance, `engine`, created in `initLevel`.

**Prototype.** `class CParticleEngine` (no base class); fields in declaration order: `hit_mc`, `prevTime`, `p_array = new Array()`, `w_array = new Array()`, `c_array = new Array()`, `t = 0.02`, `maxSteps = 2`, `gravity = 3.15`.

**Fields.** `p_array` (particles): `addParticle` pushes, `clear` empties, `computeForces` and `verlet` read. `w_array` (wheels) and `c_array` (spring constraints): filled by `addWheel` and `addSpringConstraint`. `prevTime`: written by `start`, read and rewritten by `process`, which turns the elapsed time into at most `maxSteps` steps of `t` seconds. `hit_mc`: set by `setHitMovie`, read by `checkCollisions`.

| Method | Accepted | Callers (confirmed in the scripts) |
|---|---|---|
| `CParticleEngine()` | yes | initLevel (`engine = new CParticleEngine()`) |
| `addParticle(p)` | yes | initLevel (three particles) |
| `start()` | yes | initLevel (`engine.start()`, after the level is built) |
| `addWheel(wheel, p, maxSpeed, radius)` | yes | initLevel (the two wheels) |
| `addSpringConstraint(p1, p2, koeffStiff1, koeffStiff2)` | yes | initLevel |
| `applyManFrictions()` | yes | `process` (each wheel's `applyAddedAcc`) |
| `checkCollisions()` | yes | `process` (each wheel's `checkCollision` against `hit_mc`) |
| `checkConstraints(dTime)` | yes | `process` (each constraint's `resolve`) |
| `setHitMovie(hit_mc_)` | yes | initLevel (`engine.setHitMovie(mc_level.mc.mc_hit)`) |
| `clearForces()` | yes | `process`, once its iterations are done (each wheel's `addedAcc` to zero) |
| `clear`, `computeForces`, `verlet`, `process` | no | `process` from processGame; the rest from initLevel or `process` |
