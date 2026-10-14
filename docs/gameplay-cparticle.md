# gameplay/cparticle

A point mass: `pos`, `prevPos`, `mass`, `acc` and an optional clip `mc`. `verlet` integrates pos += (pos - prevPos) x damp + acc x dt and moves `mc` to the result.

## Functions

- `Packages_CParticle_main` (not yet matched) — the class definition script
- `CParticle` (not yet matched) — the constructor: position, a copy as prevPos, mass, zero acc, no clip
- `CParticle.verlet` (not yet matched) — one Verlet step with the given damping

## Evidence

- `new CParticle(x, y, 3)` three times in `initLevel`; the body particle's `mc` is `mc_level.mc.mc_bike.mc_test`
- `CParticleEngine.verlet` passes damping 0.995
