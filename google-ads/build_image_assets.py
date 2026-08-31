#!/usr/bin/env python3
"""Search image assets, cropped from the site's own photography.

Google requires image assets to be photographs: no overlaid text, logos, buttons
or graphics. That rules out all 47 creatives in the ad-review set — every one has
a headline burned into it. Those are correct for Meta and wrong for this.

Natural branding inside a photograph — a logo on a shirt or a truck door — is
fine. It is *added* graphics that are not.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "site" / "assets"
OUT = Path(__file__).parent / "image-assets"
OUT.mkdir(exist_ok=True)

# focal = vertical centre of interest, 0 = top, 1 = bottom. The white-door shot
# is a square of a whole house; centre-cropping it lands on the roof.
SOURCES = [
    ("66b2dae9e779df43d0d269c9/66b2ec2561b760fe6fee299b_549fbd18a3bc84b4e30fc12d9d7d4ccb"
     "_new-garage-door-service-install-conroe.png", "crew-truck", 0.45),
    ("66b2dae9e779df43d0d269c9/6a542e2ec6b8791b21582f07_Photo Jul 12 2026, 7 09 27 PM (2) (1).png",
     "opener-install", 0.42),
    ("66b2dae9e779df43d0d269c9/66b2ec2555069ca418a48646_garage-door-repair-and-installer.png",
     "white-door-home", 0.72),
    ("66b2dae9e779df43d0d269c9/6a6638dbf310548aa6535691_copy_AE586C56-1DE3-4700-978C-"
     "82BBC75C202F_poster.0000000.jpg", "modern-door-dusk", 0.55),
    ("66b2dae9e779df43d0d269c9/6a54211784c18aea72a3603c_IMG_2909.jpg", "crew-springs", 0.35),
]
RATIOS = [("landscape", 1200, 628), ("square", 1200, 1200), ("portrait", 960, 1200)]


def crop(im, tw, th, focal):
    sw, sh = im.size
    tr, sr = tw / th, sw / sh
    if sr > tr:                                   # wider than target: trim sides
        nw = int(sh * tr)
        box = ((sw - nw) // 2, 0, (sw - nw) // 2 + nw, sh)
    else:                                         # taller: trim around the focal point
        nh = int(sw / tr)
        top = max(0, min(int((sh - nh) * focal), sh - nh))
        box = (0, top, sw, top + nh)
    return im.crop(box).resize((tw, th), Image.LANCZOS)


def main():
    made = 0
    for rel, name, focal in SOURCES:
        p = SRC / rel
        if not p.exists():
            print(f"  MISSING source for {name}")
            continue
        im = Image.open(p).convert("RGB")
        for label, tw, th in RATIOS:
            if label == "portrait" and im.size[1] / im.size[0] < 1.1:
                continue                          # do not invent a portrait from a landscape
            out = OUT / f"{name}-{label}-{tw}x{th}.jpg"
            crop(im, tw, th, focal).save(out, "JPEG", quality=88, optimize=True)
            print(f"  {out.name:<44} {out.stat().st_size // 1024:>4}KB")
            made += 1
    print(f"\n{made} image assets in {OUT}")


if __name__ == "__main__":
    main()
