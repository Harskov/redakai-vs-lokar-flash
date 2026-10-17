# gameplay/205

Sprite 205 is `thingsin` inside sprite 206 (`things53`), inside sprite 207, which is `hoterelement` in every level (16 placements). Its two frames switch on `_root.rotates == 53`.

## Functions

- `DefineSprite_205_frame_1_DoAction_main` (matched) — holds sprite 205 (thingsin in every level's hoterelement) on frame 1 and installs the handler that moves it to frame 2 when _root.rotates is 53
- `DefineSprite_205_frame_1_DoAction.onEnterFrame` (matched) — per frame: moves to frame 2 when _root.rotates is 53, else holds; no script writes rotates, so the trigger is not known
- `DefineSprite_205_frame_2_DoAction_main` (matched) — holds sprite 205 on frame 2 and installs the handler that returns it to frame 1 unless _root.rotates is 53; no script writes rotates
- `DefineSprite_205_frame_2_DoAction.onEnterFrame` (matched) — per frame: holds while _root.rotates is 53, else returns to frame 1 (frame 1's counterpart)

## Not known

- no script writes `rotates`, so what turns the switch is not known

## Evidence

- placements `thingsin` in 206, `things53` in 207, `hoterelement` in 219, 229, 367, 374, 379, 386 (the original's PlaceObject tags)
- `_root.rotates == 53` in both handlers
