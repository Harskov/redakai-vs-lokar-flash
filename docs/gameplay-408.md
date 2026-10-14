# gameplay/408

The health meter `health_mc`: four frames, one held each; each bomb hit on the bike advances it one frame and the bomb's handler calls `loose` when it reaches frame 4.

## Functions

- `DefineSprite_408_frame_1_DoAction_main` (matched) — the health meter (health_mc) holds frame 1, full health; a bomb hit advances it with nextFrame
- `DefineSprite_408_frame_2_DoAction_main` (matched) — the health meter holds frame 2 after the first bomb hit
- `DefineSprite_408_frame_3_DoAction_main` (matched) — the health meter holds frame 3 after the second bomb hit
- `DefineSprite_408_frame_4_DoAction_main` (matched) — the health meter holds frame 4; the bomb's handler calls loose() when the meter reaches it

## Evidence

- placement `health_mc` on root frame 15 (the original's PlaceObject tags)
- `_root.health_mc.nextFrame()` and `_currentframe >= 4` in the bomb's clip action
