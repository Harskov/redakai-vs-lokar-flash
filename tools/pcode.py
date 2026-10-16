#!/usr/bin/env python3
"""pcode.py — FFDec's AVM1 P-code export: parse, enumerate functions, cut a function's block, normalize (version 2),
score, splice. A verifier file: a change to the normalizer is a remediation with proof.

    python3 platforms/flash-avm1/scripts/pcode.py functions FILE.pcode [--json]       the functions of one script in order
    python3 platforms/flash-avm1/scripts/pcode.py cut FILE.pcode NAME                  the block of one function (nested blocks elided)
    python3 platforms/flash-avm1/scripts/pcode.py normalize FILE.pcode [NAME]          the normalized lines
    python3 platforms/flash-avm1/scripts/pcode.py score TARGET.pcode CANDIDATE.pcode  score and rows between two cut blocks

The model (design Appendix C §C.4, §C.5). A script's P-code is a stream of instruction lines; a `DefineFunction` or
`DefineFunction2` header opens a block that `}` closes, at any nesting. A *function* is such a block, or the script's
top-level stream (`<unit>_main`) with every function block elided to a placeholder line `@fn <name>`; a nested block is
elided the same way inside its parent. Names: a named header keeps its name; an unnamed header takes the string the
instruction before it pushed (`Push register2, "getUgol"` / `Push "onEnterFrame"`), which is how AVM1 assigns methods
and handlers; otherwise `anon_<n>` by order. A name that repeats within the script is disambiguated by order (`_2`).

Normalizer version 1: (a) `constantN` references resolved to their literal strings and the `ConstantPool` line dropped;
(b) registers renumbered by first use within the block to r1…rN, except the registers the DefineFunction2 header
preloads (`this`, `arguments`, `super`, `_root`, `_parent`, `_global`) and the parameter registers (`p:<name>`), which
keep their names; (c) labels renumbered by order of definition (L1…), a label the block jumps to but never defines by order of reference (X1…), a label nothing in the block jumps to dropped; (d) comments and whitespace stripped; (e) the
function header reduced to (name, parameter names, register count, preload flags); (f) everything else compared
verbatim, instruction by instruction. The score is difflib's ratio over the normalized lines in percent with two
decimals; 100 only when every line is equal; rows print `|` replaced, `<` missing from the candidate, `>` extra.
(g) A `Push` carrying several values is split into one `Push` per value: the player runs both forms identically and
FFDec's compiler always emits the split form where the original compiler merged (measured on the first target:
build evidence 03a).

Normalizer version 2 (remediation 2026-10-14-remediation-5): (h) the obfuscator's residue is dropped — a `DefineLocal` whose
name is a string literal of control-character escapes only (`"\x01"`, `"\x0f"`: the dispatcher's state variable and its
junk local, the two statements FFDec's AS1/2 deobfuscator leaves at the top of a deobfuscated stream) with a numeric
literal value; a label on a dropped line moves to the next kept line. No ActionScript source writes such a `var`, the
author never did, and nothing but `eval` can read it. The pushes are split before the rule runs, so the merged and the
split forms are treated alike. v2 is identical to v1 on every stream without such a statement (the inertness proof in
the round's record: every clean script of the first target normalizes the same under both). A `Push 0.0` (a Double) and
a `Push 0` (an integer) stay different: the source writes either (the `double-literal` residual class; cookbook C2).

Normalizer version 3 (remediation 2026-10-14-remediation-6): (i) the `DefineFunction2` header's register count is reduced
to `regs=fit` when it exceeds every register the block references (preloads and parameter registers included), and kept
as `regs=<n><<needed>` otherwise. Rule (b) already renumbers the registers, so which slots the compiler allocated is not
the source's; the count is the size of that allocation, and a slot the block never references is never read by the
player. The original compiler allocated slots the code never uses and placed parameters above gaps (Redakai's
CCamera.process declares 6 and references up to r3; FFDec's compiler declares 4) where the instructions are equal after
renumbering. What is lost: a local the author declared and never used compiles to no instruction, so it is not
recoverable from the bytes either way. v3 equals v2 on every pair v2 equates (the rule only removes information).

Normalizer version 4 (remediation 2026-10-14-remediation-14): (j) a `Push 0.0` (a Double zero) is written `Push 0`. The
original compiler encoded every zero as a Double: the first target's raw listings push zero as `0.0` 393 times and as the
integer `0` once (inside an obfuscated stream), while every non-zero integer is an integer (2,557) and no non-zero integral
Double occurs. The Double form therefore never carried a source distinction — `0` and `0.0` in the author's source compile
alike — and FFDec's compiler emits the integer for a typed `0`, for the argument count of a call without arguments
(`f()`, `o.m()`, `new C()`: `Push 0` before the name) and for the zero of a unary minus (`-x` is `Push 0`, `Subtract`), the
last two with no source lever (run 2026-10-15-015-match-batch F-1 and F-3). The pairs it newly equates: `Push 0.0 /
Push register1 / Push "replay" / CallMethod` against `Push 0 / …`; `Push 0.0 / Push register1 / Push "x" / GetMember /
Subtract` against `Push 0 / …`. v4 equals v3 on every pair v3 equates (one token rewritten the same way on both sides).
A non-zero integral Double (`Push 3.0`) stays what it is.

Normalizer version 5 (remediation 2026-10-16-remediation-24): rule (i) counts as occupied slots only the preload flags
(`this`, `arguments`, `super`, `_root`, `_parent`, `_global`), never the three suppress flags, which place nothing in a
register. Before it, a header with suppressSuper, suppressArguments and preloadThis counted three slots for one, so a block
referencing r1 and r2 read `regs=3<4` where the allocation fits; FFDec's compiler, which places a `// registers:` local at
`_loc7_`, declares more slots and read `regs=fit`, and the one header row could never be made equal from source
(CParticleEngine.clear 97.56, CVector2D.modul 97.87, run 2026-10-16-022). The pair it newly equates:
`DefineFunction2 "", 0, 3, false, false, true, false, true, false, false, true, false` over `Push register1` and
`StoreRegister 2`, against the same function declared with 8 registers over `StoreRegister 7`. A real header always declares
at least the registers its block references, so `regs=<n><<needed>` arose only from the over-count.

Register locals (the same round): FFDec's compiler places a local in a register only when it is spelled `_locN_`, and it
reads N as the slot (`_loc1_` is the preloaded `this`; 7 upward is free of the six preload slots, the parameters take the
slots left, and rule (b) renumbers); a local with a name compiles to `DefineLocal` and `GetVariable` rows. The accepted source keeps the name and names the local in a `// registers:` comment above the
function (K1 §4); `map_register_locals` rewrites those identifiers to `_locN_` in the text the compiler sees (the try,
the build's `as` form, the public `configure.py`), never in the source on disk.

Residual classes (`residual_classes` on raw blocks, `normalized_residuals` on normalized lines — the one calibrate uses):
`double-literal` (cookbook C2) and `increment` (one register updated in place by `Push 1` + `Add2` where the other side has
`Increment`, or `Push 1` + `Subtract` against `Decrement`: FFDec's draft prints `x = x + 1` where the bytes say `x++`; cookbook
C6) are the classes the source reproduces; `not-not-if` (cookbook C7), `define-kind` (C4) and `uninit-var` (a `var x;` stored as
undefined on one side) name the known shapes left, and with `push-value` and `other` are not reproducible.
"""
import argparse
import difflib
import json
import re
import sys

