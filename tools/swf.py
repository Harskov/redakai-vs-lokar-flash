#!/usr/bin/env python3
"""swf.py — a standard-library SWF reader and writer: the header, zlib (CWS) and LZMA (ZWS) decompression, the tag
stream, DefineSprite sub-tags, deterministic re-serialization as FWS (tags in the original order, no recompression),
and tag-level copy. The pack's build and check use it; it never decodes action records (FFDec does).

    python3 platforms/flash-avm1/scripts/swf.py census FILE [--json]     the header and a tag census
    python3 platforms/flash-avm1/scripts/swf.py fws IN OUT                 write IN as an uncompressed FWS, byte-exact tags

Library: parse(bytes) -> Swf(header fields, tags: [Tag(code, body bytes, long_form)]), Swf.to_bytes(), sprite_subtags(tag),
replace_subtag(tag, index, body), ACTION_TAGS (the tag codes that carry AVM1 actions).
"""
import argparse
import json
import struct
import sys
import zlib
from pathlib import Path

TAG_NAMES = {0: "End", 1: "ShowFrame", 2: "DefineShape", 4: "PlaceObject", 5: "RemoveObject", 6: "DefineBits", 7: "DefineButton",
             8: "JPEGTables", 9: "SetBackgroundColor", 10: "DefineFont", 11: "DefineText", 12: "DoAction", 13: "DefineFontInfo",
             14: "DefineSound", 15: "StartSound", 17: "DefineButtonSound", 18: "SoundStreamHead", 19: "SoundStreamBlock",
             20: "DefineBitsLossless", 21: "DefineBitsJPEG2", 22: "DefineShape2", 23: "DefineButtonCxform", 24: "Protect",
             26: "PlaceObject2", 28: "RemoveObject2", 32: "DefineShape3", 33: "DefineText2", 34: "DefineButton2", 35: "DefineBitsJPEG3",
             36: "DefineBitsLossless2", 37: "DefineEditText", 39: "DefineSprite", 43: "FrameLabel", 45: "SoundStreamHead2",
             46: "DefineMorphShape", 48: "DefineFont2", 56: "ExportAssets", 57: "ImportAssets", 58: "EnableDebugger", 59: "DoInitAction",
             60: "DefineVideoStream", 61: "VideoFrame", 62: "DefineFontInfo2", 64: "EnableDebugger2", 65: "ScriptLimits", 66: "SetTabIndex",
             69: "FileAttributes", 70: "PlaceObject3", 71: "ImportAssets2", 73: "DefineFontAlignZones", 74: "CSMTextSettings",
             75: "DefineFont3", 76: "SymbolClass", 77: "Metadata", 78: "DefineScalingGrid", 82: "DoABC", 83: "DefineShape4",
             84: "DefineMorphShape2", 86: "DefineSceneAndFrameLabelData", 87: "DefineBinaryData", 88: "DefineFontName", 91: "DefineFont4"}
ACTION_TAGS = {12, 59, 7, 34, 26, 70, 39}   # DoAction, DoInitAction, DefineButton, DefineButton2, PlaceObject2/3 (clip actions), DefineSprite


class Tag:
    __slots__ = ("code", "body", "long_form")

    def __init__(self, code, body, long_form=False):
        self.code, self.body, self.long_form = code, body, long_form

    @property
    def name(self):
        return TAG_NAMES.get(self.code, f"Tag{self.code}")

    def to_bytes(self):
        n = len(self.body)
        if n >= 63 or self.long_form:
            return struct.pack("<HI", (self.code << 6) | 63, n) + self.body
        return struct.pack("<H", (self.code << 6) | n) + self.body


class Swf:
    def __init__(self, signature, version, rect, frame_rate, frame_count, tags, rect_bytes):
        self.signature, self.version, self.rect, self.frame_rate, self.frame_count, self.tags = signature, version, rect, frame_rate, frame_count, tags
        self.rect_bytes = rect_bytes

    @property
    def stage(self):
        xmin, xmax, ymin, ymax = self.rect
        return ((xmax - xmin) / 20.0, (ymax - ymin) / 20.0)

    def to_bytes(self):
        body = self.rect_bytes + struct.pack("<HH", self.frame_rate, self.frame_count) + b"".join(t.to_bytes() for t in self.tags)
        return b"FWS" + bytes([self.version]) + struct.pack("<I", 8 + len(body)) + body


