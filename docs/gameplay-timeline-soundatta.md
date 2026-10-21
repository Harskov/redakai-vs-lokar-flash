# gameplay/timeline-soundatta

Sprite 150, placed on frame 11 `soundatta`, carries the game's init action (`DoInitAction`, tag 304; its
functions are on `core.md`, `audio.md`, `ui.md` and the gameplay pages). Its own frame-1 action is empty in
the reference too.

## Functions

- `DefineSprite_150_frame_1_DoAction_main` (matched) — an empty frame action (the reference has no statement); sprite 150 sits on frame 11 soundatta

## Not known

- no script jumps to frame 11 and frame 10 stops, so a script never brings the timeline here; the behaviour check's scripted session reaches it with the player's context-menu Forward (`docs/PRESERVATION.md`). Whether a jump from frame 10 to 15 runs this init action is not settled

## Evidence

- DoInitAction tag 304 belongs to sprite 150, on root frame 11 (the original's tag order)
- `DefineSprite_150_frame_1_DoAction_main`: the reference listing has no statement
