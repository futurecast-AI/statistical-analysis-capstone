"""Populate the supplied student-paper template with executed analysis results."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess

from docx import Document
from docx.enum.text import WD_BREAK
from docx.shared import Inches
from docx.text.paragraph import Paragraph
from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
s = json.loads((OUT / "analysis_summary.json").read_text())
groups = s["studytime_groups"]
sens = s["sensitivity"]
group_description = "; ".join(
    f"{g['study_label']}: n={g['n']}, mean={g['mean']:.2f}, median={g['median']:.0f}"
    for g in groups)

sections = [
    ("Overview",
     "This project examines whether reported weekly study-time category is associated "
     "with final Portuguese grades in the UCI Student Performance dataset "
     "(Cortez, 2008). It combines descriptive statistics, three visual models, "
     "and a two-sided Spearman hypothesis test to distinguish an observed association "
     "from a causal claim. The public dataset and variable dictionary are available "
     "at https://archive.ics.uci.edu/dataset/320/student+performance."),
    ("Dataset Description",
     f"The original semicolon-delimited CSV contains {s['rows']} student records and "
     f"{s['columns']} columns from two Portuguese secondary schools, collected through "
     "school reports and questionnaires (Cortez, 2008). Each row is a Portuguese-language "
     "course record; the overlapping mathematics dataset is not merged or analyzed. "
     "The key variables are school (GP or MS), ordered weekly study-time category "
     "(studytime), and final grade (G3, 0–20 points), with age, absences and earlier "
     "grades included in descriptive summaries. Study-time codes 1–4 mean <2, 2–5, "
     "5–10 and >10 hours, so the codes are not equally spaced measured hours. "
     "The audit found no missing cells or exact duplicate rows; all records, including "
     f"{s['zero_grades']} zero grades, were retained."),
    ("Methods",
     "The notebook displays the first rows and data types, checks a SHA-256 fingerprint, "
     "and audits missing values, distinct values, category codes, numeric ranges and "
     "full-row matches before inference. This structured screening and decision record "
     "apply Lusa et al.'s (2024) initial-data-analysis principles. Their article focuses "
     "on longitudinal data; the applicable contribution here is systematic screening, "
     "not a claim that the present cross-sectional association analysis is longitudinal.\n\n"
     "Counts describe nominal and ordinal categories. The grade mean and sample standard "
     "deviation summarize center and spread, while the median and interquartile range "
     "provide complementary summaries less dependent on extreme observations. The "
     "notebook displays df.describe, but does not interpret averages of ordinal "
     "study-time codes as actual hours. Figure 1 uses one-point histogram bins for "
     "the discrete grade distribution. Figure 2 uses boxplots with every observation "
     "overlaid to compare ordered groups and show overlap; Figure 3 displays school-specific "
     "cell means and counts to reveal differences hidden by pooling.\n\n"
     "The primary test is Spearman rank correlation, appropriate for an ordinal "
     "variable and a possible monotonic association (Schober et al., 2018). The "
     "null hypothesis is population rho_s = 0; the alternative is rho_s != 0, "
     "tested two-sided at alpha = .05. SciPy uses average ranks for ties and reports "
     "an approximate large-sample p-value. Paired measurements, meaningful ordering, "
     "nonconstant variables and independent observations are required; normal "
     "measurement distributions and equal category widths are not required. "
     "This convenience sample and possible shared classroom/school influences "
     "make the independence and sampling assumptions uncertain.\n\n"
     "A secondary sensitivity diagnostic centers both globally ranked variables "
     "within each school, then correlates the centered ranks. Study-time ranks "
     f"are permuted within schools {sens['n_resamples']:,} times using seed "
     f"{sens['seed']}; the two-sided comparison uses absolute correlations. The "
     "Monte Carlo p-value is (b+1)/(m+1), with b counting resampled statistics "
     "at least as extreme as observed; this avoids reporting zero "
     "(Phipson & Smyth, 2010). The diagnostic's null is within-school exchangeability/no "
     "association, not exactly the primary zero-correlation null. It removes between-school "
     "rank-location differences but is not a cluster-robust analysis or a control "
     "for all confounding. School-specific coefficients are reported descriptively, "
     "without separate significance claims."),
    ("Results",
     f"The overall grade mean was {s['grade_mean']:.2f}, sample SD "
     f"{s['grade_sd']:.2f}, and median {s['grade_median']:.0f}, with quartiles "
     f"{s['grade_q1']:.0f} and {s['grade_q3']:.0f} (IQR "
     f"{s['grade_q3'] - s['grade_q1']:.0f}). Figure 1 shows the distribution "
     f"of all {s['rows']} grades, including {s['zero_grades']} zero grades. "
     f"Figure 2 compares the four categories: {group_description}. "
     "The increasing medians coexist with substantial overlap, and the mean "
     "in the >10-hour group is slightly lower than in the 5–10-hour group.\n\n"
     f"The primary test statistic was rho_s = {s['primary_rho']:.6f}, with "
     f"two-sided approximate p = {s['primary_pvalue']:.6g} (n={s['rows']}). "
     "Thus H0 is rejected at .05 if the test assumptions hold. The positive "
     "coefficient, far from one, and overlapping grade distributions matter "
     "more for interpreting the pattern than the threshold decision alone "
     "(American Statistical Association, 2016).\n\n"
     f"Figure 3 separates GP (n={s['school_rhos']['GP']['n']}) and "
     f"MS (n={s['school_rhos']['MS']['n']}); their descriptive Spearman coefficients "
     f"were {s['school_rhos']['GP']['rho']:.3f} and "
     f"{s['school_rhos']['MS']['rho']:.3f}, respectively. The MS >10-hour cell "
     "contains only eight records. The school-centered rank diagnostic was "
     f"{sens['rank_correlation']:.6f}; {sens['extreme_count']} of "
     f"{sens['n_resamples']:,} sampled permutations were as extreme, giving "
     f"corrected Monte Carlo p = {sens['pvalue']:.5f}. This is the finite "
     "simulation's minimum reportable p-value, not zero or an exact enumeration. "
     "The positive pattern is not explained solely by between-school rank-location "
     "differences under this diagnostic's assumptions.\n\n"
     "Of the three visual models, Figure 2 most directly supports the question: "
     "it displays the ordered relationship and its considerable variation "
     "within categories. Figure 1 provides distributional context, whereas "
     "Figure 3 exposes school composition and small cells that require caution."),
    ("Interpretation for a Non-Technical Audience",
     "In these records, students reporting more weekly study time tended to have "
     "higher final grades, but the relationship was not strong enough to predict "
     "a particular student's outcome reliably. Students in different time groups "
     "often had similar grades, and the highest-time group did not have the highest "
     "average. The small p-value indicates incompatibility with the specified "
     "null model under its assumptions; it is not the probability that the null "
     "hypothesis is true, nor a measure of practical importance "
     "(American Statistical Association, 2016). This analysis does not show that "
     "assigning extra study hours would improve a student's grade, or that any "
     "particular number of hours is optimal."),
    ("Limitations and Potential Bias",
     "The file covers two schools rather than a documented probability sample "
     "of all students, so selection and school-context bias limit generalization. "
     "Shared teaching, classrooms or peer effects may violate student independence; "
     "the source file does not provide classroom identifiers that would allow a "
     "direct examination of classroom dependence. Two schools are insufficient "
     "for a convincing school-level cluster-robust generalization. School-restricted "
     "permutation is a sensitivity diagnostic, not a repair for these issues.\n\n"
     "Study time is self-reported in broad, unequal-width categories; recall "
     "or social-desirability bias can distort the measured association. Prior "
     "attainment, motivation and family resources may influence both study time "
     "and grades, and the analysis does not adjust for them. The small highest-time "
     "group, especially its eight MS records, makes its mean sensitive to individual "
     "observations. No missing cells does not mean no measurement or selection bias. "
     "Systematic screening documents these limitations rather than eliminating "
     "them (Lusa et al., 2024).\n\n"
     "The question and Spearman approach were proposed before downloading the file, "
     "but a preliminary inspection of its pooled correlation occurred before the "
     "completed analysis plan and notebook were written. This was not preregistered "
     "or blinded, and the school-centered analysis is explicitly secondary. "
     "Reporting the decision timing, all groups and the unequal outcomes reduces "
     "selective-reporting ambiguity; a small p-value alone cannot validate the "
     "workflow (American Statistical Association, 2016)."),
    ("Reproducibility and Next Steps",
     "The submission includes analysis.ipynb, the unchanged local CSV, its hash, "
     "requirements.txt generated by pip freeze, and saved tables and figures. "
     "The README explains installation and restarting the notebook kernel before "
     "running all cells. The executed Python/package versions and a fixed "
     "permutation seed make the analysis inspectable; pinned versions alone "
     "do not guarantee identical behavior across every operating system. A "
     "follow-up would seek documented student sampling and classroom identifiers "
     "before making broader inferential claims, and prospectively specify how "
     "prior attainment and other confounders will be handled. No machine-learning "
     "models were trained.\n\n"
     "Replit AI assisted with planning, code preparation, debugging, verification "
     "and report drafting. Numerical results come from the executed notebook and "
     "saved outputs rather than hypothetical experiments. The learner remains "
     "responsible for reviewing, understanding and revising the work and following "
     "the course's academic-integrity and AI-use policies."),
    ("Conclusion",
     "The sample shows a positive study-time/grade association and substantial "
     "individual variation. The conclusion is descriptive and conditional on "
     "the statistical assumptions: it does not establish causation, an optimal "
     "study schedule or representativeness beyond the observed schools. "
     "Preserved input data, an explicit decision record and reproducible "
     "computations make both the evidence and its limitations available for review."),
]

references = [
    ("American Statistical Association. (2016, March 7). American Statistical Association "
     "releases statement on statistical significance and p-values. "
     "https://www.amstat.org/asa/files/pdfs/P-ValueStatement.pdf",
     "American Statistical Association releases statement on statistical significance and p-values"),
    ("Cortez, P. (2008). Student Performance [Data set]. UCI Machine Learning Repository. "
     "https://doi.org/10.24432/C5TG7T", "Student Performance"),
    ("Lusa, L., Proust-Lima, C., Schmidt, C. O., Lee, K. J., le Cessie, S., Baillie, M., "
     "Lawrence, F., & Huebner, M., on behalf of TG3 of the STRATOS Initiative. (2024). "
     "Initial data analysis for longitudinal studies to build a solid foundation "
     "for reproducible analysis. PLOS ONE, 19(5), e0295726. "
     "https://doi.org/10.1371/journal.pone.0295726", "PLOS ONE, 19"),
    ("Phipson, B., & Smyth, G. K. (2010). Permutation p-values should never be zero: "
     "Calculating exact p-values when permutations are randomly drawn. "
     "Statistical Applications in Genetics and Molecular Biology, 9(1), Article 39. "
     "https://doi.org/10.2202/1544-6115.1585",
     "Statistical Applications in Genetics and Molecular Biology, 9"),
    ("Schober, P., Boer, C., & Schwarte, L. A. (2018). Correlation coefficients: "
     "Appropriate use and interpretation. Anesthesia & Analgesia, 126(5), 1763–1768. "
     "https://doi.org/10.1213/ANE.0000000000002864", "Anesthesia & Analgesia, 126"),
]

parser = argparse.ArgumentParser()
parser.add_argument("template", type=Path)
args = parser.parse_args()
doc = Document(args.template)
patterns = [deepcopy(p._p) for p in doc.paragraphs]
original_styles = doc.styles.element.xml
original_section = etree.tostring(doc.sections[0]._sectPr, method="c14n", exclusive=True)
header_footer = {str(p.partname): p.blob for p in doc.part.package.parts
                 if "header" in p.content_type or "footer" in p.content_type}
body = doc._element.body
for child in list(body):
    if child is not doc.sections[0]._sectPr:
        body.remove(child)


def append_pattern(index, text=""):
    """Preserve a template paragraph's properties while replacing its content."""
    element = deepcopy(patterns[index])
    original = Paragraph(element, doc._body)
    properties = deepcopy(original.runs[0]._r.rPr) if original.runs else None
    for child in list(element):
        if child is not element.pPr:
            element.remove(child)
    body.insert(len(body) - 1, element)
    paragraph = Paragraph(element, doc._body)
    run = paragraph.add_run(text)
    if properties is not None:
        run._r.insert(0, properties)
    return paragraph


