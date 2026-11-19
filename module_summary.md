# Study Time and Portuguese Final Grades

AI Foundations (Edward Hickman)

## Overview

This project examines whether reported weekly study-time category is associated with final Portuguese grades in the UCI Student Performance dataset (Cortez, 2008). It combines descriptive statistics, three visual models, and a two-sided Spearman hypothesis test to distinguish an observed association from a causal claim. The public dataset and variable dictionary are available at https://archive.ics.uci.edu/dataset/320/student+performance.

## Dataset Description

The original semicolon-delimited CSV contains 649 student records and 33 columns from two Portuguese secondary schools, collected through school reports and questionnaires (Cortez, 2008). Each row is a Portuguese-language course record; the overlapping mathematics dataset is not merged or analyzed. The key variables are school (GP or MS), ordered weekly study-time category (studytime), and final grade (G3, 0–20 points), with age, absences and earlier grades included in descriptive summaries. Study-time codes 1–4 mean <2, 2–5, 5–10 and >10 hours, so the codes are not equally spaced measured hours. The audit found no missing cells or exact duplicate rows; all records, including 15 zero grades, were retained.

## Methods

The notebook displays the first rows and data types, checks a SHA-256 fingerprint, and audits missing values, distinct values, category codes, numeric ranges and full-row matches before inference. This structured screening and decision record apply Lusa et al.'s (2024) initial-data-analysis principles. Their article focuses on longitudinal data; the applicable contribution here is systematic screening, not a claim that the present cross-sectional association analysis is longitudinal.

Counts describe nominal and ordinal categories. The grade mean and sample standard deviation summarize center and spread, while the median and interquartile range provide complementary summaries less dependent on extreme observations. The notebook displays df.describe, but does not interpret averages of ordinal study-time codes as actual hours. Figure 1 uses one-point histogram bins for the discrete grade distribution. Figure 2 uses boxplots with every observation overlaid to compare ordered groups and show overlap; Figure 3 displays school-specific cell means and counts to reveal differences hidden by pooling.

The primary test is Spearman rank correlation, appropriate for an ordinal variable and a possible monotonic association (Schober et al., 2018). The null hypothesis is population rho_s = 0; the alternative is rho_s != 0, tested two-sided at alpha = .05. SciPy uses average ranks for ties and reports an approximate large-sample p-value. Paired measurements, meaningful ordering, nonconstant variables and independent observations are required; normal measurement distributions and equal category widths are not required. This convenience sample and possible shared classroom/school influences make the independence and sampling assumptions uncertain.

A secondary sensitivity diagnostic centers both globally ranked variables within each school, then correlates the centered ranks. Study-time ranks are permuted within schools 19,999 times using seed 20261119; the two-sided comparison uses absolute correlations. The Monte Carlo p-value is (b+1)/(m+1), with b counting resampled statistics at least as extreme as observed; this avoids reporting zero (Phipson & Smyth, 2010). The diagnostic's null is within-school exchangeability/no association, not exactly the primary zero-correlation null. It removes between-school rank-location differences but is not a cluster-robust analysis or a control for all confounding. School-specific coefficients are reported descriptively, without separate significance claims.

## Results

The overall grade mean was 11.91, sample SD 3.23, and median 12, with quartiles 10 and 14 (IQR 4). Figure 1 shows the distribution of all 649 grades, including 15 zero grades. Figure 2 compares the four categories: <2 hours: n=212, mean=10.84, median=11; 2–5 hours: n=305, mean=12.09, median=12; 5–10 hours: n=97, mean=13.23, median=13; >10 hours: n=35, mean=13.06, median=13. The increasing medians coexist with substantial overlap, and the mean in the >10-hour group is slightly lower than in the 5–10-hour group.

The primary test statistic was rho_s = 0.274712, with two-sided approximate p = 1.06062e-12 (n=649). Thus H0 is rejected at .05 if the test assumptions hold. The positive coefficient, far from one, and overlapping grade distributions matter more for interpreting the pattern than the threshold decision alone (American Statistical Association, 2016).

Figure 3 separates GP (n=423) and MS (n=226); their descriptive Spearman coefficients were 0.268 and 0.177, respectively. The MS >10-hour cell contains only eight records. The school-centered rank diagnostic was 0.246757; 0 of 19,999 sampled permutations were as extreme, giving corrected Monte Carlo p = 0.00005. This is the finite simulation's minimum reportable p-value, not zero or an exact enumeration. The positive pattern is not explained solely by between-school rank-location differences under this diagnostic's assumptions.

