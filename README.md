# Statistical Analysis Capstone

**AI Foundations (Edward Hickman)**

This project examines the association between reported study-time category and
final Portuguese grades in the real UCI Student Performance dataset.
It includes descriptive statistics, three visualizations, a two-sided Spearman
test and a school-adjusted sensitivity diagnostic; it does not train ML models
or establish causation.
Dataset: https://archive.ics.uci.edu/dataset/320/student+performance (CC BY 4.0).

## Run the notebook

Use Python 3.11 (the tested version is 3.11.18) from the repository folder:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m jupyterlab
```

Open `analysis.ipynb`, select the environment's Python kernel, then restart the
kernel and run all cells. The original `student-por.csv` must stay beside the
notebook; it is semicolon-delimited and does not require network access.

Alternatively:

```bash
python -m nbconvert --to notebook --execute --inplace analysis.ipynb
python -m pytest tests -q
pip freeze > requirements.txt
```

## Submission

Required: `analysis.ipynb`, `module_summary.pdf`, `requirements.txt`,
`student-por.csv`. The report's editable DOCX and Markdown, supporting outputs,
tests and decision/provenance notes are extras.
Review `SUBMISSION_CHECKLIST.md` before uploading.
`ANALYSIS_PLAN.md` records assumptions and the timing of decisions.
Replit AI assistance is disclosed in the notebook and report.

## Optional report rebuild

`scripts/build_report.py <template.docx>` rebuilds the report from saved notebook
results using the previously supplied CCC APA student-paper template.
It requires a local export of that template and LibreOffice on the system;
neither is needed to run the analysis notebook. The editable completed report
is included, so a reviewer does not need the original template to read or edit it.
