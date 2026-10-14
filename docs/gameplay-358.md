# gameplay/358

Level 3's random background: sprite 358 is `mc_fon` in sprite 367 and runs the same script as sprite 159.

## Functions

- `DefineSprite_358_frame_1_DoAction_main` (not yet matched) — picks background 1-5 at random for its `bg` clip

## Evidence

- placement `mc_fon` in sprite 367 (`mc_level` frame 3; the original's PlaceObject tags)
- `bg.gotoAndStop(1 + random(5))` in `DefineSprite_358_frame_1_DoAction_main`
