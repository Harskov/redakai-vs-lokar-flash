# gameplay/cbikesynchronizer

Joins the physics to the graphics. `init` attaches the back wheel, front wheel and body (`lib_back_wheel`, `lib_forward_wheel`, `lib_bike_body`) into the level clip and puts the wheels at the body's wheel marks; `setParticles` records the three particles and the suspension geometry; `process` moves and turns the body from the particles and poses both springs and the rider.

## Functions

- `calcBikeNVector` (matched) — the bike's normal: the back-to-front wheel vector from the wheels' particles, normalised and turned a quarter turn to (-y, x); processGame leans the bike along it under `CMan.LEFT_BUTTON` or `RIGHT_BUTTON` while its y is positive
- `Packages_CBikeSynchronizer_main` (matched) — the CBikeSynchronizer class script: registers the class on _global and puts init, setParticles and process on its prototype
- `CBikeSynchronizer` (matched) — the constructor: four zero CVector2D, fdir, fpos, bdir and bpos (probably the front and back wheels' direction and position)
- `CBikeSynchronizer.init` (matched) — attaches back_w (depth 2), forward_w (1) and body (3) and places the wheels
- `CBikeSynchronizer.setParticles` (matched) — stores pBody, pBWheel, pFWheel and the front fork direction and back spring geometry
- `CBikeSynchronizer.process` (matched) — body position and rotation from the particles; front spring, rider offset and back spring rotation

## Evidence

- `attachMovie("lib_back_wheel", "back_w", 2)`, `("lib_forward_wheel", "forward_w", 1)`, `("lib_bike_body", "body", 3)` in `CBikeSynchronizer.init`
- export names lib_bike_body (sprite 98), lib_forward_wheel (115), lib_back_wheel (116)
- `bikeSync.setParticles(bikePart, backPart, forwardPart)` in `initLevel`
- `bikeSync.mc_forward_wheel.particle.pos.minusNew(bikeSync.mc_back_wheel.particle.pos)` in `calcBikeNVector`, whose two callers are in `processGame`
