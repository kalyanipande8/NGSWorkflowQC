import json
import os

from src.simulate_sequencing_runs import simulate
from src.qc_checks import run_qc_checks, flagged_run_ids
from src.validation import validate_recovery, validate_by_workflow


def main():
    df, true_issues = simulate()
    flags = run_qc_checks(df)
    flagged = flagged_run_ids(flags)

    overall = validate_recovery(df, flagged, true_issues)
    by_workflow = validate_by_workflow(df, flagged, true_issues)

    summary = {"n_runs": len(df), "n_flagged_by_rule": {k: len(v) for k, v in flags.items()},
               "overall_recovery": overall, "recovery_by_workflow": by_workflow}

    os.makedirs("results", exist_ok=True)
    with open("results/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
