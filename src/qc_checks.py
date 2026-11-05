"""Real threshold-based QC rule engine flagging library-prep issues:
adapter contamination, excessive duplication, and poor coverage
uniformity -- a flat rule list interpreted by a small dispatch table,
following the same reusable rule-engine pattern as this account's
other QC projects."""
from __future__ import annotations

import pandas as pd


def _threshold_violation(df: pd.DataFrame, field: str, max_value: float) -> pd.Series:
    return df[field] > max_value


RULES = [
    {"name": "adapter_contamination", "field": "adapter_contamination_pct", "max_value": 10.0},
    {"name": "excessive_duplication", "field": "duplication_rate_pct", "max_value": 40.0},
    {"name": "poor_coverage_uniformity", "field": "coverage_uniformity_cv", "max_value": 0.5},
]


def run_qc_checks(df: pd.DataFrame) -> dict:
    flags = {}
    for rule in RULES:
        mask = _threshold_violation(df, rule["field"], rule["max_value"])
        flags[rule["name"]] = set(df.loc[mask, "run_id"])
    return flags


def flagged_run_ids(flags: dict) -> set:
    all_flagged = set()
    for s in flags.values():
        all_flagged |= s
    return all_flagged
