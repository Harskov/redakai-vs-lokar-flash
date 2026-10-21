# CBikeSynchronizer

The bike's assembly: `initLevel` makes the one instance (`bikeSync`), `init` attaches the two wheel clips and the body clip into the level's `mc_bike` container, `setParticles` ties them to the physics engine's particles, and processGame calls `process` each frame.

**Prototype.** `class CBikeSynchronizer` (no base class); the constructor sets `fdir`, `fpos`, `bdir`, `bpos` to zero vectors (probably a direction and a position for the forward and back wheels; unverified); `init` adds `mc_back_wheel`, `mc_forward_wheel` (`lib_back_wheel`, `lib_forward_wheel`, both CWheel) and `mc_bike` (`lib_bike_body`).

| Method | Accepted | Callers (confirmed in the scripts) |
|---|---|---|
| `CBikeSynchronizer()` | yes | initLevel (`bikeSync = new CBikeSynchronizer()`) |
| `init(mc_container, sX, sY)` | yes | initLevel (`bikeSync.init(mc_level.mc.mc_bike, 0, 0)`) |
| `setParticles(pBody_, pBWheel_, pFWheel_)` | yes | initLevel |
| `process()` | yes | processGame |