def _read_rect(data, pos):
    nbits = data[pos] >> 3
    total_bits = 5 + 4 * nbits
    nbytes = (total_bits + 7) // 8
    raw = data[pos:pos + nbytes]
    bits = int.from_bytes(raw, "big")
    shift = nbytes * 8 - 5
    vals = []
    for _ in range(4):
        shift -= nbits
        v = (bits >> shift) & ((1 << nbits) - 1)
        if nbits and v & (1 << (nbits - 1)):
            v -= 1 << nbits
        vals.append(v)
    return tuple(vals), raw, pos + nbytes


def parse_tags(data, pos=0, end=None):
    end = len(data) if end is None else end
    tags = []
    while pos + 2 <= end:
        code_len, = struct.unpack_from("<H", data, pos)
        code, n = code_len >> 6, code_len & 63
        pos += 2
        long_form = n == 63
        if long_form:
            n, = struct.unpack_from("<I", data, pos)
            pos += 4
        tags.append(Tag(code, data[pos:pos + n], long_form))
        pos += n
        if code == 0:
            break
    return tags, pos


def parse(data):
    sig = data[:3]
    if sig not in (b"FWS", b"CWS", b"ZWS"):
        raise ValueError(f"not a SWF (signature {sig!r})")
    version = data[3]
    length, = struct.unpack_from("<I", data, 4)
    if sig == b"CWS":
        body = zlib.decompress(data[8:])
    elif sig == b"ZWS":
        import lzma
        body = lzma.decompress(data[17:], format=lzma.FORMAT_ALONE) if False else lzma.LZMADecompressor(format=lzma.FORMAT_RAW, filters=[{"id": lzma.FILTER_LZMA1}]).decompress(data[17:])
    else:
        body = data[8:]
    rect, rect_bytes, pos = _read_rect(body, 0)
    frame_rate, frame_count = struct.unpack_from("<HH", body, pos)
    pos += 4
    tags, _ = parse_tags(body, pos)
    return Swf(sig.decode(), version, rect, frame_rate, frame_count, tags, rect_bytes)


def load(path):
    return parse(Path(path).read_bytes())


def sprite_subtags(tag):
    """(sprite id, frame count, [Tag]) of a DefineSprite tag."""
    sid, frames = struct.unpack_from("<HH", tag.body, 0)
    subtags, _ = parse_tags(tag.body, 4)
    return sid, frames, subtags


def sprite_bytes(sid, frames, subtags):
    return struct.pack("<HH", sid, frames) + b"".join(t.to_bytes() for t in subtags)


def census(swf):
    counts = {}
    for t in swf.tags:
        counts[t.name] = counts.get(t.name, 0) + 1
        if t.code == 39:
            for s in sprite_subtags(t)[2]:
                k = f"DefineSprite/{s.name}"
                counts[k] = counts.get(k, 0) + 1
    return counts


# ---------------------------------------------------------------------------- script locations (FFDec's export layout)

CLIP_EVENTS = [(0, 0x80, "keyUp"), (0, 0x40, "keyDown"), (0, 0x20, "mouseUp"), (0, 0x10, "mouseDown"), (0, 0x08, "mouseMove"), (0, 0x04, "unload"),
               (0, 0x02, "enterFrame"), (0, 0x01, "load"), (1, 0x80, "dragOver"), (1, 0x40, "rollOut"), (1, 0x20, "rollOver"), (1, 0x10, "releaseOutside"),
               (1, 0x08, "release"), (1, 0x04, "press"), (1, 0x02, "initialize"), (1, 0x01, "data"), (2, 0x04, "construct"), (2, 0x02, "keyPress"), (2, 0x01, "dragOut")]
