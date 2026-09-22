"""Addendum R1b item 3: contact sheets for visual inspection of duplicate pairs.

24 pairs (3 sheets of 8), seed 20260921, stratified by the full-resolution
transform. Each panel shows the test image with its own boxes beside the
training twin MAPPED INTO THE TEST FRAME with its boxes, so the two annotations
can be compared directly rather than mentally un-rotated.

Sheets are written outside the repository: they contain dataset images, which
ground rule 4 forbids committing.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from addendum_concordance import INVERSE, NP_TF, PT_TF, map_norm_boxes, normalise

import numpy as np
import pickle

SEED = 20260921
CELL = 300          # each image is drawn CELL x CELL
CAP = 34            # caption strip under each pair
GAP = 12
NAMES = ["calculus", "caries", "gingivitis", "hypodontia", "tooth_discolation", "ulcer"]
COLOURS = [(230, 60, 60), (60, 160, 230), (70, 200, 110),
           (240, 170, 40), (170, 100, 220), (250, 90, 180)]


def font(sz: int):
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, sz)
        except Exception:
            pass
    return ImageFont.load_default()


def pil_transform(im: Image.Image, t: str) -> Image.Image:
    """Apply a dihedral transform to a PIL image, matching NP_TF exactly."""
    a = np.asarray(im)
    if a.ndim == 3:
        out = np.stack([np.ascontiguousarray(NP_TF[t](a[:, :, c]))
                        for c in range(a.shape[2])], axis=2)
    else:
        out = np.ascontiguousarray(NP_TF[t](a))
    return Image.fromarray(out)


def draw_panel(img: Image.Image, boxes_n: np.ndarray, cls: np.ndarray,
               title: str) -> Image.Image:
    """Square panel: the image letterboxed into CELL x CELL, boxes drawn on top."""
    im = img.convert("RGB")
    w, h = im.size
    s = min(CELL / w, CELL / h)
    nw, nh = max(1, int(w * s)), max(1, int(h * s))
    im = im.resize((nw, nh), Image.BILINEAR)
    canvas = Image.new("RGB", (CELL, CELL), (24, 24, 24))
    ox, oy = (CELL - nw) // 2, (CELL - nh) // 2
    canvas.paste(im, (ox, oy))
    dr = ImageDraw.Draw(canvas)
    f = font(11)
    for b, c in zip(boxes_n, cls):
        x1, y1, x2, y2 = b
        px1, py1 = ox + x1 * nw, oy + y1 * nh
        px2, py2 = ox + x2 * nw, oy + y2 * nh
        col = COLOURS[int(c) % len(COLOURS)]
        dr.rectangle([px1, py1, px2, py2], outline=col, width=2)
        lab = NAMES[int(c)][:11]
        tw = dr.textlength(lab, font=f)
        dr.rectangle([px1, max(0, py1 - 13), px1 + tw + 4, py1], fill=col)
        dr.text((px1 + 2, max(0, py1 - 13)), lab, fill=(0, 0, 0), font=f)
    dr.rectangle([0, 0, CELL - 1, CELL - 1], outline=(90, 90, 90))
    dr.text((3, 3), title, fill=(255, 255, 0), font=font(12))
    return canvas


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pairs-csv", required=True, type=Path)
    ap.add_argument("--test-dir", required=True, type=Path)
    ap.add_argument("--train-dir", required=True, type=Path)
    ap.add_argument("--test-boxes", required=True, type=Path)
    ap.add_argument("--train-boxes", required=True, type=Path)
    ap.add_argument("--dest", required=True, type=Path)
    ap.add_argument("--per-sheet", type=int, default=8)
    ap.add_argument("--sheets", type=int, default=3)
    args = ap.parse_args()

    tb_all = pickle.load(open(args.test_boxes, "rb"))["boxes"]
    wb_all = pickle.load(open(args.train_boxes, "rb"))["boxes"]
    test_by = {Path(p).name: p for p in tb_all}
    train_by = {Path(p).name: p for p in wb_all}

    with args.pairs_csv.open(newline="") as fh:
        rows = list(csv.DictReader(fh))

    # Stratify by full-resolution transform, proportionally, seed 20260921.
    by_tf: dict[str, list] = defaultdict(list)
    for r in rows:
        by_tf[r["full_transform"]].append(r)
    rng = random.Random(SEED)
    want = args.per_sheet * args.sheets
    chosen: list = []
    order = sorted(by_tf, key=lambda k: -len(by_tf[k]))
    pools = {}
    for t in order:
        pool = sorted(by_tf[t], key=lambda r: r["test_image"])
        rng.shuffle(pool)
        pools[t] = pool
        take = max(1, round(want * len(by_tf[t]) / len(rows)))
        chosen += pool[:take]
        pools[t] = pool[take:]
    # Proportional rounding can under- or over-fill; top up largest stratum first
    # so the sheet count is exactly what was asked for.
    chosen = chosen[:want]
    ti = 0
    while len(chosen) < want:
        t = order[ti % len(order)]
        if pools[t]:
            chosen.append(pools[t].pop(0))
        ti += 1
        if ti > 1000:
            break
    rng.shuffle(chosen)
    print(f"selected {len(chosen)} pairs: "
          f"{ {t: sum(1 for r in chosen if r['full_transform'] == t) for t in order} }")

    args.dest.mkdir(parents=True, exist_ok=True)
    manifest = []
    pw = CELL * 2 + GAP
    ph = CELL + CAP
    cols, rows_n = 2, args.per_sheet // 2
    for si in range(args.sheets):
        batch = chosen[si * args.per_sheet:(si + 1) * args.per_sheet]
        sheet = Image.new("RGB", (cols * pw + (cols + 1) * GAP,
                                  rows_n * ph + (rows_n + 1) * GAP + 26), (12, 12, 12))
        dr = ImageDraw.Draw(sheet)
        dr.text((GAP, 6), f"Duplicate pairs, sheet {si+1}/{args.sheets}  "
                          f"— left: TEST image + its labels   right: TRAINING twin "
                          f"mapped into the test frame + its labels",
                fill=(255, 255, 255), font=font(13))
        for k, r in enumerate(batch):
            tn, rn, tf = r["test_image"], r["train_image"], r["full_transform"]
            tb, wb = tb_all[test_by[tn]], wb_all[train_by[rn]]
            t_im = Image.open(args.test_dir / tn)
            w_im = Image.open(args.train_dir / rn)
            w_im_mapped = pil_transform(w_im, INVERSE[tf])
            t_boxes = normalise(tb["gt_xyxy"], tb["ori_shape"])
            w_boxes = map_norm_boxes(normalise(wb["gt_xyxy"], wb["ori_shape"]), INVERSE[tf])
            idx = si * args.per_sheet + k + 1
            left = draw_panel(t_im, t_boxes, tb["gt_cls"].astype(int), f"#{idx} TEST")
            right = draw_panel(w_im_mapped, w_boxes, wb["gt_cls"].astype(int),
                               f"#{idx} TWIN ({tf})")
            cx, cy = k % cols, k // cols
            x = GAP + cx * (pw + GAP)
            y = 26 + GAP + cy * (ph + GAP)
            sheet.paste(left, (x, y))
            sheet.paste(right, (x + CELL + GAP, y))
            cap = (f"#{idx} {tf} | test {len(tb['gt_cls'])} boxes "
                   f"[{','.join(sorted({NAMES[int(c)][:5] for c in tb['gt_cls']}))}]"
                   f"  vs twin {len(wb['gt_cls'])} "
                   f"[{','.join(sorted({NAMES[int(c)][:5] for c in wb['gt_cls']}))}]")
            dr.text((x + 2, y + CELL + 6), cap[:120], fill=(200, 200, 200), font=font(11))
            manifest.append({"panel": idx, "sheet": si + 1, "test_image": tn,
                             "train_image": rn, "transform": tf,
                             "n_test_boxes": int(len(tb["gt_cls"])),
                             "n_twin_boxes": int(len(wb["gt_cls"])),
                             "test_classes": sorted({NAMES[int(c)] for c in tb["gt_cls"]}),
                             "twin_classes": sorted({NAMES[int(c)] for c in wb["gt_cls"]})})
        out = args.dest / f"sheet_{si+1}.png"
        sheet.save(out)
        print(f"wrote {out}  ({sheet.size[0]}x{sheet.size[1]})")

    (args.dest / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"wrote {args.dest/'manifest.json'}")


if __name__ == "__main__":
    main()
