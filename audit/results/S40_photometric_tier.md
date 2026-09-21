# Photometric duplicate tier (spec Phase 2.8) — sensitivity analysis

Raw numbers in `S38_photometric_tier.json`; every candidate pair with its
distances in `S39_photometric_pairs.csv`.

## Method

The published rule compares raw grey levels, so a pair differing only by a
global brightness or contrast change scores far above 6.0 and is invisible to
it. Standardising each thumbnail — subtract its mean, divide by its standard
deviation — removes exactly those two degrees of freedom and nothing else. The
minimum is still taken over the dihedral group, as before.

For two standardised vectors, RMS² = 2(1 − r), so this statistic and the Pearson
correlation are the same information on different scales. That identity is what
makes the null interpretable.

Candidates are then verified at **full resolution** (256×256 greyscale, also
standardised), against a null of 600 random test–train pairs.

## The null separates cleanly; the candidates do not

| quantity | value | as correlation |
|---|---|---|
| null median | 1.4038 | r ≈ 0.015 |
| null minimum over 600 draws | 0.5560 | r ≈ 0.845 |
| null 0.5th percentile | 0.6387 | r ≈ 0.796 |
| screen used | 0.4472 | **r ≥ 0.90** |

Nothing random comes near the screen, so the candidates are not null artefacts.

But the candidates themselves form a **continuum, not a separable tier**:

| stage | count |
|---|---|
| candidates beyond D at r ≥ 0.90 | **280** |
| of those, verified at full resolution at r ≥ 0.95 | **163** |
| rejected (full-resolution r between 0.735 and 0.9495) | 117 |

The verified pairs run from r = 0.9505 to r = 0.9965 and the rejected ones stop
at r = 0.9495. There is no gap anywhere near the cut — the two groups abut. The
size of this tier is therefore a **function of the threshold chosen**, not a
property of the data, which is exactly what the 6.0 threshold in the published
rule avoided by sitting inside an empty band of width 6.

Transforms among the 163: identity 117, hflip 27, vflip 19.

## The spec's 322-image tier does not reproduce

The spec asks to rebuild a 322-image tier — the 259 plus 63 additional pairs —
and to verify those 63.

- The reconstruction finds **163** additional verified pairs, giving a tier of
  **422**, not 322.
- No list of the original 63 exists in the published supplementary, so they
  cannot be identified and re-verified individually. `S0_README.txt` documents
  S1–S5 and describes no photometric tier at all; 322 and 63 appear only in the
  revision spec.
- Because the candidate distribution has no gap, a tier of exactly 63 would
  correspond to a threshold of roughly r ≥ 0.988 — reachable, but chosen after
  the fact to hit a target, which is precisely the kind of choice this audit
  exists to avoid.

**Conclusion.** The tier verifies against the random-pair null but does not
verify as a discrete, threshold-independent set, and it does not reproduce at
the size the spec states. Following the spec's own instruction — *"If they do
not, report the result and drop the tier"* — the 322-image tier is **dropped**,
and analyses 2.3 and 2.4 are **not** repeated with D = 322.

What is reported instead, because it is the substantive point, is a
threshold-sensitivity statement: contamination of the test split by photometric
near-duplicates is **at least** 259 images and plausibly 422 at r ≥ 0.95, with
the count rising smoothly as the criterion loosens. Every duplicate count in
this manuscript is a lower bound, and this is a direct measurement of how much
of a lower bound: relaxing the rule by one invariance — global brightness and
contrast — increases the contaminated set by 63%.

That conclusion does not depend on where the cut is placed, and it is the one
the revision should carry.
