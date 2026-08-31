#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kompresja zdjęć w assets/ — waga strony wpływa na pozycję w Google.

Uruchamiane ręcznie po dodaniu nowych zdjęć:  python3 optimize_images.py
Zmienia pliki w miejscu, więc najpierw commit tego, co już jest.
"""
import os
import glob
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
MAX_W = 1400          # szerokość wystarczająca na ekrany retina
QUALITY = 82

def jpegs():
    for pat in ("assets/*.jpg", "assets/gallery/*/*.jpg", "assets/wall/*.jpg"):
        yield from glob.glob(os.path.join(ROOT, pat))

def main():
    before = after = 0
    for p in sorted(jpegs()):
        b = os.path.getsize(p)
        im = Image.open(p)
        im = im.convert("RGB")
        if im.width > MAX_W:
            h = round(im.height * MAX_W / im.width)
            im = im.resize((MAX_W, h), Image.LANCZOS)
        im.save(p, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        a = os.path.getsize(p)
        before += b; after += a
        if b - a > 50_000:
            print(f"  {os.path.relpath(p, ROOT)}: {b//1024}K -> {a//1024}K")

    # Emblemat: 2000x2000 PNG (3.8 MB) wisiał jako favicon na każdej stronie.
    emb = os.path.join(ROOT, "assets", "emblem.png")
    if os.path.exists(emb):
        b = os.path.getsize(emb)
        src = Image.open(emb).convert("RGB")
        src.resize((640, 640), Image.LANCZOS).save(emb, "PNG", optimize=True)
        src.resize((180, 180), Image.LANCZOS).save(
            os.path.join(ROOT, "assets", "apple-touch-icon.png"), "PNG", optimize=True)
        src.resize((32, 32), Image.LANCZOS).save(
            os.path.join(ROOT, "assets", "favicon-32.png"), "PNG", optimize=True)
        a = os.path.getsize(emb)
        before += b; after += a
        print(f"  emblem.png: {b//1024}K -> {a//1024}K (+ favicon-32, apple-touch-icon)")

    print(f"Razem: {before//1024}K -> {after//1024}K "
          f"({100 - after * 100 // max(before, 1)}% mniej)")

if __name__ == "__main__":
    main()
