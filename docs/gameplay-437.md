# gameplay/437

`themask_mc` (sprite 437): loops frames 1-507; `processGame` parks it on 508 when the masked man starts.

## Functions

- `DefineSprite_437_frame_507_DoAction_main` (matched) — themask_mc's loop: back to frame 1 and play; processGame parks it on frame 508 when the maskman starts

## Evidence

- placement `themask_mc` on root frame 15 (the original's PlaceObject tags)
- `_root.themask_mc.gotoAndStop(508)` in `processGame`
