# gameplay/197

The destructible box: placed 72 times as `box1`...`box7` in the level sprites (and box6, box7 in sprite 198). It waits on frame 1; the shot checker plays it when a bullet hits and it stops at frame 11.

## Functions

- `DefineSprite_197_frame_1_DoAction_main` (matched) — the destructible box (box1-box7 in the level sprites) waits on frame 1; the bullet checker plays it on a bullet hit; the doubled stop() is in the original
- `DefineSprite_197_frame_11_DoAction_main` (matched) — the box's last frame: holds after the destruction animation

## Evidence

- placements `box1`...`box7` in the level sprites (219, 229, ...) and in the mask sprites 198 and 226 (the original's PlaceObject tags)
- `mc_level.mc.box<pi>._currentframe == 1` then `play()` in the shot checker (frame 15, PlaceObject2_455_357)
