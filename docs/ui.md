# ui

The menus, the buttons and the readouts: the main-timeline frames 12-20, the buttons on them, the level selection and the time readout. The flow between frames is the table in `ARCHITECTURE.md`.

## Functions

- `DefineButton2_124_BUTTONCONDACTION_on_release_main` (matched) — btn1 on the logo frame: zeroes tscore and mscore, plays the game frame (15), lvls 1
- `DefineButton2_127_BUTTONCONDACTION_on_release_main` (matched) — button 127 (btn2 on frames 10 logo, 17 comple, 19 gamewin, 20 gameover): opens http://www.jeuxredakai.com/ in a new window
- `DefineButton2_147_BUTTONCONDACTION_on_release_main` (matched) — the play button on frames 11-12: plays the game frame (15) at lvls 1, leaving tscore and mscore as they are
- `DefineButton2_147_BUTTONCONDACTION_on_rollOut_main` (matched) — the play button's roll-out: plays its sta clip from frame 11
- `DefineButton2_147_BUTTONCONDACTION_on_rollOver_main` (matched) — the play button's roll-over: plays its sta clip from frame 2
- `DefineButton2_148_BUTTONCONDACTION_on_release_main` (matched) — the help button (on frames 11-12): sends the main timeline to its `help` frame (14)
- `DefineButton2_148_BUTTONCONDACTION_on_rollOut_main` (matched) — the help button's roll-out: plays its hel clip from frame 11
- `DefineButton2_148_BUTTONCONDACTION_on_rollOver_main` (matched) — the help button's roll-over: plays its `hel` clip from frame 2 (the roll-out plays it from 11)
- `DefineButton2_389_BUTTONCONDACTION_on_release_main` (matched) — button 389 (btn2 on frame 15 game): opens http://www.jeuxredakai.com in a new window
- `DefineButton2_461_BUTTONCONDACTION_on_release_main` (matched) — btn2 on comple: carries mscore into tscore, then gameStart (frame 17 has already raised lvls)
- `DefineButton2_473_BUTTONCONDACTION_on_release_main` (matched) — btn0 on gamewin and gameover: zeroes tscore and mscore and sends the main timeline to the logo frame (10)
- `showTime` (matched) — formats the elapsed game time (timeCounter, in ms) into the txtTime readout; called by processGame every frame
- `getTimeString` (matched) — a time in milliseconds as mm:ss, each part zero-padded; used by showTime, loose and processGame's finish
- `frame_12_DoAction_main` (matched) — the main frame (12): holds and sets the starting state lvls 1, scores 0, lifee 5, totascores 0
- `frame_13_DoAction_main` (matched) — the carselection frame (13): stops every sound
- `frame_14_DoAction_main` (matched) — the help frame (14): stops every sound
- `frame_17_DoAction_main` (matched) — the comple frame: holds, silences, lvls++, scorecard + 100 into txtlevel, the running total into txtscore and levelscore, gamewin once lvls is 7
- `frame_18_DoAction_main` (matched) — the level selection frame: holds, silences and installs the per-frame handler that unlocks the level buttons
- `frame_18_DoAction.onEnterFrame` (matched) — each frame: buttons le1 ... le15 up to lvls go to their frame 2 and get their press handler
- `frame_18_DoAction.onRelease` (matched) — le1's press: lvls 1 and gameStart
- `frame_18_DoAction.onRelease_2` (matched) — le2's press: lvls 2 and gameStart
- `frame_18_DoAction.onRelease_3` (matched) — le3's press: lvls 3 and gameStart
- `frame_18_DoAction.onRelease_4` (matched) — le4's press: lvls 4 and gameStart
- `frame_18_DoAction.onRelease_5` (matched) — le5's press: lvls 5 and gameStart
- `frame_18_DoAction.onRelease_6` (matched) — le6's press: lvls 6 and gameStart
- `frame_18_DoAction.onRelease_7` (matched) — le7's press: lvls 7 and gameStart
- `frame_18_DoAction.onRelease_8` (matched) — le8's press: lvls 8 and gameStart
- `frame_18_DoAction.onRelease_9` (matched) — le9's press: lvls 9 and gameStart
- `frame_18_DoAction.onRelease_10` (matched) — le10's press: lvls 10 and gameStart
- `frame_18_DoAction.onRelease_11` (matched) — le11's press: lvls 11 and gameStart; never runs: frame 18 places le1 to le10 only
- `frame_18_DoAction.onRelease_12` (matched) — le12's press: lvls 12 and gameStart; never runs: frame 18 places le1 to le10 only
- `frame_18_DoAction.onRelease_13` (matched) — le13's press: lvls 13 and gameStart; never runs: frame 18 places le1 to le10 only
- `frame_18_DoAction.onRelease_14` (matched) — le14's press: lvls 14 and gameStart; never runs: frame 18 places le1 to le10 only
- `frame_18_DoAction.onRelease_15` (matched) — le15's press: lvls 15 and gameStart; never runs: frame 18 places le1 to le10 only
- `frame_19_DoAction_main` (matched) — the gamewin frame: holds, silences, levelscore into txtfinalscore and mscore + " points" into txtscore2
- `frame_20_DoAction_main` (matched) — the gameover frame: the same as gamewin, levelscore and mscore + " points" into the two readouts

## Not known

- frame 18 offers 15 level buttons, `mc_level` has six level frames (`level1`...`level6`) and frame 17 ends the game at lvls 7; what levels 7-15 would show is not known

## Evidence

- button placements (the original's PlaceObject tags): 124 `btn1` on frame 10; 127 `btn2` on 10, 17, 19, 20; 147 and 148 on 11-12; 389 `btn2` on 15; 461 `btn2` on 17; 473 `btn0` on 19 and 20
- the string "http://www.jeuxredakai.com/" in `DefineButton2_127_BUTTONCONDACTION_on_release_main` (and without the slash in button 389)
- readouts written by the scripts: txtTime (`showTime`), txtscore and txtlevel (frame 17), txtfinalscore and txtscore2 (frames 19, 20)
