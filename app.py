# app.py
# Smart Resume Analyzer & Job Matcher — Flask Application

import os
import json
import uuid
import sys
from pathlib import Path
from flask import Flask, request, jsonify, render_template, redirect, url_for

# ── Ensure local modules are importable ───────────────────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

from models.skill_model import SKILLS_DB, JOB_ROLES
from utils.parser import parse_resume
from utils.scoring import calculate_ats_score
from utils.matcher import match_jobs, keyword_analysis

# ── App configuration ──────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB upload limit

UPLOAD_FOLDER = Path("static/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "docx", "doc"}

# In-memory store for demo (replace with SQLite/DB in production)
_results_store: dict = {}


# ── Helpers ────────────────────────────────────────────────────────────────────

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def safe_filename(filename: str) -> str:
    """Generate a unique safe filename."""
    ext = filename.rsplit(".", 1)[1].lower() if "." in filename else "pdf"
    return f"{uuid.uuid4().hex}.{ext}"


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Landing / upload page."""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_resume():
    """Handle resume upload and trigger analysis pipeline."""
    if "resume" not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Please upload PDF or DOCX only."}), 400

    # Save the file
    filename = safe_filename(file.filename)
    filepath = UPLOAD_FOLDER / filename
    file.save(str(filepath))

    # ── Run the full analysis pipeline ────────────────────────────────────────
    try:
        parsed      = parse_resume(str(filepath), SKILLS_DB)
        ats_result  = calculate_ats_score(parsed)
        job_matches = match_jobs(parsed)
        kw_result   = keyword_analysis(parsed)

        # Determine best job match for keyword analysis
        best_role = job_matches[0]["role"] if job_matches else None
        kw_result = keyword_analysis(parsed, best_role)

        # Package full result
        result_id = uuid.uuid4().hex
        result = {
            "id":           result_id,
            "filename":     file.filename,
            "parsed":       parsed,
            "ats":          ats_result,
            "job_matches":  job_matches,
            "keywords":     kw_result,
        }

        # Store result in memory (use DB in production)
        _results_store[result_id] = result

        # Clean up uploaded file (privacy)
        try:
            os.remove(str(filepath))
        except Exception:
            pass

        return jsonify({"success": True, "result_id": result_id})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


@app.route("/result/<result_id>")
def result_page(result_id: str):
    """Show the full analysis result page."""
    result = _results_store.get(result_id)
    if not result:
        return render_template("index.html", error="Result not found or expired. Please upload again.")
    return render_template("result.html", result=result)


@app.route("/dashboard/<result_id>")
def dashboard(result_id: str):
    """Analytics dashboard page."""
    result = _results_store.get(result_id)
    if not result:
        return redirect(url_for("index"))
    return render_template("dashboard.html", result=result)


@app.route("/api/result/<result_id>")
def api_result(result_id: str):
    """JSON endpoint — returns full analysis data."""
    result = _results_store.get(result_id)
    if not result:
        return jsonify({"error": "Not found"}), 404

    # Remove raw_text from API response to keep it lean
    safe = {k: v for k, v in result.items() if k != "parsed"}
    safe["parsed"] = {k: v for k, v in result["parsed"].items() if k != "raw_text"}
    return jsonify(safe)


@app.route("/api/jobs")
def api_jobs():
    """Return list of all supported job roles."""
    return jsonify({"roles": list(JOB_ROLES.keys())})


@app.route("/health")
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_ENV", "development") == "development"
    print(f"[app] Starting Smart Resume Analyzer on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