BUTTON_EVENTS = [(0, 0x04, "press"), (0, 0x08, "release"), (0, 0x40, "releaseOutside"), (0, 0x01, "rollOver"), (0, 0x02, "rollOut"),
                 (0, 0x20, "dragOver"), (0, 0x80, "dragOver"), (0, 0x10, "dragOut"), (1, 0x01, "dragOut")]


class _Bits:
    def __init__(self, data, pos):
        self.data, self.pos, self.bit = data, pos, 0

    def read(self, n):
        v = 0
        for _ in range(n):
            v = (v << 1) | ((self.data[self.pos] >> (7 - self.bit)) & 1)
            self.bit += 1
            if self.bit == 8:
                self.bit, self.pos = 0, self.pos + 1
        return v

    def align(self):
        if self.bit:
            self.bit, self.pos = 0, self.pos + 1
        return self.pos


def _skip_matrix(data, pos):
    b = _Bits(data, pos)
    if b.read(1):
        n = b.read(5); b.read(2 * n)
    if b.read(1):
        n = b.read(5); b.read(2 * n)
    n = b.read(5); b.read(2 * n)
    return b.align()


def _skip_cxform(data, pos):
    b = _Bits(data, pos)
    add, mult = b.read(1), b.read(1)
    n = b.read(4)
    if mult:
        b.read(4 * n)
    if add:
        b.read(4 * n)
    return b.align()


def _cstring(data, pos):
    e = data.index(b"\0", pos)
    return data[pos:e].decode("latin-1"), e + 1


def _place_object_head(tag):
    """(character id or None, depth, instance name or None, pos, flags, flags2, po3) of a PlaceObject2/3 tag: the fields
    up to and including the clip depth, `pos` the offset after them."""
    d = tag.body
    flags = d[0]
    pos = 1
    po3 = tag.code == 70
    flags2 = 0
    if po3:
        flags2 = d[1]
        pos = 2
    depth = struct.unpack_from("<H", d, pos)[0]
    pos += 2
    if po3 and (flags2 & 0x08) and not (flags & 0x02):   # class name without a character
        _n, pos = _cstring(d, pos)
    if po3 and (flags2 & 0x08) and (flags & 0x02):
        _n, pos = _cstring(d, pos)
    cid = None
    if flags & 0x02:
        cid = struct.unpack_from("<H", d, pos)[0]
        pos += 2
    if flags & 0x04:
        pos = _skip_matrix(d, pos)
    if flags & 0x08:
        pos = _skip_cxform(d, pos)
    if flags & 0x10:
        pos += 2
    name = None
    if flags & 0x20:
        name, pos = _cstring(d, pos)
    if flags & 0x40:
        pos += 2
    return cid, depth, name, pos, flags, flags2, po3


def placements(swf):
    """[{character_id, depth, name, parent, frame}] for every PlaceObject2/3 that places a character, on the main timeline
    (`parent` None) and inside every DefineSprite (`parent` the sprite id); `name` is the instance name or None. The data
    behind the label of a sprite without an export name (run 2026-10-14-013-docs-pass F-1)."""
    out = []

    def walk(tags, parent):
        frame = 1
        for t in tags:
            if t.code == 1:
                frame += 1
            elif t.code in (26, 70):
                cid, depth, name, _pos, _f, _f2, _po3 = _place_object_head(t)
                if cid is not None:
                    out.append({"character_id": cid, "depth": depth, "name": name, "parent": parent, "frame": frame})
            elif t.code == 39 and parent is None:
                sid, _frames, subtags = sprite_subtags(t)
                walk(subtags, sid)
    walk(swf.tags, None)
    return out


