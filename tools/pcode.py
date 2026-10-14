#!/usr/bin/env python3
"""pcode.py — FFDec's AVM1 P-code export: parse, enumerate functions, cut a function's block, normalize (version 1),
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
"""
import argparse
import difflib
import json
import re
import sys

NORMALIZER_VERSION = 1
LABEL_RE = re.compile(r"^(\w+):(.*)$")
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


def normalize(block, pool, header_info=None, version=NORMALIZER_VERSION):
    """Normalized lines of a cut block (see the module doc). header_info: the parsed header for register naming."""
    lines = [resolve_constants(l, pool) for l in block]
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
            t = f"{h['kind']} \"{h['name']}\" params=({','.join(h['params'])}) regs={h['regs']} flags={''.join('1' if x else '0' for x in (h['flags'] or []))}"
        else:
            t = re.sub(LABEL_REF, lambda m: labels.get(m.group(0), m.group(0)), t)
            t = re.sub(r"\bregister(\d+)\b", lambda m: regname(m.group(1)), t)
            t = re.sub(r"^StoreRegister (\d+)$", lambda m: "StoreRegister " + regname(m.group(1)), t)
        if t.startswith("Push "):
            # one value per Push: the player runs `Push a, b` and `Push a` + `Push b` identically; FFDec's compiler
            # emits the split form where the original compiler merged (the push-merging residual class)
            vals = parse_args_list(t[5:])
            if len(vals) > 1:
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
    order, register numbering, jump encoding (labels), header flags, push merging, other."""
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
    pt = [l for l in nt if not l.startswith("Push")]
    pc = [l for l in nc if not l.startswith("Push")]
    if pt == pc:
        classes.add("push-merging")
        return classes
    if any("Unknown_" in l for l in rt):
        classes.add("obfuscation-junk")
    classes.add("other")
    return classes


def splice(text, fns, replacements):
    """The script's P-code text with blocks replaced: `replacements` {function name: block lines (nested blocks as `@fn name`
    placeholders, as `cut` gives them; "_main" for the top-level stream)}. A placeholder expands to the function's
    replacement when one is given, else to its original block (recursively). A replacement's labels are renamed to fresh
    ones so that the blocks never collide; a jump out of a replacement block (to a label it never defines) lands on the
    line that follows the block, as the original compiler's did. The original's ConstantPool lines stay where they are."""
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
                    body, exits = expand(cut(text, f, fns)), []
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
