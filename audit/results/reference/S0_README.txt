TRAIN/TEST CONTAMINATION AUDIT — SUPPORTING DATA
Generated 2026-08-13. All figures regenerated from the datasets, not transcribed.

DATASETS (re-downloaded at pinned versions, verified identical to the training-time
splits by per-split image counts and a test-instance total of 9,688):
  Model A  Roboflow segp-fcn6m/oral-cancer-1mnve-n5yij   version 2   CC BY 4.0
  Model B  Roboflow segp-fcn6m/oral-diseases-5ctay-h9oye version 1   CC BY 4.0

Weights unchanged throughout: best.pt, sha256 4de8714f0f2b52a70564cc1be55058262564
ced400cd8a7d5815192477aad0cc. No model was retrained.

-------------------------------------------------------------------------------
FILES

modelB_124_aligned_pairs.csv                                          124 rows
  Duplicate pairs found by fixed-alignment matching. Each test image is reduced
  to a 32x32 greyscale thumbnail and compared to all 7,000 training thumbnails;
  rms_distance is the minimum RMS grey-level difference (0-255 scale). Accepted
  below 6.0, a threshold placed inside an empty band spanning [3.92, 10.01).
  Columns: test_image, train_image, rms_distance, test_source, train_source
  ("source" = filename before ".rf.", i.e. the pre-augmentation identity.)

modelB_259_orientation_pairs.csv                                      259 rows
  The same detector re-run with the test thumbnail transformed by each element
  of the dihedral group of order 8. This supersedes the 124: 135 of these rows
  are duplicates that fixed-alignment matching cannot see.

  Per-transform yields, counting every transform that put an image below
  threshold (images can qualify under more than one):
      identity 124, hflip 150, vflip 144, rot180 75,
      rot90 0, rot270 0, transpose 0, transverse 0     union = 259
  matching_transform records only the SINGLE BEST-scoring transform per image,
  so its tally differs and is not comparable to the list above:
      hflip 85, vflip 74, identity 63, rot180 37       total = 259
  Both are correct. 124 images fall below threshold under identity, but for 61
  of them some reflection scores lower still, so identity is the best transform
  for only 63. To recover the fixed-alignment set, filter on
  also_found_by_aligned_only = yes (exactly 124 rows), not on
  matching_transform = identity.
  Columns: test_image, train_image, matching_transform, rms_distance,
           also_found_by_aligned_only, test_source, train_source

modelB_orb_sample_200.csv                                             200 rows
  Random sample (seed 7) of the 1,500-image test split, scored by geometric
  matching, which tolerates crop and rescale as well as reflection. ORB with
  1,500 features on images rescaled to 480 px on the long edge; candidates
  reduced to the 60 nearest training images by normalised 8x8x8 BGR colour
  histogram; Hamming brute-force matching under Lowe's ratio test at 0.75;
  RANSAC homography at 5 px reprojection. Accepted at >= 25 inliers.
  165 of 200 accepted = 82.5%, 95% CI [77.2%, 87.8%].
  score_provenance records which rows were scored in the original sampling run
  and which were re-scored for this export under identical parameters.
  Columns: test_image, best_train_match, ransac_inliers, verdict,
           above_threshold_25, score_provenance

modelB_per_class_contamination.csv                                      7 rows
  The counts behind the 1170/9688 figure, per class, under both detectors.
  Instance-level rates exceed image-level rates because contaminated images are
  annotation-dense (9.44 instances each against 6.46 for the split).
  Columns: class_id, class_name, test_instances, test_images,
           contam_instances_aligned124, pct_instances_aligned124,
           contam_images_aligned124, contam_instances_orient259,
           pct_instances_orient259, contam_images_orient259

modelA_leaked_validation_images.csv                                    96 rows
  Model A validation images whose source photograph also appears in training.
  Model_A_Training_Master.ipynb pools Roboflow's three partitions into one flat
  labels.csv (474 + 44 + 26 = 544 images) and re-splits with
  torch.utils.data.random_split under Generator().manual_seed(42) into 435/109.
  Reproduced here exactly. Augmented copies of one source photograph are
  therefore scattered across the new boundary: 96 of 109 validation images
  (88.1%) have a sibling in training, spanning 81 distinct sources.
  Columns: validation_image, source_prefix, roboflow_origin_split,
           total_copies_in_pool, sibling_copies_in_train, sibling_train_images
  Note: Roboflow itself split before augmenting — zero sources span its own
  partitions. The leakage is introduced by the notebook's re-split.

-------------------------------------------------------------------------------
KNOWN LIMITS

All counts are LOWER BOUNDS. None of these methods detects the same lesion
photographed twice from a different angle or session, which would leak
identically. Manual inspection indicates the true Model B rate exceeds 85%:
of the 35 sample images the geometric matcher rejected, the 12 highest-scoring
(15-24 inliers) were inspected and roughly 9 were still duplicates.

The ORB null distribution (600 random test-train pairs: median 0 inliers, 95th
percentile 11, 1.83% at or above threshold) OVERSTATES the false-positive rate,
because random draws occasionally are genuine duplicates in a collection this
saturated and because null pairs are not histogram-matched candidates. It is
reported for completeness and was not used to correct the estimate. Manual
inspection found 18 of 18 accepted pairs genuine across the full inlier range,
including the weakest 25-34 band.