def place_object_actions(tag, version):
    """(character id or None, depth, [event name lists per CLIPACTIONRECORD]) of a PlaceObject2/3 tag; the list is empty
    without clip actions."""
    d = tag.body
    cid, depth, _name, pos, flags, flags2, po3 = _place_object_head(tag)
    if po3 and (flags2 & 0x01):      # filters, blend, bitmap cache: not needed for the script map
        return cid, depth, [] if not (flags & 0x80) else ["?"]
    if po3 and (flags2 & 0x02):
        pos += 1
    if po3 and (flags2 & 0x04):
        pos += 1
    events = []
    if flags & 0x80:
        pos += 2                                   # reserved
        fl = 4 if version >= 6 else 2
        pos += fl                                  # AllEventFlags
        while pos + fl <= len(d):
            ev = d[pos:pos + fl]
            if not any(ev):
                break
            pos += fl
            size = struct.unpack_from("<I", d, pos)[0]
            pos += 4
            names = [n for (byte, mask, n) in CLIP_EVENTS if byte < len(ev) and ev[byte] & mask]
            events.append(names)
            pos += size
    return cid, depth, events


def static_content(tag):
    """What a tag holds besides its scripts, to compare a replaced tag's non-script content (remediation 2026-10-17-remediation-34,
    flash-batch-qa-20): a DoAction nothing; a DoInitAction its sprite id; a DefineButton2 its records before the actions; a
    PlaceObject2/3 its fields before the clip actions; a DefineSprite its id, frame count and every subtag's own static content;
    any other tag its whole body."""
    d = tag.body
    if tag.code == 12:
        return b""
    if tag.code == 59:
        return d[:2]
    if tag.code == 34:
        off = struct.unpack_from("<H", d, 3)[0] if len(d) >= 5 else 0
        return d[:3 + off] if off else d
    if tag.code in (26, 70):
        _cid, _depth, _name, pos, flags, flags2, po3 = _place_object_head(tag)
        if not flags & 0x80:
            return d
        if po3 and (flags2 & 0x01):
            return d                       # filters before the actions: not parsed here, compared whole
        if po3 and (flags2 & 0x02):
            pos += 1
        if po3 and (flags2 & 0x04):
            pos += 1
        return d[:pos]
    if tag.code == 39:
        sid, frames, subtags = sprite_subtags(tag)
        return (sid, frames, tuple((t.code, static_content(t)) for t in subtags))
    return d


def button_actions(tag):
    """(button id, [event name lists per BUTTONCONDACTION]) of a DefineButton2 tag."""
    d = tag.body
    bid = struct.unpack_from("<H", d, 0)[0]
    off = struct.unpack_from("<H", d, 3)[0]
    out = []
    if off == 0:
        return bid, out
    pos = 3 + off
    while pos + 4 <= len(d):
        size = struct.unpack_from("<H", d, pos)[0]
        fl = d[pos + 2:pos + 4]
        names = []
        for byte, mask, n in BUTTON_EVENTS:
            if fl[byte] & mask and n not in names:
                names.append(n)
        key = fl[1] >> 1
        if key:
            names.append(f"keyPress \"{key}\"")
        out.append(names)
        if size == 0:
            break
        pos += size
    return bid, out


def export_names(swf):
    names = {}
    for t in swf.tags:
        if t.code == 56:
            n = struct.unpack_from("<H", t.body, 0)[0]
            pos = 2
            for _ in range(n):
                cid = struct.unpack_from("<H", t.body, pos)[0]
                pos += 2
                nm, pos = _cstring(t.body, pos)
                names.setdefault(cid, nm)
    return names


def _event_label(names):
    return ", ".join(names) if names else "?"