Of the three visual models, Figure 2 most directly supports the question: it displays the ordered relationship and its considerable variation within categories. Figure 1 provides distributional context, whereas Figure 3 exposes school composition and small cells that require caution.

## Interpretation for a Non-Technical Audience

In these records, students reporting more weekly study time tended to have higher final grades. Students who reported studying less than 2 hours a week averaged 10.8 out of 20, while those reporting 5 to 10 hours averaged 13.2. That is a difference of about 2.4 grade points. Students reporting more than 10 hours averaged 13.1, so the group reporting the most study time did not have the highest average.

Students in different study-time groups often had similar grades, so study time alone cannot reliably tell a student what grade to expect. A student or teacher can use this finding to start a conversation about study habits, not to promise a grade increase or set an ideal number of hours. The records do not show that extra study hours caused better grades; earlier learning, motivation or support at home could also help explain the differences. These results describe students at two schools and may not apply elsewhere.

## Limitations and Potential Bias

The file covers two schools rather than a documented probability sample of all students, so selection and school-context bias limit generalization. Shared teaching, classrooms or peer effects may violate student independence; the source file does not provide classroom identifiers that would allow a direct examination of classroom dependence. Two schools are insufficient for a convincing school-level cluster-robust generalization. School-restricted permutation is a sensitivity diagnostic, not a repair for these issues.

Study time is self-reported in broad, unequal-width categories; recall or social-desirability bias can distort the measured association. Prior attainment, motivation and family resources may influence both study time and grades, and the analysis does not adjust for them. The small highest-time group, especially its eight MS records, makes its mean sensitive to individual observations. No missing cells does not mean no measurement or selection bias. Systematic screening documents these limitations rather than eliminating them (Lusa et al., 2024).

The question and Spearman approach were proposed before downloading the file, but a preliminary inspection of its pooled correlation occurred before the completed analysis plan and notebook were written. This was not preregistered or blinded, and the school-centered analysis is explicitly secondary. Reporting the decision timing, all groups and the unequal outcomes reduces selective-reporting ambiguity; a small p-value alone cannot validate the workflow (American Statistical Association, 2016).

## Reproducibility and Next Steps

The submission includes analysis.ipynb, the unchanged local CSV, its hash, requirements.txt generated by pip freeze, and saved tables and figures. The README explains installation and restarting the notebook kernel before running all cells. The executed Python/package versions and a fixed permutation seed make the analysis inspectable; pinned versions alone do not guarantee identical behavior across every operating system. A follow-up would seek documented student sampling and classroom identifiers before making broader inferential claims, and prospectively specify how prior attainment and other confounders will be handled. No machine-learning models were trained.

Replit AI assisted with planning, code preparation, debugging, verification and report drafting. Numerical results come from the executed notebook and saved outputs rather than hypothetical experiments. The learner remains responsible for reviewing, understanding and revising the work and following the course's academic-integrity and AI-use policies.

## Conclusion

The sample shows a positive study-time/grade association and substantial individual variation. The conclusion is descriptive and conditional on the statistical assumptions: it does not establish causation, an optimal study schedule or representativeness beyond the observed schools. Preserved input data, an explicit decision record and reproducible computations make both the evidence and its limitations available for review.

## References

American Statistical Association. (2016, March 7). American Statistical Association releases statement on statistical significance and p-values. https://www.amstat.org/asa/files/pdfs/P-ValueStatement.pdf

Cortez, P. (2008). Student Performance [Data set]. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T

Lusa, L., Proust-Lima, C., Schmidt, C. O., Lee, K. J., le Cessie, S., Baillie, M., Lawrence, F., & Huebner, M., on behalf of TG3 of the STRATOS Initiative. (2024). Initial data analysis for longitudinal studies to build a solid foundation for reproducible analysis. PLOS ONE, 19(5), e0295726. https://doi.org/10.1371/journal.pone.0295726

Phipson, B., & Smyth, G. K. (2010). Permutation p-values should never be zero: Calculating exact p-values when permutations are randomly drawn. Statistical Applications in Genetics and Molecular Biology, 9(1), Article 39. https://doi.org/10.2202/1544-6115.1585

Schober, P., Boer, C., & Schwarte, L. A. (2018). Correlation coefficients: Appropriate use and interpretation. Anesthesia & Analgesia, 126(5), 1763–1768. https://doi.org/10.1213/ANE.0000000000002864

