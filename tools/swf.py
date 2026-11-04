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
        # the header's five LZMA property bytes (lc/lp/pb and the dictionary size) decode the body; LZMA1's defaults decode
        # only a file written with them (remediation-107, pack-flash#5)
        props = data[12]
        lc, lp, pb = props % 9, (props // 9) % 5, props // 45
        dict_size = max(struct.unpack_from("<I", data, 13)[0], 4096)
        body = lzma.LZMADecompressor(format=lzma.FORMAT_RAW, filters=[{"id": lzma.FILTER_LZMA1, "lc": lc, "lp": lp, "pb": pb, "dict_size": dict_size}]).decompress(data[17:])
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
# FFDec's BUTTONCONDACTION.getHeader order: dragOut before dragOver (remediation-107, pack-flash#1)
BUTTON_EVENTS = [(0, 0x04, "press"), (0, 0x08, "release"), (0, 0x40, "releaseOutside"), (0, 0x01, "rollOver"), (0, 0x02, "rollOut"),
                 (0, 0x10, "dragOut"), (1, 0x01, "dragOut"), (0, 0x20, "dragOver"), (0, 0x80, "dragOver")]
# FFDec's CLIPEVENTFLAGS.getHeader: the last of these a record sets names it onClipEvent(<event>) ...
CLIP_ON_CLIP_EVENT = [(0, 0x80, "keyUp"), (0, 0x40, "keyDown"), (0, 0x20, "mouseUp"), (0, 0x10, "mouseDown"), (0, 0x08, "mouseMove"),
                      (0, 0x04, "unload"), (0, 0x02, "enterFrame"), (0, 0x01, "load"), (1, 0x01, "data")]
# ... and any of these, in this order, names it on(<events>) instead: an instance's button handlers, on(press) and the like
CLIP_ON = [(1, 0x80, "dragOver"), (1, 0x40, "rollOut"), (1, 0x20, "rollOver"), (1, 0x10, "releaseOutside"), (1, 0x08, "release"),
           (1, 0x04, "press"), (1, 0x02, "initialize"), (2, 0x04, "construct"), (2, 0x02, "keyPress"), (2, 0x01, "dragOut")]
KEY_NAMES = {1: "<Left>", 2: "<Right>", 3: "<Home>", 4: "<End>", 5: "<Insert>", 6: "<Delete>", 8: "<Backspace>", 13: "<Enter>", 14: "<Up>",
             15: "<Down>", 16: "<PageUp>", 17: "<PageDown>", 18: "<Tab>", 19: "<Escape>", 32: "<Space>"}   # CLIPACTIONRECORD.KEYNAMES


def key_to_string(key):
    """FFDec's CLIPACTIONRECORD.keyToString: a key code's name (`<Left>`) or its character."""
    return KEY_NAMES.get(key) or chr(key)


def _key_press(key):
    """`keyPress <key>` as FFDec writes it in an export file name: the name without its angle brackets, through makeFileName."""
    return "keyPress " + make_file_name(key_to_string(key or 0).replace("<", "").replace(">", ""))


def clip_event_header(flags, key=None):
    """FFDec's file-name header of a CLIPACTIONRECORD from its event flag bytes and key code: `on(press,release)` when any
    button-style event is set, else `onClipEvent(<the last clip event set>)`."""
    header = ""
    for byte, mask, n in CLIP_ON_CLIP_EVENT:
        if byte < len(flags) and flags[byte] & mask:
            header = f"onClipEvent({n})"
    on = [(_key_press(key) if n == "keyPress" else n) for byte, mask, n in CLIP_ON if byte < len(flags) and flags[byte] & mask]
    if on:
        header = "on(" + ",".join(on) + ")"
    return header.strip()


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


def _invalid_utf8(b):
    return "{invalid_utf8=%d}" % b


def ffdec_string(raw):
    """A SWF string as FFDec 26.3.0 reads it (Utf8Helper.decode, the default charset, every SWF version): UTF-8, each byte that
    is not part of a well-formed sequence written `{invalid_utf8=N}`. SWF 5 bytes in a code page and SWF 6+ UTF-8 alike, so a
    linkage name spells as it does in FFDec's export paths (remediation-107, pack-flash#1)."""
    out, i, n = [], 0, len(raw)
    while i < n:
        b, more = raw[i], 0
        if not b & 0x80:
            out.append(chr(b))
        elif b & 0xC0 == 0x80:
            out.append(_invalid_utf8(b))
        elif b & 0xE0 == 0xC0:
            more = 1
        elif b & 0xF0 == 0xE0:
            more = 2
        elif b & 0xF8 == 0xF0:
            more = 3
        else:
            out.append(_invalid_utf8(b))
        if more:
            if i + more >= n:
                out.append(_invalid_utf8(b))
            else:
                ok = True
                for k in range(more):
                    c = raw[i + 1 + k]
                    if c & 0xC0 != 0x80:
                        if not c & 0x80:
                            more = k
                        ok = False
                        break
                if ok:
                    out.append(raw[i:i + 1 + more].decode("utf-8", "replace"))
                else:
                    out.append(_invalid_utf8(b) + "".join(_invalid_utf8(c) for c in raw[i + 1:i + 1 + more]))
                i += more
        i += 1
    return "".join(out)


_FILE_NAME_INVALID = set(range(32)) | {ord(c) for c in '\\/:*?"<>|'}
_RESERVED_FILE_NAMES = ["CON", "PRN", "AUX", "CLOCK$", "NUL"] + [f"{p}{i}" for i in range(1, 10) for p in ("COM", "LPT")]


def make_file_name(s):
    """FFDec's Helper.makeFileName: the characters a file name cannot hold as %XX, a trailing space or dot escaped, a reserved
    device name prefixed with `_`, an empty name `unnamed`. Every export path component passes through it."""
    out = "".join(f"%{ord(c):02X}" if ord(c) in _FILE_NAME_INVALID else c for c in s)
    if out.endswith(" "):
        out = out[:-1] + "%20"
    elif out.endswith("."):
        out = out[:-1] + "%2E"
    for part in _RESERVED_FILE_NAMES:
        if out.startswith(part) and (out == part or out.startswith(".")):
            out = "_" + out
    return out or "unnamed"


def _cstring(data, pos):
    e = data.index(b"\0", pos)
    return ffdec_string(data[pos:e]), e + 1


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


def place_object_translate(tag):
    """(x, y) in twips that a PlaceObject2/3's matrix moves its character to, or None without a matrix."""
    d = tag.body
    flags, pos, flags2 = d[0], 1, 0
    if tag.code == 70:
        flags2, pos = d[1], 2
    pos += 2                                               # depth
    if tag.code == 70 and flags2 & 0x08:
        _n, pos = _cstring(d, pos)
    if flags & 0x02:
        pos += 2
    if not flags & 0x04:
        return None
    b = _Bits(d, pos)
    if b.read(1):
        n = b.read(5); b.read(2 * n)
    if b.read(1):
        n = b.read(5); b.read(2 * n)
    n = b.read(5)
    tx, ty = b.read(n), b.read(n)
    signed = lambda v: v - (1 << n) if n and v >> (n - 1) else v   # noqa: E731
    return signed(tx), signed(ty)


def placements(swf, positions=False):
    """[{character_id, depth, name, parent, frame}] for every PlaceObject2/3 that places a character, on the main timeline
    (`parent` None) and inside every DefineSprite (`parent` the sprite id); `name` is the instance name or None. The data
    behind the label of a sprite without an export name (run 2026-10-14-013-docs-pass F-1). `positions` adds `x` and `y`,
    the matrix's translation in pixels (None without a matrix): the reading order of a screen's text fields."""
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
                    if positions:
                        xy = place_object_translate(t)
                        out[-1].update({"x": xy[0] / 20.0, "y": xy[1] / 20.0} if xy else {"x": None, "y": None})
            elif t.code == 39 and parent is None:
                sid, _frames, subtags = sprite_subtags(t)
                walk(subtags, sid)
    walk(swf.tags, None)
    return out


_FILTER_SIZES = {0: 23, 1: 9, 2: 15, 3: 27, 6: 80}   # DropShadow, Blur, Glow, Bevel, ColorMatrix: fixed-size bodies


def _skip_filters(d, pos):
    """The offset after a PlaceObject3's FILTERLIST."""
    count = d[pos]
    pos += 1
    for _ in range(count):
        fid = d[pos]
        pos += 1
        if fid in (4, 7):                                  # GradientGlow, GradientBevel: NumColors, RGBA and ratio per colour
            pos += 1 + 5 * d[pos] + 19
        elif fid == 5:                                     # Convolution: MatrixX, MatrixY, Divisor, Bias, the matrix, colour, flags
            pos += 2 + 8 + 4 * d[pos] * d[pos + 1] + 5
        elif fid in _FILTER_SIZES:
            pos += _FILTER_SIZES[fid]
        else:
            raise ValueError(f"PlaceObject3 filter type {fid} is not one the SWF format defines")
    return pos


def clip_actions_offset(tag):
    """The offset of a PlaceObject2/3's CLIPACTIONS in its body (after a PlaceObject3's filters, blend mode, bitmap cache,
    visibility and background colour, which FFDec reads in that order at every SWF version), or None without clip actions
    (remediation-107, pack-flash#1: the filters were not parsed and the SWF 11 fields not skipped)."""
    _cid, _depth, _name, pos, flags, flags2, po3 = _place_object_head(tag)
    if not flags & 0x80:
        return None
    if po3:
        if flags2 & 0x01:
            pos = _skip_filters(tag.body, pos)
        pos += (1 if flags2 & 0x02 else 0) + (1 if flags2 & 0x04 else 0) + (1 if flags2 & 0x20 else 0) + (4 if flags2 & 0x40 else 0)
    return pos


def clip_action_records(tag, version):
    """[(event flag bytes, key code or None, actions start, actions end)] of a PlaceObject2/3's CLIPACTIONRECORDs, offsets in
    the tag body; a ClipEventKeyPress record's key code byte precedes its actions."""
    pos = clip_actions_offset(tag)
    if pos is None:
        return []
    d = tag.body
    fl = 4 if version >= 6 else 2
    pos += 2 + fl                                          # reserved, AllEventFlags
    out = []
    while pos + fl <= len(d):
        ev = d[pos:pos + fl]
        if not any(ev):
            break
        pos += fl
        size = struct.unpack_from("<I", d, pos)[0]
        pos += 4
        key = d[pos] if fl == 4 and ev[2] & 0x02 else None
        out.append((bytes(ev), key, pos + (1 if key is not None else 0), pos + size))
        pos += size
    return out


def place_object_actions(tag, version):
    """(character id or None, depth, [event name lists per CLIPACTIONRECORD]) of a PlaceObject2/3 tag; the list is empty
    without clip actions."""
    cid, depth, *_rest = _place_object_head(tag)
    return cid, depth, [[n for (byte, mask, n) in CLIP_EVENTS if byte < len(ev) and ev[byte] & mask]
                        for ev, _key, _s, _e in clip_action_records(tag, version)]


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
        pos = clip_actions_offset(tag)
        return d if pos is None else d[:pos]
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
            names.append(_key_press(key))          # FFDec's file-name form: `keyPress Left`, `keyPress A`, `keyPress %2E`
        out.append(names)
        if size == 0:
            break
        pos += size
    return bid, out


def export_names(swf):
    """{character id: linkage name} as FFDec assigns them: the first ExportAssets entry of a character wins, and a name already
    given to another character is not given again."""
    names = {}
    for t in swf.tags:
        if t.code == 56:
            n = struct.unpack_from("<H", t.body, 0)[0]
            pos = 2
            for _ in range(n):
                cid = struct.unpack_from("<H", t.body, pos)[0]
                pos += 2
                nm, pos = _cstring(t.body, pos)
                if cid not in names and nm not in names.values():
                    names[cid] = nm
    return names


def _event_label(names):
    return ", ".join(names)


def _init_action_path(nm):
    """A DoInitAction's export path from its sprite's linkage name: every dotted name is a package path, `__Packages.a.b.C` ->
    `__Packages/a/b/C` and `my.lib.thing` -> `my/lib/thing` alike; no name `DoInitAction`."""
    if not nm:
        return "DoInitAction"
    parts = nm.split(".")
    parts = parts[:1] + [p for p in parts[1:] if p]     # FFDec drops empty parts after the first (`a..b` -> a/b, `.x` -> unnamed/x)
    return "/".join(make_file_name(p) for p in parts)


def script_locations(swf):
    """[{script, tag_type, tag_index, sub_index, character_id, frame, depth}] in FFDec's script-export naming: frame_N/DoAction,
    DefineSprite_<id>[_<export>]/frame_N/DoAction, __Packages/<Class>, <export name> or DoInitAction (DoInitAction tags),
    DefineButton2_<id>/BUTTONCONDACTION on(<events>), frame_N/PlaceObject2_<cid>[_<export>]_<depth>/CLIPACTIONRECORD
    onClipEvent(<event>) or on(<events>), PlaceObject3 likewise, DefineButton_<id>/DefineButton_<id>. Every component passes
    through FFDec's makeFileName, keys are named as FFDec names them, and a file name that repeats in one folder takes _2, _3 …
    in order, as FFDec's exporter does (remediation-107, pack-flash#1)."""
    names = export_names(swf)
    out = []
    used = {}

    def unique(path):
        folder, _, base = path.rpartition("/")
        taken = used.setdefault(folder, set())
        name, n = base, 1
        while name in taken:
            n += 1
            name = f"{base}_{n}"
        taken.add(name)
        return f"{folder}/{name}" if folder else name

    def char_label(kind, cid):
        return make_file_name(f"{kind}_{cid}" + (f"_{names[cid]}" if cid in names else ""))

    def sprite_label(cid):
        return char_label("DefineSprite", cid)

    def place_label(tag, cid, depth):
        cid = -1 if cid is None else cid                   # FFDec's getCharacterId without a character
        return make_file_name(f"{tag.name}_{cid}" + (f"_{names[cid]}" if cid in names else "") + f"_{depth}")

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
                cid, depth, *_rest = _place_object_head(t)
                for ev, key, _s, _e in clip_action_records(t, swf.version):
                    rec = make_file_name(f"CLIPACTIONRECORD {clip_event_header(ev, key)}")
                    out.append({"script": unique(f"{prefix}frame_{frame}/{place_label(t, cid, depth)}/{rec}"),
                                "tag_type": t.name, "tag_index": idx, "sub_index": sub, "character_id": cid, "frame": frame, "depth": depth})
            elif t.code == 39 and top_index is None:
                sid, _frames, subtags = sprite_subtags(t)
                walk(subtags, sprite_label(sid) + "/", j, sid)
            elif t.code == 59 and top_index is None:
                sid = struct.unpack_from("<H", t.body, 0)[0]
                path = _init_action_path(names.get(sid))
                out.append({"script": unique(path), "tag_type": "DoInitAction", "tag_index": j, "sub_index": None, "character_id": sid, "frame": frame, "depth": None})
            elif t.code in (7, 34) and top_index is None:
                if t.code == 34:
                    bid, events = button_actions(t)
                    for ev in events:
                        rec = make_file_name(f"BUTTONCONDACTION on({_event_label(ev)})")
                        out.append({"script": unique(f"{char_label('DefineButton2', bid)}/{rec}"), "tag_type": "DefineButton2",
                                    "tag_index": j, "sub_index": None, "character_id": bid, "frame": frame, "depth": None})
                else:
                    bid = struct.unpack_from("<H", t.body, 0)[0]
                    label = char_label("DefineButton", bid)        # the button is its own script: DefineButton_<id>/DefineButton_<id>
                    out.append({"script": unique(f"{label}/{label}"), "tag_type": "DefineButton", "tag_index": j, "sub_index": None,
                                "character_id": bid, "frame": frame, "depth": None})
    walk(swf.tags, "", None, None)
    return out


def frame_labels(swf, sprite_id=None):
    """[(frame, label)] of the main timeline, or of the DefineSprite `sprite_id`."""
    tags = swf.tags
    if sprite_id is not None:
        tags = next((sprite_subtags(t)[2] for t in swf.tags if t.code == 39 and struct.unpack_from("<H", t.body, 0)[0] == sprite_id), [])
    out, frame = [], 1
    for t in tags:
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
