# gameplay/415

The score pop-up `score_mc`: three animations each end on a stop: +10 (frames 2-17, a box), +50 (18-33, the helicopter), -50 (34-50, a bomb hit).

## Functions

- `DefineSprite_415_frame_1_DoAction_main` (matched) — the score pop-up (score_mc) holds frame 1, empty, between pop-ups
- `DefineSprite_415_frame_17_DoAction_main` (matched) — ends the +10 pop-up the bullet checker starts at frame 2 for a box
- `DefineSprite_415_frame_33_DoAction_main` (matched) — ends the +50 pop-up the bullet checker starts at frame 18 for the helicopter
- `DefineSprite_415_frame_50_DoAction_main` (matched) — ends the -50 pop-up the bomb's handler starts at frame 34

## Evidence

- placement `score_mc` on root frame 15 (the original's PlaceObject tags)
- `score_mc.gotoAndPlay(2)` and `(18)` in the shot checker, `(34)` in the bomb's clip action
