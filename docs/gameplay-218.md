# gameplay/218

The masked man of levels 1-5: sprite 218 is `maskman_mc` in sprites 219, 229, 367, 374, 379. `processGame` plays it from frame 2 when the bike is within 190 px of `mc_finish` and the clip is on frame 1; it stops at 34.

## Functions

- `DefineSprite_218_frame_1_DoAction_main` (matched) — holds maskman_mc (218, in levels 1-5) on frame 1 until processGame plays it near the finish line
- `DefineSprite_218_frame_34_DoAction_main` (matched) — holds maskman_mc at the end of its animation (frame 34)

## Evidence

- placements `maskman_mc` (the original's PlaceObject tags)
- `mc_level.mc.maskman_mc.gotoAndPlay(2)` and `_root.themask_mc.gotoAndStop(508)` in `processGame`
