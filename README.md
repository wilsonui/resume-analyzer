# 🧠 Smart Resume Analyzer & Job Matcher

> An AI-powered resume analysis tool that calculates ATS scores, matches job roles, identifies skill gaps, and provides actionable improvement suggestions — all in under 5 seconds.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-green) ![License](https://img.shields.io/badge/license-MIT-orange)

---

## 🏗️ System Architecture

```
User Browser
    │
    ▼
Flask Web Server (app.py)
    │
    ├── /upload ──► utils/parser.py     → Text extraction + NLP parsing
    │                utils/scoring.py   → ATS score calculation (8 dimensions)
    │                utils/matcher.py   → Cosine similarity job matching
    │
    ├── /result/<id> ──► templates/result.html
    └── /dashboard/<id> ──► templates/dashboard.html (Chart.js)

models/
└── skill_model.py  ─ Skills DB (200+ skills) + 8 Job Role definitions
```

---

## 🚀 Quick Start

### Option 1 — Automated (Linux/Mac)
```bash
git clone <your-repo>
cd resume-analyzer
chmod +x run.sh
./run.sh
```

### Option 2 — Manual
```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate          # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py

# 4. Open in browser
# http://localhost:5000
```

---

## 📁 Project Structure

```
resume-analyzer/
│
├── app.py                  ← Flask application (routes, upload handler)
├── requirements.txt        ← Python dependencies
├── run.sh                  ← Quick start script
│
├── models/
│   └── skill_model.py      ← Skills database + Job roles database
│
├── utils/
│   ├── parser.py           ← PDF/DOCX text extraction + NLP parsing
│   ├── scoring.py          ← ATS score engine (8-dimensional scoring)
│   └── matcher.py          ← Cosine similarity job matching + skill gap
│
├── templates/
│   ├── index.html          ← Upload page (drag & drop)
│   ├── result.html         ← Full analysis results page
│   └── dashboard.html      ← Analytics dashboard (Chart.js)
│
├── static/
│   └── uploads/            ← Temporary file storage (auto-cleaned)
│
└── data/
    └── sample_resume.txt   ← Sample resume for testing
```

---

## ✨ Features

| Feature | Description |
|---|---|
| **Resume Upload** | Drag & drop PDF/DOCX, up to 5MB |
| **Text Extraction** | PyPDF2 for PDFs, python-docx for DOCX |
| **Profile Parsing** | Name, email, phone, LinkedIn, GitHub |
| **Skill Detection** | 200+ skills across 9 categories |
| **ATS Score** | 0–100 score across 8 dimensions |
| **Job Matching** | Cosine similarity against 8 job roles |
| **Skill Gap** | Missing skills per role |
| **Suggestions** | Actionable improvement tips |
| **Dashboard** | 5 interactive Chart.js visualizations |

---

## 🎯 ATS Score Dimensions

| Dimension | Weight | What It Checks |
|---|---|---|
| Contact Info | 10 | Name, email, phone present |
| Section Structure | 15 | Required sections (Experience, Education, Skills) |
| Skill Diversity | 20 | Breadth of skills across categories |
| Keyword Density | 15 | ATS power words, action verbs |
| Action Verbs | 10 | Strong verbs in experience bullets |
| Measurable Impact | 10 | Numbers/metrics in experience |
| Resume Length | 10 | 300–700 word ideal range |
| Education | 10 | Education section completeness |

---

## 💼 Supported Job Roles

- Data Analyst
- Machine Learning Engineer  
- Backend Developer
- Frontend Developer
- Full Stack Developer
- DevOps Engineer
- AI/NLP Engineer
- Cybersecurity Analyst

---

## 🌐 Deployment

### Render.com (Free tier)
```bash
# 1. Push to GitHub
# 2. Connect repo on render.com
# 3. Set:
#    Build Command: pip install -r requirements.txt
#    Start Command: python app.py
#    Port: 5000
```

### Heroku
```bash
# Create Procfile:
echo "web: python app.py" > Procfile
heroku create resume-analyzer-app
git push heroku main
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```
```bash
docker build -t resume-analyzer .
docker run -p 5000:5000 resume-analyzer
```

---

## 🔮 Extra Features to Stand Out

1. **User Authentication** — Flask-Login + SQLite to save analysis history
2. **Resume Builder** — Generate improved resumes based on suggestions  
3. **Email Reports** — Send PDF analysis reports via Flask-Mail
4. **Company-Specific JD Matching** — Paste any job description to match
5. **Sentence Transformers** — Replace TF-IDF with `all-MiniLM-L6-v2` for better semantic matching
6. **Real-time Job Scraping** — Scrape LinkedIn/Indeed JDs for live matching
7. **Resume Scoring History** — Track improvement over multiple uploads
8. **REST API** — Expose `/api/analyze` for third-party integrations
9. **LinkedIn Import** — Parse LinkedIn profile PDF
10. **Dark/Light Mode Toggle** — UX enhancement

---

## 🧪 Testing

Use the included `data/sample_resume.txt` — save it as a `.txt` file, rename to `.pdf` or create a DOCX from it to test all features.

---

## 📄 License

MIT — Free for portfolio, educational, and commercial use.
