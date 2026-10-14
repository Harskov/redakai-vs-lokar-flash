# gameplay/113

The wheel rim: sprite 113 is `mc_rim` inside sprite 114, which is `mc` in both wheel sprites (115 `lib_forward_wheel`, 116 `lib_back_wheel`). `CWheel.process` turns it; its frame action dresses the tyre for the selected vehicle.

## Functions

- `DefineSprite_113_frame_1_DoAction_main` (matched) — the wheel rim (`mc_rim` of lib_forward_wheel and lib_back_wheel): sets its `tyre` to the frame _root.jeepselection names; no script writes jeepselection

## Not known

- `jeepselection` is read here and in sprite 97; no script writes it (the car selection frame has no such code)

## Evidence

- placements `mc_rim` in 114 and `mc` in 115 and 116 (the original's PlaceObject tags)
- `_loc2_.mc.mc_rim._rotation = ...` in `CWheel.process`
