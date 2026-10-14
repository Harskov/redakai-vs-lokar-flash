# Contributing to Redakai vs Lokar (Flash)

Pull requests are welcome on `src/` and `docs/`. The maintainer's tooling imports a merged pull request's source at the
next run, rebuilds it with the pinned toolchain and records a match only when the rebuilt code matches the original under
the project's criterion (not pinned yet (the calibration step has not run)); a function that does not match stays as the reference line.

## The toolchain

not pinned yet; criterion `unpinned`. `python3 configure.py` installs it from the pinned release into `tools/` and
`tools/check.py` compares the rebuilt artifact with your own original. No scratch from decomp.me or any other site is
copied here: the work is clean-room from the original file.



## Naming

A name is written only with cited evidence (a string the function references, a named caller, a frame label, a field it
reads); without evidence the systematic name stays (it is better to leave it unnamed than name it wrongly). The symbol map
in `symbols/` carries each name's evidence. Original identifiers kept by the bytecode are names with evidence.

## Readability

`python3 tools/lint_flash-avm1.py <file>` (the contributor copy of the project's lint) refuses decompiler temporaries and
artifacts, pipeline comments, debug leftovers, unexplained `!FAKE` markers and placeholders. Comments say why and what is
uncertain, at most three lines per function; they never narrate the code. One definition per type.

## Pull requests

Small, one subsystem or a handful of functions each; the subject says what changed. The audit workflow refuses any
game-derived file. AI-assisted source is welcome when it meets the criterion and the lint; say so in the pull request.
