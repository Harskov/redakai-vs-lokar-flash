# gameplay/timeline-game

The scripts on frame 15 `game`'s placed clips: the controller `mc_control`, the helicopter, the bomb and the shot checker, and the two helpers frame 15 defines. The loop they call is in `ARCHITECTURE.md`.

## Functions

- `firebomb` (not yet matched) — if the helicopter is active: the bomb under it (offset +34.6 y, -10.1 x), frame 1, opaque, a drop started (dropbomb)
- `setBright` (not yet matched) — gives a clip a ColorMatrixFilter that adds newVal to red, green and blue
- `frame_15_PlaceObject2_33_1_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (not yet matched) — mc_control each frame: _parent.processGame(), and accSnd once per press of the up key
- `frame_15_PlaceObject2_33_1_CLIPACTIONRECORD_onClipEvent_keyDown_main` (not yet matched) — _parent.keyPressed() then updateAfterEvent()
- `frame_15_PlaceObject2_33_1_CLIPACTIONRECORD_onClipEvent_keyDown__2_main` (not yet matched) — the same as the first keyDown handler
- `frame_15_PlaceObject2_33_1_CLIPACTIONRECORD_onClipEvent_load_main` (not yet matched) — _parent.initLevel()
- `frame_15_PlaceObject2_446_349_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (not yet matched) — the helicopter: 4 px left a frame while active, off past x -270; destroyed, it falls 12 px a frame at brightness -150 and comes back at (1006.4, 58.4), firing again
- `frame_15_PlaceObject2_453_353_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (not yet matched) — the bomb's flight, 22 px a frame along `degrees`: a hit on the bike costs 50 mscore and one health frame (loose at frame 4); the ground mask or y > 500 ends it
- `frame_15_PlaceObject2_453_353_CLIPACTIONRECORD_onClipEvent_load_main` (not yet matched) — the bomb's heading: rotation 220, `degrees` in radians
- `frame_15_PlaceObject2_455_357_CLIPACTIONRECORD_onClipEvent_enterFrame_main` (not yet matched) — the shot checker: bullets against boxes 1-7 (+10), any shot against the helicopter (6 bullets or 1 rocket destroy it, +50)

## Not known

- `keyPressed` is called by both keyDown handlers and defined nowhere in the scripts
- `hell`, started when the helicopter returns, is never assigned by a script

## Evidence

- placements on root frame 15 (the original's PlaceObject tags): sprite 33 `mc_control`, 446 `helicop`, 453 `bomb`, 455 `bullet_checker_mc`
- the clip-action scripts frame_15/PlaceObject2_33_1, _446_349, _453_353, _455_357 (reference/MANIFEST.json)
- 0.01745329 (pi/180) in the bomb's load handler and in `processGame`'s aim
