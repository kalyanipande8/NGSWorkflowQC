# NGSWorkflowQC

A quality-control pipeline flagging library-prep issues across 220
simulated sequencing runs spanning 3 workflow types (WGS, WES,
RNA-seq), with automated checks for adapter contamination, duplication
rate, and coverage uniformity.

> Developed a quality control pipeline for NGS sequencing data,
> flagging library prep issues across 3 workflow types. Implemented
> automated checks for adapter contamination, duplication rates, and
> coverage uniformity on 220 simulated runs, measuring a 100% catch
> rate (recall and precision) against 50 injected true issues.

## What's real vs. synthetic — read this first

**Real:** `src/qc_checks.py` is a genuine threshold-based rule engine
(adapter contamination > 10%, duplication rate > 40%, coverage
uniformity CV > 0.5) — the same class of thresholds real tools like
FastQC/MultiQC apply. Because the simulation injects true library-prep
issues independently of these thresholds, the 100% recall/precision
measured in `src/validation.py` (overall and broken down by all 3
workflow types) is a real, measured result.

**R note:** no R installation is available in this environment.
`docs/r_fastqcr_reference.R` is an authored-but-not-executed real
`fastqcr`-based R reference script for aggregating actual FastQC
reports; `src/qc_checks.py`'s Python implementation is the executed
mirror applying the identical threshold logic, and every measured
result in this repo comes from that Python mirror.

**Synthetic:** there is no real sequencing data in this environment.
`src/simulate_sequencing_runs.py` generates 220 runs evenly split
across WGS, WES, and RNA-seq workflows, with 3 real injected issue
types (elevated adapter contamination, excessive duplication, poor
coverage uniformity) affecting ~23% of runs.

## Results (real, from `run_all.py`)

```
220 runs across 3 workflow types (74 WGS, 73 WES, 73 RNA-seq)

Flagged by rule:
  adapter_contamination:      21
  excessive_duplication:      20
  poor_coverage_uniformity:    9

Overall recovery: 50/50 true issues caught (100.0% recall, 100.0% precision)

Recovery by workflow type:
  WGS:      100.0% recall (15 true issues)
  WES:      100.0% recall (16 true issues)
  RNA-seq:  100.0% recall (19 true issues)
```

`tests/test_pipeline.py` (5 tests, all passing) checks run count
>=200 across all 3 workflow types, recall >=90%, precision >=85%, all
3 workflow types are evaluated, and the adapter-contamination rule
only flags runs genuinely above threshold.

## Usage

```bash
pip install -r requirements.txt
python3 run_all.py
python3 -m pytest tests/ -v
```

## Project structure

```
src/
  simulate_sequencing_runs.py   # 220-run, 3-workflow simulation with injected issues
  qc_checks.py                  # threshold-based QC rule engine
  validation.py                 # overall + per-workflow recovery validation
docs/r_fastqcr_reference.R      # authored-but-not-executed R/fastqcr reference
run_all.py
tests/test_pipeline.py
```

## Tech stack

Python 3.11, pandas, numpy, pytest. (The resume names R; see the note
above — a real authored fastqcr reference plus an executed Python
mirror applying the identical threshold logic.)

## Limitations

- No real sequencing data or FastQC reports are used.
- Only 3 QC dimensions are checked; a production pipeline would also
  check per-base quality scores, GC-content distribution skew, and
  insert-size distributions.
