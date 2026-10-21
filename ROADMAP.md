# Roadmap — Redakai vs Lokar

The project serves four purposes — preservation, recompilation, porting and learning — and orders its milestones by what helps other people soonest. Each milestone's exit is a file or a record, not a judgment. Generated from `config/milestones.json` and the match records; never edited by hand.

| # | Milestone | Status | Exit judged on |
|---|---|---|---|
| M1 | Contributable | done | public-build.json ok=True; matched outside their unit: 0 |
| M2 | Identified | done | name pass closed: True; unlabelled game functions: 0; review pending: 0 |
| M3 | Platform boundary | done | 1/1 platform functions matched; PLATFORM.md present |
| M4 | Core | done | 13/13 core functions matched; FORMATS.md present |
| M5 | Gameplay | done | 146/146 gameplay functions matched |
| M6 | Complete | done | 202/202 game functions matched; check ok=True |
| M7 | Documented | done | docs.py check ok=True (2026-10-21T07:35:37Z) |
| M8 | Behaviour-verified | done | last behaviour compare ok=True at 2026-10-21T07:34:28Z; coverage: scripted input, 25/30 matched input handler(s) run, unexercised: frame_18_DoAction.onRelease_11, frame_18_DoAction.onRelease_12, frame_18_DoAction.onRelease_13, frame_18_DoAction.onRelease_14, frame_18_DoAction.onRelease_15 |
| M9 | Reverse-engineered | done | names without checked evidence: 0; matches since the last name pass: 0; named types with two layouts: 0 |

Readability debt: 11 function(s) carry a `// !FAKE:` body and 0 carry a lint finding (see CONTRIBUTING.md); a pull request that replaces one with plain source that still matches is welcome.

Reverse-engineering debt: 0 name(s) wait for a fact a script can check (M9); [docs/NAMES.md](docs/NAMES.md) lists every name with its evidence.
