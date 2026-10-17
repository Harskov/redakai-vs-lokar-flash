# gameplay/cparticleengine

The physics step, described in `ARCHITECTURE.md` (The physics). Fields and callers: [classes/CParticleEngine.md](classes/CParticleEngine.md).

## Functions

- `Packages_CParticleEngine_main` (not yet matched) — the class definition script
- `CParticleEngine` (matched) — the physics engine's constructor; the particle, wheel and constraint arrays and the step constants are class initialisers
- `CParticleEngine.clear` (matched) — empties the engine's particle, wheel and constraint arrays
- `CParticleEngine.setHitMovie` (matched) — stores the ground clip (hit_mc) checkCollisions passes to each wheel
- `CParticleEngine.addParticle` (matched) — adds a particle to the engine's list p_array
- `CParticleEngine.addWheel` (matched) — initialises a wheel with its particle, top speed and radius and adds it to the wheel list
- `CParticleEngine.addSpringConstraint` (matched) — springs two particles together with the given compression and stretch stiffnesses and adds the constraint
- `CParticleEngine.start` (matched) — stamps prevTime with getTimer(), the baseline process() measures the first step against
- `CParticleEngine.computeForces` (matched) — each particle's acceleration for the step: 0 across, gravity times its mass down
- `CParticleEngine.clearForces` (matched) — zeroes every wheel's addedAcc after process's steps
- `CParticleEngine.applyManFrictions` (matched) — each wheel adds its addedAcc (the rider's lean, set by processGame) to its particle
- `CParticleEngine.verlet` (not yet matched) — the particles' Verlet step, then the wheels' drive: down key -0.6, up key 1, x maxAccSpeed / 3.2
- `CParticleEngine.checkCollisions` (matched) — each wheel tests itself against the ground clip hit_mc
- `CParticleEngine.checkConstraints` (matched) — resolves every spring once, in list order, with the step time
- `CParticleEngine.process` (matched) — one frame of physics: the seconds since the last call cut into up to maxSteps steps of t, each forces, lean, verlet, springs, collisions; then the lean forces cleared

## Not known

- the class default gravity 3.15 is replaced by 4 at the top of every `processGame`; only the first `process` could see 3.15, and it runs after that assignment

## Evidence

- class initialisers t 0.02, maxSteps 2, gravity 3.15
- `engine.gravity = 4` in `processGame`
- `engine.addWheel(back, p, 28.5, 17.5)` and `(front, p, 10.5, 17.5)` in `initLevel`
