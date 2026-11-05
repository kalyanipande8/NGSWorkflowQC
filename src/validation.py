"""Validates the QC rule engine against the simulation's hidden true
library-prep issues, overall and broken down by workflow type --
because the true issues are injected independently of the rule
thresholds, recall/precision here are real, measured results."""
from __future__ import annotations

import pandas as pd


def validate_recovery(df: pd.DataFrame, flagged: set, true_issues: set) -> dict:
    tp = len(flagged & true_issues)
    recall = round(100 * tp / len(true_issues), 2) if true_issues else 100.0
    precision = round(100 * tp / len(flagged), 2) if flagged else 0.0
    return {"n_true_issues": len(true_issues), "n_flagged": len(flagged), "n_true_positives": tp,
            "recall_pct": recall, "precision_pct": precision}


def validate_by_workflow(df: pd.DataFrame, flagged: set, true_issues: set) -> dict:
    results = {}
    for workflow in df["workflow_type"].unique():
        subset_ids = set(df.loc[df["workflow_type"] == workflow, "run_id"])
        sub_flagged = flagged & subset_ids
        sub_true = true_issues & subset_ids
        tp = len(sub_flagged & sub_true)
        recall = round(100 * tp / len(sub_true), 2) if sub_true else 100.0
        results[workflow] = {"n_runs": len(subset_ids), "n_true_issues": len(sub_true), "recall_pct": recall}
    return results
