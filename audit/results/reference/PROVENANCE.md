# Reference sets: the as-published supplementary material

Copied verbatim on 2026-09-21 from
`~/Documents/SEGP Journal/Supplementary-Material.zip`
(archive mtime 2026-08-19 02:15, member mtime 2026-08-13 10:19).

These are the **as-submitted** files. They are the comparison target for spec
check 0.4.3, not an output of this revision. Nothing here was regenerated.

| file | rows | unique test images |
|---|---|---|
| S1_aligned_duplicate_pairs.csv | 124 | 124 |
| S2_orientation_duplicate_pairs.csv | 259 | 259 |
| S3_geometric_sample_200.csv | 200 | 200 |
| S4_per_class_contamination.csv | 7 | n/a (per-class) |
| S5_histopathology_leaked_validation.csv | 96 | 96 (Model A validation) |

## Two naming discrepancies, recorded rather than corrected

1. `S0_README.txt` refers to the files by different names than the archive uses:
   it calls them `modelB_124_aligned_pairs.csv`, `modelB_259_orientation_pairs.csv`,
   `modelB_orb_sample_200.csv`, `modelB_per_class_contamination.csv` and
   `modelA_leaked_validation_images.csv`. The revision spec uses the README's
   names too. The archive members are the `S*_` names in the table above. The
   contents match the README's descriptions exactly, so these are the same five
   files under two naming schemes.

2. The revision spec says D's "identity-only subset must equal S1". Filtering S2
   on `matching_transform == identity` gives **63**, not 124. The correct filter
   is `also_found_by_aligned_only == yes`, which gives exactly **124** and equals
   S1 as a set (verified). The S0 README states this explicitly:

       To recover the fixed-alignment set, filter on
       also_found_by_aligned_only = yes (exactly 124 rows), not on
       matching_transform = identity.

   The reason is that 124 images fall below threshold under identity, but for 61
   of them some reflection scores lower still, so identity is the single best
   transform for only 63. `audit/scripts/near_duplicates.py` therefore runs two
   passes and reports both quantities.

## Verified set relations (this session)

- S1 subset of S2: YES
- S1 == {S2 rows with also_found_by_aligned_only == yes}: YES (124)
- S1 == {S2 rows with matching_transform == identity}: NO (63)
- S2 best-transform tally: hflip 85, vflip 74, identity 63, rot180 37 = 259,
  exactly as the S0 README reports.
