# gameplay/52

Sprite 52, unnamed inside sprite 86 (`car1`): its clip action plays it while `_root.bexplode` is true; frame 2 clears the flag. The bomb's hit on the bike sets `bexplode`, so this is probably the hit effect on the jeep (unverified).

## Functions

- `DefineSprite_52_frame_1_DoAction_main` (matched) — holds sprite 52 (inside car1) on frame 1 until its clip action sees _root.bexplode; frame 2 clears the flag
- `DefineSprite_52_frame_2_DoAction_main` (not yet matched) — clears _root.bexplode

## Evidence

- placement in sprite 86 frame 1 with clip action PlaceObject2_52_27 (the original's PlaceObject tags)
- `_root.bexplode = true` in the bomb's clip action; `_root.bexplode = false` in the frame-2 script
