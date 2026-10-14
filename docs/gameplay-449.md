# gameplay/449

`explode_mc`: the helicopter's explosion, moved to the helicopter and played by the shot checker.

## Functions

- `DefineSprite_449_frame_1_DoAction_main` (matched) — holds explode_mc on frame 1 until the bullet checker plays it at the helicopter's position

## Evidence

- placement `explode_mc` on root frame 15 (the original's PlaceObject tags)
- `_root.explode_mc.play()` in the shot checker
