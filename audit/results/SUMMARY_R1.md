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
              caries | >=16 instances : D needs 4,  ND has 0  -> caries | 8-15
              caries | 1 instance     : D needs 26, ND has 25 -> caries | 2-3
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
            De-duplicating validation makes it HARDER. Model selection used
            fitness; 0.0052 is far smaller than the gap between adjacent epochs in
            the stored train_results, so no checkpoint choice turns on it. [S32]

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
              <tip>    Record the final commit list and apply the tag
            (the last entry is this file's own commit, so it cannot name its own
            hash; the tag v1.1-r1 points at it and the hash is in the hand-off)
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
