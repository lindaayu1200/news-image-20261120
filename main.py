"""Entry for make.fun news-image-20261120.

Copies the bundled 1024x1024 entry image (a mosaic of the world's news
of Friday 20 November 2026) to the output directory.
"""
import os
import shutil

OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUT = os.path.join(OUT, "entry.png")
os.makedirs(os.path.dirname(OUT), exist_ok=True)
shutil.copyfile(SRC, OUT)
print("wrote", OUT)
