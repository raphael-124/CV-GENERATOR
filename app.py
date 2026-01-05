from flask import Flask, render_template, request, send_file
import os
import json
import tempfile
from utils.generator import build_docx, build_pdf

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    icon_path = os.path.join(os.path.dirname(__file__), 'static', 'curriculum-vitae.png')
    if os.path.exists(icon_path):
        return send_file(icon_path, mimetype='image/png')
    return ('', 404)

@app.route("/")
def index():
    root_index = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(root_index):
        return send_file(root_index)
    return render_template("index.html")

@app.route("/classic")
def classic():
    return render_template("index.html")

@app.route("/generate", methods=["POST"]) 
def generate():
    name = request.form.get("name", "").strip()
    job_title = request.form.get("job_title", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()
    location = request.form.get("location", "").strip()
    linkedin = request.form.get("linkedin", "").strip()
    github = request.form.get("github", "").strip()
    website = request.form.get("website", "").strip()
    summary = request.form.get("summary", "").strip()
    skills = request.form.get("skills", "").strip()
    languages = request.form.get("languages", "").strip()
    references = request.form.get("references", "").strip()

    experiences_json = request.form.get("experiences_json", "[]")
    education_json = request.form.get("education_json", "[]")
    projects_json = request.form.get("projects_json", "[]")
    certifications_json = request.form.get("certifications_json", "[]")
    extras_json = request.form.get("extras_json", "[]")

    try:
        experiences = json.loads(experiences_json) if experiences_json else []
    except Exception:
        experiences = []
    try:
        education = json.loads(education_json) if education_json else []
    except Exception:
        education = []
    try:
        projects = json.loads(projects_json) if projects_json else []
    except Exception:
        projects = []
    try:
        certifications = json.loads(certifications_json) if certifications_json else []
    except Exception:
        certifications = []
    try:
        extras = json.loads(extras_json) if extras_json else []
    except Exception:
        extras = []

    output_format = request.form.get("output_format", "docx").lower()
    template = request.form.get("template", "sidebar")
    accent = request.form.get("accent", "#b87333")

    data = {
        "name": name,
        "job_title": job_title,
        "phone": phone,
        "email": email,
        "location": location,
        "linkedin": linkedin,
        "github": github,
        "website": website,
        "summary": summary,
        "skills": [s.strip() for s in skills.split("\n") if s.strip()],
        "languages": [l.strip() for l in languages.split("\n") if l.strip()],
        "references": references,
        "experiences": experiences,
        "education": education,
        "projects": projects,
        "certifications": certifications,
        "extras": extras,
    }

    tmp_dir = tempfile.mkdtemp()
    if output_format == "pdf":
        tmp_path = os.path.join(tmp_dir, f"{name or 'cv'}.pdf")
        build_pdf(data, tmp_path, template, accent)
        return send_file(tmp_path, as_attachment=True)
    else:
        tmp_path = os.path.join(tmp_dir, f"{name or 'cv'}.docx")
        build_docx(data, tmp_path, template, accent)
        return send_file(tmp_path, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

