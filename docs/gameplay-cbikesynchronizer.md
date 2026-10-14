# gameplay/cbikesynchronizer

Joins the physics to the graphics. `init` attaches the back wheel, front wheel and body (`lib_back_wheel`, `lib_forward_wheel`, `lib_bike_body`) into the level clip and puts the wheels at the body's wheel marks; `setParticles` records the three particles and the suspension geometry; `process` moves and turns the body from the particles and poses both springs and the rider.

## Functions

- `calcBikeNVector` (not yet matched) — the bike's normal: the back-to-front wheel vector, normalised and turned 90 degrees; processGame tilts the bike along it
- `Packages_CBikeSynchronizer_main` (not yet matched) — the class definition script
- `CBikeSynchronizer` (not yet matched) — the constructor: four CVector2D, fdir, fpos, bdir, bpos
- `CBikeSynchronizer.init` (not yet matched) — attaches back_w (depth 2), forward_w (1) and body (3) and places the wheels
- `CBikeSynchronizer.setParticles` (not yet matched) — stores pBody, pBWheel, pFWheel and the front fork direction and back spring geometry
- `CBikeSynchronizer.process` (not yet matched) — body position and rotation from the particles; front spring, rider offset and back spring rotation

## Evidence

- `attachMovie("lib_back_wheel", "back_w", 2)`, `("lib_forward_wheel", "forward_w", 1)`, `("lib_bike_body", "body", 3)` in `CBikeSynchronizer.init`
- export names lib_bike_body (sprite 98), lib_forward_wheel (115), lib_back_wheel (116)
- `bikeSync.setParticles(body, back, front)` in `initLevel`
