# Globals registry

Every `_root.<name>` and `_global.<name>` variable the accepted source writes, with its type, writers, readers and the evidence. `lint_as.py` reads the names in backticks here for the `global-write` advisory; S8 keeps the table current.

| Variable | Type | Writers | Readers | Evidence |
|---|---|---|---|---|
| `lvls` | integer (`1`) | frame_12_DoAction_main (`var lvls = 1`); also, not yet accepted: frame_17_DoAction_main (`lvls++`), the level buttons on frame 18 and buttons 124 and 147 (`_root.lvls = 1` … `4`) | frame_15_DoAction_main, frame_17_DoAction_main | original identifier; frame 12 is the main timeline's `main` frame, so the variable lives on `_root` |
| `scores` | Number (`0.0`) | frame_12_DoAction_main (`var scores = 0.0`); also, not yet accepted: gameStart, loose (`_root.scores = 0`) | processGame, loose | original identifier; the starting score |
| `lifee` | integer (`5`) | frame_12_DoAction_main (`var lifee = 5`); also, not yet accepted: frame_10_DoAction_main, DefineSprite_443_frame_51_DoAction.onEnterFrame (`_root.lifee -= 1`) | frame_15_DoAction_main (`lifee == 0`) | original identifier; the life count: the crash clip takes one, frame 15 tests it against 0 |
| `totascores` | Number (`0.0`) | frame_12_DoAction_main (`var totascores = 0.0`) | none in the scripts | original identifier; no reader found, probably a text field's variable on the stage (unverified) |
| `stargeted` | Number (`0.0`; `5` in processGame) | replay (`stargeted = 0.0`); also, not yet accepted: gameStart, nextLevel, newGame, processGame | processGame (`stargeted >= 3`) | original identifier; replay's `gotoAndStop("reset")` / `("game")` name main-timeline frame labels, so the DoInitAction functions run with `this` as `_root` |
| `txtTime` | String | showTime (`txtTime = getTimeString(timeCounter)`) | none in the scripts | original identifier; the elapsed-time readout, probably a text field's variable on the stage (unverified) |
