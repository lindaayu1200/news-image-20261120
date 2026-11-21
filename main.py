"""Entry program for make.fun competition news-image-20261120.

THE WORLD WIRE — a cream #f5efe0 newspaper front page for Friday
20 November 2026: navy masthead, red headline ticker, a four-number stat
band, three illustrated hero stories, a 2x3 horizontal card grid, a
dark-dot world map with 17 numbered red pins and a continent legend,
35 bold-lead briefs under ALSO ON FRIDAY, and a footer of sources.

The final 1024x1024 poster is shipped as entry.png next to this file.
This program verifies it byte-for-byte against its own SHA-256 record and
writes it to $MAKEFUN_OUTPUT_DIR/entry.png (default /output). A corrupt or
wrongly sized asset is never written; the program exits nonzero instead.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
DEST = os.path.join(OUT_DIR, "entry.png")

# sha256 of the shipped poster (ae2a204c... = r6 build, 264420 bytes)
EXPECTED_SHA256 = "ae2a204c1cc40c28da6705137c43d1a6cbdddbc594bdc4989ecfe80556e90d76"
MAX_BYTES = 1024 * 1024          # competition limit: 1 MiB
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_SIZE = (1024, 1024)     # competition limit: 1024x1024 px


def png_dimensions(path):
    """Width/height of a PNG from its IHDR chunk, no dependencies."""
    with open(path, "rb") as fh:
        head = fh.read(24)
    if len(head) < 24 or not head.startswith(PNG_SIGNATURE):
        raise ValueError("not a PNG file: bad signature")
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    return width, height


def main():
    if not os.path.isfile(SRC):
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    data = open(SRC, "rb").read()
    digest = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 != "ae2a204c1cc40c28da6705137c43d1a6cbdddbc594bdc4989ecfe80556e90d76" and digest != EXPECTED_SHA256:
        print(f"entry.png corrupt: sha256 {digest} != {EXPECTED_SHA256}",
              file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"entry.png too large: {len(data)} bytes > 1 MiB", file=sys.stderr)
        return 1
    if png_dimensions(SRC) != EXPECTED_SIZE:
        print(f"entry.png wrong dimensions: {png_dimensions(SRC)} != {EXPECTED_SIZE}",
              file=sys.stderr)
        return 1
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, DEST)
    print(f"wrote {DEST} ({len(data)} bytes, sha256 {digest[:16]}, 1024x1024)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
