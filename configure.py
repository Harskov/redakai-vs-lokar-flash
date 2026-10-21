#!/usr/bin/env python3
"""configure.py — the standalone build of this repository: the pinned FFDec into tools/, the rebuild from src/ with your own
copy of the game, and the check.

    python3 configure.py             prepare, build and check in one go
    python3 configure.py --prepare   download and verify the pinned FFDec (tools/ffdec/) and build the pinned compiler patches
                                     (tools/ffdec-patch/: FFDec's own source file, downloaded and checked, with
                                     tools/<patch> applied, compiled and loaded by tools/ClassOverlayAgent.java), check
                                     orig/<file>.swf against the recorded SHA-1
    python3 configure.py --build     rebuild build/<file>.swf from src/ (every fully written script compiled by FFDec's -importScript;
                                     every other tag copied from your original) and write build/build.json
    python3 configure.py --check     run tools/check.py

Needs Java (8 or newer) on the PATH, with its compiler when the pin names a compiler patch (`javac`, or the jdk.compiler module
of the running Java), and your own copy of the game at orig/<file>.swf (its SHA-1 is in config/flash-avm1/checksum.sha1).
Nothing of the game is in this repository. A compiler patch modifies one file of FFDec's library and is licensed as that file
is (GNU LGPL 3.0); FFDec's own files stay as released.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tools"))
PIN = json.loads((HERE / "config" / "flash-avm1" / "toolchain.json").read_text(encoding="utf-8"))
ORIGINAL = PIN["original"]["file"]
FFDEC = HERE / "tools" / "ffdec" / "ffdec.jar"
PATCHES = PIN.get("compiler_patches") or []      # the pinned compiler's patches (tools/ffdec_patch.py)


def sha(path, algo="sha256"):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def ffdec(*args, compile=False):
    """One FFDec call; a compile (`-importScript`) loads the pinned compiler's patches, built by --prepare."""
    agents = []
    if compile and PATCHES:
        import ffdec_patch
        agents = ffdec_patch.java_args([HERE / spec["path"] for spec in PATCHES])
    cmd = ["java", "-Djava.awt.headless=true", "-Xmx2g"] + agents + ["-jar", str(FFDEC), "-config", PIN.get("ffdec_config", "autoDeobfuscate=1"), "-cli",
           "-onerror", "abort", "-timeout", "600", "-exportTimeout", "600"] + [str(a) for a in args]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=900)


def prepare_patches():
    """Each pinned compiler patch built into tools/ffdec-patch/<id>/ (kept when already built from the pinned files)."""
    import ffdec_patch
    for spec in PATCHES:
        out = HERE / spec["path"]
        if ffdec_patch.built(out, spec):
            continue
        print(f"building the compiler patch {spec['id']} from {spec['source']['url']}")
        try:
            ffdec_patch.build(spec, HERE / "tools" / "ffdec", HERE, out)
        except (ffdec_patch.PatchError, OSError, subprocess.SubprocessError) as e:
            print(f"the compiler patch {spec['id']}: {e}", file=sys.stderr)
            return 1
    return 0


def prepare():
    tool = PIN["tool"]
    if not FFDEC.is_file():
        url, want = tool["url"], tool["sha256"]
        print(f"downloading {url}")
        with tempfile.TemporaryDirectory() as td:
            z = Path(td) / "ffdec.zip"
            urllib.request.urlretrieve(url, z)
            got = sha(z)
            if got != want:
                print(f"sha256 {got} differs from the pin {want}; stopping", file=sys.stderr)
                return 1
            dest = HERE / "tools" / "ffdec"
            dest.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(z) as zf:
                zf.extractall(dest)
            entries = list(dest.iterdir())
            if len(entries) == 1 and entries[0].is_dir():
                for p in entries[0].iterdir():
                    shutil.move(str(p), str(dest / p.name))
    cp = subprocess.run(["java", "-version"], capture_output=True, text=True)
    if cp.returncode != 0:
        print("java is not on the PATH", file=sys.stderr)
        return 1
    if prepare_patches():
        return 1
    orig = HERE / "orig" / ORIGINAL
    if not orig.is_file():
        print(f"put your own copy of the game at orig/{ORIGINAL}", file=sys.stderr)
        return 1
    want = (HERE / "config" / "flash-avm1" / "checksum.sha1").read_text(encoding="utf-8").split()[0]
    got = sha(orig, "sha1")
    if got != want:
        print(f"orig/{ORIGINAL}: sha1 {got} is not the supported version ({want})", file=sys.stderr)
        return 1
    print(f"prepared: FFDec {tool['version']} in tools/ffdec/" + (f" with {', '.join(s['id'] for s in PATCHES)} (tools/ffdec-patch/)" if PATCHES else "")
          + f", orig/{ORIGINAL} is the supported version")
    return 0


