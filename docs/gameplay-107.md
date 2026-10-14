# gameplay/107

Sprite 107, a two-frame clip inside sprite 108, which sits on the menu frames 10-12, 17 and 19. Each frame holds.

## Functions

- `DefineSprite_107_frame_1_DoAction_main` (matched) — holds sprite 107 on frame 1; 107 sits in sprite 108 on the root frames 10-12, 17 and 19; what the clip shows is not established
- `DefineSprite_107_frame_2_DoAction_main` (matched) — holds sprite 107 on frame 2; no script sends it there, so its trigger is not known

## Not known

- what the clip shows and what moves it to frame 2

## Evidence

- sprite 107 placed in sprite 108 frame 1, no instance name; 108 on root frames 10, 11, 12, 17, 19 (the original's PlaceObject tags)
- `DefineSprite_107_frame_1_DoAction_main` and frame 2's are each `stop()`