def script_locations(swf):
    """[{script, tag_type, tag_index, sub_index, character_id, frame, depth}] in FFDec's script-export naming: frame_N/DoAction,
    DefineSprite_<id>[_<export>]/frame_N/DoAction, __Packages/<Class>, <export name> or DoInitAction (DoInitAction tags),
    DefineButton2_<id>/BUTTONCONDACTION on(<events>), frame_N/PlaceObject2_<cid>[_<export>]_<depth>/CLIPACTIONRECORD
    onClipEvent(<events>). A name that repeats takes _2, _3 … in order, as FFDec does."""
    names = export_names(swf)
    out = []
    seen = {}

    def unique(path):
        seen[path] = seen.get(path, 0) + 1
        return path if seen[path] == 1 else f"{path}_{seen[path]}"

    def sprite_label(cid):
        return f"DefineSprite_{cid}" + (f"_{names[cid]}" if cid in names else "")

    def place_label(cid, depth):
        return f"PlaceObject2_{cid}" + (f"_{names[cid]}" if cid in names else "") + f"_{depth}"

    def walk(tags, prefix, top_index, sprite_id):
        frame = 1
        for j, t in enumerate(tags):
            idx = top_index if top_index is not None else j
            sub = j if top_index is not None else None
            if t.code == 1:
                frame += 1
            elif t.code == 12:
                out.append({"script": unique(f"{prefix}frame_{frame}/DoAction"), "tag_type": "DoAction", "tag_index": idx, "sub_index": sub,
                            "character_id": sprite_id, "frame": frame, "depth": None})
            elif t.code in (26, 70):
                cid, depth, events = place_object_actions(t, swf.version)
                for ev in events:
                    out.append({"script": unique(f"{prefix}frame_{frame}/{place_label(cid, depth)}/CLIPACTIONRECORD onClipEvent({_event_label(ev)})"),
                                "tag_type": t.name, "tag_index": idx, "sub_index": sub, "character_id": cid, "frame": frame, "depth": depth})
            elif t.code == 39 and top_index is None:
                sid, _frames, subtags = sprite_subtags(t)
                walk(subtags, sprite_label(sid) + "/", j, sid)
            elif t.code == 59 and top_index is None:
                sid = struct.unpack_from("<H", t.body, 0)[0]
                nm = names.get(sid)
                if nm and nm.startswith("__Packages."):
                    path = "__Packages/" + nm[len("__Packages."):].replace(".", "/")
                elif nm:
                    path = nm
                else:
                    path = "DoInitAction"
                out.append({"script": unique(path), "tag_type": "DoInitAction", "tag_index": j, "sub_index": None, "character_id": sid, "frame": frame, "depth": None})
            elif t.code in (7, 34) and top_index is None:
                if t.code == 34:
                    bid, events = button_actions(t)
                    for ev in events:
                        out.append({"script": unique(f"DefineButton2_{bid}/BUTTONCONDACTION on({_event_label(ev)})"), "tag_type": "DefineButton2",
                                    "tag_index": j, "sub_index": None, "character_id": bid, "frame": frame, "depth": None})
                else:
                    bid = struct.unpack_from("<H", t.body, 0)[0]
                    out.append({"script": unique(f"DefineButton_{bid}/BUTTONCONDACTION"), "tag_type": "DefineButton", "tag_index": j, "sub_index": None,
                                "character_id": bid, "frame": frame, "depth": None})
    walk(swf.tags, "", None, None)
    return out


def frame_labels(swf):
    """[(frame, label)] of the main timeline."""
    out, frame = [], 1
    for t in swf.tags:
        if t.code == 1:
            frame += 1
        elif t.code == 43:
            out.append((frame, t.body.split(b"\0")[0].decode("latin-1")))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("census"); p.add_argument("file"); p.add_argument("--json", action="store_true")
    p = sub.add_parser("fws"); p.add_argument("inp"); p.add_argument("out")
    p = sub.add_parser("scripts"); p.add_argument("file"); p.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.cmd == "scripts":
        locs = script_locations(load(a.file))
        for l in locs:
            print(json.dumps(l) if a.json else f"{l['script']}  ({l['tag_type']} tag {l['tag_index']}" + (f"/{l['sub_index']}" if l['sub_index'] is not None else "") + ")")
        return 0
    if a.cmd == "census":
        s = load(a.file)
        w, h = s.stage
        out = {"signature": s.signature, "version": s.version, "stage": [w, h], "fps": s.frame_rate / 256.0, "frames": s.frame_count, "tags": len(s.tags), "census": census(s)}
        print(json.dumps(out, indent=None if a.json else 1))
        return 0
    s = load(a.inp)
    Path(a.out).write_bytes(s.to_bytes())
    print(f"wrote {a.out}: FWS v{s.version}, {len(s.tags)} tags")
    return 0


if __name__ == "__main__":
    sys.exit(main())
