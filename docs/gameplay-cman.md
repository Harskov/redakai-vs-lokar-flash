# gameplay/cman

The rider (sprite 95, export `lib_man`, linked to CMan by `lib_man_main`): a MovieClip subclass whose state machine plays the lean animations by frame label as the arrow keys are held and released. States, from `endMove`'s transitions: 0 upright (`stay`), 1 leaning left, 2 held left (`left`), 3 returning from left, 4 leaning right, 5 held right (`right`), 6 returning from right.

## Functions

- `Packages_CMan_main` (matched) — the CMan class script: registers the rider class (a MovieClip subclass) with LEFT_BUTTON 37, RIGHT_BUTTON 39, ANIM_FRAMES 7 and puts its methods on the prototype
- `CMan` (matched) — the rider's constructor: super(), stopFlag false, state 0 (upright)
- `CMan.stopAnim` (matched) — freezes the rider's lean state machine (stopFlag set); called by processGame at the finish, pauseGame and loose
- `CMan.stopMCAnim` (matched) — stops the rider's inner animation clip mc; called by processGame at the finish and by loose
- `CMan.startAnim` (matched) — lets the lean state machine run again (stopFlag cleared); called by resume
- `CMan.onEnterFrame` (matched) — each frame unless stopped: a held left or right arrow calls toLeft or toRight; with neither held, a left lean (1, 2) or right lean (4, 5) starts its return
- `CMan.toLeft` (matched) — the left key held: from upright starts the left lean (1); from the left return (3) restarts the lean at the mirrored frame; from a right lean starts the right return (6)
- `CMan.toRight` (matched) — the right key held: the mirror of toLeft (lean 4, mirrored restart from 6, left return 3 from a left lean)
- `CMan.fromLeft` (matched) — starts the return from a left lean (state 3), at the mirrored frame when the lean was still playing (state 1)
- `CMan.fromRight` (matched) — starts the return from a right lean (state 6), at the mirrored frame when the lean was still playing (state 4)
- `CMan.endMove` (matched) — an animation's end: lean 1 holds as 2 on left, lean 4 as 5 on right, returns 3 and 6 go to 0 on stay; no script calls it, so states 2 and 5 are not reached from the code
- `lib_man_main` (matched) — links the exported symbol lib_man (sprite 95, the rider) to CMan

## Not known

- none of the file's 95 scripts calls `endMove`, so states 2 and 5 are never entered from the code
- the file has 9 sprite frame labels: `stay` (95), `on`/`off` (399), `level1`...`level6` (387) (DOSSIER.md's census and the original's FrameLabel tags). `toLeft`, `left`, `fromLeft`, `toRight`, `right` and `fromRight` are none of them, so those `gotoAndStop` calls find no frame, which AVM1 ignores. That leaves the lean graphics unexplained; S13's runtime check can show what the rider does.

## Evidence

- `Object.registerClass("lib_man", CMan)` (`lib_man_main`)
- frame label `stay` on sprite 95's frame 1 (the original)
- `Key.isDown(CMan.LEFT_BUTTON)` and `RIGHT_BUTTON` in `processGame` and `CMan.onEnterFrame`
