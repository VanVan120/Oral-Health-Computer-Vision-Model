# Revision R1 progress log

Append-only. Resume from the last entry if the session dies.

## Phase 0.0 — plan commit (DONE)

- Branch `revision-r1` created from `main` @ 5b815bb8e7f873f6e11771c55af12c3e7598d506.
- `ANALYSIS_PLAN_R1.md` = Appendix A of revision-analysis-spec.md, verbatim
  (spec lines 392-473, byte-identical, verified by diff).
- Commit: 12f3199e0669565b35fe663e3b9bc6fe993cc3a7
- ISO timestamp (author == committer): 2026-09-21T21:25:17+08:00
- Pushed to origin/revision-r1: YES

## Phase 0.2 — weights (DONE, PASS)

- git-lfs 3.8.0 installed via brew; `git lfs install --local`; `git lfs pull` OK
  (no bandwidth-quota failure). All three weight files were LFS pointers before
  the pull.
- SHA-256, and each equals its committed LFS pointer oid:
  - best.pt            4de8714f0f2b52a70564cc1be55058262564ced400cd8a7d5815192477aad0cc
  - model_a.pth        b469110a551aa4bb93189b05a424fa28239dc4f710983e779b41acf7a19a2d3f
  - triage_router.pth  59cb5a8d8445927a92b0fd0d502fc56b650a16c1a9be94246bc2d2115088f5e2
- best.pt starts 4de8714f and ends 7aad0cc as the spec requires: MATCH. No STOP.

## Phase 0.3 / 0.4 — datasets and duplicate lists (BLOCKED, partial)

**Evidence folder: FOUND.** Not on the Desktop as the spec expected, but at
`~/Documents/SEGP Journal/Supplementary-Material.zip`. Copied verbatim to
`audit/results/reference/` with `PROVENANCE.md`. Contains S0-S5. So the spec's
"if you cannot find it, ask" does not trigger.

Verified against the published S0 README, all exact:
- S1 = 124 rows / 124 unique test images
- S2 = 259 rows / 259 unique test images
- S2 best-transform tally hflip 85, vflip 74, identity 63, rot180 37 = 259
- S1 is a subset of S2, and S1 == the 124 S2 rows with
  also_found_by_aligned_only = yes
- S1 != the 63 S2 rows with matching_transform = identity  <-- see below
- S4 per-class test instances sum to exactly 9,688
- Class order, confirmed independently by S4 and by the committed
  BoxF1_curve.png legend: 0 calculus, 1 caries, 2 gingivitis, 3 hypodontia,
  4 tooth_discolation, 5 ulcer

**Correction to spec check 0.4.3.** The spec says D's "identity-only subset must
equal S1 (124)". Filtering S2 on matching_transform == identity gives 63, not
124, because for 61 of the 124 images that fall below threshold under identity,
some reflection scores lower still. The S0 README states the correct filter
explicitly. `audit/scripts/near_duplicates.py` now runs two passes -- full
dihedral and identity-only -- and reports both, so the 124 and the 259 are both
recoverable and directly diffable against S1 and S2.

**BLOCKED at 0.3.** The August scratchpad
`/private/tmp/claude-501/-Users-dev1-Desktop-Oral/c5e9d423-.../scratchpad/` no
longer exists (the whole per-project temp directory is gone). No Roboflow export
exists anywhere on this machine -- searched for data.yaml, README.roboflow.txt
and README.dataset.txt across $HOME, /private/tmp and /Volumes: zero hits.
So the datasets must be re-downloaded, which needs ROBOFLOW_API_KEY, which is
**unset**. Ground rule 5 says STOP. `audit/scripts/download_datasets.py` is
written and ready; it reads the key from the environment only and never prints it.

## Phase 5.4 — lineage (PARTIAL, blocked)

universe.roboflow.com returns HTTP 403 to non-browser clients and
api.roboflow.com needs the key, so the fork/source question is unresolved. See
`audit/results/S8_lineage_partial.md`. Search-index evidence is consistent with
reference 8 (tesisdientes/oral-diseases-5ctay-rqpxs) having 4 classes and ~4.2k
images, versus 6 classes and 10,000 in the project actually used.
