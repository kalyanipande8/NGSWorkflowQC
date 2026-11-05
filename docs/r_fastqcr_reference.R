# Authored-but-not-executed reference: the real R (fastqcr) workflow
# this QC pipeline would run against actual FastQC reports in
# production. No R installation or real FastQC output is available in
# this environment, so src/qc_checks.py implements the identical
# threshold-based flagging logic in Python as the executed mirror, and
# all measured results in this repo come from that Python mirror, not
# from this script.

library(fastqcr)

qc_dir <- "fastqc_reports/"
qc <- qc_aggregate(qc_dir)

qc_summary <- qc %>%
  select(sample, module, status) %>%
  filter(module %in% c("Overrepresented sequences", "Sequence Duplication Levels",
                        "Per base sequence quality"))

flagged_runs <- qc_summary %>%
  filter(status == "FAIL") %>%
  distinct(sample)

write.csv(flagged_runs, "results/flagged_runs.csv", row.names = FALSE)

cat(sprintf("Flagged %d of %d runs for library-prep QC issues\n",
    nrow(flagged_runs), n_distinct(qc$sample)))
