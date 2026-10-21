# gameplay/timeline-game

Everything placed on frame 15 `game` and inside the level clip `mc_level`: the controller `mc_control`, the helicopter, the bomb and the shot checker with their clip actions, the two helpers frame 15 defines, and the frame actions of the clips they drive. The loop they call is in `ARCHITECTURE.md`.

## The clips

On frame 15 (instance names from the original's PlaceObject tags):

- `health_mc` (sprite 408): four frames, one held each; each bomb hit on the bike advances it with `nextFrame`, and the bomb's handler calls `loose` once it reaches frame 4.
- `score_mc` (sprite 415): three pop-ups, each ending on a stop: +10 (frames 2-17, a box), +50 (18-33, the helicopter), -50 (34-50, a bomb hit).
- `crash` (sprite 443): `loose` plays it from frame 2, which silences every sound and plays the crash sound `cra`; frame 51 installs a handler that takes one `lifee` and calls `replay`.
- `helicop` (sprite 446) and its explosion `explode_mc` (449): `processGame` brings the helicopter in at x 786.4 when `helicounter` reaches 200; `setBright` marks its state (150 hit, -150 destroyed, 0 normal).
- `bomb` (sprite 453): reset to frame 1 by `firebomb` and `clearStuff`, played on impact, held at frame 5.
- `themask_mc` (sprite 437): loops frames 1-507; `processGame` parks it on 508 when the masked man starts.
- the on/off switch (sprite 399, frame labels `on`, `off`): its button `btnon` toggles between the two, and `off` stops every sound; probably the sound switch (unverified).
- `sd1` (sprite 440): holds frame 1; no script names it.

Inside the levels (`mc_level`, sprite 387, frames `level1`...`level6`):

- `mc_fon`, the background: sprite 159 in levels 1, 2, 4, 5, 6 and sprite 358 in level 3, each showing one of five backgrounds at random.
- the boxes `box1`...`box7` (sprite 197, 72 placements): each waits on frame 1; the shot checker plays it on a bullet hit and it holds at frame 11. Their counterparts in the box mask (sprite 198: `mask_mc` in level 1, `mask_hit_mc` inside the hit map `mc_hit`) play with them, so the ground the wheels touch changes when a box breaks.
- `maskman_mc`, the masked man: sprite 218 in levels 1-5 (held at 34) and sprite 385 in level 6 (held at 5); `processGame` plays it from frame 2 when the bike is within 190 px of `mc_finish`.
- `things53` (sprite 206) inside `hoterelement` (sprite 207, in every level): holds either of its two frames and contains sprite 205 (`thingsin`, gameplay-205.md).

## Functions

- `DefineSprite_159_frame_1_DoAction_main` (matched) — a level background (mc_fon in levels 1, 2, 4, 5, 6): shows one of five backgrounds at random on its bg clip
- `DefineSprite_197_frame_1_DoAction_main` (matched) — the destructible box (box1-box7 in the level sprites) waits on frame 1; the bullet checker plays it on a bullet hit; the doubled stop() is in the original
- `DefineSprite_197_frame_11_DoAction_main` (matched) — the box's last frame: holds after the destruction animation
- `DefineSprite_198_frame_1_DoAction_main` (matched) — holds the box mask (198: mask_mc in level 1, mask_hit_mc in the hit map) on frame 1; its box6 and box7 children play with the boxes
- `DefineSprite_206_frame_1_DoAction_main` (matched) — holds sprite 206 (things53 inside the hoterelement clip of every level) on frame 1
- `DefineSprite_206_frame_2_DoAction_main` (matched) — holds sprite 206 on frame 2; no script sends it there
- `DefineSprite_218_frame_1_DoAction_main` (matched) — holds maskman_mc (218, in levels 1-5) on frame 1 until processGame plays it near the finish line
- `DefineSprite_218_frame_34_DoAction_main` (matched) — holds maskman_mc at the end of its animation (frame 34)
- `DefineSprite_358_frame_1_DoAction_main` (matched) — level 3's background (mc_fon in sprite 367): the same random pick of five as sprite 159
- `DefineSprite_385_frame_1_DoAction_main` (matched) — holds level 6's maskman_mc (385, in sprite 386) on frame 1
- `DefineSprite_385_frame_5_DoAction_main` (matched) — holds level 6's maskman_mc on frame 5, the end of its animation
- `DefineSprite_399_frame_1_DoAction_main` (matched) — the on/off switch on frame 15 (label on): holds and points btnon's press to the off frame; probably the sound switch (unverified)
- `DefineSprite_399_frame_1_DoAction.onPress` (matched) — the on/off switch on frame 15 (labels on, off): a press while on plays from `off`, whose frame stops every sound; probably the sound switch (unverified)
- `DefineSprite_399_frame_2_DoAction_main` (matched) — the switch's off frame: holds, stops every sound and points btnon's press back to on
- `DefineSprite_399_frame_2_DoAction.onPress` (matched) — the on/off switch's press while off: plays from `on`
- `DefineSprite_408_frame_1_DoAction_main` (matched) — the health meter (health_mc) holds frame 1, full health; a bomb hit advances it with nextFrame
- `DefineSprite_408_frame_2_DoAction_main` (matched) — the health meter holds frame 2 after the first bomb hit
- `DefineSprite_408_frame_3_DoAction_main` (matched) — the health meter holds frame 3 after the second bomb hit
- `DefineSprite_408_frame_4_DoAction_main` (matched) — the health meter holds frame 4; the bomb's handler calls loose() when the meter reaches it
- `DefineSprite_415_frame_1_DoAction_main` (matched) — the score pop-up (score_mc) holds frame 1, empty, between pop-ups
- `DefineSprite_415_frame_17_DoAction_main` (matched) — ends the +10 pop-up the bullet checker starts at frame 2 for a box
- `DefineSprite_415_frame_33_DoAction_main` (matched) — ends the +50 pop-up the bullet checker starts at frame 18 for the helicopter
- `DefineSprite_415_frame_50_DoAction_main` (matched) — ends the -50 pop-up the bomb's handler starts at frame 34
- `DefineSprite_437_frame_507_DoAction_main` (matched) — themask_mc's loop: back to frame 1 and play; processGame parks it on frame 508 when the maskman starts
- `DefineSprite_440_frame_1_DoAction_main` (matched) — holds sd1 (440, frame 15) on frame 1; no script names sd1, so its role is not known
- `DefineSprite_443_frame_1_DoAction_main` (matched) — holds the crash clip (crash, frame 15) on frame 1 until loose() plays it
- `DefineSprite_443_frame_2_DoAction_main` (matched) — the crash clip's first frame: silences every sound and plays the crash sound cra once
- `DefineSprite_443_frame_51_DoAction_main` (matched) — the crash clip's frame 51 installs the handler that takes a life (lifee) and replays the level
- `DefineSprite_443_frame_51_DoAction.onEnterFrame` (matched) — the end of the crash animation: one life off (lifee) and _root.replay() restarts the level
- `DefineSprite_446_frame_1_DoAction_main` (matched) — the helicopter (helicop) holds frame 1 with its brightness restored (offset 0; -150 is the destroyed look)
- `DefineSprite_449_frame_1_DoAction_main` (matched) — holds explode_mc on frame 1 until the bullet checker plays it at the helicopter's position
- `DefineSprite_453_frame_1_DoAction_main` (matched) — the bomb holds frame 1, the frame firebomb() resets it to before a drop
- `DefineSprite_453_frame_5_DoAction_main` (matched) — the bomb holds frame 5, the end of its explosion
- `firebomb` (matched) — while the helicopter is active: the bomb to its release point under helicop (34.6 down, 10.1 left), frame 1, opaque, and dropbomb starts its fall; processGame schedules it 1.8 s after the helicopter enters, and the helicopter's clip action calls it again
- `setBright` (matched) — sets a clip's brightness: a ColorMatrixFilter that adds newVal to red, green and blue (150 hit, -150 destroyed, 0 normal in the callers)
- `frame_15_PlaceObject2_33_1_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (matched) — mc_control each frame: _parent.processGame(), and accSnd started once per press of the up key (_accSnd remembers it)
- `frame_15_PlaceObject2_33_1_CLIPACTIONRECORD_onClipEvent_keyDown_main` (matched) — mc_control's key handler: _parent.keyPressed(), which no script defines, then updateAfterEvent()
- `frame_15_PlaceObject2_33_1_CLIPACTIONRECORD_onClipEvent_keyDown__2_main` (matched) — mc_control's second key handler, identical to the first: _parent.keyPressed() then updateAfterEvent()
- `frame_15_PlaceObject2_33_1_CLIPACTIONRECORD_onClipEvent_load_main` (matched) — mc_control's load: _parent.initLevel() builds the attempt each time frame 15 places the clip
- `frame_15_PlaceObject2_446_349_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (matched) — the helicopter: 4 px left a frame while active, off past x -270; destroyed, it falls 12 px a frame at brightness -150 and comes back at (1006.4, 58.4), firing again
- `frame_15_PlaceObject2_453_353_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (matched) — the bomb's flight, 22 px a frame along `degrees`: a hit on the bike costs 50 mscore and one health frame (loose at frame 4); the ground mask or y > 500 ends it
- `frame_15_PlaceObject2_453_353_CLIPACTIONRECORD_onClipEvent_load_main` (matched) — the bomb's heading on load: rotation 220 and degrees set to that angle in radians (despite its name)
- `frame_15_PlaceObject2_455_357_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (matched) — the shot checker: bullets against boxes 1-7 (+10), any shot against the helicopter (6 bullets or 1 rocket destroy it, +50)

## Not known

- `keyPressed` is called by both keyDown handlers and defined nowhere in the scripts
- `hell`, started when the helicopter returns, is never assigned by a script
- what `sd1` is, and what sends `things53` to its frame 2
- whether sprite 399 is the sound switch: `soundOn` and `soundOff` are never called, and nothing turns the sound back on at `on`

## Evidence

- placements on root frame 15 (the original's PlaceObject tags): sprite 33 `mc_control`, 446 `helicop`, 453 `bomb`, 455 `bullet_checker_mc`, 408 `health_mc`, 415 `score_mc`, 437 `themask_mc`, 440 `sd1`, 443 `crash`, 449 `explode_mc`, sprite 399 unnamed
- placements in the level sprites 219, 229, 367, 374, 379, 386: `mc_fon` (159, 358), `box1`...`box7` (197), `mask_mc` and `mask_hit_mc` (198), `maskman_mc` (218, 385), `hoterelement` (207) holding `things53` (206)
- `_root.health_mc.nextFrame()` and `_currentframe >= 4` in the bomb's clip action; `score_mc.gotoAndPlay(2)` and `(18)` in the shot checker, `(34)` in the bomb's
- `_root.crash.gotoAndPlay(2)` in `loose`; `_root.lifee -= 1; _root.replay();` in `DefineSprite_443_frame_51_DoAction.onEnterFrame`
- `mc_level.mc.maskman_mc.gotoAndPlay(2)` and `themask_mc.gotoAndStop(508)` in `processGame`
- `mc_level.mc.box<pi>.play()`, `mask_mc.box<pi>.play()` and `mc_hit.mask_hit_mc.box<pi>.play()` in the shot checker
- `bg.gotoAndStop(1 + random(5))` in `DefineSprite_159_frame_1_DoAction_main` and `DefineSprite_358_frame_1_DoAction_main`
- frame labels `on` (1) and `off` (2) of sprite 399; `stopAllSounds()` in its frame-2 script
- the clip-action scripts frame_15/PlaceObject2_33_1, _446_349, _453_353, _455_357 (reference/MANIFEST.json)
- 0.01745329 (pi/180) in the bomb's load handler and in `processGame`'s aim
