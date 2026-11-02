#!/usr/bin/env python3
"""
Convert HEIC/HEIF images to JPG.

Setup (once):
    pip install -r requirements.txt

Usage:
    python heic_to_jpg.py photo.heic                 # single file
    python heic_to_jpg.py ~/Pictures/iphone          # every .heic in a folder
    python heic_to_jpg.py ~/Pictures -r              # include subfolders
    python heic_to_jpg.py ~/Pictures -o ~/converted  # write JPGs to another folder
    python heic_to_jpg.py ~/Pictures -q 85 --delete  # lower quality, remove originals

By default JPGs are saved next to the originals, existing JPGs are skipped,
and EXIF metadata (date taken, GPS, camera) is kept.
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
    from pillow_heif import register_heif_opener
except ImportError:
    sys.exit("Missing packages. Run:  pip install pillow pillow-heif")

register_heif_opener()

HEIC_EXTS = {".heic", ".heif"}


def find_files(paths, recursive):
    for p in paths:
        p = Path(p).expanduser()
        if p.is_file() and p.suffix.lower() in HEIC_EXTS:
            yield p, p.parent
        elif p.is_dir():
            pattern = "**/*" if recursive else "*"
            for f in sorted(p.glob(pattern)):
                if f.is_file() and f.suffix.lower() in HEIC_EXTS:
                    yield f, p
        else:
            print(f"Skipping (not a HEIC file or folder): {p}")


def convert(src, dest, quality):
    with Image.open(src) as img:
        exif = img.info.get("exif")
        icc = img.info.get("icc_profile")
        img = ImageOps.exif_transpose(img)  # apply rotation so it displays correctly
        if img.mode != "RGB":
            img = img.convert("RGB")
        kwargs = {"quality": quality, "optimize": True}
        if exif:
            # orientation is already applied, so reset the tag to "normal"
            exif_obj = Image.Exif()
            exif_obj.load(exif)
            exif_obj[0x0112] = 1
            kwargs["exif"] = exif_obj.tobytes()
        if icc:
            kwargs["icc_profile"] = icc
        dest.parent.mkdir(parents=True, exist_ok=True)
        img.save(dest, "JPEG", **kwargs)


def main():
    ap = argparse.ArgumentParser(description="Convert HEIC/HEIF images to JPG.")
    ap.add_argument("paths", nargs="+", help="HEIC files and/or folders")
    ap.add_argument("-o", "--output", help="output folder (default: next to originals)")
    ap.add_argument("-r", "--recursive", action="store_true", help="include subfolders")
    ap.add_argument("-q", "--quality", type=int, default=92, help="JPEG quality 1-95 (default 92)")
    ap.add_argument("--overwrite", action="store_true", help="replace existing JPGs")
    ap.add_argument("--delete", action="store_true", help="delete HEIC after successful conversion")
    args = ap.parse_args()

    out_root = Path(args.output).expanduser() if args.output else None
    done = skipped = failed = 0

    for src, base in find_files(args.paths, args.recursive):
        if out_root:
            dest = out_root / src.relative_to(base).with_suffix(".jpg")
        else:
            dest = src.with_suffix(".jpg")

        if dest.exists() and not args.overwrite:
            print(f"exists, skipped: {dest}")
            skipped += 1
            continue
        try:
            convert(src, dest, args.quality)
            print(f"ok: {src.name} -> {dest}")
            done += 1
            if args.delete:
                src.unlink()
        except Exception as e:
            print(f"FAILED: {src} ({e})")
            failed += 1

    print(f"\nConverted {done}, skipped {skipped}, failed {failed}.")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
