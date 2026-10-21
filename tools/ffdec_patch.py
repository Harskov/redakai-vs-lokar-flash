"""ffdec_patch.py — a pinned patch to FFDec's ActionScript 1/2 compiler, built from source beside the released FFDec (not a verb).

The compiler a target pins can be FFDec as released (`ffdec-26.3.0`) or FFDec with patches (`ffdec-26.3.0+define-kind-1`): each
patch is a unified diff against one file of FFDec's own source at the release tag, which this module downloads (sha256-checked),
patches (the patched text sha256-checked), compiles against the released jars and loads through ClassOverlayAgent, a Java agent
that defines the patched class from the jar it belongs to as it loads (FFDec's jars are signed: a class of the same package placed
earlier on the class path is refused). FFDec's files stay as released; what is distributed is the patch and this script.

The pack's install (`install.sh --patch`) and the public repository's `configure.py` share this file (the public copy is
`tools/ffdec_patch.py`; tests/ keeps the two equal). Standard library only; Java 8 or newer with its compiler (`javac` on the
PATH, else the `jdk.compiler` module of the running Java).
"""
import hashlib
import json
import os
import shutil
import subprocess
import time
import urllib.request
import zipfile
from pathlib import Path

AGENT_CLASS = "ClassOverlayAgent"
JAVAC_FLAGS = ["-source", "8", "-target", "8", "-nowarn", "-Xlint:-options", "-encoding", "UTF-8"]


class PatchError(RuntimeError):
    pass


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(Path(path).read_bytes())


def compiler_patches(compiler):
    """The patch ids of a compiler id (`ffdec-26.3.0+define-kind-1` -> ['define-kind-1']); none for FFDec as released."""
    return [p for p in str(compiler or "").split("+")[1:] if p]


def apply(text, patch_text):
    """`text` with the unified diff `patch_text` applied: every hunk's context and removed lines must stand at the hunk's line
    exactly (no fuzz), else PatchError names the hunk. Lines before the first `--- ` (the patch's header) are not read."""
    src = text.split("\n")
    lines = patch_text.split("\n")
    i = next((k for k, ln in enumerate(lines) if ln.startswith("--- ")), None)
    if i is None or i + 1 >= len(lines) or not lines[i + 1].startswith("+++ "):
        raise PatchError("no unified diff header (--- / +++)")
    i += 2
    out, pos = [], 0
    while i < len(lines):
        head = lines[i]
        if not head.startswith("@@ "):
            if head.strip():
                raise PatchError(f"unexpected line {i + 1} outside a hunk: {head[:60]!r}")
            i += 1
            continue
        old_start = int(head.split()[1][1:].split(",")[0])
        i += 1
        old, new = [], []
        while i < len(lines) and not lines[i].startswith("@@ "):
            ln = lines[i]
            if ln.startswith("\\"):            # "\ No newline at end of file"
                i += 1
                continue
            if ln == "" and i == len(lines) - 1:
                break
            tag, body = (ln[:1], ln[1:]) if ln else (" ", "")
            if tag == " ":
                old.append(body)
                new.append(body)
            elif tag == "-":
                old.append(body)
            elif tag == "+":
                new.append(body)
            else:
                raise PatchError(f"line {i + 1}: {ln[:60]!r} is not a hunk line")
            i += 1
        at = old_start - 1
        if src[at:at + len(old)] != old:
            raise PatchError(f"hunk at line {old_start} does not match the source")
        out.extend(src[pos:at])
        out.extend(new)
        pos = at + len(old)
    out.extend(src[pos:])
    return "\n".join(out)


def javac(java="java"):
    """The Java compiler command: `javac` on the PATH, else the compiler module of the running Java (Ubuntu's JRE ships it)."""
    found = shutil.which("javac")
    return [found] if found else [java, "-m", "jdk.compiler/com.sun.tools.javac.Main"]


def _run(cmd, what, timeout=300):
    cp = subprocess.run([str(c) for c in cmd], capture_output=True, text=True, timeout=timeout, stdin=subprocess.DEVNULL)
    if cp.returncode != 0:
        raise PatchError(f"{what}: rc {cp.returncode}: {(cp.stderr or cp.stdout).strip()[-400:]}")
    return cp


def ffdec_classpath(ffdec_dir):
    """FFDec's jars, listed one by one: a `lib/*` wildcard is expanded by the javac launcher only, not by the compiler module."""
    d = Path(ffdec_dir)
    jars = [d / "ffdec.jar"] + sorted((d / "lib").glob("*.jar"))
    return os.pathsep.join(str(j) for j in jars if j.is_file())


