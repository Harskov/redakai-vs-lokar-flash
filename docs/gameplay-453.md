# gameplay/453

The bomb `bomb`: reset to frame 1 by `firebomb`, played on impact, held at frame 5.

## Functions

- `DefineSprite_453_frame_1_DoAction_main` (matched) — the bomb holds frame 1, the frame firebomb() resets it to before a drop
- `DefineSprite_453_frame_5_DoAction_main` (matched) — the bomb holds frame 5, the end of its explosion

## Evidence

- placement `bomb` on root frame 15 (the original's PlaceObject tags)
- `_root.bomb.gotoAndStop(1)` in `firebomb` and `clearStuff`; `this.play()` on impact in its clip action
