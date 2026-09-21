# Weight history, the warm start, and chronology (spec Phases 5.2, 5.3, 5.6)

`git lfs fetch --all` succeeded — no bandwidth-quota block — so every checkpoint
the repository has ever referenced was retrieved and read, including the two
superseded ones. 27 LFS objects in total; three are checkpoints in the current
tree and two are historical checkpoints under the pre-restructure paths.

## 5.2 Every commit that changed a checkpoint

| path | commit | ISO date | change | LFS oid (sha256) | size |
|---|---|---|---|---|---|
| `Model B/models/best.pt` | `f7e56f7` | 2025-12-07 16:48:02 +0800 | added | `eec5aba9f720388e07b521f99687b15b94edf821d35eb91d7602b39710a97946` | 52,022,866 |
| `Model B/models/best.pt` | `122e026` | 2025-12-12 17:05:14 +0800 | modified | `4de8714f0f2b52a70564cc1be55058262564ced400cd8a7d5815192477aad0cc` | 52,035,922 |
| `→ ml_models/model_b/models/best.pt` | `065dbd4` | 2026-03-30 22:52:43 +0800 | renamed (R100, content unchanged) | `4de8714f…7aad0cc` | 52,035,922 |
| `Model A/model_a.pth` | `f7e56f7` | 2025-12-07 16:48:02 +0800 | added | `b7393a56404e16b67c088c1c69441bce04d86b9b40f429e1fa3e3b59d0ef19a1` | 107,372,550 |
| `Model A/model_a.pth` | `48e1c4e` | 2026-02-05 20:55:51 +0800 | modified | `b469110a551aa4bb93189b05a424fa28239dc4f710983e779b41acf7a19a2d3f` | 55,240,265 |
| `→ ml_models/model_a/model_a.pth` | `065dbd4` | 2026-03-30 22:52:43 +0800 | renamed (R100) | `b469110a…9a2d3f` | 55,240,265 |
| `Model Triage/triage_router.pth` | `f7e56f7` | 2025-12-07 16:48:02 +0800 | added | `59cb5a8d8445927a92b0fd0d502fc56b650a16c1a9be94246bc2d2115088f5e2` | 44,790,155 |
| `→ ml_models/model_triage/triage_router.pth` | `065dbd4` | 2026-03-30 22:52:43 +0800 | renamed (R100) | `59cb5a8d…88f5e2` | 44,790,155 |

The commit `122e026` is titled **"Model B has been enhanced via evolution
training"**, and the released checkpoint's internal `date` is
2025-12-12T16:33:59, 32 minutes before that commit. The two line up.

## 5.3 The warm start, identified

`best.pt`'s `train_args.model` is `Backend Development/Model B/models/best.pt`.
The checkpoint that path referred to is the one this repository committed at
`f7e56f7`, oid `eec5aba9…97946`. It was fetched and read directly.

| field | warm start (`eec5aba9`) | released (`4de8714f`) |
|---|---|---|
| `date` | 2025-12-06T15:51:39 | 2025-12-12T16:33:59 |
| `version` | 8.3.231 | 8.3.231 |
| `names` | calculus, caries, gingivitis, hypodontia, tooth_discolation, ulcer | **identical** |
| architecture | nc 6, depth 0.67, width 0.75 (YOLOv8m) | identical |
| `train_args.model` | **`best.pt`** | `Backend Development/Model B/models/best.pt` |
| `train_args.data` | **`oral-diseases-1/data.yaml`** | `/home/hfyic3/Backend Development/Model B/oral-diseases-1/data.yaml` |
| `epochs` requested / recorded | 50 / **50** | 200 / **48** |
| `patience` | 100 | 20 |
| `batch` | 32 | 100 |
| `seed` / `deterministic` | 0 / True | 0 / True |
| `name` | `HPC_Run_Optimized` | `yolov8m_evolved_final` |
| stored `mAP50` / `mAP50-95` | 0.75996 / 0.38730 | 0.75956 / 0.38766 |

Three conclusions follow, and each answers a reviewer point directly.

### (a) The warm start used the same dataset directory

Both runs name `oral-diseases-1/data.yaml`. The released model's ancestor was
trained on the same Roboflow export, so the released model's exposure to the
training split spans **at least two runs** — 50 epochs then 48 — not the 48 of
the final run. The manuscript should describe the training history as a chain,
not a single run.

The caveat has to be stated with it: `data.yaml` itself is not in the repository
at any commit, and `oral-diseases-1/` was never committed. So it cannot be
*proved* from these files that the two runs used the same train/valid/test
partition of that export, only that they named the same directory. Confirming
the partition needs the data.

### (b) The chain does not bottom out here

The warm start's own `train_args.model` is `best.pt` with `pretrained: True`, so
**it was itself warm-started from a third checkpoint**. That third checkpoint is
not in the repository: only two `best.pt` objects exist across all of git
history. Its origin, and what it was trained on, are **not recoverable from the
records available**. This is the honest limit of the provenance trail, and
it should be reported as such rather than closed with an assumption.

### (c) The old deployed dictionary never matched any checkpoint

Spec 5.2(3) asks whether the warm start's class order matches the old deployed
dictionary. It does not. The warm start's order is

    0 calculus, 1 caries, 2 gingivitis, 3 hypodontia, 4 tooth_discolation, 5 ulcer