def page_break():
    """Insert an explicit page break using the template's break paragraph."""
    append_pattern(13).runs[0].add_break(WD_BREAK.PAGE)


cover = {4: "Study Time and Portuguese Final Grades",
         6: "AI Foundations (Edward Hickman)", 7: "Udacity",
         8: "Project 2 — Data and Statistical Reasoning", 9: "", 10: ""}
for index in range(11):
    append_pattern(index, cover.get(index, ""))
page_break()
append_pattern(14, cover[4])
text = f"# {cover[4]}\n\n{cover[6]}\n\n"
for heading, content in sections:
    append_pattern(19, heading)
    for paragraph in content.split("\n\n"):
        append_pattern(15, paragraph)
    text += f"## {heading}\n\n{content}\n\n"

figures = [
    ("figure_1_grade_distribution.png", "All 649 records are included; zero grades are retained."),
    ("figure_2_grades_by_studytime.png",
     "Boxes show medians and IQRs; whiskers use 1.5 IQR. All observations are "
     "overlaid with seeded horizontal jitter, not altered grades."),
    ("figure_3_school_comparison.png",
     "Points are descriptive cell means and labels give cell counts. No confidence "
     "intervals are estimated; these points are not fitted predictions."),
]
for number, (filename, caption) in enumerate(figures, 1):
    page_break()
    append_pattern(19, f"Figure {number}")
    append_pattern(1).runs[0].add_picture(str(OUT / filename), width=Inches(6.5))
    append_pattern(15, f"Note. {caption} Source: executed analysis.ipynb.")

