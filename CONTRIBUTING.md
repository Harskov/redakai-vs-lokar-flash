# Contributing to Redakai vs Lokar

Pull requests are welcome on `src/`. The maintainer's tooling imports a merged pull request's source at the next run,
rebuilds it with the pinned toolchain and records a match only when the rebuilt code matches the original under the
project's criterion (the recompiled P-code must equal the original's listing, both taken with FFDec's AS1/2 deobfuscator on, after a documented normalization (constant-pool resolution, register and jump numbering, one value per push, an obfuscator's two leftover statements)); a function that does not match stays as the reference line. Everything outside
`src/` (the documentation, the symbol map, shared headers) is generated from the maintainer's workbench, so a correction
there is welcome as an issue and is carried over by hand.

## The toolchain

JPEXS Free Flash Decompiler 26.3.0; criterion `pcode-normalized`. `python3 configure.py` installs it from the pinned release into `tools/` and
`tools/check.py` compares the rebuilt artifact with your own original. No scratch from decomp.me or any other site is
copied here: the work is clean-room from the original file.

### Flash specifics

- `tools/check.py` exports the P-code of both files with the pinned FFDec and compares every script's functions under the criterion; `tools/lint_as.py` is the readability lint the maintainer's tooling applies before accepting a function (`python3 tools/lint_as.py src/...`).
- A unit file's `// @reference <fn>` line marks a function not yet written; replace the line with the function and keep every other line. The top-level stream of a script is itself a function (`<unit>_main`).
- Write what the P-code says: FFDec's compiler emits one `Push` per value, `DefineFunction` for a function without parameters, `0.0` for a Double zero; the normalizer absorbs push merging, register and label numbering and the two `var` lines an obfuscator leaves at the top of a stream (control-character names), nothing else. `tools/check.py` exports both files with FFDec's AS1/2 deobfuscator on, as the maintainer's tooling does.
- Names come from evidence only (a string literal, a linkage name, a frame label, a field); a systematic `fn_<unit>_<n>` stays until evidence exists.


## Naming

A name is written only with cited evidence (a string the function references, a named caller, a frame label, a field it
reads); without evidence the systematic name stays (it is better to leave it unnamed than name it wrongly). The symbol map
in `symbols/` carries each name's evidence. Original identifiers kept by the bytecode are names with evidence.

## Readability

`python3 tools/lint_as.py <file>` (the contributor copy of the project's lint) refuses decompiler temporaries and
artifacts, pipeline comments, debug leftovers, unexplained `!FAKE` markers and placeholders. Comments say why and what is
uncertain, at most three lines per function; they never narrate the code. One definition per type.

## Pull requests

Small, one subsystem or a handful of functions each; the subject says what changed. The audit workflow refuses any
game-derived file. AI-assisted source is welcome when it meets the criterion and the lint; say so in the pull request.
