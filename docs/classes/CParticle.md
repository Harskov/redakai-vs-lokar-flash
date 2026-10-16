# CParticle

A point mass of the physics: the bike body and the two wheel hubs are one particle each, made in `initLevel` with mass 3 at their clips' positions.

**Prototype.** `class CParticle` (no base class); fields assigned by the constructor in this order: `pos` (a CVector2D), `prevPos` (a copy of `pos`), `mass`, `acc` (a zero CVector2D), `mc` (`null` until a clip is attached).

**Fields.** `pos`, `prevPos`: advanced by `verlet` (position plus the damped difference from the previous position plus `acc` times the step); `acc`: set by `CParticleEngine.computeForces` (gravity times the mass), then added to by `CWheel.applyAddedAcc`; `mc`: when set, `verlet` moves it to `pos`.

| Method | Accepted | Callers (confirmed in the scripts) |
|---|---|---|
| `CParticle(x_, y_, mass_)` | yes | initLevel (three particles) |
| `verlet(dTime, koeffDamp)` | no | CParticleEngine.verlet (`koeffDamp` 0.995) |
| the class script | yes | the player, on frame 1's init action (registers the class on `_global` once) |
