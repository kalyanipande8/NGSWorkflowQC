import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.simulate_sequencing_runs import simulate, WORKFLOW_TYPES
from src.qc_checks import run_qc_checks, flagged_run_ids
from src.validation import validate_recovery, validate_by_workflow


def test_at_least_200_runs_across_3_workflows():
    df, _ = simulate()
    assert len(df) >= 200
    assert set(df["workflow_type"].unique()) == set(WORKFLOW_TYPES)


def test_qc_checks_catch_most_true_issues():
    df, true_issues = simulate()
    flags = run_qc_checks(df)
    flagged = flagged_run_ids(flags)
    recovery = validate_recovery(df, flagged, true_issues)
    assert recovery["recall_pct"] >= 90.0


def test_clean_runs_mostly_not_flagged():
    df, true_issues = simulate()
    flags = run_qc_checks(df)
    flagged = flagged_run_ids(flags)
    recovery = validate_recovery(df, flagged, true_issues)
    assert recovery["precision_pct"] >= 85.0


def test_all_three_workflow_types_evaluated():
    df, true_issues = simulate()
    flags = run_qc_checks(df)
    flagged = flagged_run_ids(flags)
    by_workflow = validate_by_workflow(df, flagged, true_issues)
    assert set(by_workflow.keys()) == set(WORKFLOW_TYPES)


def test_adapter_contamination_rule_only_flags_true_contamination():
    df, _ = simulate()
    flags = run_qc_checks(df)
    for run_id in flags["adapter_contamination"]:
        value = df.loc[df["run_id"] == run_id, "adapter_contamination_pct"].iloc[0]
        assert value > 10.0
