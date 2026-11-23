#!/usr/bin/env python3
"""make.fun entry for "Sum up 23 November's world news in one image".

Copies the pre-built artwork entry.png (1024x1024) from this repository into
$MAKEFUN_OUTPUT_DIR (default /output) as entry.png.

Standard library only: no PIL, no numpy, no network, no clock reads. The
output bytes are therefore identical on every run.
"""

import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_NAME = "entry.png"
TARGET_NAME = "entry.png"

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
WANT_W = 1024
WANT_H = 1024


def fail(message):
    sys.stderr.write("error: %s\n" % message)
    raise SystemExit(1)


def read_png_header(path):
    """Return (width, height) after validating PNG signature and IHDR fields."""
    with open(path, "rb") as handle:
        head = handle.read(33)
        handle.seek(-12, os.SEEK_END)
        tail = handle.read(12)
    if len(head) < 33:
        fail("%s is too short to be a PNG file" % path)
    if head[:8] != PNG_MAGIC:
        fail("%s does not start with the PNG signature" % path)
    length, kind = struct.unpack(">I4s", head[8:16])
    if kind != b"IHDR":
        fail("%s does not begin with an IHDR chunk" % path)
    if length != 13:
        fail("%s has a malformed IHDR chunk length %d (expected 13)" % (path, length))
    width, height, depth, colour = struct.unpack(">IIBB", head[16:26])
    if depth != 8:
        fail("%s uses bit depth %d, expected 8" % (path, depth))
    if colour not in (2, 6):
        fail("%s uses colour type %d, expected truecolour RGB or RGBA" % (path, colour))
    if len(tail) < 12 or tail[4:8] != b"IEND":
        fail("%s does not end with an IEND chunk (file looks truncated)" % path)
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    source = os.path.join(HERE, SOURCE_NAME)

    if not os.path.isfile(source):
        fail("artwork not found next to main.py: %s "
             "(main.py must sit beside entry.png in the repository root)" % source)

    size = os.path.getsize(source)
    if size == 0:
        fail("%s is empty" % source)
    if size > MAX_BYTES:
        fail("%s is %d bytes, over the %d-byte limit by %d bytes"
             % (source, size, MAX_BYTES, size - MAX_BYTES))

    width, height = read_png_header(source)
    if (width, height) != (WANT_W, WANT_H):
        fail("%s is %dx%d pixels, expected %dx%d"
             % (source, width, height, WANT_W, WANT_H))

    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        fail("cannot create output directory %s: %s "
             "(set MAKEFUN_OUTPUT_DIR to a writable path)" % (out_dir, exc))
    if not os.access(out_dir, os.W_OK):
        fail("output directory %s is not writable "
             "(set MAKEFUN_OUTPUT_DIR to a writable path)" % out_dir)

    target = os.path.join(out_dir, TARGET_NAME)
    try:
        shutil.copyfile(source, target)
    except OSError as exc:
        fail("failed to copy %s to %s: %s" % (source, target, exc))

    written = os.path.getsize(target)
    if written != size:
        fail("short write to %s (%d of %d bytes)" % (target, written, size))

    sys.stdout.write("wrote %s (%d bytes, %dx%d)\n" % (target, written, width, height))


if __name__ == "__main__":
    main()
