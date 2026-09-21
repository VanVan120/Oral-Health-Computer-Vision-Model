# Evidence recovered from the committed validation-run artifacts

Source: `ml_models/model_b/runs/detect/val/*`, fetched from git-lfs on
2026-09-21. These are figures committed with the original work. **The split they
were computed on, and the ultralytics version and batch size that produced them,
are not recorded in the repository** — there is no `results.csv`, `args.yaml` or
any other text artifact in that directory, only PNG/JPG. So every number below is
tagged UNKNOWN-ENVIRONMENT and must not be compared with any figure produced by
the pinned evaluator.

## Class list and order (from BoxF1_curve.png legend)

Six classes, in legend order:

    0  calculus
    1  caries
    2  gingivitis
    3  hypodontia
    4  tooth_discolation
    5  ulcer

Note the spelling **`tooth_discolation`** (not "discoloration"). A display-name
dictionary keyed on the correctly spelled word would not match this class name.
That is directly relevant to the class-mapping defect under test in Phase 3, and
to spec check 3.2(i), which requires the display-name keys to equal
`set(model.names.values())` exactly. The order above must still be confirmed
against `best.pt`'s own `names` field (Phase 5.1) before use.

## Operating point (from BoxF1_curve.png legend)

    all classes 0.73 at 0.285

i.e. ultralytics' smoothed mean-F1 curve peaked at F1 = 0.73 at confidence
0.285. This is the closest thing on record to `t_global` (spec 2.5), but it is
NOT the value the spec asks for: 2.5 requires `t_global` recomputed on the full
test split under the pinned 8.3.231 evaluator. Treat 0.285 as a prior to
cross-check against, not as the reported value.

## Not recoverable from these files

- which split (test or validation) produced them;
- the ultralytics version and batch size;
- the numeric P/R/mAP table (the curves are rasterised, and reading values off
  the pixels would be an estimate, not a measurement).
