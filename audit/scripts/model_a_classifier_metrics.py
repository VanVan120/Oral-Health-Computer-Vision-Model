"""TVNT classifier metrics from the stored confusion matrix (spec Phase 4.1.4).

Everything here is a deterministic function of the 2x2 table, so it can be
computed exactly from the notebook's stored outputs without re-running
inference. The quantities that need per-image scores -- ROC-AUC's bootstrap CI
and average precision -- are NOT computed here, because the scores are not
stored. They are reported as blocked rather than approximated.

Clopper-Pearson intervals are exact (Beta quantile) rather than normal
approximations, which matters: with 4 negatives a Wald interval on specificity
would be [0, 0], which is not a claim anyone should make.
"""
from __future__ import annotations

import json

from scipy.stats import beta


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    """Exact two-sided CI for a binomial proportion."""
    if n == 0:
        return (float("nan"), float("nan"))
    lo = 0.0 if k == 0 else float(beta.ppf(alpha / 2, k, n - k + 1))
    hi = 1.0 if k == n else float(beta.ppf(1 - alpha / 2, k + 1, n - k))
    return lo, hi


def analyse(name: str, tn: int, fp: int, fn: int, tp: int) -> dict:
    n = tn + fp + fn + tp
    n_pos, n_neg = tp + fn, tn + fp

    sens = tp / n_pos if n_pos else float("nan")
    spec = tn / n_neg if n_neg else float("nan")
    sens_ci = clopper_pearson(tp, n_pos)
    spec_ci = clopper_pearson(tn, n_neg)
    bal_acc = (sens + spec) / 2

    # MCC denominator is sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN)). Any zero factor
    # makes it 0/0, which is undefined, not zero. sklearn returns 0.0 by
    # convention; that convention is a choice, not a result.
    denom_factors = [tp + fp, tp + fn, tn + fp, tn + fn]
    mcc_defined = all(f > 0 for f in denom_factors)
    mcc = ((tp * tn - fp * fn) / (denom_factors[0] * denom_factors[1] * denom_factors[2] * denom_factors[3]) ** 0.5) if mcc_defined else None

    return {
        "set": name,
        "n": n,
        "confusion": {"TN": tn, "FP": fp, "FN": fn, "TP": tp},
        "n_positive": n_pos,
        "n_negative": n_neg,
        "base_rate_positive": n_pos / n,
        "accuracy": (tp + tn) / n,
        "sensitivity": sens,
        "sensitivity_CP95": sens_ci,
        "specificity": spec,
        "specificity_CP95": spec_ci,
        "balanced_accuracy": bal_acc,
        "mcc": mcc,
        "mcc_note": None if mcc_defined else
            f"undefined: MCC denominator has a zero factor ({denom_factors}); "
            "sklearn.matthews_corrcoef returns 0.0 by convention",
        "predicted_positive_for_every_image": (tn == 0 and fn == 0),
    }


def main() -> None:
    # Read verbatim from the stored outputs of cell 9 of
    # ml_models/model_a/Model_A_Training_Master.ipynb.
    out = {
        "source": "Model_A_Training_Master.ipynb cell 9 stored outputs",
        "results": [
            analyse("validation (n=109)", tn=0, fp=4, fn=0, tp=105),
            analyse("training (n=435)", tn=0, fp=14, fn=0, tp=421),
        ],
        "stored_auc": {"validation": 0.6476, "training": 0.9333},
        "not_computed_here": [
            "ROC-AUC bootstrap CI stratified by class - needs per-image scores, which are not stored",
            "average precision (positive as target, and negative as target) - same reason",
            "source-level counts - needs the 544 images to recover the .rf. stems",
        ],
    }
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
