# gameplay/443

The crash clip `crash`: `loose` plays it from frame 2, which silences every sound and plays the crash sound once; frame 51 installs a handler that takes a life and replays the level.

## Functions

- `DefineSprite_443_frame_1_DoAction_main` (matched) — holds the crash clip (crash, frame 15) on frame 1 until loose() plays it
- `DefineSprite_443_frame_2_DoAction_main` (matched) — the crash clip's first frame: silences every sound and plays the crash sound cra once
- `DefineSprite_443_frame_51_DoAction_main` (matched) — the crash clip's frame 51 installs the handler that takes a life (lifee) and replays the level
- `DefineSprite_443_frame_51_DoAction.onEnterFrame` (not yet matched) — each frame: lifee - 1 and _root.replay()

## Evidence

- placement `crash` on root frame 15 (the original's PlaceObject tags)
- `_root.crash.gotoAndPlay(2)` in `loose`
- `_root.lifee -= 1; _root.replay();` in the frame-51 handler
