"""Expert-review packet (spec Phase 6.3). Prepared, not sent.

Written to the scratchpad, never into the repository: it contains dataset images,
which must not be committed.

Two parts:
  A. 100 test images, stratified by class with seed 20260921, drawn with their
     annotated boxes and class labels, plus a per-box rating form.
  B. All 18 TVNT-negative histopathology images plus 18 random positives, in
     shuffled order and UNLABELLED, with a form asking OSCC / normal epithelium
     / cannot tell. The point is to find out whether a "negative" is non-tumour
     tissue or simply an OSCC field nobody annotated, so the rater must not be
     able to tell which is which.
"""
from __future__ import annotations

import argparse
import csv
import random
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw

SEED = 20260921
NAMES = ["calculus", "caries", "gingivitis", "hypodontia", "tooth_discolation", "ulcer"]
COLOURS = [(230, 60, 60), (60, 160, 230), (70, 200, 110), (240, 170, 40), (170, 100, 220), (250, 90, 180)]


def read_boxes(label: Path):
    out = []
    if label.exists():
        for line in label.read_text().splitlines():
            p = line.split()
            if len(p) >= 5:
                out.append((int(p[0]), *(float(x) for x in p[1:5])))
    return out


def part_a(test_images: Path, test_labels: Path, dest: Path, n: int = 100) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    by_class = defaultdict(list)
    for p in sorted(test_images.glob("*")):
        for c, *_ in read_boxes(test_labels / (p.stem + ".txt")):
            by_class[c].append(p)
    rng = random.Random(SEED)
    chosen, per = [], max(1, n // len(NAMES))
    for c in range(len(NAMES)):
        pool = sorted(set(by_class.get(c, [])))
        rng.shuffle(pool)
        chosen += [p for p in pool[:per] if p not in chosen]
    pool = sorted({p for v in by_class.values() for p in v} - set(chosen))
    rng.shuffle(pool)
    chosen = (chosen + pool)[:n]

    rows = []
    for p in chosen:
        boxes = read_boxes(test_labels / (p.stem + ".txt"))
        with Image.open(p) as im:
            im = im.convert("RGB")
            W, H = im.size
            dr = ImageDraw.Draw(im)
            for bi, (c, xc, yc, bw, bh) in enumerate(boxes, 1):
                x1, y1 = (xc - bw / 2) * W, (yc - bh / 2) * H
                x2, y2 = (xc + bw / 2) * W, (yc + bh / 2) * H
                dr.rectangle([x1, y1, x2, y2], outline=COLOURS[c % len(COLOURS)], width=3)
                dr.text((x1 + 3, y1 + 3), f"{bi}:{NAMES[c]}", fill=COLOURS[c % len(COLOURS)])
                rows.append({"image": p.name, "box_id": bi, "annotated_class": NAMES[c],
                             "verdict_correct_wrongclass_notalesion": "",
                             "if_wrong_class_what_is_it": ""})
            im.save(dest / p.name)
        if not boxes:
            rows.append({"image": p.name, "box_id": "", "annotated_class": "",
                         "verdict_correct_wrongclass_notalesion": "", "if_wrong_class_what_is_it": ""})

    with (dest / "rating_form_boxes.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    with (dest / "rating_form_images.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["image", "missed_lesion_yes_no", "notes"])
        for p in chosen:
            w.writerow([p.name, "", ""])
    print(f"A: {len(chosen)} images, {len(rows)} box rows -> {dest}")


def part_b(model_a_root: Path, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    negs, poss = [], []
    for split in ("train", "valid", "test"):
        idir, ldir = model_a_root / split / "images", model_a_root / split / "labels"
        if not idir.is_dir():
            continue
        for p in sorted(idir.glob("*")):
            (poss if read_boxes(ldir / (p.stem + ".txt")) else negs).append(p)
    rng = random.Random(SEED)
    sample = negs + rng.sample(poss, min(18, len(poss)))
    rng.shuffle(sample)

    key, rows = [], []
    for i, p in enumerate(sample, 1):
        code = f"H{i:03d}{p.suffix.lower()}"
        with Image.open(p) as im:
            im.convert("RGB").save(dest / code)          # unlabelled, renamed
        key.append({"code": code, "true_filename": p.name,
                    "tvnt_label": "negative(no annotation)" if p in negs else "positive"})
        rows.append({"code": code, "verdict_OSCC_normalepithelium_cannottell": "", "notes": ""})

    with (dest / "rating_form_histopathology.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with (dest / "UNBLINDING_KEY_do_not_send.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(key[0])); w.writeheader(); w.writerows(key)
    print(f"B: {len(negs)} negatives + {len(sample) - len(negs)} positives, shuffled -> {dest}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--test-images", required=True, type=Path)
    ap.add_argument("--test-labels", required=True, type=Path)
    ap.add_argument("--model-a-root", required=True, type=Path)
    ap.add_argument("--dest", required=True, type=Path)
    args = ap.parse_args()
    part_a(args.test_images, args.test_labels, args.dest / "A_detector_100")
    part_b(args.model_a_root, args.dest / "B_histopathology_blinded")
    (args.dest / "README.txt").write_text(
        "Expert-review packet, prepared but NOT sent.\n\n"
        "A_detector_100/  100 test images stratified by class (seed 20260921), drawn with\n"
        "                 their annotated boxes. rating_form_boxes.csv takes one verdict per\n"
        "                 box (correct / wrong class / not a lesion); rating_form_images.csv\n"
        "                 takes a missed-lesion flag per image.\n\n"
        "B_histopathology_blinded/  All TVNT-negative images plus 18 random positives, renamed\n"
        "                 and shuffled so the rater cannot tell them apart. The question is\n"
        "                 whether a TVNT negative is non-tumour tissue or an OSCC field with\n"
        "                 no annotated feature. UNBLINDING_KEY_do_not_send.csv stays here.\n")
    print(f"packet at {args.dest}")


if __name__ == "__main__":
    main()
