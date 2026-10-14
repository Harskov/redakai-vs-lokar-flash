# Redakai vs Lokar (Flash)

[![Audit](https://github.com/Harskov/redakai-vs-lokar-flash/actions/workflows/audit.yml/badge.svg)](https://github.com/Harskov/redakai-vs-lokar-flash/actions/workflows/audit.yml)

A decompilation of Redakai vs Lokar (Flash) (Adobe Flash, AVM1 (ActionScript 1/2)) for preservation, recompilation, porting and study. **This repository contains
no game assets**: no original file, no extracted asset, no decompiler output and no reference P-code or assembly. Building
it needs your own copy of the game (see Building).

## How the source was made, and the AI disclosure

The source here was written function by function and accepted only when the pinned toolchain rebuilt it to match the
original under the project's criterion (not pinned yet (the calibration step has not run)). Much of it was drafted with AI assistance (Claude, and the
batch lane's models); every accepted function was rebuilt and compared by the tooling on the maintainer's machine, and
the commit that adds a function carries a credit line naming who wrote it (`Co-Authored-By: Claude <noreply@anthropic.com>`
for the operator's model, `Assisted-by: <model> (batch)` for the batch lane). Names are given only with cited evidence (a
string, a caller, a frame label, a field); otherwise the systematic placeholder stays. A function marked `// !FAKE:` matches
through an implausible form and is listed as readability debt in [ROADMAP.md](ROADMAP.md).



## Supported version

| File | SHA-1 | Size |
|---|---|---|
| `Redakai vs Lokar.swf` | `1395899485f5b41da5b94ba05401d22ea1810ae0` | 1542563 bytes |

## Progress

**0 of 0 game functions are matched** (0 of 0 instructions, 0.0 %). 0 functions carry a name backed by evidence; 0 carry a subsystem label.

| Milestone | Status | Exit judged on |
|---|---|---|
| M1 Contributable | current | public-build.json ok=None; matched outside their unit: 0 |
| M2 Identified | later | name pass closed: False; unlabelled game functions: 0; review pending: 0 |
| M3 Platform boundary | later | 0/0 platform functions matched; PLATFORM.md missing |
| M4 Core | later | 0/0 core functions matched; FORMATS.md missing |
| M5 Gameplay | later | 0/0 gameplay functions matched |
| M6 Complete | later | 0/0 game functions matched; check ok=None |
| M7 Documented | later | docs.py check ok=None (never run) |
| M8 Behaviour-verified | later | last behaviour compare ok=None at never |

The milestones and why they come in this order: [ROADMAP.md](ROADMAP.md).

## Building

1. Clone this repository.
2. Put your own copy of the game at `orig/Redakai vs Lokar.swf` (its SHA-1 must be the one above).
3. `python3 configure.py` downloads the pinned toolchain (not pinned yet) into `tools/`, rebuilds from `src/` and runs
   `tools/check.py`, which compares the rebuilt artifact with your original under the project's criterion.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md): the layout, the toolchain, the naming rule, the readability lint and what the
maintainer's tooling does with a merged pull request.

## Layout

`src/` the source in the layout the toolchain consumes (one file per unit; a function not yet accepted is a reference
line) · `docs/` the architecture, the subsystem pages and the code map · `config/flash-avm1/` the toolchain pin and the
checksum · `symbols/` the symbol map with its evidence · `tools/` the contributor copies of the lint and the check ·
`progress/report.json` the progress report.

## License

MIT for the source in this repository (see LICENSE). The game itself is not covered: nothing of it is here.
