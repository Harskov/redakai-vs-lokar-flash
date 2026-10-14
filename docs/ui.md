# ui

The menus, the buttons and the readouts: the main-timeline frames 12-20, the buttons on them, the level selection and the time readout. The flow between frames is the table in `ARCHITECTURE.md`.

## Functions

- `DefineButton2_124_BUTTONCONDACTION_on_release_main` (not yet matched) — btn1 on the logo frame: zeroes tscore and mscore, plays from frame 15, lvls 1
- `DefineButton2_127_BUTTONCONDACTION_on_release_main` (matched) — button 127 (btn2 on frames 10 logo, 17 comple, 19 gamewin, 20 gameover): opens http://www.jeuxredakai.com/ in a new window
- `DefineButton2_147_BUTTONCONDACTION_on_release_main` (not yet matched) — the play button on frames 11-12: plays from frame 15, lvls 1
- `DefineButton2_147_BUTTONCONDACTION_on_rollOut_main` (not yet matched) — plays the button's `sta` clip from frame 11
- `DefineButton2_147_BUTTONCONDACTION_on_rollOver_main` (not yet matched) — plays the button's `sta` clip from frame 2
- `DefineButton2_148_BUTTONCONDACTION_on_release_main` (matched) — the help button (on frames 11-12): sends the main timeline to its `help` frame (14)
- `DefineButton2_148_BUTTONCONDACTION_on_rollOut_main` (not yet matched) — plays the help button's `hel` clip from frame 11
- `DefineButton2_148_BUTTONCONDACTION_on_rollOver_main` (matched) — the help button's roll-over: plays its `hel` clip from frame 2 (the roll-out plays it from 11)
- `DefineButton2_389_BUTTONCONDACTION_on_release_main` (matched) — button 389 (btn2 on frame 15 game): opens http://www.jeuxredakai.com in a new window
- `DefineButton2_461_BUTTONCONDACTION_on_release_main` (not yet matched) — btn2 on `comple`: tscore = mscore, then gameStart
- `DefineButton2_473_BUTTONCONDACTION_on_release_main` (not yet matched) — btn0 on `gamewin` and `gameover`: zeroes tscore and mscore, the root to frame 10
- `showTime` (matched) — formats the elapsed game time (timeCounter, in ms) into the txtTime readout; called by processGame every frame
- `getTimeString` (not yet matched) — milliseconds as mm:ss with leading zeros
- `frame_12_DoAction_main` (matched) — the main frame (12): holds and sets the starting state lvls 1, scores 0, lifee 5, totascores 0
- `frame_13_DoAction_main` (matched) — the carselection frame (13): stops every sound
- `frame_14_DoAction_main` (matched) — the help frame (14): stops every sound
- `frame_17_DoAction_main` (not yet matched) — `comple`: lvls++, scorecard + 100, the level and total score texts, `gamewin` at lvls 7
- `frame_18_DoAction_main` (not yet matched) — `level selection`: stops, silences, installs the per-frame handler
- `frame_18_DoAction.onEnterFrame` (not yet matched) — each frame: buttons le1 ... le15 up to lvls go to their frame 2 and get their press handler
- `frame_18_DoAction.onRelease` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_2` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_3` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_4` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_5` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_6` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_7` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_8` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_9` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_10` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_11` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_12` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_13` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_14` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_18_DoAction.onRelease_15` (not yet matched) — a level button's press (le1 ... le15 in order): sets lvls to its number and calls gameStart
- `frame_19_DoAction_main` (not yet matched) — `gamewin`: levelscore into txtfinalscore, mscore + " points" into txtscore2
- `frame_20_DoAction_main` (not yet matched) — `gameover`: the same two readouts as gamewin

## Not known

- frame 18 offers 15 level buttons, `mc_level` has six level frames (`level1`...`level6`) and frame 17 ends the game at lvls 7; what levels 7-15 would show is not known

## Evidence

- button placements (the original's PlaceObject tags): 124 `btn1` on frame 10; 127 `btn2` on 10, 17, 19, 20; 147 and 148 on 11-12; 389 `btn2` on 15; 461 `btn2` on 17; 473 `btn0` on 19 and 20
- the string "http://www.jeuxredakai.com/" in `DefineButton2_127_BUTTONCONDACTION_on_release_main` (and without the slash in button 389)
- readouts written by the scripts: txtTime (`showTime`), txtscore and txtlevel (frame 17), txtfinalscore and txtscore2 (frames 19, 20)