which is identical to the released checkpoint's. The pre-fix dictionary was

    0 Caries, 1 Calculus, 2 Gingivitis, 3 Tooth Discoloration, 4 Ulcers, 5 Hypodontia

So the wrong dictionary was not a stale copy of some earlier, once-valid class
order. **No checkpoint in this repository's history has ever had that order.**
The chronology confirms it: the dictionary was introduced in the *first* commit,
`f7e56f7` (2025-12-07 16:48:02), which is also the commit that added the warm
start whose order it already failed to match, and it survived unchanged until
`0b21474` (2026-08-13 15:55:35) removed it — roughly **eight months** in the
deployed code.

## Model A was redesigned, not merely retrained

The superseded `model_a.pth` (`b7393a56`, added 2025-12-07, replaced
2026-02-05) has the same DenseNet-169 backbone but a **different head set**:

| checkpoint | heads |
|---|---|
| `b7393a56` (old) | `head_tvnt` (2), `head_poi` (**5**), `head_pni` (2), `head_tb` (1), `head_mi` (1), plus a `decoder` (72 tensors) |
| `b469110a` (current) | `head_tvnt` (2), `head_mitotic` (1), `head_nucleol` (1), `head_hyperchrom` (1) |

The old model carried heads for what appear to be pattern of invasion (5
classes), perineural invasion (2 classes), tumour budding and mitotic index, and
a decoder branch. The current model dropped all of those and kept TVNT plus
three scalar heads. This is a change of task, not a retrain, and it explains the
size difference (107 MB vs 55 MB). Only the current model is evaluated in the
manuscript; the old one is recorded here because "the model" is not one thing
across the repository's history.

## 5.6 Chronology

Full list: `S16_chronology_all_commits.txt` (62 commits across all refs, three of
them made by this revision). Authors: 54 commits by `Your Name
<youremail@example.com>`, an unconfigured git identity, and 8 by `VanVan120`.
Range: `f7e56f7` 2025-12-07 16:48:02 +0800 to the current branch tip.

Commits bearing on the audit, the class-mapping fix, the environment pin or the
manuscript evidence:

| commit | ISO date | subject |
|---|---|---|
| `f7e56f7` | 2025-12-07 16:48:02 | Oral AI first commit — **introduces the wrong class dictionary**, the warm-start checkpoint, Model A and the router |
| `b2f2ba4` | 2025-12-07 17:09:39 | Fix Dockerfile and ignore notebooks |
| `c7c4ff0` | 2025-12-09 22:59:02 | fixing the image recognition issue for rubbish data |
| `122e026` | 2025-12-12 17:05:14 | Model B has been enhanced via evolution training — **the released checkpoint** |
| `9038f35` | 2026-01-30 18:25:35 | modify the entire UI design and added a database |
| `dc96dd9` | 2026-01-30 18:30:38 | fix the requirement error |
| `5c9f92f` | 2026-02-03 20:15:11 | updated requirement |
| `2588cff` | 2026-02-03 20:22:01 | added missing import module |
| `48e1c4e` | 2026-02-05 20:55:51 | update the design for the analysis view for users — this commit also **replaces `Model A/model_a.pth`**, changing its head set |
| `376437e` | 2026-02-06 12:08:38 | updated setting up requirement |
| `5c2dc35` | 2026-03-01 16:12:17 | evaluation for all model — commits the 12 `runs/detect/val` figures |
| `065dbd4` | 2026-03-30 22:52:43 | restructure the folder structure and added pytest |
| `7210dea` | 2026-04-24 13:04:02 | latest changes — the commit the spec names for the pre-fix dictionary (it carries the dictionary but does not change it) |
| `0b21474` | 2026-08-13 15:55:35 | **Key display names on the model's class registry, not on index** — the fix |
| `2eccc76` | 2026-08-13 15:56:06 | Fall back to CPU when no GPU is present, and stop committing databases |
| `5b815bb` | 2026-08-13 16:02:51 | Ignore the remediation and leakage-audit specs — **the as-submitted commit** |
| `12f3199` | 2026-09-21 21:25:17 | Pre-register the revision R1 analysis plan |
| `aa758e6` | 2026-09-21 21:39:10 | Add the R1 audit scaffold, scripts and reference sets |
| `7239808` | 2026-09-21 21:54:46 | Pin both evaluation environments and read the checkpoints' provenance |

### Surviving August files

The August 2026 working scratchpad
(`/private/tmp/claude-501/-Users-dev1-Desktop-Oral/c5e9d423-…/scratchpad/`) is
**gone**; the entire per-project temp directory no longer exists. What does
survive is the submitted supplementary material, found at
`~/Documents/SEGP Journal/Supplementary-Material.zip` (archive mtime 2026-08-19
02:15, members mtime 2026-08-13 10:19), alongside
`Char-et-al-SUBMISSION.docx`, `Char-et-al-SUBMISSION-PREVIEW.pdf` and
`Figure_1.tif`. Its contents are copied into `audit/results/reference/`.

Note the member timestamp: the supplementary files are dated 2026-08-13 10:19,
which is **before** the class-mapping fix at 15:55 the same day. The audit
evidence therefore predates the fix, which is consistent with the manuscript's
account of the sequence.
