# Redakai vs Lokar

[![Audit](https://github.com/Harskov/redakai-vs-lokar-flash/actions/workflows/audit.yml/badge.svg)](https://github.com/Harskov/redakai-vs-lokar-flash/actions/workflows/audit.yml)
[![Code](https://bytematch.dev/Harskov/redakai-vs-lokar-flash.svg?label=Code&measure=matched_code_percent)](https://bytematch.dev/Harskov/redakai-vs-lokar-flash)
[![Functions](https://bytematch.dev/Harskov/redakai-vs-lokar-flash.svg?label=Functions&measure=matched_functions)](https://bytematch.dev/Harskov/redakai-vs-lokar-flash)

A decompilation of Redakai vs Lokar (Adobe Flash, AVM1 (ActionScript 1/2)). It builds the following file:

| File | SHA-1 | Size |
|---|---|---|
| `Redakai vs Lokar.swf` | `1395899485f5b41da5b94ba05401d22ea1810ae0` | 1542563 bytes |

**This repository contains no game assets**: no original file, no extracted asset, no decompiler output and no reference
P-code or assembly. Building it needs your own copy of the game. The source was written function by function, much of it
with AI assistance, and accepted only when the pinned toolchain rebuilt it to match the original; see
[How the source was made](#how-the-source-was-made-and-the-ai-disclosure).

## Building

1. Clone this repository.
2. Put your own copy of the game at `orig/Redakai vs Lokar.swf` (its SHA-1 must be the one above).
3. `python3 configure.py` downloads the pinned toolchain (JPEXS Free Flash Decompiler 26.3.0) into `tools/`, rebuilds from `src/` and runs
   `tools/check.py`, which compares the rebuilt artifact with your original under the project's criterion and prints
   `check: OK` when they agree.

## Progress

**179 of 202 game functions are matched** (5,393 of 10,936 instructions, 49.31 %). 90 of the matched and 107 of all game functions carry a name whose evidence a script checked; so do 9 of 9 types, 137 of 137 members the matched code reaches; 202 functions carry a subsystem label. Every name and its evidence: [docs/NAMES.md](docs/NAMES.md).

| Milestone | Status | Exit judged on |
|---|---|---|
| M1 Contributable | done | public-build.json ok=True; matched outside their unit: 0 |
| M2 Identified | done | name pass closed: True; unlabelled game functions: 0; review pending: 0 |
| M3 Platform boundary | done | 1/1 platform functions matched; PLATFORM.md present |
| M4 Core | current | 12/13 core functions matched; FORMATS.md missing |
| M5 Gameplay | later | 127/146 gameplay functions matched |
| M6 Complete | later | 179/202 game functions matched; check ok=True |
| M7 Documented | done | docs.py check ok=True (2026-10-17T06:09:47Z) |
| M8 Behaviour-verified | later | last behaviour compare ok=True at 2026-10-16T06:36:49Z; coverage: no input (28 matched input handler(s) unexercised) |
| M9 Reverse-engineered | later | names without checked evidence: 0; matches since the last name pass: 58; named types with two layouts: 0 |

The milestones and why they come in this order: [ROADMAP.md](ROADMAP.md).

The same reports are tracked on [ByteMatch](https://bytematch.dev/Harskov/redakai-vs-lokar-flash): the report workflow uploads it on every push (`swf_report`). Its code sizes count P-code instructions, not bytes.

## How the source was made, and the AI disclosure

The source here was written function by function and accepted only when the pinned toolchain rebuilt it to match the
original under the project's criterion (the recompiled P-code must equal the original's listing, both taken with FFDec's AS1/2 deobfuscator on, after a documented normalization (constant-pool resolution, register and jump numbering, one value per push, an obfuscator's two leftover statements)). Much of it was drafted with AI assistance (Claude, and the
batch lane's models); every accepted function was rebuilt and compared by the tooling on the maintainer's machine, and
the commit that adds a function carries a credit line naming who wrote it (`Co-Authored-By: Claude <noreply@anthropic.com>`
for the operator's model, `Assisted-by: <model> (batch)` for the batch lane). A name — of a function, a type, a struct member
or a global — is written only after a script has checked each fact it cites against the code (a string, an SDK prototype, a
library symbol, a checked caller, what the matched code does with a member) and every word of the name against those facts;
otherwise the systematic placeholder stays. [docs/NAMES.md](docs/NAMES.md) lists every name with its evidence, so each one can
be checked again. A function marked `// !FAKE:` matches
through an implausible form and is listed as readability debt in [ROADMAP.md](ROADMAP.md).

## Platform: Adobe Flash (AVM1, ActionScript 1/2)

The game is an SWF whose code runs on the first ActionScript virtual machine. The source under `src/` is ActionScript 1/2 in the layout JPEXS Free Flash Decompiler (FFDec) consumes for its `-importScript` rebuild: one file per script (a frame's `DoAction`, a class's `DoInitAction`, a button's or a clip's actions). A function is accepted when FFDec compiles it to P-code that equals the original's under the project's criterion (the recompiled P-code must equal the original's listing, both taken with FFDec's AS1/2 deobfuscator on, after a documented normalization (constant-pool resolution, register and jump numbering, one value per push, an obfuscator's two leftover statements)); the community has no single convention for Flash, so this project states its own here. The original's listing is taken with FFDec's AS1/2 deobfuscator on (`-config autoDeobfuscate=1`, the same way `tools/check.py` exports both files): where the file was run through an obfuscator (a jump over junk, undefined opcodes, a state-machine dispatcher, decoy constant pools, decoy copies of functions), the reference is the code the player runs, which is what the author wrote; the two `var` statements the obfuscator leaves behind are dropped by the normalizer and are not in the source. This repository contains no SWF, no assets and no P-code: the rebuild needs your own copy of the game. Ruffle plays the rebuilt file; the behaviour checks compare renders of the original and the rebuilt file at the checkpoints listed in `tests/behaviour/checkpoints.json`.


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md): the layout, the toolchain, the naming rule, the readability lint and what the
maintainer's tooling does with a merged pull request.

## Layout

`src/` the source in the layout the toolchain consumes (one file per unit; a function not yet accepted is a reference
line) · `docs/` the architecture, the subsystem pages, the code map and `NAMES.md` (every name and its evidence) · `config/flash-avm1/` the toolchain pin and the
checksum · `symbols/` the symbol map with its evidence · `tools/` the contributor copies of the lint and the check ·
`progress/report.json` the progress report.

## License

The source in this repository is dedicated to the public domain under CC0 1.0 Universal (see LICENSE). The game itself is not
covered: nothing of it is here.
