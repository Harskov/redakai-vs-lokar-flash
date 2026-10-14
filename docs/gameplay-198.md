# gameplay/198

The box mask: sprite 198 is `mask_mc` in level 1 and `mask_hit_mc` inside the hit map (sprite 202, `mc_hit`). When a box breaks, the shot checker also plays its counterparts in `mask_mc` and `mc_hit.mask_hit_mc`, so the ground the wheels touch changes with it.

## Functions

- `DefineSprite_198_frame_1_DoAction_main` (matched) — holds the box mask (198: mask_mc in level 1, mask_hit_mc in the hit map) on frame 1; its box6 and box7 children play with the boxes

## Evidence

- placements `mask_hit_mc` in 202 and `mask_mc` in 219; 202 is `mc_hit` in 219 (the original's PlaceObject tags)
- `mc_level.mc.mask_mc.box<pi>.play()` and `mc_level.mc.mc_hit.mask_hit_mc.box<pi>.play()` in the shot checker
