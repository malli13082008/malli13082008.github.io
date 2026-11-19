# ClearCV - Smart Resume Analyzer

ClearCV is the Flask resume analyzer for this repository. It accepts PDF and DOCX resumes, checks basic structure, compares skills with a selected role, and shows a score and improvement suggestions.

## Run it locally

Install Python 3.10 or newer. In PowerShell, open this repository folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open <http://127.0.0.1:5000>. Keep the PowerShell window open while using the website. The `START_CLEARCV.bat` launcher sets port 8000 instead and prints the address to open.

## Deploy on Render

This application needs a Python web server. GitHub Pages serves static files and cannot run the Flask backend. The included `render.yaml` configures the Flask service for Render. Connect the repository to Render and deploy it as a Blueprint; see [deployment instructions](docs/DEPLOYMENT.md).

The public demo uses temporary storage and sample resumes only. Do not upload real resumes to a public demo. The app deletes original files after analysis, but retains extracted resume text and results in SQLite for each browser session until the report is deleted. There are no user accounts.

## Project structure

```text
app.py                  Flask routes, PDF/DOCX parsing, scoring, session storage
templates/              Overview, report, and history pages
static/                 Responsive CSS and upload behavior
requirements.txt        Flask, pypdf, Gunicorn
render.yaml             Render web service configuration
docs/                   Project and deployment documentation
deliverables/            Capstone report, presentation, and sample resumes
```

The score is a transparent prototype heuristic: 55% section completeness and 45% exact skill-term coverage for the selected role. It is not a hiring decision or a prediction of real ATS outcomes.
