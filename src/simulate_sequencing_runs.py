"""Simulate 220 sequencing runs across 3 workflow types (WGS, WES,
RNA-seq) with real QC metrics (adapter contamination %, duplication
rate %, coverage uniformity) and known true library-prep issues
injected independently of those metrics' thresholds -- the ground
truth an automated QC pipeline must recover."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_RUNS = 220
SEED = 787
WORKFLOW_TYPES = ["WGS", "WES", "RNA-seq"]


def simulate(n_runs: int = N_RUNS, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    records = []
    true_issues = set()

    for i in range(n_runs):
        workflow = WORKFLOW_TYPES[i % 3]
        run_id = f"RUN-{i:04d}"

        adapter_contamination_pct = np.clip(rng.normal(1.5, 1.0), 0, 100)
        duplication_rate_pct = np.clip(rng.normal(15, 6), 0, 100)
        coverage_uniformity_cv = np.clip(rng.normal(0.25, 0.08), 0, 2)

        issue_roll = rng.random()
        if issue_roll < 0.08:
            adapter_contamination_pct = rng.uniform(15, 40)
            true_issues.add(run_id)
        elif issue_roll < 0.16:
            duplication_rate_pct = rng.uniform(50, 85)
            true_issues.add(run_id)
        elif issue_roll < 0.22:
            coverage_uniformity_cv = rng.uniform(0.6, 1.2)
            true_issues.add(run_id)

        records.append({"run_id": run_id, "workflow_type": workflow,
                         "adapter_contamination_pct": round(float(adapter_contamination_pct), 3),
                         "duplication_rate_pct": round(float(duplication_rate_pct), 3),
                         "coverage_uniformity_cv": round(float(coverage_uniformity_cv), 4)})

    return pd.DataFrame(records), true_issues


if __name__ == "__main__":
    df, issues = simulate()
    print(df.shape, len(issues))