NORMALIZER_VERSION = 5
LABEL_RE = re.compile(r"^(\w+):(.*)$")
REGISTERS_COMMENT_RE = re.compile(r"^[ \t]*//[ \t]*registers?[ \t]*:[ \t]*(.*?)[ \t]*$", re.M)
IDENT_RE = r"[A-Za-z_$][\w$]*"
AS_TOKEN_RE = re.compile(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|//[^\n]*|/\*.*?\*/|[A-Za-z_$][\w$]*', re.S)
UNKNOWN_RE = re.compile(r"^Unknown_[0-9A-Fa-f]+$")
RESIDUE_NAME_RE = re.compile(r'^"(?:\\x[0-9a-fA-F]{2})+"$')   # a string literal of control-character escapes only, as FFDec prints "\x01"
NUMBER_RE = re.compile(r"^-?\d+(?:\.\d+)?$")
DOUBLE_INT_RE = re.compile(r"^Push (-?\d+)\.0$")
LABEL_REF = r"\b(?:loc[0-9a-fA-F]+|spl[0-9a-f]+)\b"
HDR_RE = re.compile(r"^(DefineFunction2?)\s+(.*)\s*\{\s*$")
PRELOAD_ORDER = ("this", "arguments", "super", "_root", "_parent", "_global")


def parse_args_list(s):
    """Split a comma-separated argument list with quoted strings into tokens (strings keep their quotes)."""
    out, i, n = [], 0, len(s)
    while i < n:
        while i < n and s[i] in " \t":
            i += 1
        if i >= n:
            break
        if s[i] == '"':
            j = i + 1
            while j < n:
                if s[j] == "\\":
                    j += 2
                    continue
                if s[j] == '"':
                    break
                j += 1
            out.append(s[i:j + 1])
            i = j + 1
        else:
            j = s.find(",", i)
            if j < 0:
                j = n
            out.append(s[i:j].strip())
            i = j
        while i < n and s[i] in " \t":
            i += 1
        if i < n and s[i] == ",":
            i += 1
    return out


def lines_of(text):
    """The lines of an export split on newline only: a string literal may hold \x85 or \x1c, which str.splitlines() would split."""
    out = text.split("\n")
    if out and out[-1] == "":
        out.pop()
    return out


def split_line(raw):
    """(label or None, text without the label)"""
    m = LABEL_RE.match(raw)
    if m:
        return m.group(1), m.group(2)
    return None, raw


class Fn:
    def __init__(self, name, kind, header, start, end, depth, index, params, regs, flags):
        self.name, self.kind, self.header, self.start, self.end, self.depth, self.index = name, kind, header, start, end, depth, index
        self.params, self.regs, self.flags = params, regs, flags
        self.children = []

    def as_dict(self):
        return {"name": self.name, "kind": self.kind, "index": self.index, "depth": self.depth, "start": self.start, "end": self.end,
                "define_kind": self.header.split()[0], "params": self.params, "register_count": self.regs, "flags": self.flags}


def parse_header(text):
    m = HDR_RE.match(text.strip())
    if not m:
        return None
    kind, rest = m.group(1), m.group(2)
    toks = parse_args_list(rest)
    name = toks[0].strip('"') if toks else ""
    if kind == "DefineFunction":
        nparams = int(toks[1]) if len(toks) > 1 else 0
        params = [t.strip('"') for t in toks[2:2 + nparams]]
        return {"kind": kind, "name": name, "params": params, "regs": 4, "flags": None, "preg": {}}
    nparams = int(toks[1]) if len(toks) > 1 else 0
    regs = int(toks[2]) if len(toks) > 2 else 4
    flags = [t == "true" for t in toks[3:12]]
    pairs = toks[12:]
    preg = {}
    params = []
    for k in range(0, len(pairs) - 1, 2):
        try:
            preg[int(pairs[k])] = pairs[k + 1].strip('"')
        except ValueError:
            pass
        params.append(pairs[k + 1].strip('"'))
    return {"kind": kind, "name": name, "params": params, "regs": regs, "flags": flags, "preg": preg}


def last_pushed_string(lines, i):
    """The last string literal the instruction before line i pushed, or None."""
    j = i - 1
    while j >= 0 and not lines[j].strip():
        j -= 1
    if j < 0:
        return None
    _l, t = split_line(lines[j])
    t = t.strip()
    if not t.startswith("Push "):
        return None
    toks = parse_args_list(t[5:])
    strs = [x for x in toks if x.startswith('"')]
    return strs[-1].strip('"') if strs else None


def functions(text, unit="unit", class_name=None):
    """The functions of a script in order: Fn objects with start/end line indexes (header line, closing line)."""
    lines = lines_of(text)
    stack, out = [], []
    counter = 0
    anon = 0
    for i, raw in enumerate(lines):
        _label, t = split_line(raw)
        h = parse_header(t)
        if h:
            if h["name"]:
                name, kind = h["name"], "function"
            else:
                s = last_pushed_string(lines, i)
                nxt = next((split_line(x)[1].strip() for x in lines[i + 1:] if False), None)
                if s and re.fullmatch(r"[A-Za-z_$][\w$]*", s):
                    if class_name and s == class_name:
                        name, kind = class_name, "constructor"
                    elif class_name:
                        name, kind = f"{class_name}.{s}", "method"
                    else:
                        name, kind = s, "handler"
                else:
                    anon += 1
                    name, kind = f"anon_{anon}", "anon"
            fn = Fn(name, kind, t.strip(), i, None, len(stack), counter, h["params"], h["regs"], h["flags"])
            fn.preg = h["preg"]
            counter += 1
            if stack:
                stack[-1].children.append(fn)
            stack.append(fn)
            out.append(fn)
        elif t.strip() == "}" and stack:
            fn = stack.pop()
            fn.end = i
    for fn in out:
        if fn.end is None:
            fn.end = len(lines) - 1
    seen = {}
    for fn in out:
        seen[fn.name] = seen.get(fn.name, 0) + 1
        if seen[fn.name] > 1:
            fn.name = f"{fn.name}_{seen[fn.name]}"
    return out


def pool_of(text):
    for raw in lines_of(text):
        _l, t = split_line(raw)
        if t.startswith("ConstantPool"):
            return [x.strip('"') for x in parse_args_list(t[len("ConstantPool"):])]
    return []


def resolve_constants(line, pool):
    def sub(m):
        i = int(m.group(1))
        return '"' + pool[i] + '"' if i < len(pool) else m.group(0)
    return re.sub(r"\bconstant(\d+)\b", sub, line)


def cut(text, fn=None, fns=None, unit="unit", class_name=None, keep_pool=False):
    """The lines of one function's block with nested blocks elided to `@fn <name>`; fn None = the top-level stream, whose
    ConstantPool lines are dropped unless keep_pool (the splice keeps them in place: an obfuscated stream carries several)."""
    lines = lines_of(text)
    fns = fns if fns is not None else functions(text, unit, class_name)
    if fn is None:
        start, end, depth = 0, len(lines) - 1, 0
        inner = [f for f in fns if f.depth == 0]
        rng = range(0, len(lines))
    else:
        start, end, depth = fn.start, fn.end, fn.depth
        inner = fn.children
        rng = range(start, end + 1)
    out = []
    i = rng.start
    stop = rng.stop
    skip = {f.start: f for f in inner}
    while i < stop:
        if i in skip:
            f = skip[i]
            label, _t = split_line(lines[i])
            out.append((label + ":" if label else "") + f"@fn {f.name}")
            i = f.end + 1
            continue
        out.append(lines[i])
        i += 1
    if fn is None and not keep_pool:
        out = [l for l in out if not split_line(l)[1].startswith("ConstantPool")]
    return out


def split_pushes(block):
    """Rule (g) as a pass: one value per Push; a label stays on the first of the split lines."""
    out = []
    for l in block:
        lab, t = split_line(l)
        t = t.strip()
        if t.startswith("Push "):
            vals = parse_args_list(t[5:])
            if len(vals) > 1:
                out.append((lab + ":" if lab else "") + "Push " + vals[0])
                out.extend("Push " + v for v in vals[1:])
                continue
        out.append(l)
    return out


def drop_residue(lines):
    """Rule (h): `Push "<control chars>"`, `Push <number>`, `DefineLocal` dropped (the lines one value per Push); a label on a
    dropped line is carried to the next kept line and every reference to it renamed."""
    out, alias, carry, i = [], {}, [], 0
    while i < len(lines):
        lab, t = split_line(lines[i])
        t = t.strip()
        if t.startswith("Push ") and RESIDUE_NAME_RE.match(t[5:].strip()) and i + 2 < len(lines):
            l1, t1 = split_line(lines[i + 1])
            l2, t2 = split_line(lines[i + 2])
            t1, t2 = t1.strip(), t2.strip()
            if t1.startswith("Push ") and NUMBER_RE.match(t1[5:].strip()) and t2 == "DefineLocal":
                carry += [x for x in (lab, l1, l2) if x]
                i += 3
                continue
        if carry:
            lab = lab or carry[0]
            for x in carry:
                if x != lab:
                    alias[x] = lab
            carry = []
        out.append((lab + ":" if lab else "") + t)
        i += 1
    if alias:
        out = [re.sub(LABEL_REF, lambda m: alias.get(m.group(0), m.group(0)), l) for l in out]
    return out


def deobfuscator_leftover(text):
    """The lines of a reference listing the deobfuscator should have removed and did not (the always-logged event
    deobfuscator-leftover): an undefined opcode, a second ConstantPool, a control-character string outside the residue, a function
    whose name is control characters."""
    lines = drop_residue(split_pushes(lines_of(text)))
    out = [l for l in lines if UNKNOWN_RE.match(split_line(l)[1].strip())]
    pools = [l for l in lines if split_line(l)[1].strip().startswith("ConstantPool")]
    out += pools[1:]
    out += [l for l in lines if split_line(l)[1].strip().startswith("Push ") and RESIDUE_NAME_RE.match(split_line(l)[1].strip()[5:].strip())]
    for l in lines:                      # a surviving junk function (the dispatcher's `\x04\x05`)
        t = split_line(l)[1].strip()
        h = parse_header(t) if HDR_RE.match(t) else None
        if h and h["name"] and RESIDUE_NAME_RE.match('"' + h["name"] + '"'):
            out.append(l)
    return out


def register_locals_of(comment_text):
    """The identifiers a `// registers:` comment names, in order, from entries separated by commas: `r2 = the alias of
    this (back)`, `r2 = back`, `back = the alias of this`, `back`. An entry that names no identifier is skipped."""
    out = []
    for entry in comment_text.split(","):
        e = entry.strip()
        if not e:
            continue
        m = re.match(r"^r\d+\s*=\s*(.*)$", e)
        if m:
            e = m.group(1).strip()
        m = re.search(rf"\(({IDENT_RE})\)\s*$", e)
        name = m.group(1) if m else None
        if name is None:
            m = re.match(rf"^({IDENT_RE})(?:\s*=.*)?$", e)
            name = m.group(1) if m else None
        if name and name not in out:
            out.append(name)
    return out


def _function_span(text, start):
    """(open, close) offsets of the first function body at or after `start`: the brace-matched block that follows the next
    `function` keyword, braces inside strings and comments ignored. None without one."""
    m = re.compile(r"\bfunction\b").search(text, start)
    if not m:
        return None
    i = text.find("{", m.end())
    if i < 0:
        return None
    depth, j = 0, i
    while j < len(text):
        tok = AS_TOKEN_RE.match(text, j)
        if tok and tok.group(0)[0] in "\"'/":
            j = tok.end()
            continue
        c = text[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return i, j + 1
        j += 1
    return None


def map_register_locals(text):
    """The text FFDec's compiler sees for a source that names register locals: every identifier a `// registers:` comment
    names is rewritten to `_locN_` inside the function body the comment precedes (its brace-matched block), outside strings
    and comments; the comment line itself and everything else stay as they are. FFDec places a local in a register only
    under that spelling (whatever N); the source on disk keeps the author's name (K1 §4). A text without such a comment
    comes back unchanged."""
    if not REGISTERS_COMMENT_RE.search(text):
        return text
    used = {int(n) for n in re.findall(r"\b_loc(\d+)_\b", text)}
    nxt = max(used | {6}) + 1     # FFDec reads `_locN_` as register N: 1-6 are the preload slots (`_loc1_` is `this` when preloaded)
    out, pos = [], 0
    for cm in REGISTERS_COMMENT_RE.finditer(text):
        names = register_locals_of(cm.group(1))
        span = _function_span(text, cm.end())
        if not names or span is None or span[0] < pos:
            continue
        open_, close = span
        mapping = {}
        for nm in names:
            mapping[nm] = f"_loc{nxt}_"
            nxt += 1
        body = text[open_:close]

        def swap(t):
            s = t.group(0)
            if s[0] in "\"'/" or (t.start() > 0 and body[t.start() - 1] == "."):   # a string, a comment, a member name
                return s
            return mapping.get(s, s)
        body = AS_TOKEN_RE.sub(swap, body)
        out.append(text[pos:open_])
        out.append(body)
        pos = close
    out.append(text[pos:])
    return "".join(out)


def normalize(block, pool, header_info=None, version=NORMALIZER_VERSION):
    """Normalized lines of a cut block (see the module doc). header_info: the parsed header for register naming."""
    lines = [resolve_constants(l, pool) for l in block]
    if version >= 2:
        lines = drop_residue(split_pushes(lines))
    lines = [l for l in lines if not split_line(l)[1].startswith("ConstantPool")]
    labels = {}
    referenced = set()
    for l in lines:
        referenced.update(re.findall(LABEL_REF, split_line(l)[1]))
    for l in lines:
        lab, _t = split_line(l)
        if lab and lab not in labels and lab in referenced:   # a label nothing in the block jumps to is dropped
            labels[lab] = f"L{len(labels) + 1}"
    ext = 0
    for l in lines:   # a jump out of the block (to the line after its `}`) names a label the block never defines
        for ref in re.findall(LABEL_REF, split_line(l)[1]):
            if ref not in labels:
                ext += 1
                labels[ref] = f"X{ext}"
    regmap = {}
    h = header_info
    if h and h.get("flags") is not None:
        r = 1
        fl = h["flags"]
        order = [("this", fl[7]), ("arguments", fl[5]), ("super", fl[3]), ("_root", fl[1]), ("_parent", fl[0]), ("_global", fl[8])]
        for nm, on in order:
            if on:
                regmap[r] = nm
                r += 1
        for reg, pname in (h.get("preg") or {}).items():
            regmap[reg] = f"p:{pname}"
    nxt = [1]
    regs_text = None
    if h and h.get("flags") is not None:
        regs_text = str(h["regs"])
        if version >= 3:     # rule (i)
            used = {int(x) for l in lines[1:] for x in re.findall(r"\bregister(\d+)\b|^StoreRegister (\d+)$", split_line(l)[1].strip()) for x in x if x}
            # v5: only the preload flags occupy a slot (the suppress flags at 2, 4 and 6 place nothing)
            slots = sum(1 for i in (7, 5, 3, 1, 0, 8) if i < len(h["flags"]) and h["flags"][i]) if version >= 5 else sum(1 for f in h["flags"] if f)
            used |= set((h.get("preg") or {}).keys()) | set(range(1, slots + 1))
            needed = max(used | {0}) + 1
            regs_text = "fit" if h["regs"] >= needed else f"{h['regs']}<{needed}"

    def regname(n):
        n = int(n)
        if n not in regmap:
            regmap[n] = f"r{nxt[0]}"
            nxt[0] += 1
        return regmap[n]
    out = []
    for i, l in enumerate(lines):
        lab, t = split_line(l)
        t = t.strip()
        if not t or t.startswith(";") or t.startswith("//"):
            continue
        t = re.sub(r"\s+", " ", t)
        if i == 0 and h and HDR_RE.match(t):
            t = f"{h['kind']} \"{h['name']}\" params=({','.join(h['params'])}) regs={regs_text if regs_text is not None else h['regs']} flags={''.join('1' if x else '0' for x in (h['flags'] or []))}"
        else:
            t = re.sub(LABEL_REF, lambda m: labels.get(m.group(0), m.group(0)), t)
            t = re.sub(r"\bregister(\d+)\b", lambda m: regname(m.group(1)), t)
            t = re.sub(r"^StoreRegister (\d+)$", lambda m: "StoreRegister " + regname(m.group(1)), t)
        if t.startswith("Push "):
            # one value per Push: the player runs `Push a, b` and `Push a` + `Push b` identically; FFDec's compiler
            # emits the split form where the original compiler merged (the push-merging residual class)
            raw_vals = parse_args_list(t[5:])
            vals = ["0" if v == "0.0" else v for v in raw_vals] if version >= 4 else raw_vals   # rule (j): one zero
            if len(vals) > 1 or vals != raw_vals:
                lab = labels.get(lab) if lab else None
                out.append((lab + ":" if lab else "") + "Push " + vals[0])
                out.extend("Push " + v for v in vals[1:])
                continue
        lab = labels.get(lab) if lab else None
        out.append((lab + ":" if lab else "") + t)
    return out


def score(target, cand):
    """(percent, rows, equal) over two normalized line lists."""
    if target == cand:
        return 100.0, [], True
    sm = difflib.SequenceMatcher(a=target, b=cand, autojunk=False)
    pct = round(100.0 * sm.ratio(), 2) if (target or cand) else 100.0
    if pct >= 100.0:
        pct = 99.99
    rows = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        if tag == "replace":
            for k in range(max(i2 - i1, j2 - j1)):
                a = target[i1 + k] if i1 + k < i2 else ""
                b = cand[j1 + k] if j1 + k < j2 else ""
                rows.append(f"| {a:<40} | {b}")
        elif tag == "delete":
            for k in range(i1, i2):
                rows.append(f"< {target[k]}")
        else:
            for k in range(j1, j2):
                rows.append(f"> {cand[k]}")
    return pct, rows, False


def residual_classes(target, cand, pool_t, pool_c):
    """The classes of difference between two raw blocks when their normalized forms are equal or close: constant-pool
    order, register numbering, jump encoding (labels), header flags, push merging, double literal, push value, other."""
    classes = set()
    raw_t = [split_line(l)[1].strip() for l in target]
    raw_c = [split_line(l)[1].strip() for l in cand]
    if raw_t == raw_c:
        return classes
    rt = [resolve_constants(l, pool_t) for l in raw_t]
    rc = [resolve_constants(l, pool_c) for l in raw_c]
    if rt == rc:
        classes.add("constant-pool")
        return classes
    if [re.sub(r"\bloc[0-9a-fA-F]+\b", "L", l) for l in rt] == [re.sub(r"\bloc[0-9a-fA-F]+\b", "L", l) for l in rc]:
        classes.add("jump-encoding")
        return classes
    nt = [re.sub(r"\bregister\d+\b|StoreRegister \d+", "R", re.sub(r"\bloc[0-9a-fA-F]+\b", "L", l)) for l in rt]
    nc = [re.sub(r"\bregister\d+\b|StoreRegister \d+", "R", re.sub(r"\bloc[0-9a-fA-F]+\b", "L", l)) for l in rc]
    if nt == nc:
        classes.add("register-numbering")
        return classes
    ht = [l for l in nt if HDR_RE.match(l)]
    hc = [l for l in nc if HDR_RE.match(l)]
    if [l for l in nt if not HDR_RE.match(l)] == [l for l in nc if not HDR_RE.match(l)] and ht != hc:
        classes.add("header-flags")
        return classes
    st, sc = drop_residue(split_pushes(nt)), drop_residue(split_pushes(nc))
    if st == sc:
        classes.add("push-merging")        # the original compiler merged consecutive pushes; FFDec's emits one per value
        return classes
    if [DOUBLE_INT_RE.sub(r"Push \1", l) for l in st] == [DOUBLE_INT_RE.sub(r"Push \1", l) for l in sc]:
        classes.add("double-literal")      # a Double literal the draft prints as an integer (cookbook C2: write 0.0)
        return classes
    if [l for l in st if not l.startswith("Push")] == [l for l in sc if not l.startswith("Push")]:
        classes.add("push-value")          # the pushed values differ
        return classes
    if any("Unknown_" in l for l in rt):
        classes.add("obfuscation-junk")
    classes.add("other")
    return classes


NORM_LABEL_RE = re.compile(r"^((?:L|X)\d+:)?(.*)$")


def _rewrite_double(lines):
    out = []
    for l in lines:
        lab, t = NORM_LABEL_RE.match(l).groups()
        m = DOUBLE_INT_RE.match(t)
        out.append((lab or "") + (f"Push {m.group(1)}" if m else t))
    return out


def _rewrite_increment(lines):
    """`Push R`, `Push 1`, `Add2|Subtract`, `StoreRegister R` (one register updated in place: what `x++` / `x--` compiles to
    with `Increment` / `Decrement`, and `x = x + 1` with the pair) -> the one-instruction form. Only that shape: `a = b + 1`
    has no `++` spelling, and a jump target inside the pair keeps it."""
    out, i = [], 0
    while i < len(lines):
        m = re.match(r"^Push (r\d+|p:\S+)$", NORM_LABEL_RE.match(out[-1]).group(2)) if out else None
        if (m and lines[i] == "Push 1" and i + 2 < len(lines) and lines[i + 1] in ("Add2", "Subtract")
                and lines[i + 2] == f"StoreRegister {m.group(1)}"):
            out.append("Increment" if lines[i + 1] == "Add2" else "Decrement")
            i += 2
            continue
        out.append(lines[i])
        i += 1
    return out


def _rewrite_not_not(lines):
    """`Not`, `Not`, `If X` -> `If X` (cookbook C7: the original compiler kept the double Not that FFDec's folds)."""
    out, i = [], 0
    while i < len(lines):
        lab, t = NORM_LABEL_RE.match(lines[i]).groups()
        if t == "Not" and i + 2 < len(lines):
            lab2, t2 = NORM_LABEL_RE.match(lines[i + 1]).groups()
            lab3, t3 = NORM_LABEL_RE.match(lines[i + 2]).groups()
            if t2 == "Not" and not lab2 and not lab3 and t3.startswith("If "):
                out.append((lab or "") + t3)
                i += 3
                continue
        out.append(lines[i])
        i += 1
    return out


def _rewrite_define_kind(lines):
    """A function header's kind, register count and flags dropped, its name and parameters kept (cookbook C4: DefineFunction
    against DefineFunction2 follows from the parameter list and the preloaded identifiers)."""
    return [re.sub(r"^((?:L|X)\d+:)?DefineFunction2? (\"[^\"]*\") params=\(([^)]*)\).*$", r"\1Define \2 (\3)", l) for l in lines]


def _rewrite_uninit(lines):
    """`Push undefined`, `StoreRegister R`, `Pop` dropped: a `var x;` stored as undefined on one side only."""
    out, i = [], 0
    while i < len(lines):
        if (NORM_LABEL_RE.match(lines[i]).group(2) == "Push undefined" and i + 2 < len(lines)
                and re.match(r"^StoreRegister r\d+$", lines[i + 1]) and lines[i + 2] == "Pop"):
            i += 3
            continue
        out.append(lines[i])
        i += 1
    return out


# named, not reproducible: they say which known shape is left, and none counts toward the pin (calibrate's REPRODUCIBLE)
DIAGNOSTIC_REWRITES = (("not-not-if", _rewrite_not_not), ("define-kind", _rewrite_define_kind), ("uninit-var", _rewrite_uninit))


def _diff_rows(a, b):
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    return sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal")


def normalized_residuals(target, cand):
    """The residual classes of two normalized blocks the normalizer does not equate: the reproducible rewrites
    (`double-literal`, `increment`), then the diagnostic ones (`not-not-if`, `define-kind`, `uninit-var`; redakai run
    2026-10-16-026 F-1: these fell to `other` though the cookbook names them), are applied to both sides in turn and a class is
    reported when its rewrite reduced the differing rows; sides still unequal after every rewrite add `push-value` (only
    pushed values differ) or `other`. A mix
    of reproducible classes is classed as such (redakai run 2026-10-14-005-calibrate F-2: CParticle's double-literal rows
    beside a parameter-register order the normalizer absorbs fell to `other` under the raw classifier)."""
    if target == cand:
        return set()
    classes = set()
    t, c = list(target), list(cand)
    for name, rw in (("double-literal", _rewrite_double), ("increment", _rewrite_increment)) + DIAGNOSTIC_REWRITES:
        t2, c2 = rw(t), rw(c)
        if _diff_rows(t2, c2) < _diff_rows(t, c):
            classes.add(name)
        t, c = t2, c2
    if t != c:
        strip = lambda ls: [x for x in (NORM_LABEL_RE.match(l).group(2) for l in ls) if not x.startswith("Push")]  # noqa: E731
        classes.add("push-value" if strip(t) == strip(c) else "other")
    return classes


def splice(text, fns, replacements):
    """The script's P-code text with blocks replaced: `replacements` {function name: block lines (nested blocks as `@fn name`
    placeholders, as `cut` gives them; "_main" for the top-level stream)}. A placeholder expands to the function's
    replacement when one is given, else to its original block (recursively). A replacement's labels are renamed to fresh
    ones so that the blocks never collide; a jump out of a block, replaced or original (to a label it never defines), lands
    on the line that follows the block, as the original compiler's did. The original's ConstantPool lines stay where they are."""
    by = {f.name: f for f in fns}
    counter = [0]

    def fresh():
        counter[0] += 1
        return f"spl{counter[0]:04x}"

    def relabel(block):
        defined = {}
        for l in block:
            lab, _t = split_line(l)
            if lab and lab not in defined:
                defined[lab] = fresh()
        exits = {}
        out = []
        for l in block:
            lab, t = split_line(l)

            def sub(m):
                name = m.group(0)
                if name in defined:
                    return defined[name]
                exits.setdefault(name, fresh())
                return exits[name]
            t = re.sub(LABEL_REF, sub, t)
            out.append((defined[lab] + ":" if lab else "") + t)
        return out, list(exits.values())

    def detach(block):
        """An original block's jumps out of itself (to a label in its parent, which the compiler puts on the line after
        the block) renamed to fresh exit labels, so they still land after the block when the parent was replaced and
        relabelled."""
        defined = {split_line(l)[0] for l in block} - {None}
        exits = {}
        out = []
        for l in block:
            lab, t = split_line(l)
            t = re.sub(LABEL_REF, lambda m: m.group(0) if m.group(0) in defined else exits.setdefault(m.group(0), fresh()), t)
            out.append((lab + ":" if lab else "") + t)
        return out, list(exits.values())

    def settle(out, pending, lab):
        """Point every pending exit label at `lab` in the lines emitted so far."""
        pat = re.compile(r"\b(" + "|".join(re.escape(x) for x in pending) + r")\b")
        return [pat.sub(lab, x) for x in out]

    def expand(block_lines):
        out = []
        pending = []          # exit labels of replaced blocks waiting for the next line
        for l in block_lines:
            lab, t = split_line(l)
            if t.strip().startswith("@fn "):
                name = t.strip()[4:].strip()
                f = by.get(name)
                if name in replacements:
                    body, exits = relabel(replacements[name])
                    body = expand(body)
                elif f is not None:
                    body, exits = detach(cut(text, f, fns))
                    body = expand(body)
                else:
                    raise KeyError(f"@fn {name}: no such function in the script")
                if not body:
                    continue
                blab, bt = split_line(body[0])
                if lab:                       # the placeholder's label names the block's header in the parent's namespace
                    body[0] = lab + ":" + bt
                    blab = lab
                if pending:
                    if not blab:
                        blab = pending[0]
                        body[0] = blab + ":" + bt
                    out = settle(out, pending, blab)
                    pending = []
                out.extend(body)
                pending.extend(exits)
            else:
                if pending:
                    if not lab:
                        lab = pending[0]
                        l = lab + ":" + t
                    out = settle(out, pending, lab)
                    pending = []
                out.append(l)
        return out

    main_block = replacements.get("_main") or cut(text, None, fns, keep_pool=True)
    if "_main" in replacements:
        main_block, _exits = relabel(main_block)
    return "\n".join(expand(main_block)) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0], formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("functions"); p.add_argument("file"); p.add_argument("--class-name"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("cut"); p.add_argument("file"); p.add_argument("name"); p.add_argument("--class-name")
    p = sub.add_parser("normalize"); p.add_argument("file"); p.add_argument("name", nargs="?"); p.add_argument("--class-name")
    p = sub.add_parser("score"); p.add_argument("target"); p.add_argument("candidate")
    a = ap.parse_args()
    if a.cmd == "score":
        t = open(a.target, encoding="utf-8").read().splitlines()
        c = open(a.candidate, encoding="utf-8").read().splitlines()
        pct, rows, eq = score(t, c)
        for r in rows[:40]:
            print(r)
        print(f"score {pct}")
        return 0 if eq else 1
    text = open(a.file, encoding="utf-8", errors="replace").read()
    fns = functions(text, class_name=a.class_name)
    if a.cmd == "functions":
        for f in fns:
            print(json.dumps(f.as_dict()) if a.json else f"{f.index:3d} d{f.depth} {f.kind:<11} {f.name:<40} lines {f.start}-{f.end} regs {f.regs}")
        return 0
    pool = pool_of(text)
    fn = None if a.cmd == "normalize" and not a.name else next((f for f in fns if f.name == a.name), None)
    if a.name and fn is None and a.name != "_main":
        print(f"no function {a.name}", file=sys.stderr)
        return 2
    if a.name == "_main":
        fn = None
    block = cut(text, fn, fns, class_name=a.class_name)
    if a.cmd == "cut":
        print("\n".join(block))
        return 0
    hinfo = parse_header(fn.header) if fn else None
    print("\n".join(normalize(block, pool, hinfo)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
