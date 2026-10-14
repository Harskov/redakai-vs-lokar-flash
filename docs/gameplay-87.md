# gameplay/87

The jeep (sprite 87, `jeep` inside sprite 97): holds frame 1; it contains `car1` (sprite 86), and `loose` plays `jeep.car1`, `car2` and `car3` from frame 2.

## Functions

- `DefineSprite_87_frame_1_DoAction_main` (matched) — holds the jeep clip (87, in sprite 97) on frame 1; sprite 97 then picks the selected jeep frame

## Evidence

- placement `jeep` in sprite 97 (the original's PlaceObject tags)
- `_root.bikeSync.mc_bike.mc.jeep.car1.gotoAndPlay(2)` in `loose`
