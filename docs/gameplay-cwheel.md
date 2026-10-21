# gameplay/cwheel

A wheel: a MovieClip subclass linked to `lib_back_wheel` and `lib_forward_wheel`. It holds its particle, radius, drive (`accSpeed`, `speed`) and 32 rim points with inward normals; it collides by `hitTest` against the ground clip and pushes itself out.

## Functions

- `Packages_CWheel_main` (matched) — the CWheel class script: registers the wheel class (a MovieClip subclass) with its field initialisers (maxSpeed 800, koeffSpring 0.05, koeffSlip 0.15, koeffFriction 0.97, hitCount 32) and its methods
- `CWheel` (matched) — the wheel's constructor: super() only; the fields come from the class initialisers and init
- `CWheel.init` (matched) — particle, radius, maxAccSpeed x 4, the rim points and their normals
- `CWheel.process` (matched) — integrates the drive and turns the rim clip mc.mc_rim
- `CWheel.checkCollision` (matched) — samples the rim against the hit clip, groups contiguous hits, bounces, pushes out, then validateRotation; all 32 points inside: steps back 70%
- `CWheel.pushOut` (matched) — moves the particle out along the contact normal
- `CWheel.validateRotation` (matched) — turns the contact into rolling speed, with slip and friction
- `CWheel.applyAddedAcc` (matched) — adds the wheel's addedAcc times its particle's mass to the particle's acceleration
- `lib_back_wheel_main` (matched) — links the exported symbol lib_back_wheel (sprite 116) to CWheel, so CBikeSynchronizer.init's attachMovie builds a CWheel
- `lib_forward_wheel_main` (matched) — links the exported symbol lib_forward_wheel (sprite 115) to CWheel

## Evidence

- `Object.registerClass("lib_back_wheel", CWheel)` and `("lib_forward_wheel", CWheel)`
- sprite 113 is `mc_rim` inside sprite 114, which is `mc` in both wheel sprites 115 and 116 (the original's PlaceObject tags)
- `6.283185 / hitCount` in `CWheel.init`
