"""Smart Resume Analyzer - Flask application for an explainable capstone prototype."""
from __future__ import annotations

import json
import os
import re
import sqlite3
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree

from flask import Flask, flash, g, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

try:
    from pypdf import PdfReader
except ImportError:  # Clear setup error will be shown on PDF upload.
    PdfReader = None

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("RESUME_ANALYZER_DATA", BASE_DIR / "instance"))
UPLOAD_DIR = DATA_DIR / "uploads"
DB_PATH = DATA_DIR / "resume_analyzer.sqlite3"
ALLOWED_EXTENSIONS = {"pdf", "docx"}
MAX_UPLOAD_BYTES = 8 * 1024 * 1024

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-capstone-demo-change-me")
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES

ROLE_SKILLS = {
    "Data Analyst": ["sql", "excel", "python", "statistics", "tableau", "power bi", "data visualization", "pandas", "data cleaning", "communication"],
    "Web Developer": ["html", "css", "javascript", "react", "git", "rest api", "responsive design", "testing", "sql", "accessibility"],
    "AI Engineer": ["python", "machine learning", "nlp", "scikit-learn", "pytorch", "tensorflow", "data preprocessing", "model evaluation", "api", "git"],
    "Cloud Engineer": ["aws", "azure", "google cloud", "docker", "kubernetes", "linux", "terraform", "ci/cd", "networking", "python"],
}


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("""CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY, filename TEXT NOT NULL, role TEXT NOT NULL,
            created_at TEXT NOT NULL, resume_score INTEGER NOT NULL,
            ats_score INTEGER NOT NULL, metrics_json TEXT NOT NULL,
            feedback_json TEXT NOT NULL, extracted_text TEXT NOT NULL
        )""")
        g.db.commit()
    return g.db


@app.teardown_appcontext
def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def extract_text(path: Path, suffix: str) -> str:
    if suffix == ".pdf":
        if PdfReader is None:
            raise RuntimeError("PDF support is not installed. Run: pip install -r requirements.txt")
        reader = PdfReader(str(path))
        if reader.is_encrypted:
            raise ValueError("This PDF is password protected. Export an unlocked copy and try again.")
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    with zipfile.ZipFile(path) as archive:
        root = ElementTree.fromstring(archive.read("word/document.xml"))
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    return "\n".join("".join(node.itertext()) for node in root.findall(".//w:p", ns))


