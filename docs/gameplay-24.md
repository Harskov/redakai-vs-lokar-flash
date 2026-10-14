# gameplay/24

`mc_gas` (sprite 24): `processGame` plays it from frame 2 when the up key starts an acceleration (`accFlag` set, `accCounter` over 10, sound on).

## Functions

- `DefineSprite_24_frame_1_DoAction_main` (matched) — holds mc_gas (24, root frames 1-12) on frame 1; processGame plays it from frame 2 when the up key starts an acceleration

## Not known

- it is placed on frames 1 and 10-12, not 15; whether it is still on stage when `processGame` addresses it is not established

## Evidence

- placement `mc_gas` on root frames 1, 10, 11, 12 (the original's PlaceObject tags)
- `mc_gas.gotoAndPlay(2)` in `processGame`
