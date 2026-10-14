# gameplay/bullet_id

The gun's shots. `processGame` attaches a `bullet_id` clip (G, key 71) or a `rocket_id` clip (F, key 70) as `bullet_id<kval>` (kval cycles 1000-1100) at the muzzle point (mx3, my3), turned to the angle from (mx1, my1) to (mx2, my2), and lists it in `_root.bulletArray`; `fire` plays it 50 ms later and `resetkfire` re-arms the gun after 290 ms. The aim points come from sprite 86 (gameplay-86.md).

## Functions

- `DefineSprite_20_bullet_id_frame_1_DoAction_main` (matched) — holds the bullet (export bullet_id) on frame 1 until fire() plays it from frame 2
- `DefineSprite_20_bullet_id_frame_39_DoAction_main` (not yet matched) — the bullet removes itself on frame 39
- `fire` (not yet matched) — plays the newest shot (bullet_id<kval>) from frame 2
- `resetkfire` (not yet matched) — sets kfire, re-arming the gun

## Evidence

- export name `bullet_id` = sprite 20 (the original's ExportAssets); sprite 20 is also `bullet_mc` inside sprite 86
- `setTimeout(fire, 50)` and `setTimeout(resetkfire, 290)` in `processGame`
- `Key.isDown(71)` / `Key.isDown(70)` choose weapontype "bullet" / "rocket" in `processGame`
