# gameplay/timeline-1

`mc_gas` (sprite 24), placed on the main timeline's frame 1 (and 10-12): the gas effect. It holds frame 1;
`processGame` plays it from frame 2 when the up key starts an acceleration (`accFlag` newly set,
`accCounter` over 10, sound not muted).

## Functions

- `DefineSprite_24_frame_1_DoAction_main` (matched) — holds mc_gas (24, root frames 1-12) on frame 1; processGame plays it from frame 2 when the up key starts an acceleration

## Not known

- none on its placement: frame 12 places it at depth 345 and no RemoveObject takes it off before frame 17, so it is
  on stage on frames 15 and 16 when `processGame` addresses it; its 19 frames hold no shape and no sound (the original's
  tags), so playing it shows and sounds nothing

## Evidence

- placement `mc_gas` on root frames 1, 10, 11, 12 (the original's PlaceObject tags)
- `mc_gas.gotoAndPlay(2)` in `processGame`
