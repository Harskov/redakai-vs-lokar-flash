# gameplay/86

`car1` (sprite 86) inside the jeep: it carries the gun's aim points. Two clips publish their stage positions each frame as (mx1, my1) and (mx2, my2); `processGame` aims along that line and puts the shot at (mx3, my3). `loose` plays it from frame 2.

## Functions

- `DefineSprite_86_frame_1_DoAction_main` (matched) — holds car1 (sprite 86 inside the jeep) on frame 1 until loose() plays it from frame 2
- `DefineSprite_86_frame_1_PlaceObject2_20_bullet_id_21_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (not yet matched) — bullet_mc's stage position into mx2, my2
- `DefineSprite_86_frame_1_PlaceObject2_39_23_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (not yet matched) — the first marker's stage position into mx1, my1
- `DefineSprite_86_frame_1_PlaceObject2_39_25_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (not yet matched) — the muzzle marker's stage position into mx3, my3
- `DefineSprite_86_frame_1_PlaceObject2_52_27_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (not yet matched) — plays sprite 52 while _root.bexplode

## Evidence

- placement `car1` in sprite 87 (`jeep`) (the original's PlaceObject tags)
- `localToGlobal` and `_root.mx1` ... `_root.my3` in its three clip actions
- `Math.atan2(_root.my2 - _root.my1, _root.mx2 - _root.mx1)` in `processGame`
