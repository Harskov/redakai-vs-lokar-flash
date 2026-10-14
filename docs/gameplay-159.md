# gameplay/159

A random background: sprite 159 is `mc_fon` in levels 1, 2, 4, 5 and 6; on frame 1 it shows one of five backgrounds at random.

## Functions

- `DefineSprite_159_frame_1_DoAction_main` (not yet matched) — picks background 1-5 at random for its `bg` clip

## Evidence

- placements `mc_fon` in sprites 219, 229, 374, 379, 386 (the level frames of `mc_level`; the original's PlaceObject tags)
- `var bgss = 1 + random(5); bg.gotoAndStop(bgss);` (`DefineSprite_159_frame_1_DoAction_main`)
