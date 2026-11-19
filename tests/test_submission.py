import hashlib
import json
from pathlib import Path

from docx import Document
import pymupdf as fitz
import nbformat
import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
SUMMARY = json.loads((ROOT / "outputs/analysis_summary.json").read_text())


def test_original_real_dataset():
    raw = (ROOT / "student-por.csv").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SUMMARY["source_sha256"]
    data = pd.read_csv(ROOT / "student-por.csv", sep=";")
    assert data.shape == (649, 33)
    assert data.isna().sum().sum() == 0
    assert data.duplicated().sum() == 0
    assert data["G3"].eq(0).sum() == SUMMARY["zero_grades"] == 15


def test_primary_statistics_independently():
    data = pd.read_csv(ROOT / "student-por.csv", sep=";")
    primary = stats.spearmanr(data["studytime"], data["G3"])
    assert np.isclose(primary.statistic, SUMMARY["primary_rho"])
    assert np.isclose(primary.pvalue, SUMMARY["primary_pvalue"], rtol=1e-12, atol=0)
    assert np.isclose(data["G3"].std(ddof=1), SUMMARY["grade_sd"])
    assert np.isclose(data["G3"].mean(), SUMMARY["grade_mean"])


def test_group_counts_and_summaries():
    groups = pd.read_csv(ROOT / "outputs/studytime_summary.csv")
    assert groups["n"].tolist() == [212, 305, 97, 35]
    assert groups["n"].sum() == 649
    assert groups["median"].tolist() == [11, 12, 13, 13]
    cells = pd.read_csv(ROOT / "outputs/school_studytime_summary.csv")
    assert cells["n"].sum() == 649
    assert cells.loc[(cells.school == "MS") & (cells.studytime == 4), "n"].item() == 8


def test_notebook_executed_and_figures_embedded():
    notebook = nbformat.read(ROOT / "analysis.ipynb", as_version=4)
    code = [c for c in notebook.cells if c.cell_type == "code"]
    assert all(c.execution_count is not None for c in code)
    assert not any(o.output_type == "error" for c in code for o in c.outputs)
    images = [o for c in code for o in c.outputs if "image/png" in o.get("data", {})]
    assert len(images) == 3
    assert notebook.cells[0].cell_type == "markdown"
    assert "AI Foundations (Edward Hickman)" in notebook.cells[0].source


def test_hypotheses_comparison_and_final_summary():
    notebook = nbformat.read(ROOT / "analysis.ipynb", as_version=4)
    text = "\n".join(c.source for c in notebook.cells if c.cell_type == "markdown")
    assert "**H0:**" in text and "**H1:**" in text
    assert "Figure 2 best" in text
    assert "not a" in text
    last = notebook.cells[-1]
    assert last.cell_type == "markdown"
    assert "Notebook summary" in last.source
    assert len(last.source.split("\n\n", 1)[1].split(".\n")) == 5


def test_secondary_permutation_statistic_and_correction():
    data = pd.read_csv(ROOT / "student-por.csv", sep=";")
    x = pd.Series(stats.rankdata(data.studytime))
    y = pd.Series(stats.rankdata(data.G3))
    x -= x.groupby(data.school).transform("mean")
    y -= y.groupby(data.school).transform("mean")
    result = SUMMARY["sensitivity"]
    assert np.isclose(np.corrcoef(x, y)[0, 1], result["rank_correlation"])
    assert result["pvalue"] == (result["extreme_count"] + 1) / (result["n_resamples"] + 1)
    assert result["pvalue"] > 0
    assert result["n_resamples"] == 19999


def test_report_sections_and_values():
    doc = Document(ROOT / "module_summary.docx")
    text = "\n".join(p.text for p in doc.paragraphs)
    for heading in ["Overview", "Dataset Description", "Methods", "Results",
                    "Interpretation for a Non-Technical Audience",
                    "Limitations and Potential Bias", "References"]:
        assert heading in text
    for value in ["0.274712", "1.06062e-12", "0.00005", "649", "33"]:
        assert value in text
    assert len(doc.inline_shapes) == 3
    assert "Instructor Name" not in text
    assert "Lusa et al." in text and "Schober et al." in text


def test_pdf_is_readable_and_contains_figures():
    with fitz.open(ROOT / "module_summary.pdf") as doc:
        assert len(doc) >= 5
        text = "\n".join(page.get_text() for page in doc)
        assert "AI Foundations (Edward Hickman)" in text
        assert "0.274712" in text
        assert sum(len(p.get_images()) for p in doc) >= 3
        assert "References" in doc[-1].get_text()
        assert "10.1371/journal.pone.0295726" in text


def test_plain_language_section_matches_review_feedback():
    markdown = (ROOT / "module_summary.md").read_text()
    docx = "\n".join(p.text for p in Document(ROOT / "module_summary.docx").paragraphs)
    with fitz.open(ROOT / "module_summary.pdf") as pdf:
        pdf_text = "\n".join(page.get_text() for page in pdf)
    for text in [markdown, docx, pdf_text]:
        section = text.split("Interpretation for a Non-Technical Audience", 1)[1]
        section = section.split("Limitations and Potential Bias", 1)[0]
        section = " ".join(section.split())
        for jargon in ["p-value", "null model", "null hypothesis", "rho",
                       "American Statistical Association", "(2016)"]:
            assert jargon.lower() not in section.lower()
        for value in [f"{SUMMARY['studytime_groups'][i]['mean']:.1f}" for i in [0, 2, 3]]:
            assert value in section
        assert "2.4 grade points" in section
        assert "out of 20" in section
        assert "not to promise a grade increase" in section
        assert "do not show that extra study hours caused better grades" in section
        assert "two schools" in section


def test_template_preserved():
    audit = json.loads((ROOT / "outputs/report_template_audit.json").read_text())
    assert audit["styles_preserved"] and audit["section_preserved"]
    assert audit["headers_preserved"]
    doc = Document(ROOT / "module_summary.docx")
    assert all(abs(float(m) / 914400 - 1) < .001 for m in
               [doc.sections[0].top_margin, doc.sections[0].bottom_margin,
                doc.sections[0].left_margin, doc.sections[0].right_margin])


def test_required_files_and_frozen_dependencies():
    for name in ["analysis.ipynb", "module_summary.pdf", "requirements.txt",
                 "student-por.csv", "README.md"]:
        assert (ROOT / name).is_file()
    requirements = (ROOT / "requirements.txt").read_text().lower()
    for name in ["numpy", "pandas", "matplotlib", "seaborn", "scipy", "nbconvert"]:
        assert f"{name}==" in requirements
