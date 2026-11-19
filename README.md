# ClearCV — Smart Resume Analyzer

A local-first Flask capstone prototype that analyzes a resume against a selected job role. It implements the five modules in the supplied SkillOrbit capstone brief: upload and parsing, resume scoring, ATS keyword matching, smart feedback, and a results dashboard.

## Run locally

1. Install Python 3.10 or newer.
2. Open a terminal in this folder and create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

3. Start the application:

   ```powershell
   python app.py
   ```

4. Open <http://127.0.0.1:5000>.

The app accepts text-based PDF and DOCX resumes up to 8 MB. It stores the analysis and extracted text in `instance/resume_analyzer.sqlite3`; the uploaded file itself is deleted after parsing. Use **Analysis history** to review or delete saved reports. The database is local and has no authentication, so treat this as a single-user educational prototype.

## Project map

```text
app.py                  Flask routes, parsing, scoring, SQLite storage
templates/              Jinja pages: overview, report, history
static/                 Responsive CSS and small upload interaction script
requirements.txt        Runtime dependencies
docs/                   Project documentation and presentation/report sources
deliverables/            Final editable PPTX and PDF report
```

## Analysis method

- **Resume score (0–100):** 55% section completeness + 45% target-role skill coverage.
- **ATS match:** exact term match across a small, editable sample skill list for Data Analyst, Web Developer, AI Engineer, and Cloud Engineer.
- **Section checks:** contact details, skills, education, experience/projects, and a practical word-count range.
- **Feedback:** flags missing sections and suggests skills from the role list. Suggestions explicitly ask users to include only skills they can support with evidence.

These are transparent prototype heuristics, not a validated hiring or ATS model. A scanned PDF without an embedded text layer will need OCR before analysis; OCR is outside this capstone scope.

## Privacy and safety

This is a local prototype without user accounts or authorization. It retains extracted resume text and scores in the local SQLite database until a report is deleted. Do not expose the development server to the public internet or upload sensitive resumes to a shared machine. In a production version, add authentication, CSRF protection, retention controls, encrypted storage, accessibility review, and security testing.

## Deployment notes

The supplied brief suggests Render, Netlify, or Vercel. This project is a Flask server, so Render or another Python application host is the most direct path. Set `SECRET_KEY` to a strong random value and configure persistent storage for SQLite (or move to managed PostgreSQL) before deployment. The deployment URL, repository URL, and demo video are intentionally left for the student to create in their own accounts.

## Capstone mapping

See `docs/PROJECT_DOCUMENTATION.md` for module-by-module coverage and the `deliverables/` folder for the report PDF, editable presentation, and synthetic sample resume.
