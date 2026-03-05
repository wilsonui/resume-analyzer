# utils/matcher.py
# Job description matching and skill gap analysis using cosine similarity

import re
import math
from models.skill_model import JOB_ROLES


# ─────────────────────────────────────────────
# TEXT VECTORIZATION (TF-IDF without sklearn dependency issues)
# ─────────────────────────────────────────────

def tokenize(text: str) -> list:
    """Simple tokenizer: lowercase, remove punctuation, split."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s+#./]", " ", text)
    return [t for t in text.split() if len(t) > 1]


def build_vocab(docs: list) -> list:
    """Build vocabulary from list of token lists."""
    vocab = set()
    for tokens in docs:
        vocab.update(tokens)
    return sorted(vocab)


def tf(term: str, doc_tokens: list) -> float:
    """Term frequency."""
    if not doc_tokens:
        return 0.0
    return doc_tokens.count(term) / len(doc_tokens)


def idf(term: str, all_docs: list) -> float:
    """Inverse document frequency."""
    n_docs = len(all_docs)
    df = sum(1 for doc in all_docs if term in doc)
    if df == 0:
        return 0.0
    return math.log((n_docs + 1) / (df + 1)) + 1.0


def tfidf_vector(tokens: list, vocab: list, all_docs: list) -> list:
    """Compute TF-IDF vector for a document."""
    return [tf(term, tokens) * idf(term, all_docs) for term in vocab]


def cosine_similarity(vec_a: list, vec_b: list) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a ** 2 for a in vec_a))
    mag_b = math.sqrt(sum(b ** 2 for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


# ─────────────────────────────────────────────
# SKILL-BASED MATCHING
# ─────────────────────────────────────────────

def skill_overlap_score(resume_skills: list, job_required: list, job_nice: list) -> float:
    """
    Calculate match based on skill overlap.
    Required skills carry 70% weight, nice-to-have 30%.
    """
    resume_lower = [s.lower() for s in resume_skills]

    # Required skills match
    if job_required:
        req_matched = sum(1 for s in job_required if s.lower() in resume_lower)
        req_score = req_matched / len(job_required)
    else:
        req_score = 0.0

    # Nice-to-have match
    if job_nice:
        nice_matched = sum(1 for s in job_nice if s.lower() in resume_lower)
        nice_score = nice_matched / len(job_nice)
    else:
        nice_score = 0.0

    return (req_score * 0.70) + (nice_score * 0.30)


def keyword_overlap_score(resume_text: str, job_keywords: list) -> float:
    """Check how many job-specific keywords appear in the resume."""
    text_lower = resume_text.lower()
    if not job_keywords:
        return 0.0
    matched = sum(1 for kw in job_keywords if kw.lower() in text_lower)
    return matched / len(job_keywords)


# ─────────────────────────────────────────────
# JOB MATCHING ENGINE
# ─────────────────────────────────────────────

def match_jobs(parsed: dict) -> list:
    """
    Match the resume against all job roles.
    Returns a sorted list of matches with scores and gap analysis.
    """
    resume_text = parsed.get("raw_text", "")
    flat_skills = parsed.get("flat_skills", [])
    results = []

    # Build TF-IDF corpus
    resume_tokens = tokenize(resume_text)
    job_texts = {role: tokenize(info["description"] + " " + " ".join(info["keywords"]))
                 for role, info in JOB_ROLES.items()}

    all_docs = [resume_tokens] + list(job_texts.values())
    vocab = build_vocab(all_docs)

    # Precompute resume vector
    resume_vec = tfidf_vector(resume_tokens, vocab, all_docs)

    for role, info in JOB_ROLES.items():
        job_tokens = job_texts[role]
        job_vec = tfidf_vector(job_tokens, vocab, all_docs)

        # 1. Text similarity (cosine)
        text_sim = cosine_similarity(resume_vec, job_vec)

        # 2. Skill overlap
        skill_sim = skill_overlap_score(flat_skills, info["required_skills"], info["nice_to_have"])

        # 3. Keyword overlap
        kw_sim = keyword_overlap_score(resume_text, info["keywords"])

        # Weighted blend: skills matter most
        final_score = (skill_sim * 0.55) + (text_sim * 0.25) + (kw_sim * 0.20)
        final_pct = round(min(final_score * 100, 100), 1)

        # Skill gap analysis
        gap = skill_gap(flat_skills, info["required_skills"], info["nice_to_have"])

        results.append({
            "role": role,
            "match_percentage": final_pct,
            "skill_match": round(skill_sim * 100, 1),
            "text_match": round(text_sim * 100, 1),
            "keyword_match": round(kw_sim * 100, 1),
            "matched_skills": gap["matched"],
            "missing_required": gap["missing_required"],
            "missing_nice": gap["missing_nice"],
            "fit_label": fit_label(final_pct),
            "fit_color": fit_color(final_pct),
            "description": info["description"].strip().split("\n")[0]
        })

    # Sort by match percentage descending
    results.sort(key=lambda x: x["match_percentage"], reverse=True)
    return results


# ─────────────────────────────────────────────
# SKILL GAP ANALYSIS
# ─────────────────────────────────────────────

def skill_gap(resume_skills: list, required: list, nice_to_have: list) -> dict:
    """Compute which required and nice-to-have skills are missing."""
    resume_lower = [s.lower() for s in resume_skills]

    matched = [s for s in required if s.lower() in resume_lower]
    missing_req = [s for s in required if s.lower() not in resume_lower]
    missing_nice = [s for s in nice_to_have if s.lower() not in resume_lower]

    return {
        "matched": matched,
        "missing_required": missing_req[:8],    # Top 8 missing required
        "missing_nice": missing_nice[:5],        # Top 5 nice-to-have
    }


# ─────────────────────────────────────────────
# KEYWORD OPTIMIZATION
# ─────────────────────────────────────────────

def keyword_analysis(parsed: dict, job_role: str = None) -> dict:
    """
    Analyse keywords: found good ones, missing important ones, overused ones.
    Optionally filter by a specific job role.
    """
    resume_text = parsed.get("raw_text", "").lower()
    flat_skills = parsed.get("flat_skills", [])
    keywords = parsed.get("keywords", [])

    # Word frequency for overuse detection
    words = re.findall(r"\b[a-z]{3,}\b", resume_text)
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1

    overused = [w for w, c in sorted(freq.items(), key=lambda x: -x[1]) if c >= 5 and len(w) > 4][:10]

    good_keywords = flat_skills[:15]

    if job_role and job_role in JOB_ROLES:
        job_info = JOB_ROLES[job_role]
        all_job_keywords = job_info["keywords"] + job_info["required_skills"]
        missing = [kw for kw in all_job_keywords if kw.lower() not in resume_text][:10]
    else:
        # Generic missing keywords from all jobs
        all_keywords = set()
        for info in JOB_ROLES.values():
            all_keywords.update(info["keywords"])
        missing = [kw for kw in list(all_keywords)[:20] if kw.lower() not in resume_text][:10]

    return {
        "good_keywords": good_keywords,
        "missing_keywords": missing,
        "overused_words": overused
    }


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def fit_label(score: float) -> str:
    if score >= 75:
        return "Excellent Fit"
    elif score >= 55:
        return "Good Fit"
    elif score >= 35:
        return "Partial Fit"
    else:
        return "Low Match"


def fit_color(score: float) -> str:
    if score >= 75:
        return "#22c55e"
    elif score >= 55:
        return "#3b82f6"
    elif score >= 35:
        return "#f59e0b"
    else:
        return "#ef4444"