def fetch_source(spec, dest):
    """spec['source'] downloaded to `dest` (kept when its sha256 is already the pin's); returns the path."""
    src = spec["source"]
    dest = Path(dest)
    if dest.is_file() and sha256_file(dest) == src["sha256"]:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    urllib.request.urlretrieve(src["url"], tmp)
    got = sha256_file(tmp)
    if got != src["sha256"]:
        raise PatchError(f"{src['url']}: sha256 {got} differs from the pin {src['sha256']}")
    os.replace(tmp, dest)
    return dest


def built(out_dir, spec):
    """The build record when `out_dir` holds this patch built from the pinned source, patch and agent, else None."""
    rec = Path(out_dir) / "build.json"
    try:
        data = json.loads(rec.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    want = (spec["source"]["sha256"], spec["patch_sha256"], spec["patched_sha256"])
    if (data.get("source_sha256"), data.get("patch_sha256"), data.get("patched_sha256")) != want:
        return None
    if not (Path(out_dir) / "overlay-agent.jar").is_file() or not any((Path(out_dir) / "classes").rglob("*.class")):
        return None
    return data


def build(spec, ffdec_dir, tree, out_dir, source_path=None, java="java"):
    """Build one patch into out_dir (classes/, overlay-agent.jar, build.json): the pinned source file (downloaded unless
    `source_path` holds it), the patch read from `tree` (the public tree's root: the pack's templates/public-repo/, or the
    public repository), both sha256-checked, compiled against FFDec's jars. Returns the build record; raises PatchError."""
    out = Path(out_dir)
    tree = Path(tree)
    patch_file = tree / spec["patch"]
    agent_file = tree / spec["agent"]
    patch_bytes = patch_file.read_bytes()
    if sha256_bytes(patch_bytes) != spec["patch_sha256"]:
        raise PatchError(f"{spec['patch']}: sha256 {sha256_bytes(patch_bytes)} differs from the pin {spec['patch_sha256']}")
    src = Path(source_path) if source_path else fetch_source(spec, out / "src" / spec["source"]["file"])
    if sha256_file(src) != spec["source"]["sha256"]:
        raise PatchError(f"{src.name}: sha256 differs from the pin {spec['source']['sha256']}")
    patched = apply(src.read_text(encoding="utf-8"), patch_bytes.decode("utf-8"))
    if sha256_bytes(patched.encode("utf-8")) != spec["patched_sha256"]:
        raise PatchError(f"the patched {spec['source']['file']}: sha256 {sha256_bytes(patched.encode('utf-8'))} differs from the pin "
                         f"{spec['patched_sha256']}")
    stamp = time.strftime("%Y%m%d%H%M%S")
    work = out.parent / f"{out.name}.build-{stamp}"
    (work / "patched").mkdir(parents=True)
    pfile = work / "patched" / spec["source"]["file"]
    pfile.write_text(patched, encoding="utf-8", newline="")
    cmd = javac(java)
    _run(cmd + JAVAC_FLAGS + ["-cp", ffdec_classpath(ffdec_dir), "-d", work / "classes", pfile], f"javac {spec['source']['file']}")
    _run(cmd + JAVAC_FLAGS + ["-d", work / "agent", agent_file], f"javac {agent_file.name}")
    with zipfile.ZipFile(work / "overlay-agent.jar", "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("META-INF/MANIFEST.MF", f"Manifest-Version: 1.0\nPremain-Class: {AGENT_CLASS}\n")
        z.write(work / "agent" / f"{AGENT_CLASS}.class", f"{AGENT_CLASS}.class")
    ver = subprocess.run(cmd + ["-version"], capture_output=True, text=True)
    classes = {str(p.relative_to(work / "classes")).replace(os.sep, "/"): sha256_file(p) for p in sorted((work / "classes").rglob("*.class"))}
    rec = {"id": spec["id"], "source_url": spec["source"]["url"], "source_sha256": spec["source"]["sha256"],
           "patch": spec["patch"], "patch_sha256": spec["patch_sha256"], "patched_sha256": spec["patched_sha256"],
           "classes": classes, "agent_sha256": sha256_file(work / "overlay-agent.jar"),
           "javac": (ver.stderr or ver.stdout).strip().splitlines()[0] if (ver.stderr or ver.stdout).strip() else None,
           "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (work / "build.json").write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    if out.exists():
        out.rename(out.parent / f"{out.name}.previous-{stamp}")
    work.rename(out)
    return rec


def java_args(out_dirs):
    """The JVM options that load the built patches (one agent per patch), to put before `-jar ffdec.jar`."""
    return [f"-javaagent:{Path(d) / 'overlay-agent.jar'}={Path(d) / 'classes'}" for d in out_dirs]
