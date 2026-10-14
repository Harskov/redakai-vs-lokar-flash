# gameplay/446

The helicopter `helicop`: flown by its clip action on frame 15 (gameplay-timeline-game.md); `processGame` brings it in at x 786.4 when `helicounter` reaches 200. Brightness marks its state: 150 when hit, -150 destroyed, 0 normal.

## Functions

- `DefineSprite_446_frame_1_DoAction_main` (matched) — the helicopter (helicop) holds frame 1 with its brightness restored (offset 0; -150 is the destroyed look)

## Evidence

- placement `helicop` on root frame 15 (the original's PlaceObject tags)
- `_root.setBright(_root.helicop, ...)` with 150, -150 and 0 in the shot checker, the clip action and `DefineSprite_446_frame_1_DoAction_main`
