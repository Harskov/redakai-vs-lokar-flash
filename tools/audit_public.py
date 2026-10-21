#!/usr/bin/env python3
"""audit_public.py — nothing from the game may be tracked in this repository.

    python3 tools/audit_public.py                 # audit every file git tracks (exit 1 on a hit)
    python3 tools/audit_public.py --self-test     # plant a game-shaped fixture; the audit fails on it, and passes a clean one
    python3 tools/audit_public.py --files a b c   # audit these paths (no git)
    python3 tools/audit_public.py --root DIR ...  # the repository root (default: this file's parent's parent)

The workflow .github/workflows/audit.yml runs it on every push and pull request. Four rules, each a line
`<rule>  <path>  <why>` on a hit:
  path      a tracked file under orig/ (except orig/.gitkeep and orig/<release>/.gitkeep), reference/, build/, asm/, wip/, renders/ or tests/behaviour/renders/,
            or with an original, export, object, archive or render extension (.swf .fla .xfl .pcode .o .obj .a .elf .exe .dll
            .so .iso .bin .img .png .jpg .jpeg .mp3 .wav .flv .s .S .asm .pyc .lock .zip .tar.gz)
  magic     a tracked file whose first bytes are an SWF (FWS/CWS/ZWS), an ELF, a Unix archive, a PE/DOS executable, a PNG,
            a JPEG, a ZIP or an ISO 9660 image
  checksum  a tracked file whose SHA-1 equals a hash recorded in config/*/checksum.sha1 (the original file)
  size      a tracked file over the ceiling no source file reaches: 1 MiB (16 MiB for progress/report.json and a release's progress/<VERSION>/report.json)
Exit 0 when every tracked file passes, 1 on any hit, 2 on usage.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

IGNORED_DIRS = ("orig/", "reference/", "build/", "asm/", "wip/", "renders/", "tests/behaviour/renders/")
IGNORED_EXT = {".swf", ".fla", ".xfl", ".pcode", ".o", ".obj", ".a", ".elf", ".exe", ".dll", ".so", ".iso", ".bin", ".img",
               ".png", ".jpg", ".jpeg", ".mp3", ".wav", ".flv", ".s", ".S", ".asm", ".pyc", ".lock", ".zip", ".gz",
               ".gmd", ".gm6", ".gmk", ".bmp", ".mid", ".midi", ".ico"}
GITKEEP_RE = re.compile(r"^orig/(?:[^/]+/)?\.gitkeep$")   # orig/<SERIAL>/.gitkeep: a PS2 target keeps one folder per release
MAGIC = ((b"FWS", 0, "uncompressed SWF"), (b"CWS", 0, "zlib-compressed SWF"), (b"ZWS", 0, "LZMA-compressed SWF"),
         (b"\x7fELF", 0, "ELF executable or object"), (b"!<arch>\n", 0, "Unix archive"), (b"MZ", 0, "PE/DOS executable"),
         (b"\x89PNG", 0, "PNG image"), (b"\xff\xd8\xff", 0, "JPEG image"), (b"PK\x03\x04", 0, "ZIP archive"), (b"CD001", 0x8001, "ISO 9660 disc image"),
         (b"\xa4\xc6\x12\x00", 0, "Game Maker 5 game data"), (b"RIFF", 0, "RIFF media (WAV, AVI)"), (b"MThd", 0, "MIDI file"))
CEILING = 1 << 20
REPORT_CEILING = 16 << 20
REPORT_RE = re.compile(r"^progress/(?:[^/]+/)?report\.json$")   # a further release's: progress/<VERSION>/report.json
SHA1_LINE_RE = re.compile(r"^([0-9a-fA-F]{40})\s+\*?(\S.*)$")


def tracked_files(root):
    cp = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=True)
    return [f for f in cp.stdout.decode("utf-8", "replace").split("\0") if f]


def recorded_hashes(root):
    out = {}
    for p in sorted(Path(root).glob("config/*/checksum.sha1")):
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            m = SHA1_LINE_RE.match(line.strip())
            if m:
                out[m.group(1).lower()] = f"{p.relative_to(root)}: {m.group(2)}"
    return out


def audit(root, files):
    root = Path(root)
    hashes = recorded_hashes(root)
    hits = []
    for rel in files:
        p = root / rel
        if not p.is_file():
            continue
        if any(rel.startswith(d) or ("/" + d) in rel for d in IGNORED_DIRS) and not GITKEEP_RE.match(rel):
            hits.append(("path", rel, "under an ignored folder"))
        elif p.suffix.lower() in IGNORED_EXT:
            hits.append(("path", rel, f"{p.suffix} is an ignored class"))
        size = p.stat().st_size
        with open(p, "rb") as f:
            head = f.read(0x8001 + 5)
        for magic, off, what in MAGIC:
            if head[off:off + len(magic)] == magic:
                hits.append(("magic", rel, what))
                break
        if hashes and size:
            h = hashlib.sha1()
            with open(p, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            if h.hexdigest() in hashes:
                hits.append(("checksum", rel, f"SHA-1 recorded in {hashes[h.hexdigest()]}"))
        ceiling = REPORT_CEILING if REPORT_RE.match(rel) else CEILING
        if size > ceiling:
            hits.append(("size", rel, f"{size} bytes, over the {ceiling >> 20} MiB ceiling"))
    return hits


def report(hits, n):
    for rule, rel, why in hits:
        print(f"{rule:<9} {rel}  {why}")
    if hits:
        print(f"audit: {len(hits)} hit(s) in {n} tracked file(s). Nothing from the game is tracked here; remove the file(s) from the change.")
        return 1
    print(f"audit: {n} tracked file(s), no game-derived file")
    return 0


def self_test():
    ok = True
    with tempfile.TemporaryDirectory(prefix="audit-fixture-") as td:
        root = Path(td)
        (root / "orig").mkdir()
        (root / "orig" / "game.swf").write_bytes(b"CWS\x09" + b"\0" * 64)
        (root / "src").mkdir()
        (root / "src" / "a.as").write_text("function a() {\n}\n", encoding="utf-8")
        (root / "config" / "p").mkdir(parents=True)
        secret = b"the original file's bytes"
        (root / "config" / "p" / "checksum.sha1").write_text(hashlib.sha1(secret).hexdigest() + "  orig/game.swf\n", encoding="utf-8")
        (root / "src" / "copy.txt").write_bytes(secret)
        (root / "src" / "big.txt").write_bytes(b"x" * (CEILING + 1))
        (root / "src" / "export.pcode").write_text("Push 1\n", encoding="utf-8")
        bad = audit(root, ["orig/game.swf", "src/copy.txt", "src/big.txt", "src/export.pcode"])
        rules = {r for r, _, _ in bad}
        if rules != {"path", "magic", "checksum", "size"}:
            print(f"self-test FAILED: expected every rule to fire, got {sorted(rules)}")
            ok = False
        good = audit(root, ["src/a.as"])
        if good:
            print(f"self-test FAILED: the clean fixture produced hits: {good}")
            ok = False
    print("self-test: " + ("ok — the audit rejects the planted fixture and passes the clean one" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--files", nargs="*")
    ap.add_argument("--root")
    a = ap.parse_args()
    if a.self_test:
        return self_test()
    root = Path(a.root) if a.root else Path(__file__).resolve().parent.parent
    files = a.files if a.files is not None else tracked_files(root)
    return report(audit(root, files), len(files))


if __name__ == "__main__":
    sys.exit(main())
