# CWheel

A bike wheel: a MovieClip class registered for both wheel symbols (`Object.registerClass("lib_back_wheel", CWheel)` and `"lib_forward_wheel"`), attached by `CBikeSynchronizer.init`. It turns its rim, tests 32 points of its rim against the ground clip and pushes its particle out of it.

**Prototype.** `class CWheel extends MovieClip`; field defaults `maxSpeed = 800`, `koeffSpring = 0.05`, `koeffSlip = 0.15`, `koeffFriction = 0.97`, `hitCount = 32`; `init` adds `particle`, `rad`, `maxAccSpeed`, `speed`, `accSpeed`, `rot`, `addedAcc`, `intersectionFlag`, `lastIntersPoint`, `lastN` and the hit-point, normal, hit and intersection arrays.

**Fields.** `addedAcc`: written by processGame (the rider's lean, as `mc_forward_wheel.addedAcc` and `mc_back_wheel.addedAcc`), cleared by `CParticleEngine.clearForces`, applied to the particle by `applyAddedAcc` (times its mass).

| Method | Accepted | Callers (confirmed in the scripts) |
|---|---|---|
| `CWheel()` | yes | the player, when a wheel symbol is attached (registerClass) |
| `init(particle_, maxAccSpeed_, rad_)` | no | CParticleEngine.addWheel |
| `applyAddedAcc()` | yes | CParticleEngine.applyManFrictions |
| `process`, `checkCollision`, `pushOut`, `validateRotation` | no | CParticleEngine (`checkCollisions`, `process`); each other |
