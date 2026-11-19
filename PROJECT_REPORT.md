# Smart Resume Analyzer with AI-Based Feedback

## Abstract

ClearCV is a local-first web prototype that helps students review a resume against a selected entry-level role. It extracts text from PDF and DOCX documents, checks basic resume structure, compares role-specific skill terms, and presents an explainable score with targeted feedback. The implementation uses Flask, SQLite, and straightforward natural-language processing rules. It follows the capstone's stated scope by avoiding model training and complex recommendation systems.

## Problem statement

Students may not know how applicant tracking systems parse documents, what skills are relevant to a target role, or whether a resume clearly communicates education and project experience. ClearCV provides a small, inspectable workflow for checking these points.

## Objectives

1. Accept PDF and DOCX resumes.
2. Extract readable text and store report data.
3. Calculate a resume score out of 100.
4. Compare terms against four sample job-role vocabularies.
5. Suggest practical improvements.
6. Display reports through a responsive dashboard and history page.

## Method

The parser uses pypdf for PDF files and reads WordprocessingML paragraphs for DOCX files. Analysis checks for contact information, a skills section, education, experience or projects, and a word count between 150 and 1200. The role match uses case-insensitive whole-term matching against a small skill list.

Section completeness and skill coverage are combined as follows:

**Overall score = 55% × section completeness + 45% × role keyword coverage**

Feedback identifies missing sections and unrepresented role skills. Every missing-skill suggestion includes a reminder to list only skills the student can substantiate.

## Implementation

The Flask application contains routes for the overview, upload analysis, report display, report history, and report deletion. SQLite persists the analysis ID, filename, role, timestamp, scores, metrics, feedback, and extracted text. The source file is removed after extraction. Jinja templates render the dashboard, while CSS and a small JavaScript file provide responsive layout and drag-and-drop upload behavior.

## Results

The prototype implements all five modules in the capstone brief: resume upload and parsing, scoring, ATS keyword matching, smart feedback, and dashboard reporting. The four example roles in the brief are included. The analysis is deterministic and transparent: the same text and selected role produce the same score.

## Limitations

The prototype does not perform OCR, semantic understanding, or deep learning. Its skill lists are sample vocabularies rather than a current labor-market dataset. Exact keyword matching may miss synonyms or context and can reward keyword presence without measuring proficiency. The scores have not been validated as hiring predictors. The application has no authentication or multi-user isolation and is intended for local educational use.

## Conclusion

ClearCV demonstrates a complete, explainable resume-analysis workflow using a small web stack. It connects document handling, rule-based NLP, persistence, and dashboard design in a project that can be run and extended locally. Future work can add vetted skill taxonomies, synonym-aware matching, user security, and a deployed Python service after privacy and security requirements are addressed.

## References

- SkillOrbit, *Artificial Intelligence Capstone Project: Smart Resume Analyzer with AI-Based Feedback*, user-provided project brief (8 pages).
- Flask documentation: https://flask.palletsprojects.com/
- pypdf documentation: https://pypdf.readthedocs.io/
- Python `sqlite3` documentation: https://docs.python.org/3/library/sqlite3.html
