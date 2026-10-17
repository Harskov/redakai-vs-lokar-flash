#!/usr/bin/env python3
"""tools/check.py — compare build/<file>.swf with your original tag by tag under the project's criterion.

    python3 tools/check.py [--json]

A tag that holds no script is byte-identical; a tag the build replaced has every function of its scripts equal to the
original's under the criterion in config/flash-avm1/toolchain.json (pcode-normalized: the normalizer in tools/pcode.py;
pcode-bytes: the raw P-code lines). Both files' P-code comes from the pinned FFDec with its AS1/2 deobfuscator on (the export
configuration recorded in config/flash-avm1/toolchain.json), so an obfuscated original compares as the code the player runs, which
is what its author wrote. Writes build/check.json. Exit 0 green, 1 red.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import pcode  # noqa: E402
import swf as swfmod  # noqa: E402

PIN = json.loads((HERE / "config" / "flash-avm1" / "toolchain.json").read_text(encoding="utf-8"))
ORIGINAL = PIN["original"]["file"]
FFDEC = HERE / "tools" / "ffdec" / "ffdec.jar"


def export_pcode(swf, outdir):
    cmd = ["java", "-Djava.awt.headless=true", "-Xmx2g", "-jar", str(FFDEC), "-config", PIN.get("ffdec_config", "autoDeobfuscate=1"), "-cli", "-onerror", "abort",
           "-timeout", "600", "-exportTimeout", "600", "-format", "script:pcode", "-export", "script", str(outdir), str(swf)]
    cp = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    out = {}
    root = Path(outdir) / "scripts"
    if root.is_dir():
        for p in sorted(root.rglob("*.pcode")):
            out[str(p.relative_to(root))[:-6]] = p.read_text(encoding="utf-8", errors="replace")
    return cp.returncode, out


def functions(script, text):
    cls = script.split("/")[-1] if script.startswith("__Packages/") else None
    return pcode.functions(text, script.replace("/", "_"), cls)


def main():
    as_json = "--json" in sys.argv
    crit = PIN.get("match_criterion") or "pcode-normalized"
    orig = HERE / "orig" / ORIGINAL
    built = HERE / "build" / ORIGINAL
    if not orig.is_file() or not built.is_file():
        print("orig/<file>.swf or build/<file>.swf missing (configure.py)", file=sys.stderr)
        return 2
    o, b = swfmod.load(orig), swfmod.load(built)
    smap = json.loads((HERE / "config" / "flash-avm1" / "script-map.json").read_text(encoding="utf-8"))["scripts"]
    claimed = {}
    for script, meta in smap.items():
        claimed.setdefault(meta["tag_index"], []).append(script)
    ob, bb = [t.to_bytes() for t in o.tags], [t.to_bytes() for t in b.tags]
    first = None
    rows = []
    if len(ob) != len(bb):
        first = {"unit": None, "function": None, "row": f"tag count {len(ob)} -> {len(bb)}"}
    differing = [i for i in range(min(len(ob), len(bb))) if ob[i] != bb[i]]
    ref = new = {}
    if differing:
        with tempfile.TemporaryDirectory() as td:
            _rc, ref = export_pcode(orig, Path(td) / "orig")
            _rc2, new = export_pcode(built, Path(td) / "built")
    for i in differing:
        if i not in claimed:
            first = first or {"unit": None, "function": None, "row": f"tag {i} ({o.tags[i].name}) holds no script and differs"}
            continue
        if swfmod.static_content(o.tags[i]) != swfmod.static_content(b.tags[i]):
            # what a replaced tag holds besides its scripts is the original's (the pack's check.py; remediation-34)
            first = first or {"unit": None, "function": None, "row": f"tag {i} ({o.tags[i].name}): its non-script content differs"}
        for script in claimed[i]:
            a, c = ref.get(script), new.get(script)
            if a is None or c is None:
                rows.append({"name": script, "ok": False, "detail": "script missing from an export"})
                first = first or {"unit": script, "function": None, "row": "missing"}
                continue
            fa, fc = functions(script, a), functions(script, c)
            ok, detail = True, f"every function equal under {crit}"
            if len(fa) != len(fc):
                ok, detail = False, f"function count {len(fa)} -> {len(fc)}"
            # a script FFDec's deobfuscator changed never passes a bytes criterion: its bytes carry what the listings no longer
            # show (the pack's check.py since remediation-5; this copy since remediation 2026-10-17-remediation-34, flash-batch-qa-19)
            deob = bool((smap.get(script) or {}).get("deobfuscated"))
            for f, g in ([(None, None)] + list(zip(fa, fc))) if ok else []:
                x, y = pcode.cut(a, f, fa), pcode.cut(c, g, fc)
                if crit.endswith("-bytes"):
                    same = not deob and [pcode.split_line(l)[1].strip() for l in x] == [pcode.split_line(l)[1].strip() for l in y]
                else:
                    same = pcode.normalize(x, pcode.pool_of(a), pcode.parse_header(f.header) if f else None) == pcode.normalize(y, pcode.pool_of(c), pcode.parse_header(g.header) if g else None)
                if not same:
                    ok, detail = False, f"{f.name if f else 'main'} differs"
                    break
            rows.append({"name": script, "ok": ok, "detail": detail})
            if not ok:
                first = first or {"unit": script, "function": detail.split(" ")[0], "row": detail}
    for i, scripts in claimed.items():
        if i not in differing:
            for s in scripts:
                rows.append({"name": s, "ok": True, "detail": "tag byte-identical"})
    check = {"ok": first is None and all(r["ok"] for r in rows), "criterion": crit, "first_diff": first, "units": rows,
             "tags": {"count": len(ob), "identical": len(ob) - len(differing)}}
    (HERE / "build").mkdir(exist_ok=True)
    (HERE / "build" / "check.json").write_text(json.dumps(check, indent=2) + "\n", encoding="utf-8")
    print(f"check: {'OK' if check['ok'] else 'RED'} — {check['tags']['identical']}/{check['tags']['count']} tags identical" + (f"; first diff {first}" if first else ""))
    if as_json:
        print(json.dumps(check))
    return 0 if check["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
