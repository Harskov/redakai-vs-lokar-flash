# gameplay/112

The tyre: sprite 112 is `tyre` inside sprite 113 (the wheel rim). Its frame 1 holds until sprite 113 picks a frame by `_root.jeepselection`.

## Functions

- `DefineSprite_112_frame_1_DoAction_main` (matched) — holds the wheel's `tyre` clip (112, in sprite 113) on frame 1 until sprite 113 picks the selected frame

## Evidence

- placement `tyre` in sprite 113 (the original's PlaceObject tags)
- `tyre.gotoAndStop(_root.jeepselection)` in `DefineSprite_113_frame_1_DoAction_main`
