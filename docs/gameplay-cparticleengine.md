# gameplay/cparticleengine

The physics step, described in `ARCHITECTURE.md` (The physics). Fields and callers: [classes/CParticleEngine.md](classes/CParticleEngine.md).

## Functions

- `Packages_CParticleEngine_main` (not yet matched) — the class definition script
- `CParticleEngine` (matched) — the physics engine's constructor; the particle, wheel and constraint arrays and the step constants are class initialisers
- `CParticleEngine.clear` (not yet matched) — empties the particle, wheel and constraint arrays
- `CParticleEngine.setHitMovie` (not yet matched) — stores the ground clip the wheels collide with
- `CParticleEngine.addParticle` (matched) — adds a particle to the engine's list p_array
- `CParticleEngine.addWheel` (not yet matched) — initialises the wheel with its particle, max speed and radius, and adds it
- `CParticleEngine.addSpringConstraint` (not yet matched) — adds a new CSpringConstraint
- `CParticleEngine.start` (matched) — stamps prevTime with getTimer(), the baseline process() measures the first step against
- `CParticleEngine.computeForces` (not yet matched) — each particle's acc = (0, gravity x mass)
- `CParticleEngine.clearForces` (not yet matched) — zeroes each wheel's addedAcc
- `CParticleEngine.applyManFrictions` (not yet matched) — each wheel's applyAddedAcc (the rider's lean)
- `CParticleEngine.verlet` (not yet matched) — the particles' Verlet step, then the wheels' drive: down key -0.6, up key 1, x maxAccSpeed / 3.2
- `CParticleEngine.checkCollisions` (not yet matched) — each wheel against the hit clip
- `CParticleEngine.checkConstraints` (not yet matched) — resolves each spring
- `CParticleEngine.process` (not yet matched) — up to maxSteps fixed steps of t for the time since the last call

## Not known

- the class default gravity 3.15 is replaced by 4 at the top of every `processGame`; only the first `process` could see 3.15, and it runs after that assignment

## Evidence

- class initialisers t 0.02, maxSteps 2, gravity 3.15
- `engine.gravity = 4` in `processGame`
- `engine.addWheel(back, p, 28.5, 17.5)` and `(front, p, 10.5, 17.5)` in `initLevel`