def analyze_resume(text: str, role: str) -> dict:
    normalized = re.sub(r"\s+", " ", text.lower())
    words = re.findall(r"[a-zA-Z][a-zA-Z+#./-]*", text)
    skills = ROLE_SKILLS[role]
    matched = [skill for skill in skills if re.search(r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])", normalized)]
    missing = [skill for skill in skills if skill not in matched]

    sections = {
        "Contact details": bool(re.search(r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}", text) or re.search(r"\+?\d[\d ()-]{7,}\d", text)),
        "Skills section": bool(re.search(r"\b(skills|technical skills|core competencies)\b", normalized)),
        "Education section": bool(re.search(r"\b(education|bachelor|master|university|college)\b", normalized)),
        "Experience or projects": bool(re.search(r"\b(experience|employment|internship|projects|project)\b", normalized)),
        "Readable length": 150 <= len(words) <= 1200,
    }
    section_score = round(sum(sections.values()) / len(sections) * 100)
    keyword_score = round(len(matched) / max(len(skills), 1) * 100)
    # Explainable prototype score: structure and target-role skill coverage.
    resume_score = round(section_score * 0.55 + keyword_score * 0.45)

    feedback = []
    for label, present in sections.items():
        if not present:
            advice = {
                "Contact details": "Add a professional email and a reachable phone number.",
                "Skills section": "Add a clearly labeled skills section with relevant tools and methods.",
                "Education section": "List your degree or current studies, institution, and expected graduation year.",
                "Experience or projects": "Add experience, internships, or projects with your contribution and results.",
                "Readable length": "Add enough relevant detail to explain your work, while keeping the resume concise.",
            }[label]
            feedback.append({"priority": "High", "title": f"Strengthen {label.lower()}", "detail": advice})
    for skill in missing[:5]:
        feedback.append({"priority": "Role match", "title": f"Consider adding {skill}", "detail": f"The selected {role} role commonly uses this skill. Include it only if you can support it with real experience."})
    if not feedback:
        feedback.append({"priority": "Next step", "title": "Add measurable outcomes", "detail": "Make strong bullets more specific with scale, time saved, accuracy, users, or other results you can verify."})

    return {
        "resume_score": resume_score,
        "ats_score": keyword_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "sections": sections,
        "word_count": len(words),
        "feedback": feedback,
    }


@app.context_processor
def inject_globals():
    return {"roles": list(ROLE_SKILLS), "current_year": datetime.now().year}


@app.route("/")
def index():
    db = get_db()
    recent = db.execute("SELECT id, filename, role, created_at, resume_score, ats_score FROM analyses ORDER BY created_at DESC LIMIT 5").fetchall()
    total = db.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
    avg = db.execute("SELECT ROUND(AVG(resume_score)) FROM analyses").fetchone()[0] or 0
    return render_template("index.html", recent=recent, total=total, average=avg)


@app.post("/analyze")
def analyze():
    upload = request.files.get("resume")
    role = request.form.get("role", "")
    if not upload or not upload.filename:
        flash("Choose a PDF or DOCX resume to continue.", "error")
        return redirect(url_for("index"))
    safe_name = secure_filename(upload.filename)
    suffix = Path(safe_name).suffix.lower()
    if suffix not in {".pdf", ".docx"}:
        flash("Use a PDF or DOCX file.", "error")
        return redirect(url_for("index"))
    if role not in ROLE_SKILLS:
        flash("Select one of the supported target roles.", "error")
        return redirect(url_for("index"))

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    stored_path = UPLOAD_DIR / f"{uuid.uuid4().hex}{suffix}"
    upload.save(stored_path)
    try:
        text = extract_text(stored_path, suffix)
        if len(text.strip()) < 30:
            raise ValueError("We could not read enough text. If this is a scanned PDF, export a text-based PDF or DOCX.")
        result = analyze_resume(text, role)
    except (ValueError, RuntimeError, zipfile.BadZipFile) as exc:
        stored_path.unlink(missing_ok=True)
        flash(str(exc), "error")
        return redirect(url_for("index"))
    except Exception:
        stored_path.unlink(missing_ok=True)
        app.logger.exception("Resume analysis failed")
        flash("The file could not be analyzed. Check it is a valid PDF or DOCX, then try again.", "error")
        return redirect(url_for("index"))

    analysis_id = uuid.uuid4().hex[:12]
    metrics = {k: v for k, v in result.items() if k != "feedback"}
    db = get_db()
    db.execute("INSERT INTO analyses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (
        analysis_id, safe_name, role, datetime.now(timezone.utc).isoformat(),
        result["resume_score"], result["ats_score"], json.dumps(metrics),
        json.dumps(result["feedback"]), text[:100000],
    ))
    db.commit()
    stored_path.unlink(missing_ok=True)  # Keep analysis data, discard the original upload.
    return redirect(url_for("result", analysis_id=analysis_id))


@app.route("/analysis/<analysis_id>")
def result(analysis_id):
    row = get_db().execute("SELECT * FROM analyses WHERE id = ?", (analysis_id,)).fetchone()
    if not row:
        flash("That analysis could not be found.", "error")
        return redirect(url_for("index"))
    return render_template("result.html", analysis=row, metrics=json.loads(row["metrics_json"]), feedback=json.loads(row["feedback_json"]))


@app.route("/history")
def history():
    rows = get_db().execute("SELECT id, filename, role, created_at, resume_score, ats_score FROM analyses ORDER BY created_at DESC").fetchall()
    return render_template("history.html", rows=rows)


@app.post("/analysis/<analysis_id>/delete")
def delete_analysis(analysis_id):
    get_db().execute("DELETE FROM analyses WHERE id = ?", (analysis_id,))
    get_db().commit()
    flash("Analysis deleted.", "success")
    return redirect(url_for("history"))


@app.errorhandler(413)
def file_too_large(_error):
    flash("The file is larger than 8 MB. Choose a smaller resume file.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1", port=int(os.environ.get("PORT", 5000)))