page_break()
append_pattern(37, "References")
text += "## References\n\n"
for reference, italic_span in references:
    p = append_pattern(38)
    props = deepcopy(p.runs[0]._r.rPr)
    for run in list(p.runs):
        p._p.remove(run._r)
    before, after = reference.split(italic_span, 1)
    for value, italic in [(before, False), (italic_span, True), (after, False)]:
        run = p.add_run(value)
        if props is not None:
            run._r.insert(0, deepcopy(props))
        run.italic = italic
    text += f"{reference}\n\n"

doc.core_properties.title = cover[4]
doc.core_properties.author = cover[6]
doc.core_properties.subject = cover[8]
doc.core_properties.comments = "AI assistance disclosed. Instructor and due date not supplied."
assert doc.styles.element.xml == original_styles
assert etree.tostring(doc.sections[0]._sectPr, method="c14n",
                      exclusive=True) == original_section
assert header_footer == {str(p.partname): p.blob for p in doc.part.package.parts
                         if "header" in p.content_type or "footer" in p.content_type}
doc.save(ROOT / "module_summary.docx")
(ROOT / "module_summary.md").write_text(text)
subprocess.run([
    "libreoffice", "-env:UserInstallation=file:///tmp/statistical-report-office",
    "--headless", "--convert-to", "pdf", "--outdir", str(ROOT),
    str(ROOT / "module_summary.docx")], check=True)
(OUT / "report_template_audit.json").write_text(json.dumps({
    "template_url": "https://docs.google.com/document/d/1cv_MjQVKnGc9sbaYiOUna2155jMEvUxACwyDax-XYWI/edit",
    "template_sha256": hashlib.sha256(args.template.read_bytes()).hexdigest(),
    "styles_preserved": True, "section_preserved": True, "headers_preserved": True,
    "omitted_fields": ["Instructor", "Due date"],
    "pdf_font": "Liberation Sans substitutes for retained Arial DOCX styles",
}, indent=2) + "\n")
