# Roadmap — Redakai vs Lokar (Flash)

The project serves four purposes — preservation, recompilation, porting and learning — and orders its milestones by what helps other people soonest. Each milestone's exit is a file or a record, not a judgment. Generated from `config/milestones.json` and the match records; never edited by hand.

| # | Milestone | Status | Exit judged on |
|---|---|---|---|
| M1 | Contributable | done | public-build.json ok=True; matched outside their unit: 0 |
| M2 | Identified | current | name pass closed: False; unlabelled game functions: 202; review pending: 0 |
| M3 | Platform boundary | later | 0/0 platform functions matched; PLATFORM.md present |
| M4 | Core | later | 0/0 core functions matched; FORMATS.md missing |
| M5 | Gameplay | later | 0/0 gameplay functions matched |
| M6 | Complete | later | 12/202 game functions matched; check ok=True |
| M7 | Documented | later | docs.py check ok=None (never run) |
| M8 | Behaviour-verified | later | last behaviour compare ok=None at never |

Readability debt: 0 function(s) carry a `// !FAKE:` body and 0 carry a lint finding (see CONTRIBUTING.md); a pull request that replaces one with plain source that still matches is welcome.
