# ClearCV — Project Documentation

## 1. Project overview

**Title:** Smart Resume Analyzer with AI-Based Feedback  
**Implementation:** ClearCV, a Flask web application using explainable rule-based NLP techniques.  
**Purpose:** Help students review resume completeness, compare skills with a chosen entry-level role, and get actionable suggestions.

The capstone brief describes a clean, functional HR-tech prototype and excludes deep learning, large language model training, complex recommendation engines, enterprise authentication, and large-scale cloud architecture. This implementation follows those limits.

## 2. Requirements from the brief

| Brief requirement | Implementation |
|---|---|
| Upload PDF or DOCX | Upload form, extension validation, 8 MB cap |
| Extract resume text | pypdf for PDF; WordprocessingML XML parsing for DOCX |
| Store resume information | SQLite stores analysis data and extracted text; original file is removed after parsing |
| Resume score out of 100 | Weighted structure and role skill coverage score |
| ATS keyword checker | Exact normalized term comparison against selected role skill list |
| Example roles | Data Analyst, Web Developer, AI Engineer, Cloud Engineer |
| Smart feedback | Missing-section guidance and role skill suggestions |
| Dashboard | Summary, analysis report, skill match, structure review, feedback, history |
| Dataset | Small hand-authored role skill lists; no external resume dataset is bundled |

## 3. System modules

### Module 1 — Resume upload and parsing

The upload endpoint validates the file suffix and selected role. The file is saved under a random name while parsing. PDF text is extracted page by page. DOCX paragraphs are read from `word/document.xml`. Files with too little extracted text produce a clear error; this includes most image-only/scanned PDFs. The original file is deleted after analysis or on failure. A session-scoped workspace ID keeps each browser session's history separate.

### Module 2 — Resume score analyzer

Five checks are applied: contact details, skills section, education, experience/projects, and readable length (150–1200 words). Section score is the percentage of checks present. Role keyword score is the percentage of sample role skills found. The overall score is:

`resume_score = round(0.55 × section_score + 0.45 × keyword_score)`

This simple formula is visible in the report so the user can understand the score.

### Module 3 — ATS keyword checker

The user selects one of four sample roles. The app performs case-insensitive whole-term checks and returns matched and missing skills. The role lists live in `ROLE_SKILLS` in `app.py`, making them easy to adapt. A match score is not a prediction of a real ATS result.

### Module 4 — Smart feedback

Missing resume sections produce high-priority suggestions. Missing role skills produce optional suggestions, with a reminder to list only skills supported by genuine experience. When all checks are present, the system recommends adding verifiable outcomes.

### Module 5 — Dashboard and report

The overview shows workspace totals and recent analyses. Each report shows the two scores, matched/missing skills, section checks, word count, and suggested next steps. History can open or delete saved reports.

## 4. Architecture and data flow

1. Browser submits a PDF or DOCX and target role.
2. Flask validates file and role; the parser extracts text.
3. Rule-based analysis computes metrics and feedback.
4. SQLite saves the report under the current browser session; the source upload is deleted.
5. The browser displays the report and history entry.

**Stack:** Python, Flask, pypdf, SQLite, HTML, CSS, JavaScript, Jinja templates.  
**Main files:** `app.py`, `templates/`, `static/`, `requirements.txt`.

## 5. Data model

`analyses` contains an ID, original filename, target role, UTC timestamp, resume score, ATS score, JSON metrics, JSON feedback, extracted text, and a browser-session owner ID. The actual uploaded document is not retained. Data is stored in SQLite.

## 6. Setup and operation

Follow the PowerShell steps in the root `README.md`. The local server is available at `http://127.0.0.1:5000`. The app creates its data directory and database on first use. It accepts text-based PDF and DOCX documents up to 8 MB.

## 7. Limitations and future work

- No OCR for scanned documents.
- Sample role vocabularies are intentionally small and need review by domain experts.
- Whole-term matching misses synonyms and context; a term may appear without proof of proficiency.
- Scores are heuristic and have not been validated against recruiters or hiring outcomes.
- No user accounts are included. Browser sessions are isolated and form posts use CSRF tokens, but this is not production authentication.
- The Render demo uses temporary storage, so saved analyses can disappear on restart or redeploy.
- No demo video, GitHub repository, or hosted deployment URL is generated; these require the student's accounts and a screen recording.

Possible next steps: configurable skill taxonomies; synonym-aware NLP; authenticated users and retention controls; exportable reports; automated accessibility and security review; deployment to a Python host with persistent storage.

## 8. Responsible use

Use this tool to improve a resume, not to rank people. Do not infer a candidate's suitability from the score. Review suggestions for relevance and include only accurate qualifications. Use synthetic resumes on public demos.

## 9. Submission checklist

- [x] Complete source code
- [x] Project documentation
- [x] Project report PDF
- [x] Presentation PPTX
- [ ] GitHub repository URL (create in the student's account)
- [ ] Deployment URL (deploy and configure storage)
- [ ] Demo video (record locally)
- [ ] Place all completed items in one Google Drive folder and submit its share link
