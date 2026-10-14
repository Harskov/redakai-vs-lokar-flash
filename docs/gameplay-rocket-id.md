# gameplay/rocket_id

The rocket shot (sprite 12, export `rocket_id`). `processGame` attaches it under the same `bullet_id<kval>` names as bullets, 40 px left and 30 px up of the muzzle and turned 40 degrees less; one rocket destroys the helicopter (gameplay-timeline-game.md).

## Functions

- `DefineSprite_12_rocket_id_frame_1_DoAction_main` (matched) — holds the rocket (export rocket_id) on frame 1 until fire() plays it from frame 2
- `DefineSprite_12_rocket_id_frame_39_DoAction_main` (matched) — the rocket removes itself on frame 39, the frame clearStuff and the bullet checker also send spent shots to

## Evidence

- export name `rocket_id` = sprite 12
- `_root.attachMovie("rocket_id", "bullet_id" + kval, ...)` in `processGame`
- the weapontype "rocket" test in the shot checker on frame 15
