# core

The game's control functions: the init action of sprite 150 (`DoInitAction`, frame 11) and the preloader on frame 1. They write `gameState` and move the main timeline between `main`, `reset`, `game` and `comple`. The frame-by-frame flow and the main loop are in `ARCHITECTURE.md`.

## Functions

- `DoInitAction_main` (not yet matched) — declares the globals and their first values: stopSoundFlag false, zastSoundFlag true, life 10, highQuality true, bikeSync/engine/objCamera/back1/back2 null
- `gameStart` (not yet matched) — a new run: scores, timeCounter and stargeted 0, life 10, the in-game music (zastSoundFlag false), level 0, then nextLevel
- `nextLevel` (not yet matched) — level++ and through `reset` back to `game`; at level 10 it calls newGame instead
- `replay` (matched) — restarts the current level: clears stargeted and steps the timeline through reset back to game; called by the crash clip
- `newGame` (not yet matched) — back to the `main` frame with the other music loop (zastSoundFlag true)
- `initLevel` (not yet matched) — builds one attempt at the current level: the level frame, the minimap, the physics objects, gameState 0
- `processGame` (not yet matched) — the per-frame step while gameState is 0: time, input, physics, camera, shots, helicopter, finish line, crash test
- `resume` (not yet matched) — from pause: the music, the message cleared, the rider animation on, gameState 0
- `pauseGame` (not yet matched) — the `pause` message, the music and the rider animation stopped, gameState 4
- `clearStuff` (not yet matched) — removes every shot listed in bulletArray, hides the bomb, resets the helicopter and both brightnesses
- `loose` (not yet matched) — a lost attempt: clearStuff, the fail sound, the message clip, life--, the jeep parts' crash frames, the crash clip, gameState 1
- `frame_1_DoAction_main` (not yet matched) — the preloader frame: the bar at width 0, then its handler
- `frame_1_DoAction.onEnterFrame` (not yet matched) — the bar's width is the loaded percent x 5; at 100% the handler deletes itself and plays from frame 10

## Not known

- `loose` decrements `life`; the crash clip decrements `lifee`, and only `lifee` is tested (frame 15). No script reads `life` otherwise.
- `processGame` calls `addLevelScores`, which no script defines.

## Evidence

- `gameState` writers in the reference listing: `initLevel` and `resume` (0), `loose` (1), `processGame` (2, 3), `pauseGame` (4)
- the frame labels `main`, `reset`, `game`, `comple` (DOSSIER.md) named by `newGame`, `nextLevel`, `replay`, `processGame`
- `mc_control` (sprite 33, root frame 15) calls `initLevel` on load and `processGame` on enterFrame (gameplay-timeline-game.md)
- DoInitAction tag 304 belongs to sprite 150 and sits on root frame 11 (the original's tag order)
