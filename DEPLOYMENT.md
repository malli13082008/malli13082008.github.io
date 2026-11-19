# Deploy ClearCV on Render

GitHub stores the source code. GitHub Pages only serves static HTML/CSS/JavaScript and cannot run this Flask application. Use a Python web service for the working analyzer.

## Deploy from the repository

1. Push the contents of this project folder to a GitHub repository.
2. Sign in to Render and choose **New + > Blueprint**.
3. Connect the repository and select the branch containing `render.yaml`.
4. Review the service settings and start the deployment.
5. Open the `onrender.com` URL shown in the Render service dashboard.

The included Blueprint sets `pip install -r requirements.txt` as the build command and starts Gunicorn on Render's `PORT`. It also creates a random `SECRET_KEY` and uses temporary storage for the demo database.

## Demo data and privacy

Use only the included synthetic sample resumes for a public demo. Each browser session gets its own private analysis history, and form submissions use CSRF tokens. The sample deployment stores reports in temporary disk space; saved analyses may disappear when the service restarts or redeploys. Do not upload real resumes to this public capstone demo. A production service would need a reviewed retention policy, managed persistent database, authentication, and a security review.

## GitHub Pages

The `github.com/...` URL is the repository. A profile Pages site typically uses `https://USERNAME.github.io/`, but that serves static files and is not the running Flask analyzer. Keep Pages for a project landing page if desired, and link from it to the Render service URL.
