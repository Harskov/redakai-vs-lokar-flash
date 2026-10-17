#!/usr/bin/env python3
"""lint_as.py — the readability lint for ActionScript 2 source (design Appendix C §C.6; a verifier file).

    python3 platforms/flash-avm1/scripts/lint_as.py --repo R [FILE ...] [--json]

Without files: every src/**/*.as. Errors: register-name (`_locN_`, `__regN`, `_tempN` in accepted source), ffdec-artifact
(`§§`, `// unresolved`, `loopN:` labels and `addrN` targets, a bare `undefined;` statement, `ÿ`-escaped or `\\xNN` identifiers),
process-comment (a comment naming a run, a score, a tool, a friction id, a K-file or a round), trace-leftover (a `trace(` the
draft under reference/as did not have), fake-body-unexplained (`!FAKE` without a reason), placeholder-left (`TODO`, `FIXME`,
`XXX`, `???`). Advisories: goto-emulation (a labelled loop with a multi-level break or continue the draft did not have),
magic-number (a numeric literal other than 0, 1, -1, 2 with no named constant or comment within three lines), dynamic-ref
(`eval(`, `this["…" + …]`, `_root["…"]`), global-write (an assignment to `_root.x`, `_global.x` or `eval("_root").x`, and in a
script that runs on the main timeline — src/frame_<n>/DoAction*.as, src/DoInitAction*.as — a bare write no enclosing function
declares and a `var` outside every function, not listed in docs/globals.md), globals-stale (a whole-tree run with the ledger: a
docs/globals.md row whose "not yet accepted" clause names a matched function),
long-function (> 150 lines), nested-depth (> 5), fake-body (the marker with its reason). Reference lines (`// @reference`) and
body markers are not findings. Prints `path:line: rule: text`; the JSON line carries {findings: [{path, line, rule, level, text}],
errors, readability_debt}. Writes nothing. Exit 0 clean, 1 error findings, 2 usage.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import flash_common as C  # noqa: E402
except ImportError:            # the contributor copy under a public repository's tools/: no reference exports, no ledger
    class C:  # noqa: N801
        @staticmethod
        def record(repo, fn):
            return None

        @staticmethod
        def ref_as_text(repo, script):
            return None

        @staticmethod
        def add_repo_args(ap):
            ap.add_argument("--target", metavar="SLUG", help="(the pack's registry; not available in a contributor copy)")
            ap.add_argument("--repo", metavar="PATH", help="the repository (default: the folder above tools/)")

        @staticmethod
        def repo_of(a, default=None):
            if a.target:
                print("--target needs the pack's registry; a contributor copy takes --repo <path> or runs from tools/", file=sys.stderr)
                sys.exit(2)
            return Path(a.repo).resolve() if a.repo else Path(default).resolve()

REGISTER = re.compile(r"\b(_loc\d+_|__reg\d+|_temp_?\d+)\b")
ARTIFACT = re.compile(r"§§|//\s*unresolved|^\s*loop\d+:|\baddr\d+\b|^\s*undefined;\s*$|\\x[0-9a-fA-F]{2}|ÿ|\(not compilable\)|^\s*§")
# a match percentage outside the word boundaries: `\b` after `%` needs a word character, so `97.5%` never matched (remediation
# 2026-10-17-remediation-34, flash-batch-qa-8); a game's own percentage (`a 50% chance`) is no narration
PROCESS = re.compile(r"\b(run \d{4}-\d{2}-\d{2}|score:? \d+|F-\d+\b|K[1-9]-|round [A-Z]-?\d|FFDec|ffdec|normalizer|attempt-\d|ledger|batch|campaign)\b"
                     r"|\bmatch\w*\s+(?:at\s+)?\d{1,3}(?:\.\d+)?\s?%|\b\d{1,3}(?:\.\d+)?\s?%\s+match", re.I)
PLACEHOLDER = re.compile(r"\b(TODO|FIXME|XXX)\b|\?\?\?")
FAKE = re.compile(r"!FAKE(\s*:\s*(\S.*))?")
DYNAMIC = re.compile(r"\beval\s*\(|\bthis\s*\[\s*\"|_root\s*\[\s*\"|_global\s*\[\s*\"")
GLOBAL_WRITE = re.compile(r"\b(_root|_global)\.([A-Za-z_$][\w$]*)\s*(=(?!=)|\+=|-=|\*=|/=|\+\+|--)")
# the same write through `eval("_root")` (cookbook C8's spelling, which keeps the original DefineFunction), read before the
# strings are emptied (redakai run 2026-10-17-034 F-1: clearStuff and processGame wrote 11 globals this way, none advised)
EVAL_WRITE = re.compile(r"\beval\s*\(\s*([\"'])(_root|_global)\1\s*\)\s*\.\s*([A-Za-z_$][\w$]*)\s*(=(?!=)|\+=|-=|\*=|/=|\+\+|--)")
# a bare write: an identifier that is no member, assigned or stepped; in a script that runs on the main timeline it lands on _root
BARE_WRITE = re.compile(r"(?<![\w$.])([A-Za-z_$][\w$]*)\s*(?:=(?!=)|\+=|-=|\*=|/=|%=|\+\+|--)|(?:\+\+|--)\s*([A-Za-z_$][\w$]*)(?![\w$.(\[])")
VAR_DECL = re.compile(r"\bvar\s+([A-Za-z_$][\w$]*)")
FUNCTION = re.compile(r"\bfunction\b\s*(?:[A-Za-z_$][\w$]*)?\s*\(([^)]*)\)")
AS_WORDS = {"var", "this", "super", "arguments", "true", "false", "null", "undefined", "new", "return", "typeof", "delete", "in",
            "instanceof", "void", "function", "if", "else", "for", "while", "do", "switch", "case", "default", "break", "continue",
            "with", "try", "catch", "finally", "throw", "_root", "_global", "_parent"}
# a timeline's own event handlers: installing one is no game state (redakai's frame 18 installs fifteen)
CLIP_EVENTS = {"onEnterFrame", "onLoad", "onUnload", "onData", "onPress", "onRelease", "onReleaseOutside", "onRollOver",
               "onRollOut", "onDragOver", "onDragOut", "onKeyDown", "onKeyUp", "onMouseDown", "onMouseUp", "onMouseMove",
               "onSetFocus", "onKillFocus"}
# the scripts that run with `this` as _root: the main timeline's frames and the root DoInitAction (its functions name the main
# timeline's frame labels; redakai's docs/globals.md): src/frame_<n>/DoAction*.as, src/DoInitAction*.as
ROOT_SCOPE = re.compile(r"^(?:frame_\d+/DoAction[^/]*|DoInitAction[^/]*)\.as$")
NUMBER = re.compile(r"(?<![\w.$])-?\d+(\.\d+)?(?![\w.])")
LABELLED_LOOP = re.compile(r"^\s*[A-Za-z_$][\w$]*\s*:\s*(for|while|do)\b")
MULTI_BREAK = re.compile(r"\b(break|continue)\s+[A-Za-z_$][\w$]*\s*;")
COMMENT = re.compile(r"//(.*)$|/\*(.*?)\*/")
REFERENCE = re.compile(r"^\s*//\s*@reference\s|/\*\s*@reference\s")


def strip_strings(line):
    return re.sub(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'', '""', line)


STRING_AT = re.compile(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'')


def code_and_comments(lines):
    """[(code, comment text)] per line: the code with its string literals emptied and its comments out, and the text of every
    comment on the line — a `//` outside a string, each `/* */` part, and the inner lines of a block comment that spans
    several (remediation 2026-10-17-remediation-34, flash-batch-qa-9: a URL's `//` was read as a comment, and a block
    comment's second line was read as code)."""
    out, in_block = [], False
    for raw in lines:
        code, com, i, n = [], [], 0, len(raw)
        while i < n:
            if in_block:
                j = raw.find("*/", i)
                com.append(raw[i:] if j < 0 else raw[i:j])
                i, in_block = (n, True) if j < 0 else (j + 2, False)
                continue
            if raw[i] in "\"'":
                m = STRING_AT.match(raw, i)
                code.append('""' if m else raw[i:])
                i = m.end() if m else n
                continue
            if raw.startswith("//", i):
                com.append(raw[i + 2:])
                break
            if raw.startswith("/*", i):
                in_block, i = True, i + 2
                continue
            code.append(raw[i])
            i += 1
        out.append(("".join(code), " ".join(c for c in com if c.strip())))
    return out


def draft_text(repo, path):
    """The FFDec draft of the unit this file belongs to (reference/as/scripts/<script>.as), or None."""
    try:
        rel = Path(path).resolve().relative_to((repo / "src").resolve())
    except ValueError:
        # an attempt file: wip/<fn>/attempt-N.as -> the function's script
        m = re.search(r"wip/([^/]+)/", str(path))
        if m:
            rec = C.record(repo, m.group(1))
            if rec:
                return C.ref_as_text(repo, (rec.get("pack") or {}).get("script") or "")
        return None
    return C.ref_as_text(repo, str(rel)[:-3])


def script_rel(repo, path):
    """The file's path under src/ ('frame_15/DoAction.as'), an attempt file's by its function's script, or None."""
    try:
        return str(Path(path).resolve().relative_to((repo / "src").resolve())).replace("\\", "/")
    except ValueError:
        m = re.search(r"wip/([^/]+)/", str(path))
        rec = C.record(repo, m.group(1)) if m else None
        script = (rec.get("pack") or {}).get("script") if rec else None
        return f"{script}.as" if script else None


def scopes(code_lines):
    """[(first line, last line, names)] per function: its parameters and every `var` inside it (hoisted, so a write before
    the declaration is the function's own too; an inner function's vars are counted for the outer as well)."""
    frames, stack, pending, depth = [], [], None, 0
    for i, code in enumerate(code_lines, 1):
        fm = FUNCTION.search(code)
        if fm:
            pending = {p.strip() for p in fm.group(1).split(",") if p.strip()}
        for ch in code:
            if ch == "{":
                if pending is not None:
                    stack.append([i, None, set(pending), depth])
                    pending = None
                depth += 1
            elif ch == "}":
                depth -= 1
                if stack and stack[-1][3] == depth:
                    f = stack.pop()
                    f[1] = i
                    frames.append(f)
    for f in stack:
        f[1] = len(code_lines)
        frames.append(f)
    for f in frames:
        for code in code_lines[f[0] - 1:f[1]]:
            f[2].update(VAR_DECL.findall(code))
    return [(a, b, names) for a, b, names, _d in frames]


def root_writes(code_lines):
    """{line: [names]} of the main-timeline variables a root-scope script writes: a bare write no enclosing function declares,
    and a `var` outside every function."""
    frames = scopes(code_lines)
    out = {}
    for i, code in enumerate(code_lines, 1):
        inside = [names for a, b, names in frames if a <= i <= b]
        declared = set().union(*inside) if inside else set()
        found = []
        if not inside:
            found += VAR_DECL.findall(code)
        for m in BARE_WRITE.finditer(code):
            n = m.group(1) or m.group(2)
            pre = code[:m.start()].rstrip()
            if n in AS_WORDS or n in CLIP_EVENTS or REGISTER.match(n) or n in declared or (pre.endswith("var") and inside):
                continue
            found.append(n)
        if found:
            out[i] = list(dict.fromkeys(found))
    return out


def globals_stale(repo):
    """docs/globals.md rows whose "not yet accepted" clause names a function the ledger has matched: [(line, [names])]. Workbench
    only (a contributor copy has no ledger); redakai run 2026-10-17-034 F-2: 14 rows went stale with no signal."""
    p = repo / "docs" / "globals.md"
    led = getattr(C, "ledger", None)
    if not p.is_file() or led is None:
        return []
    matched = {r.get("name") for r in led(repo) if r.get("status") == "matched"}
    out = []
    for i, line in enumerate(p.read_text(encoding="utf-8").split("\n"), 1):
        for clause in re.findall(r"not yet accepted:([^|]*)", line):
            plain = re.sub(r"`[^`]*`", "", clause)
            names = [n for n in re.findall(r"[A-Za-z_$][\w$]*", plain) if n in matched]
            if names:
                out.append((i, list(dict.fromkeys(names))))
    return out


def globals_known(repo):
    p = repo / "docs" / "globals.md"
    if not p.is_file():
        return set()
    return set(re.findall(r"`(?:_root|_global)\.([A-Za-z_$][\w$]*)`", p.read_text(encoding="utf-8")))


def lint_file(repo, path, known_globals):
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    draft = draft_text(repo, path) or ""
    draft_traces = draft.count("trace(")
    draft_labelled = bool(LABELLED_LOOP.search(draft)) or bool(MULTI_BREAK.search(draft))
    out = []

    def add(i, rule, level, t):
        out.append({"path": str(path), "line": i, "rule": rule, "level": level, "text": t.strip()[:100]})
    traces = 0
    depth = 0
    fn_start = None
    rel = script_rel(repo, path)
    cc = code_and_comments(lines)
    bare = root_writes([("" if REFERENCE.search(r) else cc[k][0]) for k, r in enumerate(lines)]) \
        if rel and ROOT_SCOPE.match(rel) else {}
    for i, raw in enumerate(lines, 1):
        if REFERENCE.search(raw):
            continue
        code, ctext = cc[i - 1]
        if REGISTER.search(code):
            add(i, "register-name", "error", raw)
        if ARTIFACT.search(raw):
            add(i, "ffdec-artifact", "error", raw)
        if ctext and PROCESS.search(ctext):
            add(i, "process-comment", "error", raw)
        if "trace(" in code:
            traces += 1
            if traces > draft_traces:
                add(i, "trace-leftover", "error", raw)
        m = FAKE.search(raw)
        if m:
            if m.group(2):
                add(i, "fake-body", "advisory", raw)
            else:
                add(i, "fake-body-unexplained", "error", raw)
        if PLACEHOLDER.search(ctext) or PLACEHOLDER.search(code):
            add(i, "placeholder-left", "error", raw)
        if DYNAMIC.search(code):
            add(i, "dynamic-ref", "advisory", raw)
        written = [m.group(2) for m in GLOBAL_WRITE.finditer(code)] + [m.group(3) for m in EVAL_WRITE.finditer(COMMENT.sub("", raw))] \
            + bare.get(i, [])
        if any(n not in known_globals for n in written):
            add(i, "global-write", "advisory", raw)
        if LABELLED_LOOP.search(code) or MULTI_BREAK.search(code):
            if not draft_labelled:
                add(i, "goto-emulation", "advisory", raw)
        for nm in NUMBER.finditer(code):
            v = nm.group(0)
            if v in ("0", "1", "-1", "2", "0.0", "1.0"):
                continue
            window = "\n".join(lines[max(0, i - 4):i + 3])
            if "//" in window or "/*" in window or re.search(r"\b[A-Z][A-Z0-9_]{2,}\b", code):
                continue
            add(i, "magic-number", "advisory", raw)
            break
        opens = code.count("{")
        closes = code.count("}")
        if re.search(r"\bfunction\b", code) and fn_start is None and opens:
            fn_start = i
        depth += opens - closes
        if depth > 5 and opens:
            add(i, "nested-depth", "advisory", raw)
        if fn_start is not None and depth == 0 and closes:
            if i - fn_start + 1 > 150:
                add(fn_start, "long-function", "advisory", lines[fn_start - 1])
            fn_start = None
    return out


def readability_debt(findings, files):
    by = {}
    for f in findings:
        by[f["rule"]] = by.get(f["rule"], 0) + 1
    return {"files": len(files), "error_findings": sum(1 for f in findings if f["level"] == "error"),
            "advisory_findings": sum(1 for f in findings if f["level"] == "advisory"), "fake_bodies": by.get("fake-body", 0), "by_rule": by}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0], formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    C.add_repo_args(ap)      # default: the folder above tools/ when run as a contributor copy
    ap.add_argument("files", nargs="*")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    repo = C.repo_of(a, default=Path(__file__).resolve().parent.parent)
    files = []
    for f in a.files:
        p = Path(f)
        files.append(p if p.is_absolute() else (repo / f if (repo / f).exists() else p))
    if not a.files:
        files = sorted((repo / "src").rglob("*.as")) if (repo / "src").is_dir() else []
    known = globals_known(repo)
    findings = []
    for f in files:
        if not Path(f).is_file():
            print(f"{f}: not found", file=sys.stderr)
            return 2
        findings += lint_file(repo, f, known)
    if not a.files:
        for line, names in globals_stale(repo):
            findings.append({"path": str(repo / "docs" / "globals.md"), "line": line, "rule": "globals-stale", "level": "advisory",
                             "text": f"'not yet accepted' names matched function(s): {', '.join(names)}"})
    for f in sorted(findings, key=lambda f: (f["level"] != "error", f["path"], f["line"])):
        print(f"{f['path']}:{f['line']}: {f['rule']}{' (advisory)' if f['level'] == 'advisory' else ''}: {f['text']}")
    errs = sum(1 for f in findings if f["level"] == "error")
    print(f"lint: {len(files)} file(s), {errs} error finding(s), {len(findings) - errs} advisory")
    print(json.dumps({"findings": findings, "errors": errs, "readability_debt": readability_debt(findings, files)}, ensure_ascii=False))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
