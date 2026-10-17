# gameplay/lib_forward_wheel

The wheel graphics. Both wheel symbols, `lib_forward_wheel` (sprite 115) and `lib_back_wheel` (116), hold
sprite 114 as `mc`, whose rim `mc_rim` (sprite 113) `CWheel.process` turns. The rim's frame action dresses its
tyre (`tyre`, sprite 112) for the selected vehicle by sending it to the frame `_root.jeepselection` names; the
tyre holds frame 1 until then. The label names the forward wheel, but the same sprites serve the back wheel.
The class behind both wheel symbols is `CWheel` (gameplay-cwheel.md).

## Functions

- `DefineSprite_112_frame_1_DoAction_main` (matched) — holds the wheel's `tyre` clip (112, in sprite 113) on frame 1 until sprite 113 picks the selected frame
- `DefineSprite_113_frame_1_DoAction_main` (matched) — the wheel rim (`mc_rim` of lib_forward_wheel and lib_back_wheel): sets its `tyre` to the frame _root.jeepselection names; no script writes jeepselection

## Not known

- `jeepselection` is read here and in sprite 97 and written by no script

## Evidence

- placements `tyre` (112) in 113, `mc_rim` (113) in 114, `mc` (114) in 115 and 116 (the original's PlaceObject tags)
- export names `lib_forward_wheel` = sprite 115, `lib_back_wheel` = sprite 116
- `tyre.gotoAndStop(_root.jeepselection)` in `DefineSprite_113_frame_1_DoAction_main`
- `mc.mc_rim._rotation` set in `CWheel.process`
