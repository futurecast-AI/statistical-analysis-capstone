# Dataset provenance

- Dataset: Student Performance, Portuguese-language course (`student-por.csv`).
- Creator: Paulo Cortez.
- Repository: UCI Machine Learning Repository.
- Landing page: https://archive.ics.uci.edu/dataset/320/student+performance
- Dataset DOI: https://doi.org/10.24432/C5TG7T
- Download: https://archive.ics.uci.edu/static/public/320/student+performance.zip
- The download contains `student.zip`; the CSV was extracted unchanged from it.
- License: Creative Commons Attribution 4.0, as listed by UCI.
- CSV SHA256: `a7594a11d7771c0efe1a740824e0e833da9c4cad07c39a9766a874575563fb3f`.
- Dimensions: 649 records by 33 columns; semicolon delimiter.
- Unit: a student record in the Portuguese-language course.
- Collected through school reports and questionnaires from two Portuguese
  secondary schools. These are real observational data, not generated data.
- Source notes warn that 382 students occur in both the mathematics and
  Portuguese datasets. Only Portuguese data are analyzed, without merging.
- This is not the Titanic dataset used in the preceding capstone.

Key fields: `school` (GP or MS), `studytime` (four ordered weekly-time
categories), `G3` (final grade on a 0–20 scale), `G1` and `G2` (earlier grades),
`age`, and `absences`. The repository's variable dictionary is the authority
for interpretation. Codes 1–4 for study time are not equal-width hour values.

Full rows have no stable student identifiers. Exact-match checks are audits,
not proof of unique people. All 649 rows are retained. No missing values,
exact duplicate rows, imputations, or numeric coercions were found/required.
