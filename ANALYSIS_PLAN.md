# Analysis plan and decision record

Author: AI Foundations (Edward Hickman)

## Question

Is reported weekly study-time category associated with final Portuguese grades
in the UCI Student Performance Portuguese-language sample?

The question, dataset and Spearman approach were proposed before downloading
the CSV. This is a documented educational analysis, not a preregistered study.
The decisions below are recorded before running the completed notebook.
An initial data inspection already revealed the sample size, missingness,
group counts and pooled correlation; no claim of blinded planning is made.

## Primary analysis

- Use only `student-por.csv`; do not combine the mathematics sample, which
  overlaps in students and has fewer than 500 records.
- Preserve the original semicolon-delimited CSV, with 649 records and 33 columns.
- Treat `studytime` as an ordered category, not measured hours: 1 = <2 hours,
  2 = 2–5 hours, 3 = 5–10 hours, 4 = >10 hours weekly.
- Use the final grade `G3`, scored 0–20. Do not exclude zero grades or unusual
  records simply to improve the association.
- H0: population Spearman rank correlation between study-time category and
  final grade is zero. H1: it is not zero. Use a two-sided SciPy Spearman
  test at alpha = .05, with average ranks for ties.
- Report the coefficient and approximate p-value, not only a significance
  decision. The p-value relies on independent student observations and
  appropriate sampling assumptions; this convenience sample cannot establish
  population-wide validity.
- No test selection based on which result is significant and no ML training.

## Descriptions and figures

Use counts for categories; mean, sample SD, median and IQR for final grades.
Figure 1 is the final-grade histogram. Figure 2 compares grade distributions
across ordered study-time categories using boxplots and all observations.
Figure 3 compares mean grades by study-time category within each school,
with each cell's count labeled. Figure 2 most directly addresses the question;
Figure 3 checks whether the pooled pattern conceals school differences.

## Sensitivity analysis

Report each school's Spearman coefficient descriptively, without additional
significance claims. As a secondary diagnostic, rank both variables globally,
center each rank variable within school, and calculate their correlation.
Permute the centered study-time ranks within each school 19,999 times, using
seed 20261119; count absolute statistics at least as large as observed, with
p = (b + 1) / (m + 1). The diagnostic tests within-school exchangeability/no
association, not exactly the primary zero-correlation null.

This controls between-school rank-location differences only; it is not a
cluster-robust analysis, does not control student/family/classroom confounding,
and cannot justify generalization from two schools. Classroom identifiers and
a probability sampling design are unavailable. Both p-values are conditional
on assumptions that cannot be established from this file.

## Sources and integrity

Follow Lusa et al. (2024) for systematic initial data screening and reporting,
not for an inappropriate longitudinal model. Use Schober et al. (2018) to
justify ordinal-data rank correlation and Phipson and Smyth (2010) for the
nonzero Monte Carlo p-value correction. Cite the UCI source and acknowledge
Replit AI assistance. Have the learner review and understand the final work.