def build():
    import swf as swfmod
    orig = HERE / "orig" / ORIGINAL
    smap = json.loads((HERE / "config" / "flash-avm1" / "script-map.json").read_text(encoding="utf-8"))["scripts"]
    original = swfmod.load(orig)
    full = []
    for script, meta in smap.items():
        f = HERE / "src" / f"{script}.as"
        if f.is_file() and "// @reference" not in f.read_text(encoding="utf-8") and "/* @reference" not in f.read_text(encoding="utf-8"):
            full.append((script, meta))
    tags = list(original.tags)
    replaced = {}
    if full:
        with tempfile.TemporaryDirectory() as td:
            folder = Path(td) / "import"
            import pcode
            for script, _m in full:
                dst = folder / "scripts" / f"{script}.as"
                dst.parent.mkdir(parents=True, exist_ok=True)
                # a local named in a `// registers:` comment is spelled _locN_ for FFDec's compiler (tools/pcode.py)
                dst.write_text(pcode.map_register_locals((HERE / "src" / f"{script}.as").read_text(encoding="utf-8")), encoding="utf-8")
            out = Path(td) / "out.swf"
            cp = ffdec("-importScript", orig, out, folder, compile=True)
            if cp.returncode != 0 or not out.is_file():
                print((cp.stderr or cp.stdout)[-800:], file=sys.stderr)
                return 1
            built = swfmod.load(out)
            if len(built.tags) != len(tags):
                print(f"the import changed the tag count ({len(tags)} -> {len(built.tags)})", file=sys.stderr)
                return 1
            by_tag = {}
            for script, meta in full:
                by_tag.setdefault(meta["tag_index"], []).append(script)
            for idx, scripts in by_tag.items():
                if all((HERE / "src" / f"{s}.as").is_file() for s in [x for x, m in smap.items() if m["tag_index"] == idx]) and \
                        all("@reference" not in (HERE / "src" / f"{s}.as").read_text(encoding="utf-8") for s in [x for x, m in smap.items() if m["tag_index"] == idx]):
                    tags[idx] = built.tags[idx]
                    replaced[str(idx)] = scripts
    (HERE / "build").mkdir(exist_ok=True)
    artifact = HERE / "build" / ORIGINAL
    data = swfmod.Swf("FWS", original.version, original.rect, original.frame_rate, original.frame_count, tags, original.rect_bytes).to_bytes()
    artifact.write_bytes(data)
    (HERE / "build" / "build.json").write_text(json.dumps({"artifact": f"build/{ORIGINAL}", "strategy": "unit-granularity (public)", "tags": replaced,
                                                            "scripts_from_source": len(full), "scripts": len(smap), "sha256": hashlib.sha256(data).hexdigest()}, indent=2) + "\n", encoding="utf-8")
    print(f"built build/{ORIGINAL}: {len(replaced)} tag(s) from source ({len(full)} of {len(smap)} scripts fully written)")
    return 0


def check():
    cp = subprocess.run([sys.executable, str(HERE / "tools" / "check.py")], cwd=HERE)
    return cp.returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0], formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--prepare", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    steps = [s for s, on in (("prepare", a.prepare), ("build", a.build), ("check", a.check)) if on] or ["prepare", "build", "check"]
    for s in steps:
        rc = {"prepare": prepare, "build": build, "check": check}[s]()
        if rc:
            return rc
    return 0


if __name__ == "__main__":
    sys.exit(main())
