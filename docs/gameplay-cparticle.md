# gameplay/cparticle

A point mass: `pos`, `prevPos`, `mass`, `acc` and an optional clip `mc`. `verlet` integrates pos += (pos - prevPos) x damp + acc x dt and moves `mc` to the result.

## Functions

- `Packages_CParticle_main` (matched) — the CParticle class script: registers the point-mass class on _global and puts verlet on its prototype
- `CParticle` (matched) — the point mass's constructor: pos at (x, y), prevPos a copy of it, the mass, zero acc, no clip
- `CParticle.verlet` (not yet matched) — one Verlet step with the given damping

## Evidence

- `new CParticle(x, y, 3)` three times in `initLevel`; the body particle's `mc` is `mc_level.mc.mc_bike.mc_test`
- `CParticleEngine.verlet` passes damping 0.995
