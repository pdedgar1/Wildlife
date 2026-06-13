#!/usr/bin/env python3
"""Generate thumbnails and tiny base64 placeholders for all JPG images."""
import os, base64, json
from PIL import Image
from io import BytesIO

SRC_DIR = "."
THUMB_DIR = "thumbs"
THUMB_MAX = 1200   # max width/height for gallery thumbnails
TINY_MAX  = 24     # width for blur-up placeholder

os.makedirs(THUMB_DIR, exist_ok=True)

placeholders = {}

for fname in sorted(os.listdir(SRC_DIR)):
    if not fname.upper().endswith(".JPG"):
        continue
    src = os.path.join(SRC_DIR, fname)
    dst = os.path.join(THUMB_DIR, fname)

    with Image.open(src) as img:
        img = img.convert("RGB")

        # Full thumbnail
        img.thumbnail((THUMB_MAX, THUMB_MAX), Image.LANCZOS)
        img.save(dst, "JPEG", quality=78, optimize=True, progressive=True)
        print(f"  thumb: {fname}  ({os.path.getsize(dst)//1024} KB)")

        # Tiny placeholder (base64)
        tiny = img.copy()
        tiny.thumbnail((TINY_MAX, TINY_MAX), Image.LANCZOS)
        buf = BytesIO()
        tiny.save(buf, "JPEG", quality=40)
        b64 = base64.b64encode(buf.getvalue()).decode()
        placeholders[fname] = f"data:image/jpeg;base64,{b64}"

with open("placeholders.json", "w") as f:
    json.dump(placeholders, f)
print("Done. placeholders.json written.")
