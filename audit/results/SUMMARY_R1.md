# Revision R1 summary

Every phase of `revision-analysis-spec.md` has been run. Each number below is
tagged with the file it comes from. Numbers produced by different evaluators or
environments are never compared, and mAP@0.5 is never set beside mAP@0.5:0.95.

Unless stated otherwise, every detector figure comes from one evaluator in one
environment: the Phase 1 cached evaluator, **ultralytics 8.3.231, CPU, FP32,
batch 1**.

Three conclusions in this document **correct earlier conclusions in this same
audit**. They are marked CORRECTION and the superseded claim is stated.

```
PLAN        12f3199e0669565b35fe663e3b9bc6fe993cc3a7
            2026-09-21T21:25:17+08:00
            pushed: YES (origin/revision-r1)
            ANALYSIS_PLAN_R1.md == Appendix A verbatim, byte-identical
            (diff-verified; only the "(none)" placeholder under ## DEVIATIONS
            was replaced, by D1-D5 as they arose)

ENV         both venvs: Python 3.12.13, macOS 26.6.2 arm64, Apple M5, 10 CPUs,
            torch 2.7.1, torchvision 0.22.1, sahi 0.11.15, numpy 2.5.3,
            scipy 1.18.1, pandas 3.0.6, scikit-learn 1.9.1, pillow 12.3.0,
            cv2 5.0.0 (headless), matplotlib 3.11.2; CUDA False, MPS True
            (unused), default dtype float32
            venv 1: ultralytics 8.3.231   venv 2: ultralytics 8.4.118
            torch.get_num_threads() = 4  -- PINNED
            locks differ in 3 lines only: ultralytics, nvidia-ml-py (8.4.118
            only, inert on a Mac), pip (8.3.231 only)
            [audit/env/lock-ul8.3.231.txt, lock-ul8.4.118.txt,
             env-ul8.3.231.json, env-ul8.4.118.json, ENVIRONMENT_NOTES.md]
            The pinned torch installed cleanly; no substitution needed.
            sahi is pinned in requirements.txt as ">=0.11.15" -- a floor, not an
            exact pin; 0.11.15 was installed.

WEIGHTS     best.pt            4de8714f0f2b52a70564cc1be55058262564ced400cd8a7d5815192477aad0cc
            model_a.pth        b469110a551aa4bb93189b05a424fa28239dc4f710983e779b41acf7a19a2d3f
            triage_router.pth  59cb5a8d8445927a92b0fd0d502fc56b650a16c1a9be94246bc2d2115088f5e2
            best.pt starts 4de8714f and ends 7aad0cc: MATCH. No STOP.
            All three equal their committed LFS pointer oids.
            [audit/env/weight-sha256.txt, S12]

IDENTITY    Model B 7000/1500/1500, 9688 instances -- **MATCH**
            Model A 474/44/26 = 544 -- **MATCH**
            D == S2 (259), symmetric difference 0 -- **YES**
            identity-only subset == S1 (124), symmetric difference 0 -- **YES**
            0 background images; per-class test counts match published S4 exactly.
            Both datasets pulled by pinned version in the URL, never "latest".
            [S22, S23]
            Counting note: `cat labels/*.txt | grep -c .` undercounts by one line
            per file (no trailing newlines), giving a spurious 8,189. Count per file.

EXACTNESS   evaluate() vs val(batch=1), on every reported metric including
            per-class P, R, AP50 and AP50-95:
              full split (1500)   max abs diff  0.0   PASS
              ND (1241)           max abs diff  0.0   PASS
              ctrl1 (1241)        max abs diff  0.0   PASS
              ctrl2 (1241)        max abs diff  0.0   PASS
            Exact agreement, not agreement to 1e-9. [S24, S41]
            The first attempt gave 6.158e-08 on ctrl2. Cause found, not tolerated:
            rect=True sorts the dataloader by aspect ratio (338 distinct image
            sizes) and ap_per_class takes float32 cumulative sums, which are
            order-sensitive. Replaying in the validator's own order removes it
            entirely. Both numbers reported.

BATCH       full split, 8.3.231, CPU:
              metric        batch16    batch1     b16 - b1
              P             0.74521    0.74542    -0.00021
              R             0.72836    0.73123    -0.00287
              mAP@0.5       0.77100    0.77094    +0.00006
              mAP@0.5:0.95  0.40103    0.40094    +0.00009
            All four batch-16 values reproduce the spec's expected figures
            (P 0.7452, R 0.7284, mAP50 0.7710, mAP50-95 0.4010) exactly at the
            precision quoted. No deviation. [S28, S41]
            Explains the 0.0025 August discrepancy? **NO.** The batch effect on
            mAP@0.5 is 0.00006 -- about 44x too small. Batch composition is ruled
            out. See VERSION below, which does account for a gap of that size.

CLUSTERS    1,445 connected components over 1,500 test images.
            size 1: 1394, size 2: 47, size 3: 4 (largest 3).
            214 contain a D image, 1,231 do not.
            104 edges from a shared training twin, 59 from test-test duplicates.
            [S25]

HEADLINE    set    images  instances     P        R       mAP@0.5  mAP@0.5:0.95
            All      1500       9688  0.74542  0.73123   0.77094    0.40094
            ND       1241       7413  0.75397  0.72675   0.77194    0.40205
            D         259       2275  0.56268  0.75338   0.66023    0.31508
            D carries 2,275 instances = 9,688 - 7,413, matching published S4's
            contam_instances_orient259 = 2275 exactly.

            per class, full split:
            class               inst  imgs      P        R      AP@0.5  AP@0.5:0.95
            calculus            1465   342   0.6675   0.6007   0.6402    0.2811
            caries              1694   536   0.7741   0.7922   0.8282    0.4361
            gingivitis          1544   297   0.6288   0.5039   0.5537    0.2381
            hypodontia           334   184   0.7067   0.7485   0.7684    0.3507
            tooth_discolation   4153   610   0.7745   0.8304   0.8776    0.5718
            ulcer                498   274   0.9208   0.9116   0.9575    0.5279
            [S24, S29]

REMOVAL     Delta (ND - All) mAP@0.5      = +0.000997  95% CI [-0.01249, +0.01418]
            Delta (ND - All) mAP@0.5:0.95 = +0.001111  95% CI [-0.00738, +0.00957]
            10,000 cluster-bootstrap resamples over 1,445 clusters, stratified by
            whether a cluster contains any D image (214 / 1,231). [S29]

            per-class Delta AP (D - ND), and the recall/precision contrasts with
            cluster-bootstrap CIs, are under CONTRASTS below.

            Removing every duplicated image RAISES mAP@0.5 by one part in a
            thousand, and the interval spans zero.

RANDOM      design        metric        ctrl mean     SD      2.5-97.5%              obs Delta   rank    p      MDE
            stratified    mAP@0.5       -0.002413  0.003911  [-0.00994, +0.00529]   +0.000997   80.7   0.390  0.01095
            stratified    mAP@0.5:0.95  +0.000329  0.002501  [-0.00457, +0.00527]   +0.001111   62.5   0.751  0.00700
            unstratified  mAP@0.5       -0.000339  0.003321  [-0.00678, +0.00612]   +0.000997   65.8   0.688  0.00930
            unstratified  mAP@0.5:0.95  -0.000099  0.002523  [-0.00508, +0.00487]   +0.001111   68.8   0.620  0.00707
            10,000 draws each. p = (1 + #{|dc - median| >= |d - median|}) / (1 + 10000),
            exactly as pre-registered. MDE = (1.96 + 0.84) x SD. [S29, S30]

            Removing THESE 259 images is statistically indistinguishable from
            removing ANY 259. The MDE is the number to quote: this design could
            only have detected ~0.011 mAP@0.5 or ~0.007 mAP@0.5:0.95.

            balance table:
            quantity                              D        control mean
            images                              259        259
            instances removed                  2275       2139.5
            mean instances per image           8.78       8.26
            calculus / caries / gingivitis   455/251/597   365.1/226.3/501.1
            hypodontia / tooth_disc / ulcer  144/825/3     139.1/908.0/0.0

            merged (widened) strata: 22 strata, 2 could not be filled from their
            own bin and were widened, both reported rather than merged silently:
              caries     | >=16 instances : D needs 4,  ND has 0  -> caries | 8-15
              hypodontia | 1 instance     : D needs 26, ND has 25 -> hypodontia | 2-3
            (CORRECTED in addendum R1b item 7: the second stratum is `3|1`, whose
            dominant class index 3 is HYPODONTIA. It was mislabelled caries here.)
            That ND holds NO caries-dominant image with >=16 instances while D
            holds four is itself a composition difference: D is not a random
            sample of the split. Ulcer cannot be balanced at all (D has 3
            instances, controls average 0.0), so ulcer is excluded from CONTRASTS.
            Allocation is greedy against a used-set, so no two strata can draw the
            same image and no stratum is emptied by an earlier one (deviation D5).

CONTRASTS   t_global = 0.2823, from the max of the smoothed mean F1 curve on the
            full split. The committed BoxF1_curve.png legend records 0.285 for the
            original run, whose split, version and batch size are unrecorded --
            a sanity check, not a reproduction. [S32, S9]

            eligible classes: calculus, caries, gingivitis, hypodontia,
            tooth_discolation (ulcer excluded, see balance table above)

            class               AP50_D   AP50_ND   dAP50    dAP50-95
            calculus            0.6253   0.6481   -0.0228   -0.0048
            caries              0.7514   0.8385   -0.0871   -0.0572
            gingivitis          0.5646   0.5495   +0.0151   +0.0124
            hypodontia          0.7992   0.7462   +0.0530   +0.0494
            tooth_discolation   0.8121   0.8909   -0.0788   -0.0908

            dR and dP (D - ND) with cluster-bootstrap 95% CIs, 2,000 resamples:
            class (deployed thr)  dR @ t_global             dR @ deployed
            calculus   (0.25)     +0.025 [-0.057, +0.110]   +0.023 [-0.064, +0.104]
            caries     (0.35)     -0.039 [-0.118, +0.038]   -0.069 [-0.152, +0.011]
            gingivitis (0.30)     +0.074 [-0.021, +0.171]   +0.070 [-0.025, +0.161]
            hypodontia (0.60)     +0.026 [-0.090, +0.142]   +0.003 [-0.144, +0.150]
            tooth_disc (0.40)     -0.049 [-0.104, +0.001]   -0.067 [-0.130, -0.008]

            class (deployed thr)  dP @ t_global             dP @ deployed
            calculus   (0.25)     -0.055 [-0.132, +0.024]   -0.054 [-0.132, +0.022]
            caries     (0.35)     -0.057 [-0.155, +0.032]   -0.053 [-0.149, +0.041]
            gingivitis (0.30)     -0.032 [-0.128, +0.058]   -0.031 [-0.124, +0.062]
            hypodontia (0.60)     +0.010 [-0.108, +0.126]   +0.018 [-0.093, +0.124]
            tooth_disc (0.40)     -0.071 [-0.129, -0.012]   -0.062 [-0.126, -0.007]

            Nine of ten recall intervals include zero, and the only class that
            clears zero does so in the WRONG direction: on tooth_discolation the
            model is worse on duplicated images than on clean ones. This is the
            opposite of what memorisation predicts. MEMORISE explains why.

MEMORISE    (a) M by split, same evaluator:
            split   images  instances     P        R      mAP@0.5  mAP@0.5:0.95
            train     7000      44786  0.87238  0.88620  0.93416    0.61313
            valid     1500       9396  0.73178  0.73121  0.75769    0.38737
            test      1500       9688  0.74542  0.73123  0.77094    0.40094
            All 7,000 training images were evaluated -- the pass took ~11 minutes,
            far inside the spec's two-hour threshold, so no 2,000-image sample was
            needed. The train-test gap is an ordinary overfitting gap, and notably
            validation and test agree closely with each other.

            (b) twin concordance, 259 pairs, normalised-IoU box matching:
                                precision   recall     F1
            class-agnostic       0.6857    0.6721   0.6788
            class-aware          0.6686    0.6554   0.6619
            2,275 test-side boxes vs 2,230 twin-side boxes.
            pairs with IDENTICAL label sets: **57 / 259 = 22.0%**
            box-level class disagreements: 38
            per class (test boxes / twin boxes / matched same class):
              calculus 455/509/291   caries 251/269/180   gingivitis 597/551/367
              hypodontia 144/139/97  tooth_disc 825/762/556  ulcer 3/0/0

            (c) recall vs own labels vs twin labels, at t_global:
            subset                        vs own    vs twin
            all D (n=259)                 0.6844    0.6955
            differing-label subset (202)  0.6717    0.6835
            The model agrees slightly BETTER with the training twin's annotation
            than with the test image's own -- the direction memorisation predicts.

            (d) M(twins, own labels) vs M(D):
            set                     images  instances   mAP@0.5  mAP@0.5:0.95
            training twins             224       1974   0.88202    0.54968
            D                          259       2275   0.66023    0.31508
            The SAME 224 photographs score 0.882 under their training labels and
            0.660 under their test labels. The images are identical up to a
            dihedral transform; only the annotations differ. [S31]

VALID       S7 exported: **256** validation images match a training image under
            the dihedral rule, **120** under identity alone -- exactly the spec's
            expected 256 / 120.
            set              images  instances  mAP@0.5  mAP@0.5:0.95  fitness
            full               1500       9396  0.75769    0.38737     0.42440
            de-duplicated      1244       7179  0.74827    0.38264     0.41920
            delta                                -0.00942   -0.00473   -0.00520
            De-duplicating validation makes it HARDER. [S32]
            CORRECTED (addendum R1b item 6): the fitness figures above used this
            plan's formula 0.1*mAP50 + 0.9*mAP50-95, which is WRONG for the pinned
            ultralytics 8.3.231 -- its DetMetrics.fitness weights are [0,0,0,1],
            so fitness IS mAP@0.5:0.95. Corrected: fitness full 0.38737,
            de-duplicated 0.38264, delta **-0.00473** (deviation D7).
            The sentence "no checkpoint choice turns on it" is WITHDRAWN: it was
            unsupported. The relevant comparison is the SELECTION MARGIN between
            the best and runner-up epoch, which is 0.00111 -- about a quarter of
            the 0.00473 level shift. See the ADDENDUM for why a level shift
            measured on one checkpoint still cannot show how the ranking of epochs
            would change.

PHOTOMETRIC verified: **NO** -- and the tier is therefore DROPPED, exactly as the
            spec instructs ("If they do not, report the result and drop the tier").
            REMOVAL and RANDOM are NOT repeated with D = 322. [S38, S39, S40]
            The candidates separate cleanly from a 600-pair random null (null
            median 1.4038 = r 0.015; screen at r >= 0.90; nothing random comes
            close), but they do NOT form a discrete tier: 280 candidates beyond D
            at r >= 0.90, of which 163 verify at full resolution at r >= 0.95,
            giving 422 rather than the spec's 322. The verified pairs run
            r = 0.9505-0.9965 and the rejected ones stop at 0.9495 -- the groups
            abut, with no gap at any cut, so the tier size is a function of the
            threshold, not a property of the data. No list of the original 63
            exists in the published supplementary, so they cannot be re-verified
            individually; 322 and 63 appear only in the revision spec.
            What is reported instead is the substantive point: relaxing the rule
            by one invariance -- global brightness and contrast -- raises the
            contaminated set from 259 to 422, a **63% increase**. Every duplicate
            count in this manuscript is a lower bound, and this measures how much.

VERSION     full split, batch 16:
            metric        8.3.231    8.4.118   version effect   spec expected
            mAP@0.5       0.770997   0.766830   -0.004167       0.7710 -> 0.7668 OK
            mAP@0.5:0.95  0.401032   0.389203   -0.011828       0.4010 -> 0.3892 OK
            P             0.7452059011127984  identical  0.000000
            R             0.7283569800360402  identical  0.000000

            batch 1:
            set    metric        8.3.231    8.4.118    version effect
            full   mAP@0.5       0.770945   0.766750    -0.004195
            full   mAP@0.5:0.95  0.400938   0.389135    -0.011804
            ND     mAP@0.5       0.771942   0.767119    -0.004823
            ND     mAP@0.5:0.95  0.402050   0.389903    -0.012147
            removal effect under 8.4.118: mAP@0.5 +0.000369, mAP@0.5:0.95 +0.000768
            -- same sign, same order, same conclusion. [S33, S44]
            Each effect is reported per metric; the two metrics are never mixed.

            2.9(3) DECOMPOSITION -- done, and decisive. Across all 1,500 images and
            **61,159 predictions**, the cached tp / conf / pred_cls / target_cls /
            target_img arrays are **bit-identical** between the two versions (max
            abs difference 0.0 on every array, identical shapes and counts).
            Predictions, NMS and letterboxing do not change at all. The ENTIRE
            version effect is in the metric code.
            The change is two lines in compute_ap: 8.3.231 runs the PR curve
            straight from the highest achieved recall r_max to 1.0, so the
            101-point interpolation credits a linear ramp of precision over recall
            the model never reached; 8.4.118 inserts a point at (r_max, 0) first,
            so that region contributes nothing. **8.3.231 overestimates AP;
            8.4.118 corrects it.** The mechanism predicts a larger effect where
            recall is lower, and the effect is 2.8x larger on mAP@0.5:0.95 than on
            mAP@0.5 -- as observed.
            This is the substance of R1.3, and it dwarfs the contamination:
            changing the library moves mAP@0.5 by -0.0042 against the +0.0010 of
            removing every duplicated image. A reader comparing a Table 2 figure
            (8.3.231) with a Table 1 figure (8.4.118) is reading a version
            artefact, not a result.

E2E         REQUEST PATH: one reachable upload endpoint, POST /analyze
            (main.py:194). Router first at softmax 0.95, compared as
            "< threshold rejects", so exactly 0.95 is accepted. THREE gates fire
            before the network: mean brightness < 40, > 250, or std < 15 ->
            "Unknown". The router returns its own exceptions as strings and
            main.py collapses every string that is not Clinical/Histopathological
            into one user message, so an internal failure is indistinguishable
            from an out-of-domain rejection. Deployed per-class thresholds, keyed
            by display name: Ulcers 0.75, Tooth Discoloration 0.40, Caries 0.35,
            Hypodontia 0.60, Calculus 0.25, Gingivitis 0.30; default 0.25.
            "No Issues Detected" when len(detections) == 0 after thresholding.
            screening_result "Normal" is unreachable dead code. [S13, S46]

            PYTEST: **45 passed, 0 skipped.** [S18]
            All six assertion-(iii) tests now run on REAL images (the earlier
            39/6 run predated the dataset; two needed MODEL_B_TEST_SCAN raised to
            1500, because the first 400 images hold no hypodontia detection at
            >=0.60 nor an ulcer detection at >=0.75 -- the two highest deployed
            thresholds). verify_classes.py under the pinned env: "0 of 6 classes
            are reported under the wrong name." [S11]

            AGREEMENT POST-FIX: 11,831 detections mapped, agreement **100%**, and
            100% BY CONSTRUCTION -- after 0b21474 the display name is derived from
            the checkpoint's own names registry, so the old permutation is no
            longer representable.

            PRE-FIX, FULL 7210dea PATH (primary, deviation D2):
              displayed findings, total                      1,994
              displayed findings under a WRONG name          1,464  = **73.4%**
              images with any wrong name                     1,302 / 1,500 = 86.8%
              images where EVERY displayed name was wrong    1,074 / 1,500 = **71.6%**
            PRE-FIX, MAPPING ONLY (secondary, as pre-specified):
              displayed findings, total                      2,106
              displayed findings under a wrong name          1,582  = 75.1%
              images with any wrong name                     1,309 / 1,500
              images where every displayed name was wrong    1,011 / 1,500
            The full path reports FEWER findings (1,994 vs 2,106) because the two
            stricter mis-lookups (calculus judged at 0.35, tooth_discolation at
            0.75) remove more than the three looser ones add. A "finding" is a
            distinct display name on one image, not a box.

            PERMUTATION TABLE, measured (box-level detections):
            idx  true class          displayed PRE-fix      detections  correct?
            0    calculus            Caries                      1,162   NO
            1    caries              Calculus                    1,792   NO
            2    gingivitis          Gingivitis                  1,178   yes
            3    hypodontia          Tooth Discoloration           301   NO
            4    tooth_discolation   Ulcers                      1,962   NO
            5    ulcer               Hypodontia                    413   NO
            Each true class maps to exactly one display name: a clean permutation,
            one transposition (0<->1) and one 3-cycle (3->4->5->3). FIVE OF SIX
            wrong; gingivitis is correct only because index 2 is a fixed point.

            SAHI COUNT: **standard 1500, sahi 0.**
            CORRECTION. An earlier note in this audit (S13) said the Roboflow
            export is 640x640 and every benchmark image therefore takes the SAHI
            branch. **That is wrong and the opposite is true.** The export
            preserves original dimensions: 338 distinct sizes, width 123-644,
            height **33-612**. Height never reaches 640, so NO image satisfies
            `width >= 640 and height >= 640`. SAHI -- a headline feature, and the
            path a full-size phone photograph would take -- is never exercised by
            any reported result. [S46]

            IMAGE-QUALITY GATES, per set (deviation D3):
            set                  n     bright<40  bright>250  std<15  softmax<0.95
            Model B test       1500        3          0         0         341
            Model A histopath   544        0          0         0         134
            COCO128             128        3          0         0         114
            The gates are nearly inert: 6 rejections across 2,172 images, all from
            the dark-image check; the over-bright and low-detail gates NEVER fire.
            The router's behaviour is essentially entirely the softmax threshold.

IMAGE-LEVEL per condition, over all 1,500 test images, Wilson 95% CIs. [S45, S34]
            WITH THE ROUTER (the deployed system):
            condition             reported|present          reported|absent          no-finding|present
            Calculus         280/342 .8187 [.7744,.8559]  41/1158 .0354 [.0262,.0477]  .0673 [.0452,.0989]
            Caries           391/536 .7295 [.6903,.7654]  41/964  .0425 [.0315,.0572]  .1978 [.1662,.2336]
            Gingivitis       213/297 .7172 [.6634,.7654]  45/1203 .0374 [.0281,.0497]  .0808 [.0549,.1174]
            Hypodontia        95/184 .5163 [.4445,.5874]   1/1316 .0008 [.0001,.0043]  .3424 [.2777,.4135]
            Tooth Discol.    481/610 .7885 [.7544,.8191]  74/890  .0831 [.0667,.1031]  .1246 [.1007,.1532]
            Ulcers           100/274 .3650 [.3102,.4235]   0/1226 .0000 [.0000,.0031]  .6241 [.5654,.6794]

            WITHOUT THE ROUTER (detector alone):
            Calculus         293/342 .8567 [.8156,.8899]  48/1158 .0415 [.0314,.0545]  .0058 [.0016,.0211]
            Caries           489/536 .9123 [.8853,.9334]  45/964  .0467 [.0351,.0619]  .0131 [.0063,.0267]
            Gingivitis       233/297 .7845 [.7343,.8275]  46/1203 .0382 [.0288,.0506]  .0000 [.0000,.0128]
            Hypodontia       126/184 .6848 [.6145,.7476]   2/1316 .0015 [.0004,.0055]  .1522 [.1074,.2111]
            Tooth Discol.    544/610 .8918 [.8647,.9140]  84/890  .0944 [.0769,.1154]  .0066 [.0026,.0167]
            Ulcers           196/274 .7153 [.6592,.7655]   0/1226 .0000 [.0000,.0031]  .2664 [.2176,.3217]

            OVERALL "No Issues Detected": **0.2687 [0.2468, 0.2917] with the
            router, 0.0740 [0.0618, 0.0884] without it.**
            CORRECTED (addendum R1b item 4): the with-router 0.2687 is NOT one
            event. It is 0.2293 [0.2088, 0.2513] of images REFUSED by the router
            or a gate -- the user is told the photograph is not a valid oral
            health image -- plus 0.0393 [0.0307, 0.0503] ACCEPTED and then found
            to contain nothing. Only the second is a detector miss. Calling the
            sum a "No Issues Detected" rate overstates the detector's misses by
            about six-fold. Full four-outcome decomposition in the ADDENDUM.

            what the router costs (d reported-when-present):
              Ulcers -0.350 | Caries -0.183 | Hypodontia -0.169
              Tooth Discoloration -0.103 | Gingivitis -0.067 | Calculus -0.038
            The router removes a third of ulcer detections and more than triples
            the rate at which a user with a visible condition is told "No Issues
            Detected". No detector metric in the manuscript includes this: the mAP
            figures describe a component, this table describes the product.
            Ulcers is worst-hit because its deployed threshold (0.75) is the
            highest of any class, so it loses detections at both stages.

            NOT ESTIMABLE from this benchmark, and to be stated as such: the split
            contains no healthy mouths and no patient identifiers, so
            patient-level sensitivity, specificity in healthy mouths, predictive
            values at population prevalence and referral burden cannot be derived
            at any confidence. "Reported when absent" above is per-condition
            within images that all contain some other condition -- it is NOT a
            false-positive rate in a healthy population.

ROUTER      CLASSES: ResNet-18, fc (2, 512), classes ['Clinical',
            'Histopathological'] = index 0, 1, fixed by a hard-coded list in
            triage_inference.py. The checkpoint stores NO class names, so nothing
            would detect a mismatch -- structurally the same hazard as the Model B
            defect, and still unguarded.
            TRAINING DATA: ./dataset, assembled by hand, split 0.8 with seed 42
            into ./dataset_final. NEITHER IS IN THE REPOSITORY AT ANY COMMIT.
            Stored log: 20 epochs, "Best val Acc: 1.000000" -- a training-time
            number on its own split.
            RESULTS BY SET at the deployed threshold 0.95 [Wilson 95%]:
            set                    n     correct                unknown                wrong domain
            Model B test (Clin)  1500  1156 .7707 [.7487,.7912]  344 .2293 [.2088,.2513]   0 [.0000,.0026]
            Model A (Histo)       544   410 .7537 [.7158,.7880]  134 .2463 [.2120,.2842]   0 [.0000,.0070]
            COCO128 (reject)      128   117 .9141 [.8527,.9513]  117                      11 .0859 [.0487,.1473]
            Two findings: it refuses ~a quarter of the system's OWN in-domain
            images (22.9% of the detector benchmark, 24.6% of the histopathology
            set), and it never confuses the two clinical domains but ACCEPTS 8.6%
            of COCO128 -- 10 ordinary photographs routed to the oral detector and
            1 to the histopathology model. [S35, S19]
            OVERLAP KNOWN: **NO -- UNKNOWN, and undeterminable.** The obvious way
            to populate ./dataset is from these same two Roboflow projects, which
            would make this evaluation partly an evaluation on training data. Any
            router number must carry that caveat.

MODEL A     SPLIT REPRODUCED: **YES, exactly.** random_split with
            torch.manual_seed(42) over the 544 pooled images gives 435 / 109.
            Directory order matters and is resolved: SORTED order recovers 96/96
            of the published S5 leaked validation images; os.listdir order
            recovers only 22/96. Sorted order is used. [S36, S42]

            CONFUSION MATRIX (model_a.pth, deterministic transform):
              validation n=109: TN 0, FP 4, FN 0, TP 105  -- **MATCHES stored**
              training   n=435: TN 0, FP 14, FN 0, TP 421 -- **MATCHES stored**

            DOES model_a.pth REPRODUCE THE PUBLISHED FIGURES? **PARTLY -- the
            confusion matrix exactly, the AUC and the count metrics not at all.**
            quantity                  stored (cell 9)   model_a.pth   match
            confusion matrix, both splits   see above      see above   YES exact
            TVNT ROC-AUC, validation          0.6476        0.8310     no
            TVNT ROC-AUC, training            0.9333        0.9554     no
            Mitotic MAE                       0.1436        0.1352     no
            Mitotic R2                       -0.0154       +0.0719     no
            Mitotic exact match               93.58%        93.58%     YES exact
            Mitotic within +-1 / +-2      99.08%/100%   99.08%/100%    YES exact
            Nucleol MAE / R2 / exact   2.0272/0.6887/12.84%  1.7528/0.7445/18.35%  no
            Hyperchrom MAE / R2 / exact 2.1767/0.4834/25.69% 2.0719/0.4380/26.61% no

            WHY: the cause is the evaluation pipeline, not the weights. Cell 6
            builds the dataset with train_transform and never reassigns it:
                full_dataset = OSCCRealDataset(IMG_DIR, CSV_FILE, transform=train_transform)
                # Note: For proper validation, we should use val_transform   <- author's own comment
            random_split returns Subset views of that one object, so the
            VALIDATION loader applies RandomHorizontalFlip, RandomVerticalFlip,
            RandomRotation(15) and ColorJitter at evaluation time. val_transform
            is defined and never used. model.eval() and torch.no_grad() switch
            BatchNorm and dropout but do nothing to the input pipeline.
            Five re-runs of the AUGMENTED path with model_a.pth give validation
            AUCs of 0.7667, 0.7881, 0.6524, 0.7690, 0.6048. **The published
            0.6476 lies inside that spread: it is one draw, not a model
            property.** The deterministic value is 0.8310.
            The pattern is exactly what shared weights under a different input
            transform predict: decisions thresholded at 0.5 are robust (both
            confusion matrices identical), small counts that round to 0 are robust
            (mitotic exact-match identical), continuous quantities move.

            RELATION OF model_a.pth TO model_a_best.pth -- **CORRECTION.**
            An earlier conclusion in this audit said the published metrics
            describe "a checkpoint that no longer exists". That is misleading and
            is withdrawn. The FILE model_a_best.pth is genuinely absent -- not in
            the working tree, not in any of the 62 commits across all refs, not in
            any git object, not in `git lfs ls-files --all`. But its WEIGHTS are
            what model_a.pth contains. Evidence:
              - save calls: cell 8 `torch.save(model.state_dict(), "model_a_best.pth")`
                on validation improvement; cell 9
                `model.load_state_dict(torch.load("model_a_best.pth"))` then
                evaluates; cell 10 `save_path = "model_a.pth";
                torch.save(model.state_dict(), save_path)`.
              - execution counts are CONSECUTIVE: cell 8 = 22, cell 9 = 23,
                cell 10 = 24. Cell 10 ran in the same kernel session immediately
                after cell 9 had already overwritten the in-memory `model` with
                the best weights. So cell 10 did NOT save the final-epoch model;
                it re-serialised the best checkpoint under a second name. The
                comment "# 7. Export Model" and the message "Final model saved to
                model_a.pth" both misdescribe that line.
              - cell 10's stored output confirms the file existed then:
                "Best validation model saved to model_a_best.pth".
              - empirically, re-running model_a.pth reproduces the stored
                confusion matrix on BOTH splits exactly -- implausible for a
                different checkpoint.
              - file sizes and dates: model_a.pth entered at f7e56f7 2025-12-07
                (oid b7393a56, 107,372,550 bytes) and was REPLACED at 48e1c4e
                2026-02-05 20:55:51 (oid b469110a, 55,240,265 bytes) -- the
                deployed one. The size halving is consistent with saving a
                state_dict rather than a pickled model. No commit message in the
                62-commit history mentions model_a_best.pth at all.
            Per instruction, the model_a.pth results ARE treated as the deployed
            model's metrics below.

            DEPLOYED-MODEL METRICS (model_a.pth, validation n=109):
              sensitivity   1.0000  Clopper-Pearson 95% [0.9655, 1.0000]
              specificity   0.0000  Clopper-Pearson 95% [0.0000, 0.6024]
              balanced acc  0.5000
              accuracy      0.9633  == the base rate, exactly
              base rate     0.9633 positive
              ROC-AUC       0.8310  bootstrap 95% [0.6571, 0.9714], 10,000 resamples
              AP positive as target  0.9924
              AP negative as target  0.1872
              MCC           **UNDEFINED** (0/0; TN+FN = 0). sklearn returns 0.0 by
                            convention -- a convention, not a result.
            training n=435: sens 1.0000 [0.9913, 1.0000], spec 0.0000
              [0.0000, 0.2316], bal acc 0.5000, AUC 0.9554 [0.9046, 0.9919],
              AP+ 0.9984, AP- 0.6817, base rate 0.9678.
            Per-image scores for all 544 images: S37.

            **THE CLASSIFIER IS DEGENERATE.** FN = 0 and TN = 0 in both splits:
            it predicts "Abnormal" for every image. AUC 0.83 with specificity 0.00
            is not a contradiction -- the scores carry some ranking information,
            but every score sits above the 0.5 decision threshold, so no image is
            ever called normal. A ranking metric and a fixed-threshold metric
            answer different questions, and only the second describes the product.

            SOURCE-LEVEL COUNTS: 544 images from **228** distinct source
            photographs. Validation: 109 images from **94** sources, so 15 are
            augmented copies of a source already in validation. 96 of 109 have a
            source that also appears in training (the published S5).
            13-UNLEAKED SUBSET: n = 13, **all 13 TVNT-positive**. TN=FP=FN=0,
            TP=13. Sensitivity 1.0000 [0.7529, 1.0000]; specificity, balanced
            accuracy, ROC-AUC and MCC are all **UNDEFINED** on it. The subset
            cannot settle the question it was meant to settle -- a property of the
            split, not of this analysis.

SOURCES     NAME-PATTERN TABLE: every one of the 544 images matches
            `OSCC_400x_<n>_jpg.rf.<32 hex>.jpg`. Source = the stem before ".rf.".
            ALL OSCC_400x? **YES -- 544 / 544, with no exceptions.**
            THE 18 NEGATIVES' SOURCES: the 18 TVNT-negative images come from only
            **8** distinct source photographs --
              OSCC_400x_159 (x3), OSCC_400x_222, OSCC_400x_291 (x3),
              OSCC_400x_317, OSCC_400x_322 (x3), OSCC_400x_349,
              OSCC_400x_366 (x3), OSCC_400x_493 (x3)
            so the effective negative sample size is 8, not 18.
            **All 4 validation negatives (from 3 sources: 291, 322, 493) have
            their source photograph in TRAINING. Zero unleaked negatives exist**,
            so specificity has no unleaked support whatsoever.
            This bears directly on R1.8: the filenames say every image, including
            every "negative", is a 400x field of an OSCC slide. A TVNT "negative"
            therefore means "no mitotic figure, no multiple nucleoli and no
            hyperchromatism were annotated in this field of a cancer slide" -- not
            "normal epithelium". The blinded expert packet (Phase 6.3) was built
            to settle exactly this and is prepared but not sent.
            RAHMAN ET AL. THUMBNAIL MATCH: **NOT ATTEMPTED** (optional in 4.2).

R2          FUNCTION: sklearn.metrics.r2_score(targets, preds_clipped), cell 9
            line 151, guarded by np.var(targets) > 0, predictions clipped at 0.
            REFERENCE MEAN: the mean of the y_true passed in -- the evaluation
            set's OWN mean. A validation R2 and a training R2 are therefore
            referenced to different means and are not comparable.
            Stored validation Mitotic R2 = -0.0154, i.e. worse than predicting
            that set's own mean. Recomputed on the deployed checkpoint: +0.0719
            (the difference is the stochastic transform, above).

PROVENANCE  best.pt metadata [S10]:
              date 2025-12-12T16:33:59.554724, ultralytics version 8.3.231
              names {0 calculus, 1 caries, 2 gingivitis, 3 hypodontia,
                     4 tooth_discolation, 5 ulcer}
              architecture nc 6, depth 0.67, width 0.75 (YOLOv8m)
              train_metrics (VALIDATION split, GPU, batch 100, 8.3.231):
                mAP50 0.75956, mAP50-95 0.38766, P 0.73058, R 0.73320,
                fitness 0.38766 -- NOT test-split figures; must not be set beside
                the abstract's or Table 1's numbers.
              train_results holds 48 epochs, not 200: with patience 20 the run
                stopped early. Do not describe it as a 200-epoch run.
              The checkpoint's own `version` is 8.3.231, so the revision's pin is
                the TRAINING-TIME library. That carries no implication about
                which version should be used to EVALUATE -- see VERSION.

            FULL train_args OF BOTH DETECTOR CHECKPOINTS (all 105 keys each).
            **`save_dir` is ABSENT from train_args in BOTH checkpoints** -- it is
            not stored by ultralytics in the args dict, so it cannot be reported
            from the weights. The nearest recoverable equivalent is
            `project` + `name`, given below.

            The keys the instruction names explicitly, first:
              key             RELEASED (122e026)                        WARM START (superseded)
              save_dir        <ABSENT>                                  <ABSENT>
              batch           100                                       32
              epochs          200                                       50
              patience        20                                        100
              project         'oral_cancer_screening'                   None
              name            'yolov8m_evolved_final'                   'HPC_Run_Optimized'
              model           'Backend Development/Model B/models/b...  'best.pt'
              data            '/home/hfyic3/Backend Development/Mod...  'oral-diseases-1/data.yaml'
              device          '0'                                       '0'
              workers         16                                        8
              imgsz           640                                       640
              seed            0                                         0
              deterministic   True                                      True
              pretrained      True                                      True
              rect            False                                     False
              optimizer       'auto'                                    'auto'
              lr0             0.01555                                   0.01
              lrf             0.0071                                    0.01

            Complete listing, released checkpoint (best.pt, oid 4de8714f):
              agnostic_nms: False
              amp: True
              augment: False
              auto_augment: 'randaugment'
              batch: 100
              bgr: 0.0
              box: 8.42592
              cache: False
              cfg: None
              classes: None
              close_mosaic: 10
              cls: 0.72633
              compile: False
              conf: None
              copy_paste: 0
              copy_paste_mode: 'flip'
              cos_lr: False
              cutmix: 0.0
              data: '/home/hfyic3/Backend Development/Model B/oral-diseases-1/data.yaml'
              degrees: 0
              deterministic: True
              device: '0'
              dfl: 1.30086
              dnn: False
              dropout: 0.0
              dynamic: False
              embed: None
              epochs: 200
              erasing: 0.4
              exist_ok: True
              fliplr: 0.27883
              flipud: 0.0
              format: 'torchscript'
              fraction: 1.0
              freeze: None
              half: False
              hsv_h: 0.01594
              hsv_s: 0.45409
              hsv_v: 0.48923
              imgsz: 640
              int8: False
              iou: 0.7
              keras: False
              kobj: 1.0
              line_width: None
              lr0: 0.01555
              lrf: 0.0071
              mask_ratio: 4
              max_det: 300
              mixup: 0.0
              mode: 'train'
              model: 'Backend Development/Model B/models/best.pt'
              momentum: 0.89158
              mosaic: 0.98321
              multi_scale: False
              name: 'yolov8m_evolved_final'
              nbs: 64
              nms: False
              opset: None
              optimize: False
              optimizer: 'auto'
              overlap_mask: True
              patience: 20
              perspective: 0.0
              plots: True
              pose: 12.0
              pretrained: True
              profile: False
              project: 'oral_cancer_screening'
              rect: False
              resume: False
              retina_masks: False
              save: True
              save_conf: False
              save_crop: False
              save_frames: False
              save_json: False
              save_period: -1
              save_txt: False
              scale: 0.70338
              seed: 0
              shear: 0.0
              show: False
              show_boxes: True
              show_conf: True
              show_labels: True
              simplify: True
              single_cls: False
              source: None
              split: 'val'
              stream_buffer: False
              task: 'detect'
              time: None
              tracker: 'botsort.yaml'
              translate: 0.09419
              val: True
              verbose: True
              vid_stride: 1
              visualize: False
              warmup_bias_lr: 0.0
              warmup_epochs: 1
              warmup_momentum: 0.80556
              weight_decay: 0.00047
              workers: 16
              workspace: None

            Complete listing, warm start (oid eec5aba9, 2025-12-06):
              agnostic_nms: False
              amp: True
              augment: False
              auto_augment: 'randaugment'
              batch: 32
              bgr: 0.0
              box: 7.5
              cache: False
              cfg: None
              classes: None
              close_mosaic: 10
              cls: 0.5
              compile: False
              conf: None
              copy_paste: 0.0
              copy_paste_mode: 'flip'
              cos_lr: False
              cutmix: 0.0
              data: 'oral-diseases-1/data.yaml'
              degrees: 0.0
              deterministic: True
              device: '0'
              dfl: 1.5
              dnn: False
              dropout: 0.0
              dynamic: False
              embed: None
              epochs: 50
              erasing: 0.4
              exist_ok: True
              fliplr: 0.5
              flipud: 0.0
              format: 'torchscript'
              fraction: 1.0
              freeze: None
              half: False
              hsv_h: 0.015
              hsv_s: 0.7
              hsv_v: 0.4
              imgsz: 640
              int8: False
              iou: 0.7
              keras: False
              kobj: 1.0
              line_width: None
              lr0: 0.01
              lrf: 0.01
              mask_ratio: 4
              max_det: 300
              mixup: 0.0
              mode: 'train'
              model: 'best.pt'
              momentum: 0.937
              mosaic: 1.0
              multi_scale: False
              name: 'HPC_Run_Optimized'
              nbs: 64
              nms: False
              opset: None
              optimize: False
              optimizer: 'auto'
              overlap_mask: True
              patience: 100
              perspective: 0.0
              plots: True
              pose: 12.0
              pretrained: True
              profile: False
              project: None
              rect: False
              resume: False
              retina_masks: False
              save: True
              save_conf: False
              save_crop: False
              save_frames: False
              save_json: False
              save_period: -1
              save_txt: False
              scale: 0.5
              seed: 0
              shear: 0.0
              show: False
              show_boxes: True
              show_conf: True
              show_labels: True
              simplify: True
              single_cls: False
              source: None
              split: 'val'
              stream_buffer: False
              task: 'detect'
              time: None
              tracker: 'botsort.yaml'
              translate: 0.1
              val: True
              verbose: True
              vid_stride: 1
              visualize: False
              warmup_bias_lr: 0.0
              warmup_epochs: 3.0
              warmup_momentum: 0.8
              weight_decay: 0.0005
              workers: 8
              workspace: None

            DIFFERENCES THAT MATTER: the released run used batch 100 (not 32),
            epochs 200 with patience 20 (not 50 with patience 100), and evolved
            hyperparameters (box 8.42592, cls 0.72633, lr0 0.01555, mosaic
            0.98321, fliplr 0.27883) against the warm start's library defaults
            (box 7.5, cls 0.5, lr0 0.01, mosaic 1.0, fliplr 0.5) -- consistent
            with its name, 'yolov8m_evolved_final'. AutoBatch was not used:
            batch is an explicit integer in both.

            WEIGHT HISTORY [S15]:
              Model B/models/best.pt  f7e56f7 2025-12-07 16:48:02  added
                                      oid eec5aba9...97946, 52,022,866 bytes
              Model B/models/best.pt  122e026 2025-12-12 17:05:14  modified
                                      oid 4de8714f...7aad0cc, 52,035,922 bytes
              -> ml_models/...        065dbd4 2026-03-30 22:52:43  rename R100
              Model A/model_a.pth     f7e56f7 2025-12-07 16:48:02  added
                                      oid b7393a56...f19a1, 107,372,550 bytes
              Model A/model_a.pth     48e1c4e 2026-02-05 20:55:51  modified
                                      oid b469110a...9a2d3f, 55,240,265 bytes
              Model Triage/...pth     f7e56f7 2025-12-07 16:48:02  added, never changed
              27 LFS objects in total; both superseded checkpoints were fetched
              and read directly.

            WARM START IDENTIFIED: **YES.** oid eec5aba9, dated 2025-12-06.
              names: IDENTICAL to the released checkpoint.
              ITS DATA: train_args.data = 'oral-diseases-1/data.yaml' -- THE SAME
              dataset directory as the released run. Training exposure therefore
              spans at least two runs, 50 epochs then 48, not the 48 of the final
              run alone.
              It was ITSELF warm-started from a third 'best.pt' (train_args.model
              = 'best.pt') that is NOT in the repository. Origin NOT RECOVERABLE.
              That is the end of the provenance trail.
              OVERLAP WITH TEST: **NOT MEASURABLE.** data.yaml was never
              committed, so it cannot even be established that the two runs used
              the same partition -- only the same directory NAME. Since the
              released run is warm-started from a model trained on a directory of
              that name, any test image that was in the earlier run's TRAIN split
              has been seen in training regardless of the current split. This is
              unquantifiable from the records that exist and must be stated as a
              limitation rather than bounded.

            CLASS ORDER vs THE OLD DICTIONARY: does NOT match. No checkpoint in
            this repository's history has EVER had the old dictionary's order.
            The dictionary was introduced in the FIRST commit f7e56f7 -- the same
            commit that added the warm start it already failed to match -- and
            survived until 0b21474 removed it, about EIGHT MONTHS later. It was
            never a stale copy of a once-valid order; it was wrong when written.

LINEAGE     Resolved from the Roboflow API with pinned versions. [S26]
            Model B: segp-fcn6m/oral-diseases-5ctay-h9oye version 1 --
              10,000 images, 6 classes, CC BY 4.0, one version, **NO
              augmentation**. So its near-duplicates were present in the SOURCE
              UPLOAD; the platform did not create them.
            Model A: segp-fcn6m/oral-cancer-1mnve-n5yij version 2 --
              228 source images expanded to 544 by DECLARED augmentation (3
              versions per image: flips, 90-degree rotations, crop 0-20%).
            REF 8 / 9 CORRECT: **NOT ESTABLISHED, and not refutable either.**
            Neither project exposes a fork/source field through the API, so the
            fork question cannot be answered from the platform. Search-index
            evidence, labelled as such: reference 8
            (tesisdientes/oral-diseases-5ctay-rqpxs) has 4 classes (calculos,
            caries, gingivitis, ulcera) and ~4.2k images -- consistent with the
            revision's claim that it does not describe the six-class,
            10,000-image project actually used. The shared slug stems
            (oral-diseases-5ctay-*, oral-cancer-1mnve-*) are consistent with a
            fork but are a naming inference only, and must be confirmed against
            project metadata before print.

INDEPENDENCE [S17]
            1. Patient IDs?            **NO.** No dataset image carries a subject
               identifier; the schema has User/Appointment/DailyHabitLog/
               GenAIFeedback and stores no image or study. The patient_id at
               core/models.py:16 is the appointment foreign key to an app user and
               never touches an image -- a grep alone gives a false positive here.
            2. Source-photograph IDs?  **YES.** The filename stem before ".rf.",
               materialised as test_source/train_source in S1 and S2 and
               source_prefix in S5, and implemented in near_duplicates.py.
            3. Episode or visit info?  **NO.**
            4. Upstream augmentation?  **YES**, with multiplicities: of S5's 96
               rows, 66 sources have 3 copies in the pool and 30 have 2, spanning
               81 distinct sources, all originating in Roboflow's train partition.
               Confirmed independently by the API: Model A declares 3 versions per
               source image; Model B declares none.
            CONSEQUENCE: the source photograph is the available unit of
            independence and the analyses cluster on it; patient-level clustering
            is impossible. Because the stem catches only augmented copies of one
            FILE, and not one lesion photographed twice, every contamination count
            here is a LOWER BOUND -- quantified in PHOTOMETRIC as at least 63%.

CHRONOLOGY  62 commits across all refs [S16]. 54 by "Your Name
            <youremail@example.com>", an unconfigured identity; 8 by VanVan120.
            Range 2025-12-07 16:48:02 to the submitted tip.
            key commits: f7e56f7 2025-12-07 first commit (introduces the wrong
            dictionary AND the warm start); 122e026 2025-12-12 the released
            checkpoint; 48e1c4e 2026-02-05 Model A replaced; 5c2dc35 2026-03-01
            the 12 runs/detect/val figures; 065dbd4 2026-03-30 restructure;
            7210dea 2026-04-24 carries the pre-fix dictionary; 0b21474 2026-08-13
            15:55:35 the fix; 5b815bb 2026-08-13 16:02:51 as-submitted.
            SURVIVING AUGUST FILES: the August scratchpad is GONE (the whole
            per-project temp directory no longer exists). The submitted
            supplementary survives at ~/Documents/SEGP Journal/
            Supplementary-Material.zip (members dated 2026-08-13 10:19, i.e.
            BEFORE the 15:55 fix, consistent with the manuscript's sequence),
            alongside the submission .docx, its PDF preview and Figure_1.tif.
            The August offline evaluator's CODE is not in the repository at any
            commit, so its 0.7643 cannot be re-derived -- only bounded, as under
            BATCH and VERSION.

PACKAGING   audit/ tree:
              audit/README.md              what each script does, in order
              audit/run_all.sh             regenerates every number in results/
              audit/env/                   2 locks, 2 env records, weight-sha256,
                                           ENVIRONMENT_NOTES.md
              audit/scripts/               19 files (17 .py, 2 .sh)
              audit/results/               this file, PROGRESS.md, S2, S7-S46,
                                           reference/ (S0-S5 + PROVENANCE.md)
            run_all.sh TESTED: **YES, end to end**, in the form actually used --
            0.1-0.4 and 1.x directly, then 2.2-4.1 through run_remaining.sh, then
            2.8, 3.2 and 6.3. Every step is idempotent (skips when its output
            exists), so it was re-entered safely after interruptions. bash -n
            clean. Two scripts that produce committed results
            (checkpoint_metadata.py, model_a_classifier_metrics.py) were NOT
            reachable from run_all.sh and have been wired in, so the claim that it
            regenerates every number is now true.
            commit hashes on revision-r1, oldest first:
              12f3199  Pre-register the revision R1 analysis plan
              aa758e6  Add the R1 audit scaffold, scripts and the as-published reference sets
              7239808  Pin both evaluation environments and read the checkpoints' provenance
              f68e14f  Trace the request path, the class-mapping defect and the full weight provenance
              47d1f9a  Report the histopathology findings, the router, and the R1 summary
              e8fdd91  Land the datasets, regenerate D exactly, and add the Phase 1-4 analysis code
              5eb022d  Reproduce Model A on the deployed checkpoint and resolve the lineage
              a4ad95b  Bring audit/README.md and run_all.sh up to the full pipeline
              0cc2120  Photometric tier: verifies against the null, but does not reproduce at 322
              2c5731a  Run Phases 1, 2 and 4.1: exactness gate, contamination statistics, Model A
              d52b1b2  Phase 2.9: the ultralytics version effect is entirely in the metric code
              abb3e29  Phase 3 end to end, and the R1 summary
              3cad249  Record the final commit list and apply the v1.1-r1 tag
                       <- tag v1.1-r1 points here, and is NOT moved
              81f8b8f  Addendum R1b: ten follow-ups, and a null that turns out
                       to be a cancellation
              <tip>    Record the R1b commit list and apply the v1.1-r1b tag
            (the last entry is this file's own commit, so it cannot name its own
            hash; the tag v1.1-r1b points at it and the hash is in the hand-off)
            zip, addendum: ~/Desktop/audit-results-R1b.zip
            tag: v1.1-r1 at the final commit. Branch and tag pushed normally;
            never force-pushed, no history rewritten. The merge into main is left
            for the human.
            zip: ~/Desktop/audit-results-R1.zip  (audit/results/ only)
            NOT COMMITTED, by ground rule: any dataset image. The expert packet
            lives in the scratchpad at r1-scratch/work/expert_packet/.
```

## UNFINISHED, and why

1. **Rahman et al. thumbnail match** (Phase 4.2, marked optional). Not attempted.
   The source images are 400x histopathology fields with no distinguishing
   metadata, and the comparison would rest on a visual match to figures in
   another paper that this audit has no licensed copy of.
2. **Overlap between the warm start's training data and the test split**
   (Phase 5.3). Not measurable, not merely unmeasured: `data.yaml` was never
   committed, so the earlier run's partition is unrecoverable. Recorded as a
   limitation under PROVENANCE rather than estimated.
3. **The router's training-data overlap** (Phase 3.5). Same situation:
   `./dataset` was never committed. UNKNOWN and undeterminable.
4. **The August offline evaluator's 0.7643** cannot be re-derived: its code is
   in no commit. Bounded rather than reproduced.
5. **The photometric tier's original 63 pairs** cannot be identified: no list
   exists in the published supplementary, so they cannot be individually
   re-verified. The tier is dropped per the spec's own instruction.
6. **Reference 8/9 fork confirmation** needs project metadata Roboflow does not
   expose through the API.

Nothing was run and then hidden. Every analysis the spec asked for either
produced a number above or appears in this list with the reason it could not.

## UNEXPECTED

Everything found that the spec did not anticipate, ordered by how much it
matters to the manuscript.

1. **The ultralytics version moves the headline metric about four times as much
   as the contamination does** (−0.0042 mAP@0.5 against +0.0010), and the
   predictions are provably identical — 61,159 of them, bit-for-bit. The entire
   effect is a two-line change in `compute_ap`: 8.3.231 credits AP for a linear
   precision ramp over recall the model never achieves, and 8.4.118 fixes it.
   The older version overestimates AP. This is the real content of R1.3.

2. **The contamination has no detectable effect on the headline metric, and the
   study was never powered to find one.** Δ mAP@0.5 = +0.001 [−0.012, +0.014],
   randomization p = 0.39–0.69, MDE ≈ 0.011. Removing *these* 259 images is
   indistinguishable from removing *any* 259. The manuscript's framing needs to
   change from "leakage inflated the metric" to "leakage is present, its effect
   is below what 1,500 test images can resolve, and here is the bound".

3. **Only 22% of duplicate pairs carry the same labels.** The same photograph
   appears in train and test with *different* annotations 78% of the time, and
   the same 224 photographs score mAP@0.5 0.882 under their training labels
   against 0.660 under their test labels. The contamination is an annotation-
   consistency problem, not a leaderboard-inflation problem — and that is a
   *better* finding, because it is large and well-estimated.

4. **SAHI is never exercised by any reported number.** Height in the test split
   never reaches 640 (range 33–612), so the sliced path is unreachable on this
   data. A full-size phone photograph — the intended input — takes a code path
   the entire evaluation leaves untested. (This also corrects an earlier claim
   in this audit that said the opposite.)

5. **The deployed router refuses about a quarter of the system's own in-domain
   images** (22.9% of the detector benchmark, 24.6% of the histopathology set)
   and accepts 8.6% of COCO128. It more than triples the "No Issues Detected"
   rate (7.4% → 26.9%) and costs 35 points of ulcer sensitivity. No detector
   metric in the manuscript reflects any of this.

6. **Model A's published AUC is one draw from a random process, not a model
   property.** The validation loader inherits `train_transform` — random flips,
   rotation, colour jitter at evaluation time — because `val_transform` is
   defined and never assigned, with the author's own comment noting it. Five
   re-runs give 0.6048–0.7881; the published 0.6476 sits inside. The
   deterministic value is 0.8310.

7. **`model_a.pth` is `model_a_best.pth`.** Consecutive execution counts show
   cell 10 saved the in-memory model that cell 9 had just loaded from the best
   checkpoint. The file is missing; the weights are not. *This audit's own
   earlier conclusion that the published metrics describe an unrecoverable
   checkpoint was wrong and is withdrawn.*

8. **Every histopathology image is an OSCC field, including all 18 "negatives"**
   — 544/544 match `OSCC_400x_*`. A TVNT negative means "no feature was
   annotated in this field of a cancer slide", not "normal epithelium". This is
   R1.8's question, and the filenames answer it.

9. **The 18 negatives come from only 8 source photographs, and all 4 validation
   negatives are leaked from training.** There are *zero* unleaked negatives, so
   specificity — already 0.0000 — has no unleaked support at all. The
   13-image unleaked subset is entirely positive, so it cannot measure
   specificity either.

10. **The histopathology classifier is degenerate**: TN = 0 and FN = 0 in both
    splits, specificity 0.0000, balanced accuracy 0.5000, accuracy exactly equal
    to the base rate, MCC undefined. An AUC of 0.83 alongside specificity 0.00
    is not a contradiction; it means every score sits above the 0.5 threshold.

11. **The wrong class dictionary was never right.** It entered in the very first
    commit, alongside a checkpoint whose class order it already failed to match,
    and no checkpoint in the repository's history has ever had its order.

12. **The pre-fix defect changed thresholds as well as names**, because the
    threshold table is keyed by display name. It reported *fewer* findings
    (1,994 vs 2,106), not merely mislabelled ones, so the spec's mapping-isolated
    estimand is a lower bound. 71.6% of images showed only wrong names.

13. **The warm start used the same dataset directory** and was itself
    warm-started from a third checkpoint that no longer exists, so training
    exposure spans at least two runs and the provenance trail does not close.
    `data.yaml` was never committed, so the partition cannot be checked.

14. **`save_dir` is absent from `train_args` in both detector checkpoints.**
    ultralytics does not store it there, so the output directory cannot be
    recovered from the weights; only `project` + `name` survive.

15. **`best.pt` records `batch: 100` and 48 of 200 epochs.** The run was not a
    200-epoch run, and AutoBatch was not used. The warm start used batch 32,
    50 epochs, patience 100 and library-default hyperparameters.

16. **Importing ultralytics before torch silently drops CPU threads from 4 to 1**
    (`ultralytics/__init__.py` sets `OMP_NUM_THREADS=1` when unset). Threaded
    reductions are order-sensitive and the Phase 1.2 gate compares at 1e-9, so
    this could have failed the gate for reasons unrelated to the evaluator, or
    passed on one machine and failed on another. Now pinned explicitly.

17. **The two venvs shared one global ultralytics `settings.json`** and rewrote
    each other's schema — mutable shared state in the middle of a comparison
    whose whole purpose is to isolate the library version. Each venv now has its
    own `YOLO_CONFIG_DIR`.

18. **PIL draft mode silently loses 12% of the duplicate set.** The DCT-scaled
    decode pads JPEG blocks asymmetrically, so a reflected copy lands on a
    different pixel grid and reflected matches vanish: 228 pairs instead of 259.
    One pair traced end to end: RMS 6.9408 with draft mode, 0.3903 without — the
    latter exactly the published value. Recorded as deviation D4.

19. **Float32 `cumsum` in `ap_per_class` is order-sensitive, and `rect=True`
    makes the order non-obvious.** The dataloader sorts by aspect ratio and this
    split has 338 distinct image sizes, so replaying cached metrics in filename
    order differs from validator order by 6.158e-08 — above a 1e-9 gate. Not
    tolerated; diagnosed and eliminated.

20. **Two OpenCV distributions are installed at once** (`opencv-python` 4.7.0.72
    and `opencv-python-headless` 5.0.0.93). They ship the same `cv2` package, so
    one silently overwrites the other; headless 5.0.0 wins here. Nothing pins
    which.

21. **Spec check 0.4.3 as written would fail.** "Identity-only subset" has to
    mean below-threshold-under-identity (124), not best-transform-is-identity
    (63). Recorded as deviation D1.

22. **ND contains no caries-dominant image with ≥16 instances while D contains
    four**, so one stratum could not be matched from its own bin at all. D is
    not a random sample of the split — a fact the balance table makes visible
    and which no single summary statistic would have shown.

23. **The supplementary uses two different naming schemes.** `S0_README.txt`
    calls the files `modelB_124_aligned_pairs.csv` etc., and the spec follows the
    README, but the archive members are named `S1_…` through `S5_…`. Same files;
    the S4 "ALL" row has 9 fields against a 10-field header.

24. **Two user-visible display defects**, neither affecting any metric: a result
    of "Issues Detected" has no i18n key in any of the four languages, so the
    user is shown the literal string `screeningResultIssuesDetected`; and
    `screening_result = "Normal"` is unreachable dead code.

25. **The router cannot be distinguished from a broken router** from the outside:
    it returns its own exceptions as strings and `main.py` collapses every
    unrecognised string into the same "not a valid oral health image" message.

26. **Two of the three image-quality gates never fire.** Across 2,172 images the
    over-bright (>250) and low-detail (std<15) gates reject nothing; the dark
    gate rejects 6. The router's behaviour is essentially entirely its softmax
    threshold.

27. **The router checkpoint stores no class names**, so a class-order mismatch
    there would be undetectable — structurally the same defect as Model B's,
    still unguarded, in the component that gates every request.

---

# ADDENDUM R1b

Ten follow-ups, run 2026-09-22 on the existing caches. **No new inference was
performed**: every number below comes from the Phase 1 caches, the box caches,
the published CSVs, the checkpoint, or the image files.

**Scope.** Earlier sections are unchanged except for the three corrections
explicitly requested — item 4 (IMAGE-LEVEL), item 6 (VALID) and item 7 (RANDOM),
each marked CORRECTED in place. Everything else is appended here. Where a result
here supersedes an earlier table, it says so.

**Pre-registration.** Deviations **D6** (contrast resamples and point estimate),
**D7** (the plan's fitness formula is wrong for the pinned ultralytics) and
**D8** (which of these analyses are exploratory) are recorded in
`ANALYSIS_PLAN_R1.md`. Items 1, 2, 3, 8 and the item-4 decomposition are
**EXPLORATORY**: they are not in the pre-registered plan.

**Adversarial review.** Items 1 and 2 were independently re-checked by three
adversarial agents, one of which returned a **fatal** objection to the first cut
of item 2. That objection was correct, is adopted below, and changes the
headline. The checks and the numbers were then re-derived independently
(`S52_addendum_robustness.json`); the agents' figures are not taken on trust.

```
ITEM 1  TWIN CONCORDANCE, TRANSFORM CHECK  [S47, S48, S52]  — EXPLORATORY

  Method: both images greyscale, resized to 256x256, RMS over all 8 dihedral
  transforms. The transform maps TEST -> TRAIN, so its inverse carries the
  twin's boxes into the test frame. The algebra was verified pixel-exhaustively
  against the array operations, including group closure and both-sided
  inverses.

  CROSS-TAB, thumbnail transform (row) vs full-resolution transform (col):

                 identity   hflip   vflip  rot180
      identity         59       0       0       0
      hflip             0      80       0       0
      vflip             0       0      77       0
      rot180            0       0       0      43

  Perfectly diagonal: 259/259 agree. No pair resolves to rot90, rot270,
  transpose or transverse.

  IDENTICAL PIXEL DIMENSIONS:  258 / 259
  SAME ASPECT RATIO (+-1%):    259 / 259
  The single dimension mismatch is 612x375 against 295x180 — the same picture at
  two scales (aspect ratios 1.6320 and 1.6389, 0.42% apart).

  HOW MUCH DOES THE 259/259 ACTUALLY PROVE? Less than it looks, and this is
  reported because the first draft of this addendum overstated it.
  The argmin is not close: the runner-up transform's RMS exceeds the winner's by
  at least 22.12 units on a 0-255 scale (median gap 43.02), a ratio of at least
  3.64 (median 25.29). ZERO pairs have a ratio below 2. Thumbnail and
  full-resolution resolutions could scarcely have disagreed, so this is a
  consistency check, not independent corroboration.

  WHERE THE REAL INSTABILITY IS. Against the PUBLISHED S2:
      same transform as published    225 / 259
      same train image as published  222 / 259
      same twin but different transform    0 / 259
      published transform recovered when run on the published pairing  37 / 37
  So the transform RULE is fully reproducible — given the same twin it returns
  the same answer, and it reproduces the published transform on the published
  pairing every time. The irreproducible step is WHICH training image is
  nearest: on the 37 disagreeing pairs the competing twins differ in RMS by a
  median of 3.8%, and 22 of 37 are within 10% of each other. D is stable as a
  SET of test images (symmetric difference 0 against S2); the per-pair
  assignment is not, and the transform column should not be leaned on.

  2.6(b) RECOMPUTED with the full-resolution transform, greedy IoU >= 0.5:

                        precision  recall     F1
      class-agnostic      0.6857   0.6721   0.6788
      class-aware         0.6686   0.6554   0.6619
      identical label sets  57 / 259 = 22.0%
      2,275 test-side boxes vs 2,230 twin-side boxes

  IDENTICAL to the original 2.6(b), to four decimals. That is expected — the
  transform is the same and all four axis-safe transforms are self-inverse — and
  it settles the question the item was asked to settle: **the annotation
  disagreement in 2.6(b) is not an artefact of a misregistered frame.**

  BY TRANSFORM:
      transform   n   agnostic F1  aware F1  identical  oracle F1
      identity   59     0.7487      0.7452     28.8%     0.7901
      hflip      80     0.6904      0.6586     23.7%     0.6506
      vflip      77     0.6234      0.6101     18.2%     0.6068
      rot180     43     0.6444      0.6277     16.3%     0.6558

  ORACLE UPPER BOUND — the best class-aware box F1 each pair could reach under
  ANY of the four transforms the published rule can produce:
      per-pair F1 at the chosen transform  0.6690
      per-pair F1 at the best transform    0.6702
      mean gain                            +0.0013
      pairs where a different transform would help      2 / 259
  Registration is not the limiting factor. Even an oracle that picked the best
  transform per pair would move concordance by about one part in a thousand.
  (This bound is over the four transforms the published rule emits, not over all
  eight; all 259 pairs resolve to those four, so it is valid as stated.)

  UNDER THE PUBLISHED PAIRING instead of the regenerated one: class-agnostic F1
  0.6983, class-aware 0.6846, identical label sets 22.8% — the same picture.

ITEM 2  MODEL CONSISTENCY vs LABEL CONSISTENCY  [S47, S52]  — EXPLORATORY

  Class-aware box F1, greedy matching at IoU >= 0.5, at t_global = 0.2823,
  twin boxes and twin predictions mapped through the full-resolution transform.
  Micro-averaged (pooled counts). 10,000-resample cluster bootstrap over the
  Phase 2.1 components containing a D image.

  contrast                              F1      95% CI
  (i)   predictions D vs predictions twin   0.7875  [0.7590, 0.8157]
  (ii)  labels D vs labels twin             0.6619  [0.6231, 0.7001]
  (iii) predictions D vs D's own labels     0.6798  [0.6450, 0.7134]
  (iv)  predictions D vs twin's labels      0.6839  [0.6461, 0.7205]
  (v)   predictions twin vs twin's labels   0.8006  [0.7686, 0.8312]

  (iv) - (iii) = +0.0041  [-0.0320, +0.0403]

  **THE POOLED (iv)-(iii) IS A CANCELLATION ARTEFACT. DO NOT READ IT AS A NULL.**

  This is the correction an adversarial reviewer forced, and it is the most
  important result in this addendum. best.pt was trained with
  **fliplr 0.27883, flipud 0.0, degrees 0**. The model can only have memorised a
  twin's labels in a frame that training could actually present. So the
  hypothesis is testable on identity and hflip pairs, and NOT testable on vflip
  and rot180 pairs, where the model provably cannot express the preference.

  stratum        transforms          n     (iv)-(iii)   95% CI
  reachable      identity, hflip    139     +0.0736   [+0.0333, +0.1125]
  unreachable    vflip, rot180      120     -0.0809   [-0.1347, -0.0323]
  INTERACTION    reachable - unreachable   +0.1546   [+0.0947, +0.2182]
                 P(interaction <= 0) = 0.0000 over 10,000 resamples
  identity alone (no registration at all, n=59)  +0.0682

  Both stratum CIs exclude zero, in OPPOSITE directions. Pooling them produces
  +0.0041 and the appearance of a null.

  BALANCE CONTROLS — is the unreachable stratum simply harder? No.
      quantity                           reachable  unreachable
      (iii) predictions D vs D's labels    0.6820     0.6770
      (v)   predictions twin vs twin's     0.8003     0.8010
      (i)   predictions D vs predictions   0.8702     0.6881
  The two WITHIN-frame contrasts are indistinguishable across strata. Only the
  CROSS-frame quantities move. That is the signature of a frame-transfer effect,
  not of pair difficulty.

  ROBUSTNESS of the stratified result — the sign holds at every operating point:
      threshold   pooled    reachable  unreachable
      0.05        -0.0066    +0.0258     -0.0451
      0.10        -0.0038    +0.0438     -0.0608
      0.20        -0.0015    +0.0614     -0.0777
      t_global    +0.0041    +0.0736     -0.0809
      0.35        +0.0048    +0.0724     -0.0784
      0.45        +0.0120    +0.0835     -0.0763
      0.60        +0.0162    +0.0793     -0.0605
  The POOLED statistic crosses zero inside this range and its sign depends on
  the threshold — another reason not to report it. The STRATIFIED result is
  positive on reachable and negative on unreachable at all seven thresholds.

  WEIGHTING. 259 pairs cover 224 distinct training twins (29 used twice, 3 three
  times), so micro-averaging pools some twins repeatedly into the (ii)/(iv)/(v)
  denominators while every test image enters once:
      micro-averaged (pooled)              +0.0041
      macro-averaged (per pair)            +0.0003
      micro, one pair per distinct twin    +0.0134
  The pooled figure is weighting-dependent; the stratified contrast is what
  survives.

  MATCHING RULE. The first implementation matched class-agnostically and then
  filtered for class agreement, so a wrong-class pairing could block a
  correct-class one. Re-matched within each class separately:
      (i) 0.7875 -> 0.7923   (iii) 0.6798 -> 0.6819   (iv) 0.6839 -> 0.6861
      (ii) and (v) unchanged;  (iv)-(iii) identical at +0.0041
  Benign, and reported so it is not mistaken for an unexamined confound.

  WHAT (i) > (ii) ACTUALLY SAYS — weaker than it first appears.
  F1 here is the Dice coefficient 2tp/(np+nt), which mixes spatial agreement
  with agreement about HOW MANY boxes there are. Restricting to the 53 pairs
  where both contrasts have equal counts on the two sides:
      all 259 pairs:        (i) 0.7875  (ii) 0.6619   gap +0.1256
      53 equal-count pairs: (i) 0.8769  (ii) 0.8689   gap +0.0080
      P(equal box counts):  model 0.375   annotators 0.328
  Almost the entire gap lives on pairs where the two sides disagree about the
  number of boxes. So "the model is more self-consistent than the annotators
  are" is substantially "the model emits a more reproducible box COUNT" — a
  near-mechanical consequence of thresholding one deterministic scorer at one
  fixed cut on near-identical pixels. It is NOT strong evidence about annotation
  quality, and the earlier draft of this addendum overstated it.

  WHAT ITEM 2 SUPPORTS:
   - On pairs whose frame the training augmentation could reach, the model
     reproduces the TRAINING twin's annotation better than the test image's own,
     by +0.0736 [+0.0333, +0.1125]. That is a memorisation signature, and it is
     mechanistically predicted rather than fished: the stratifying variable is
     fixed by best.pt's own train_args.
   - On pairs it could not reach, the effect reverses.
   - The interaction is +0.1546 [+0.0947, +0.2182] and survives every sensitivity
     check applied.
  CAVEAT, stated plainly: the stratification was chosen AFTER seeing the
  per-transform breakdown. The augmentation rationale is pre-existing and the
  balance controls are clean, but this is an exploratory finding on 259 pairs
  and should be replicated before it carries weight in print.

ITEM 3  VISUAL CHECK, 24 PAIRS  [~/Desktop/concordance_sheets/]  — EXPLORATORY

  3 sheets of 8, seed 20260921, stratified by transform (8 hflip, 7 vflip,
  5 identity, 4 rot180). Left panel: the test image with its own boxes. Right:
  the training twin mapped into the test frame with its boxes. NOT COMMITTED —
  they contain dataset images.

  SAME PHOTOGRAPH: **24 / 24 = YES.** Every twin registers onto its test image
  exactly — same subject, framing, lighting and specular highlights. No pair is
  merely a similar clinical photograph, and no mapping is visibly wrong, which
  is an end-to-end check of the transform algebra by eye.

  LABELS DIFFER: **20 / 24 = YES**, 4 = no. The four that agree (#12, #21, #22,
  #23) are exactly the four the IoU-based flag calls identical — my reading and
  the computed statistic agree on all 24 panels.

   #  tf        test/twin boxes  how the labels differ
   1  rot180     6 / 12   extra boxes in twin; twin adds gingivitis, absent in test
   2  rot180    22 / 21   twin adds calculus; only 8 of 22 boxes match
   3  hflip      2 / 3    extra calculus box in twin
   4  rot180    11 / 11   same classes and counts; one box differs in extent
   5  hflip     13 / 11   missing boxes in twin
   6  hflip     18 / 13   twin omits gingivitis entirely
   7  vflip      9 / 5    twin omits tooth_discolation entirely
   8  identity  12 / 3    twin omits tooth_discolation; 3 boxes against 12
   9  hflip      7 / 7    same counts; 2 of 7 differ in extent
  10  identity   4 / 2    twin omits hypodontia
  11  vflip     19 / 19   same counts; 3 matched boxes carry DIFFERENT classes
  12  vflip      2 / 2    -- identical --
  13  vflip     14 / 8    twin omits gingivitis and tooth_discolation; 2 of 14 match
  14  vflip      4 / 3    one hypodontia box missing in twin
  15  rot180     1 / 8    twin adds calculus and tooth_discolation; 1 box vs 8
  16  identity  11 / 9    missing boxes and differing extent
  17  hflip      1 / 3    test under-annotated: 1 hypodontia box against 3
  18  vflip     22 / 25   extra boxes in twin; 20 of 22 match
  19  identity  14 / 12   twin omits gingivitis
  20  vflip     23 / 29   twin omits caries but adds 6 boxes; 1 class disagreement
  21  hflip      1 / 1    -- identical --
  22  hflip      2 / 2    -- identical --
  23  identity   2 / 2    -- identical --
  24  hflip     13 / 15   twin omits calculus; 3 matched boxes carry different classes

  The dominant failure is a WHOLE CLASS present on one side and absent on the
  other (#6, #7, #8, #10, #13, #19, #20, #24 — 8 of 24), not small
  disagreements about box extent. Two pairs (#11, #24) put a different class on
  the same lesion. The four agreeing pairs are all small: one or two boxes.

ITEM 4  ROUTER OUTCOMES, DECOMPOSED  [S49]  — refinement of 3.4, not a new estimand

  The earlier IMAGE-LEVEL section reported a with-router "No Issues Detected"
  rate of 0.2687. That number adds together two events that mean OPPOSITE things
  to a user: an image the router refused as "not a valid oral health image", and
  an image the router accepted on which the detector then found nothing. Only
  the second is a detector miss. The wording is CORRECTED in place above and in
  S46; the decomposition is here.

  Four mutually exclusive, exhaustive outcomes. Wilson 95% and the pre-specified
  10,000-resample cluster bootstrap (Phase 2.1 components, stratified by whether
  a component contains a D image).

  ALL 1,500 IMAGES
    outcome                          k      prop    Wilson 95%        cluster boot 95%
    rejected by router or gate     344    0.2293  [0.2088, 0.2513]  [0.2090, 0.2498]
    accepted, no finding            59    0.0393  [0.0306, 0.0504]  [0.0294, 0.0495]
    accepted, >=1 finding         1097    0.7313  [0.7083, 0.7532]  [0.7093, 0.7532]
  (With no condition named, outcomes 3 and 4 collapse; "accepted, other findings
  only" is empty by construction.)

  So of the 26.87% shown "No Issues Detected", **85.4% were never analysed at
  all** and 14.6% were analysed and came back clean. Quoting 26.9% as a
  no-finding rate overstates the detector's misses roughly six-fold.

  BY CONDITION PRESENT — proportion [Wilson 95%] (cluster bootstrap 95%):

  Calculus (n=342)
    rejected            0.0614 [0.0405,0.0920] (0.0375,0.0882)
    accepted no finding 0.0058 [0.0016,0.0211] (0.0000,0.0152)
    condition reported  0.8187 [0.7744,0.8559] (0.7758,0.8592)
    other findings only 0.1140 [0.0845,0.1521] (0.0800,0.1500)
  Caries (n=536)
    rejected            0.1866 [0.1559,0.2217] (0.1547,0.2204)
    accepted no finding 0.0112 [0.0051,0.0242] (0.0036,0.0207)
    condition reported  0.7295 [0.6903,0.7654] (0.6916,0.7663)
    other findings only 0.0728 [0.0537,0.0979] (0.0520,0.0952)
  Gingivitis (n=297)
    rejected            0.0808 [0.0549,0.1174] (0.0512,0.1128)
    accepted no finding 0.0000 [0.0000,0.0128] (0.0000,0.0000)
    condition reported  0.7172 [0.6634,0.7654] (0.6656,0.7682)
    other findings only 0.2020 [0.1603,0.2514] (0.1572,0.2491)
  Hypodontia (n=184)
    rejected            0.2228 [0.1687,0.2883] (0.1650,0.2849)
    accepted no finding 0.1196 [0.0803,0.1744] (0.0714,0.1706)
    condition reported  0.5163 [0.4445,0.5874] (0.4415,0.5895)
    other findings only 0.1413 [0.0983,0.1990] (0.0932,0.1937)
  Tooth Discoloration (n=610)
    rejected            0.1230 [0.0992,0.1514] (0.0979,0.1495)
    accepted no finding 0.0016 [0.0003,0.0092] (0.0000,0.0051)
    condition reported  0.7885 [0.7544,0.8191] (0.7555,0.8211)
    other findings only 0.0869 [0.0670,0.1119] (0.0651,0.1109)
  Ulcers (n=274)
    rejected            0.5146 [0.4556,0.5732] (0.4558,0.5730)
    accepted no finding 0.1095 [0.0778,0.1520] (0.0744,0.1481)
    condition reported  0.3650 [0.3102,0.4235] (0.3083,0.4225)
    other findings only 0.0109 [0.0037,0.0317] (0.0000,0.0249)

  **THE ROUTER'S REJECTION IS STRONGLY CONDITION-DEPENDENT, AND WORST WHERE IT
  MATTERS MOST.** It refuses 51.5% of ulcer-bearing images against 6.1% of
  calculus-bearing ones — an eight-fold difference, with non-overlapping
  intervals. Ulcers are the condition most likely to need urgent review, and
  they are also the ones the gate in front of the detector discards most often.
  The earlier reading, that ulcer sensitivity is low because the class threshold
  is 0.75, is only part of it: most of the loss happens BEFORE the detector runs.
  Of the 63.5% of ulcer images not reported, four fifths were never analysed.

ITEM 5  PER-CLASS CONTRASTS AT 10,000 RESAMPLES  [S32]  — deviation D6

  **This table REPLACES the CONTRASTS table above**, which used 2,000 resamples
  and reported the bootstrap MEAN in the point-estimate column. The plan
  specified 10,000, and the point estimate should be the observed difference.

  Observed D minus ND, with percentile cluster-bootstrap 95% CIs, 10,000
  resamples. t_global = 0.2823.

  class (deployed thr)   dRecall @ t_global        dRecall @ deployed
  calculus   (0.25)      +0.0245 [-0.0592,+0.1090]  +0.0221 [-0.0613,+0.1065]
  caries     (0.35)      -0.0367 [-0.1221,+0.0374]  -0.0673 [-0.1576,+0.0108]
  gingivitis (0.30)      +0.0715 [-0.0198,+0.1657]  +0.0680 [-0.0249,+0.1649]
  hypodontia (0.60)      +0.0270 [-0.0924,+0.1463]  +0.0029 [-0.1399,+0.1471]
  tooth_disc (0.40)      -0.0483 [-0.1050,+0.0013]  -0.0669 [-0.1290,-0.0116]

  class (deployed thr)   dPrecision @ t_global     dPrecision @ deployed
  calculus   (0.25)      -0.0547 [-0.1327,+0.0230]  -0.0538 [-0.1298,+0.0207]
  caries     (0.35)      -0.0568 [-0.1555,+0.0345]  -0.0511 [-0.1493,+0.0401]
  gingivitis (0.30)      -0.0333 [-0.1257,+0.0572]  -0.0327 [-0.1250,+0.0616]
  hypodontia (0.60)      +0.0108 [-0.1098,+0.1282]  +0.0177 [-0.0905,+0.1245]
  tooth_disc (0.40)      -0.0695 [-0.1322,-0.0150]  -0.0605 [-0.1220,-0.0073]

  Bootstrap mean minus observed, deployed thresholds: calculus +0.00099,
  caries -0.00212, gingivitis +0.00132, hypodontia +0.00061, tooth_disc -0.00102.
  The bias is small, so no conclusion changes — nine of ten recall intervals
  still span zero and tooth_discolation still clears zero in the WRONG direction
  — but the point estimates above are the correct ones.

ITEM 6  VALIDATION  [S32, S53]  — deviation D7

  (a) The sentence "no checkpoint choice turns on it" is WITHDRAWN from the VALID
      section. It was unsupported.

  (b) The plan's fitness formula is wrong for the pinned library. ultralytics
      8.3.231 defines DetMetrics.fitness with
          w = [0.0, 0.0, 0.0, 1.0]   over [P, R, mAP@0.5, mAP@0.5:0.95]
      so **fitness IS mAP@0.5:0.95**. Confirmed against the installed source and
      against best.pt, whose stored fitness 0.38766 equals its stored
      mAP50-95 0.38766 exactly.

      validation set     mAP@0.5    mAP@0.5:0.95 = fitness
      full (1500)        0.75769    0.38737
      de-duplicated(1244) 0.74827   0.38264
      delta              -0.00942   **-0.00473**
      (The plan's formula gave -0.00520. Direction and magnitude unchanged.)

  (c) From best.pt's full train_results — 48 epochs, read from the checkpoint,
      since S10 stored only the first 7 — ranked by validation mAP@0.5:0.95:

        rank  epoch   mAP@0.5:0.95   mAP@0.5
          1     28      0.38766      0.75956   <- the released checkpoint
          2      8      0.38655      0.75886
          3     26      0.38469      0.75435
          4     25      0.38459      0.75771
          5     35      0.38377      0.75385

      **SELECTION MARGIN (best - runner-up) = 0.00111.**

      The relevant comparison is the selection margin, not the level shift. The
      de-duplication level shift is 0.00473 — about **4.3x the margin** that
      separated the chosen epoch from the next one. So the contamination is large
      enough to matter to checkpoint selection in principle.

      **But a level shift measured on one checkpoint cannot show how the ranking
      of epochs would change.** The shift was computed for epoch 28's weights
      only. Whether epoch 8 would overtake epoch 28 on a de-duplicated validation
      set depends on epoch 8's OWN de-duplicated score, which would require that
      checkpoint. Only `best.pt` and one superseded warm start survive; the
      per-epoch checkpoints were never committed. The honest statement is that
      the shift exceeds the margin and the ranking is therefore NOT demonstrably
      safe — not that the ranking would change, and not that it would not.

ITEM 7  STRATUM LABEL  — CORRECTED in place

  The second widened stratum is **`3|1` = HYPODONTIA-dominant, one instance**,
  not caries. Dominant class index 3 is hypodontia. Corrected in the RANDOM
  section above and in S43. The counts (26 needed, 25 available) and every
  downstream number are unaffected; only the class name was wrong. The first
  stratum, `1|>=16`, IS caries-dominant and was labelled correctly.

ITEM 8  VALIDATION PAIRS VERIFIED AT FULL RESOLUTION  [S50, S51]  — EXPLORATORY

  The 256 validation-training pairs from S7 were found by the 32x32 screen. Each
  was re-checked at 256x256 greyscale with per-image standardisation, minimum
  over the dihedral group, against the same random-pair null construction used
  for the test side in S40: 600 random query-train pairs scored identically.
  Decision rule r >= 0.95, the rule S40 used.

  set                     pairs   verified r>=0.95   below the null minimum
  validation               256      **256 / 256**         256 / 256
  test (reference)         259      **259 / 259**         258 / 259

  Pearson r across the 256 validation pairs: min 0.9817, median 0.9990.
  Thumbnail vs full-resolution transform agreement: 256 / 256.
  Null: median z-RMS 1.2615 (r = 0.204), minimum 0.5342 (r = 0.857).

  **All 256 validation pairs verify.** The validation contamination is as real as
  the test contamination; neither is a screening artefact.

  One observation worth recording: the TEST-side null minimum corresponds to
  r = 0.9615, which is above the r >= 0.95 decision rule. A "random" test-train
  pair drawn for the null was itself a genuine duplicate — unsurprising, since
  259 such pairs exist among 1500 x 7000 candidates. The null is therefore
  slightly contaminated by the very effect it calibrates, which biases it
  CONSERVATIVE (it makes real duplicates look less exceptional). It does not
  affect the pass counts, which are decided by the fixed r >= 0.95 rule.

ITEM 9  DEPLOYMENT RECORD  [repository + one read-only HTTP check]

  WHAT THE REPOSITORY RECORDS. All claims verified directly in the working tree
  and in git history.

  SPACE IDENTITY — two spellings of one Space:
    canonical  IvanJun/Oral_AI_Cancer_Disease_Detection   (README.md:13 badge)
    subdomain  ivanjun-oral-ai-cancer-disease-detection.hf.space
               (README.md:20 live-demo link, and main.py:615 as the BASE_URL default)
  URLs:
    https://huggingface.co/spaces/IvanJun/Oral_AI_Cancer_Disease_Detection
    https://ivanjun-oral-ai-cancer-disease-detection.hf.space

  README.md YAML FRONT MATTER, verbatim, lines 1-9 at HEAD:
      ---
      title: Oral AI Cancer Disease Detection
      emoji: 🦷
      colorFrom: blue
      colorTo: green
      sdk: docker
      pinned: false
      app_port: 7860
      ---
  Note what is ABSENT: no sdk_version, no app_file, no python_version, no
  hardware key. `sdk: docker` with `app_port: 7860` means a Docker Space, which
  matches Dockerfile:33 `EXPOSE 7860` and Dockerfile:37
  `CMD ["uvicorn","main:app","--host","0.0.0.0","--port","7860"]`. There is no
  gradio or streamlit anywhere in the tree or in any commit (0 commits match
  either string), so the Space serves the FastAPI app directly.

  DATES (all +0800, from git log --date=iso):
    2025-12-07 16:48:02  f7e56f7  first commit; final.txt line 1 is the intent
                                  "push to hugging face spaces so that its free
                                  for everyone to use it"; Dockerfile already
                                  carries the 7860 comment
    2025-12-07 17:04:18  3f9583a  "Add README.md with Hugging Face configuration"
                                  — the YAML front matter first appears
    2025-12-07 17:44:02  89cc020  "Update email link to use Hugging Face URL" —
                                  main.py BASE_URL default switched from
                                  http://127.0.0.1:8000 to the .hf.space URL
    2025-12-08 23:09:30  a0352b2  badge and live-demo link added to README
    2025-12-08 23:58:54  7930619  README rewritten; the YAML block is DELETED
    2025-12-09 00:04:48  337cdd3  "Restore Hugging Face YAML configuration
                                  metadata" — identical block restored ~6 min later
    2026-03-30 22:52:43  065dbd4  restructure; deletes final.txt
    2026-08-13 15:55:45  46fddfb  last commit on main touching README.md; the
                                  front matter is still present and identical
  No huggingface remote is configured in .git/config (origin is the GitHub repo
  only), and there is no CI workflow, so the repository does not record HOW the
  Space is updated.

  DOES THE URL RESPOND? **YES.** Checked 2026-09-22T03:47Z, read-only, no login,
  nothing modified:
    GET https://ivanjun-oral-ai-cancer-disease-detection.hf.space/
        -> HTTP 200, three consecutive attempts, ~2.9-3.2 s
        response header `server: uvicorn` (consistent with the FastAPI app)
        HEAD -> HTTP 405 with `allow: GET`
    GET https://huggingface.co/spaces/IvanJun/Oral_AI_Cancer_Disease_Detection
        -> HTTP 200
    GET https://huggingface.co/api/spaces/IvanJun/Oral_AI_Cancer_Disease_Detection
        -> HTTP 200; sdk "docker", private false, runtime.stage "RUNNING",
           createdAt 2025-12-07T08:45:24Z, lastModified 2026-04-24T05:04:02Z

  ONE THING THE DATES RAISE, flagged as an INFERENCE and not verified.
  The Space's lastModified is **2026-04-24**. In this repository, 2026-04-24 is
  the date of commit 7210dea — the commit that carries the PRE-FIX class
  dictionary. The fix landed on 2026-08-13 (0b21474). If lastModified reflects
  the last code push to the Space, then **the live public demo may still be
  running the pre-fix mapping and showing five of six conditions under the wrong
  name** — the defect quantified in the E2E section at 73.4% of displayed
  findings. This was NOT confirmed: doing so means reading the Space's files,
  which is beyond the read-only status check requested. It is cheap to settle and
  should be settled before publication, because a live medical-screening demo
  displaying wrong condition names is a patient-facing problem, not a manuscript
  one.

ITEM 10  GENERATIVE AI STATEMENT

  The model that performed this audit and wrote these analyses:
      Model name:  Claude Opus 5 (1M context)
      Model ID:    claude-opus-5[1m]
      Provider:    Anthropic
      Interface:   Claude Code (CLI agent), invoked in this repository
      Dates:       2026-09-21 and 2026-09-22
  Subagents used for the adversarial verification in items 1 and 2 ran under the
  same model ID. Suggested wording for the paper's statement: "Analysis code,
  statistical analysis and the audit report were produced with the assistance of
  Anthropic's Claude Opus 5 (model claude-opus-5) operating as an agent in the
  project repository; all numerical results were regenerated from the committed
  scripts and verified by the authors."
  The authors should verify every figure before publication; this statement
  describes the tool, not a transfer of responsibility.
```

## What changed in the conclusions

1. **Item 2 overturns a null.** The pooled (iv)-(iii) = +0.0041 is a cancellation
   artefact. Split by whether the training augmentation could reach the twin's
   frame, the model reproduces the training twin's labels better than the test
   image's own on reachable pairs (+0.0736 [+0.0333, +0.1125]) and worse on
   unreachable ones (-0.0809 [-0.1347, -0.0323]); interaction +0.1546
   [+0.0947, +0.2182]. This is the clearest memorisation signal in the audit —
   exploratory, post hoc in its stratification, and in need of replication.

2. **Item 4 corrects a misleading headline.** The 26.9% "No Issues Detected"
   rate is 22.9% refused plus 3.9% analysed-and-clean. And the router's refusal
   is condition-dependent in the worst possible way: 51.5% of ulcer images
   against 6.1% of calculus images.

3. **Item 1 closes off the obvious objection to 2.6(b)**, and weakens its own
   evidence honestly: the transform is right, registration is not the limiting
   factor (oracle gain +0.0013), but the 259/259 agreement is a consistency
   check rather than corroboration, and the per-pair PAIRING is only 222/259
   reproducible against the published S2.

4. **Item 6 removes an unsupported claim** and replaces it with the comparison
   that matters: the de-duplication shift (0.00473) is 4.3x the epoch-selection
   margin (0.00111), so the ranking is not demonstrably safe — while noting that
   a shift measured on one checkpoint cannot settle how the ranking would move.

5. **Items 3 and 8 confirm what was already reported**: every sampled pair is
   genuinely the same photograph, 20 of 24 disagree on labels, and all 256
   validation pairs verify at full resolution.

6. **Item 9 surfaces a live-deployment risk** that no earlier phase looked at.
