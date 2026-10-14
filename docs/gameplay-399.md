# gameplay/399

An on/off switch on frame 15 (sprite 399, frame labels `on` and `off`): its button `btnon` toggles between the two; the `off` frame stops every sound.

## Functions

- `DefineSprite_399_frame_1_DoAction_main` (not yet matched) — holds and installs btnon's press (to `off`)
- `DefineSprite_399_frame_1_DoAction.onPress` (matched) — the on/off switch on frame 15 (labels on, off): a press while on plays from `off`, whose frame stops every sound; probably the sound switch (unverified)
- `DefineSprite_399_frame_2_DoAction_main` (not yet matched) — holds, stops every sound, installs btnon's press (to `on`)
- `DefineSprite_399_frame_2_DoAction.onPress` (matched) — the on/off switch's press while off: plays from `on`

## Not known

- whether this is the sound switch: `soundOn`/`soundOff` are never called, and nothing turns the sound back on at `on`

## Evidence

- frame labels `on` (1) and `off` (2) of sprite 399, unnamed placement on root frame 15 (the original's PlaceObject tags)
- `stopAllSounds()` in the frame-2 script
