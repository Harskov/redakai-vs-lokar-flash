# gameplay/lib_bike_body

The bike's body, the symbol `CBikeSynchronizer.init` attaches as `body` (export `lib_bike_body`, sprite 98).
Its inner clip `mc` (sprite 97) holds the jeep (`jeep`, sprite 87), the rider (`mc_body_man`) and the wheel
marks `CBikeSynchronizer` reads (`mc_f_point`, `mc_s_wheel_back`). Inside the jeep, `car1` (sprite 86) carries
the gun's aim points: three clip actions publish their stage positions every frame as (mx1, my1), (mx2, my2)
and (mx3, my3); `processGame` aims along the line from the first to the second and puts a new shot at the
third. A fourth clip action plays sprite 52 while `_root.bexplode` is set, the flag the bomb's hit on the bike
sets, so sprite 52 is probably the hit effect on the jeep (unverified). `loose` plays `jeep.car1`, `car2` and
`car3` from frame 2.

## Functions

- `DefineSprite_52_frame_1_DoAction_main` (matched) — holds sprite 52 (inside car1) on frame 1 until its clip action sees _root.bexplode; frame 2 clears the flag
- `DefineSprite_52_frame_2_DoAction_main` (matched) — clears _root.bexplode, the flag the bomb's hit sets and car1's clip action plays sprite 52 on
- `DefineSprite_86_frame_1_DoAction_main` (matched) — holds car1 (sprite 86 inside the jeep) on frame 1 until loose() plays it from frame 2
- `DefineSprite_86_frame_1_PlaceObject2_20_bullet_id_21_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (matched) — each frame, bullet_mc's stage position into (mx2, my2), the far end of processGame's aim line
- `DefineSprite_86_frame_1_PlaceObject2_39_23_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (matched) — each frame, the first aim marker's stage position into (mx1, my1), the start of processGame's aim line
- `DefineSprite_86_frame_1_PlaceObject2_39_25_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (matched) — each frame, the muzzle marker's stage position into (mx3, my3), where processGame puts a new shot
- `DefineSprite_86_frame_1_PlaceObject2_52_27_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (matched) — plays sprite 52 (inside car1) while _root.bexplode is set
- `DefineSprite_87_frame_1_DoAction_main` (matched) — holds the jeep clip (87, in sprite 97) on frame 1; sprite 97 then picks the selected jeep frame
- `DefineSprite_97_frame_1_DoAction_main` (matched) — the bike body's inner clip: sends jeep to the frame _root.jeepselection names; no script writes jeepselection

## Not known

- `jeepselection`, which sprite 97 sends the jeep to (and sprite 113 the tyre), has no writer in the scripts;
  the `carselection` frame has no such code
- what sprite 52 shows

## Evidence

- placements (the original's PlaceObject tags): `mc` (97) in 98; `jeep` (87), `mc_body_man`, `mc_f_point`,
  `mc_s_wheel_back` in 97; `car1` (86) in 87; sprite 52 unnamed in 86 with clip action PlaceObject2_52_27
- `attachMovie("lib_bike_body", "body", 3)` in `CBikeSynchronizer.init`; export `lib_bike_body` = sprite 98
- `localToGlobal` and `_root.mx1` … `_root.my3` in the three aim clip actions;
  `Math.atan2(_root.my2 - _root.my1, _root.mx2 - _root.mx1)` in `processGame`
- `_root.bexplode = true` in the bomb's clip action; `_root.bexplode = false` in `DefineSprite_52_frame_2_DoAction_main`
- `_root.bikeSync.mc_bike.mc.jeep.car1.gotoAndPlay(2)` in `loose`
