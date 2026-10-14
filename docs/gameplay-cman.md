# gameplay/cman

The rider (sprite 95, export `lib_man`, linked to CMan by `lib_man_main`): a MovieClip subclass whose state machine plays the lean animations by frame label as the arrow keys are held and released. States, from `endMove`'s transitions: 0 upright (`stay`), 1 leaning left, 2 held left (`left`), 3 returning from left, 4 leaning right, 5 held right (`right`), 6 returning from right.

## Functions

- `Packages_CMan_main` (not yet matched) — the class definition script, with LEFT_BUTTON 37, RIGHT_BUTTON 39, ANIM_FRAMES 7
- `CMan` (not yet matched) — the constructor: super(), stopFlag false, state 0
- `CMan.stopAnim` (not yet matched) — sets stopFlag, freezing the state machine
- `CMan.stopMCAnim` (not yet matched) — stops the inner clip mc
- `CMan.startAnim` (not yet matched) — clears stopFlag
- `CMan.onEnterFrame` (not yet matched) — left or right key held: toLeft / toRight; otherwise a lean returns
- `CMan.toLeft` (not yet matched) — starts the left lean, or reverses a return from the right at the mirrored frame
- `CMan.toRight` (not yet matched) — the mirror of toLeft
- `CMan.fromLeft` (not yet matched) — starts the return from a left lean
- `CMan.fromRight` (not yet matched) — starts the return from a right lean
- `CMan.endMove` (not yet matched) — an animation's end: 1 to 2, 3 to 0, 4 to 5, 6 to 0
- `lib_man_main` (matched) — links the exported symbol lib_man (sprite 95, the rider) to CMan

## Not known

- none of the file's 95 scripts calls `endMove`, so states 2 and 5 are never entered from the code
- the file has 9 sprite frame labels: `stay` (95), `on`/`off` (399), `level1`...`level6` (387) (DOSSIER.md's census and the original's FrameLabel tags). `toLeft`, `left`, `fromLeft`, `toRight`, `right` and `fromRight` are none of them, so those `gotoAndStop` calls find no frame, which AVM1 ignores. That leaves the lean graphics unexplained; S13's runtime check can show what the rider does.

## Evidence

- `Object.registerClass("lib_man", CMan)` (`lib_man_main`)
- frame label `stay` on sprite 95's frame 1 (the original)
- `Key.isDown(CMan.LEFT_BUTTON)` and `RIGHT_BUTTON` in `processGame` and `CMan.onEnterFrame`
