# utils/scoring.py
# ATS Score calculation engine

import re
from models.skill_model import (
    ATS_POWER_WORDS, WEAK_VERBS, REQUIRED_SECTIONS, RESUME_SECTIONS
)

# ─────────────────────────────────────────────
# SCORING WEIGHTS
# ─────────────────────────────────────────────
WEIGHTS = {
    "contact_info":      10,   # Name, email, phone present
    "section_structure": 15,   # Required sections present
    "skill_diversity":   20,   # Breadth of skills across categories
    "keyword_density":   15,   # Keywords matching ATS expectations
    "action_verbs":      10,   # Strong action verbs used
    "quantification":    10,   # Metrics/numbers in experience
    "length_quality":    10,   # Appropriate resume length
    "education":         10,   # Education section present and detailed
}

assert sum(WEIGHTS.values()) == 100, "Weights must sum to 100"


# ─────────────────────────────────────────────
# INDIVIDUAL SCORERS
# ─────────────────────────────────────────────

def score_contact_info(parsed: dict) -> tuple[float, list]:
    """Score based on presence of name, email, phone."""
    score = 0
    tips = []
    max_score = WEIGHTS["contact_info"]

    if parsed.get("name") and parsed["name"] != "Not Found":
        score += max_score * 0.4
    else:
        tips.append("Add your full name prominently at the top of your resume.")

    if parsed.get("email"):
        score += max_score * 0.35
    else:
        tips.append("Include a professional email address.")

    if parsed.get("phone"):
        score += max_score * 0.25
    else:
        tips.append("Add your phone number for recruiters to contact you.")

    return round(score, 1), tips


def score_section_structure(parsed: dict) -> tuple[float, list]:
    """Score based on presence of required resume sections."""
    sections = [s.lower() for s in parsed.get("sections_found", [])]
    max_score = WEIGHTS["section_structure"]
    score = 0
    tips = []

    # Required sections carry more weight
    required_found = sum(1 for s in REQUIRED_SECTIONS if s in sections)
    score += (required_found / len(REQUIRED_SECTIONS)) * (max_score * 0.7)

    # Extra sections (projects, certifications, summary) add bonus
    bonus_sections = ["projects", "certifications", "summary", "achievements"]
    bonus_found = sum(1 for s in bonus_sections if s in sections)
    score += min(bonus_found, 3) / 3 * (max_score * 0.3)

    missing_required = [s for s in REQUIRED_SECTIONS if s not in sections]
    if missing_required:
        tips.append(f"Add missing sections: {', '.join(s.title() for s in missing_required)}.")

    if "summary" not in sections:
        tips.append("Add a professional summary/objective (3-4 lines) at the top.")

    if "certifications" not in sections:
        tips.append("Consider adding a Certifications section to boost your profile.")

    return round(score, 1), tips


def score_skill_diversity(parsed: dict) -> tuple[float, list]:
    """Score based on breadth and number of detected skills."""
    skills_dict = parsed.get("skills", {})
    flat_skills = parsed.get("flat_skills", [])
    max_score = WEIGHTS["skill_diversity"]
    tips = []

    # Number of skill categories
    num_categories = len(skills_dict)
    # Total skills found
    num_skills = len(flat_skills)

    # Category score (up to 60% of weight)
    category_score = min(num_categories / 4, 1.0) * (max_score * 0.5)
    # Total skills score (up to 40% of weight)
    skill_count_score = min(num_skills / 15, 1.0) * (max_score * 0.5)

    score = category_score + skill_count_score

    if num_skills < 5:
        tips.append("Add more technical skills — aim for at least 10-15 relevant skills.")
    if num_categories < 2:
        tips.append("Diversify your skills across multiple categories (e.g., languages + frameworks + tools).")
    if "soft_skills" not in skills_dict:
        tips.append("Include soft skills like leadership, communication, or teamwork.")
    if "cloud_devops" not in skills_dict:
        tips.append("Add cloud/DevOps tools (Docker, Git, AWS) even if you have basic knowledge.")

    return round(score, 1), tips


def score_keyword_density(parsed: dict) -> tuple[float, list]:
    """Score based on presence of ATS-friendly power keywords."""
    text_lower = parsed.get("raw_text", "").lower()
    max_score = WEIGHTS["keyword_density"]
    tips = []

    found_power_words = [w for w in ATS_POWER_WORDS if w in text_lower]
    found_weak_verbs = [w for w in WEAK_VERBS if re.search(r"\b" + w + r"\b", text_lower)]

    # Power word score
    power_ratio = min(len(found_power_words) / 8, 1.0)
    score = power_ratio * max_score

    # Penalize weak verbs
    if len(found_weak_verbs) > 3:
        penalty = min((len(found_weak_verbs) - 3) * 0.5, max_score * 0.3)
        score = max(0, score - penalty)
        tips.append(f"Replace weak verbs ({', '.join(found_weak_verbs[:4])}) with strong action verbs.")

    if len(found_power_words) < 4:
        tips.append(
            f"Use more action verbs like: built, developed, optimized, implemented, deployed."
        )

    return round(score, 1), tips


def score_action_verbs(parsed: dict) -> tuple[float, list]:
    """Score based on strong action verbs in experience section."""
    experience_text = parsed.get("sections", {}).get("experience", "").lower()
    max_score = WEIGHTS["action_verbs"]
    tips = []

    found_verbs = [v for v in ATS_POWER_WORDS if re.search(r"\b" + v + r"\b", experience_text)]
    ratio = min(len(found_verbs) / 5, 1.0)
    score = ratio * max_score

    if len(found_verbs) < 3:
        tips.append("Start each bullet point in your experience section with a strong action verb.")

    return round(score, 1), tips


def score_quantification(parsed: dict) -> tuple[float, list]:
    """Score based on presence of numbers/metrics in experience."""
    experience_text = parsed.get("sections", {}).get("experience", "")
    raw_text = parsed.get("raw_text", "")
    max_score = WEIGHTS["quantification"]
    tips = []

    # Look for patterns like: 20%, 3x, $50K, reduced by 40, 10+ users
    metric_pattern = r"\b\d+[\%xX]?\b|\$\s*\d+|\d+\s*(?:users|customers|projects|percent|%)"
    metrics_in_exp = re.findall(metric_pattern, experience_text)
    metrics_total = re.findall(metric_pattern, raw_text)

    count = len(metrics_in_exp)
    score = min(count / 4, 1.0) * max_score

    if count == 0:
        tips.append("Add measurable achievements — e.g., 'Improved performance by 30%' or 'Served 10K+ users'.")
    elif count < 3:
        tips.append("Quantify more achievements with numbers, percentages, or metrics.")

    return round(score, 1), tips


def score_length_quality(parsed: dict) -> tuple[float, list]:
    """Score based on resume length (word count)."""
    word_count = parsed.get("word_count", 0)
    max_score = WEIGHTS["length_quality"]
    tips = []

    # Ideal range: 300-700 words for a 1-page resume
    if 300 <= word_count <= 700:
        score = max_score
    elif 200 <= word_count < 300 or 700 < word_count <= 900:
        score = max_score * 0.7
        if word_count < 300:
            tips.append("Your resume seems too short. Add more detail to your experience and projects.")
        else:
            tips.append("Your resume is a bit long. Consider trimming to 1-2 pages for better readability.")
    elif word_count < 200:
        score = max_score * 0.4
        tips.append("Resume is very sparse. Significantly expand your experience, skills, and project descriptions.")
    else:
        score = max_score * 0.5
        tips.append("Resume is very long. ATS systems prefer concise resumes under 700 words for entry-level roles.")

    return round(score, 1), tips


def score_education(parsed: dict) -> tuple[float, list]:
    """Score based on education section quality."""
    education = parsed.get("education", [])
    sections = parsed.get("sections_found", [])
    max_score = WEIGHTS["education"]
    tips = []

    if not education and "education" not in sections:
        tips.append("Add an Education section with your degree, institution, and graduation year.")
        return 0, tips

    score = max_score * 0.5  # Base for having education
    if len(education) >= 1:
        score += max_score * 0.3
    if len(education) >= 2:
        score += max_score * 0.2

    # Check if year is present in education
    has_year = any(re.search(r"\b(19|20)\d{2}\b", e) for e in education)
    if not has_year:
        tips.append("Include graduation year(s) in your education entries.")

    return round(score, 1), tips


# ─────────────────────────────────────────────
# MASTER SCORE CALCULATOR
# ─────────────────────────────────────────────

def calculate_ats_score(parsed: dict) -> dict:
    """
    Calculate the overall ATS score and return a full breakdown
    with per-category scores, suggestions, and grade.
    """
    scorers = [
        ("contact_info",      score_contact_info),
        ("section_structure", score_section_structure),
        ("skill_diversity",   score_skill_diversity),
        ("keyword_density",   score_keyword_density),
        ("action_verbs",      score_action_verbs),
        ("quantification",    score_quantification),
        ("length_quality",    score_length_quality),
        ("education",         score_education),
    ]

    breakdown = {}
    all_suggestions = []
    total_score = 0.0

    for key, scorer_fn in scorers:
        s, tips = scorer_fn(parsed)
        breakdown[key] = {
            "score": s,
            "max": WEIGHTS[key],
            "percentage": round((s / WEIGHTS[key]) * 100) if WEIGHTS[key] > 0 else 0,
            "label": _label(key)
        }
        total_score += s
        all_suggestions.extend(tips)

    total = round(total_score)

    return {
        "total_score": total,
        "grade": _grade(total),
        "grade_color": _grade_color(total),
        "breakdown": breakdown,
        "suggestions": all_suggestions,
        "summary": _score_summary(total)
    }


def _label(key: str) -> str:
    labels = {
        "contact_info":      "Contact Info",
        "section_structure": "Section Structure",
        "skill_diversity":   "Skill Diversity",
        "keyword_density":   "Keyword Density",
        "action_verbs":      "Action Verbs",
        "quantification":    "Measurable Impact",
        "length_quality":    "Resume Length",
        "education":         "Education",
    }
    return labels.get(key, key.replace("_", " ").title())


def _grade(score: int) -> str:
    if score >= 85:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 55:
        return "C"
    elif score >= 40:
        return "D"
    else:
        return "F"


def _grade_color(score: int) -> str:
    if score >= 85:
        return "#22c55e"   # green
    elif score >= 70:
        return "#3b82f6"   # blue
    elif score >= 55:
        return "#f59e0b"   # amber
    elif score >= 40:
        return "#f97316"   # orange
    else:
        return "#ef4444"   # red


def _score_summary(score: int) -> str:
    if score >= 85:
        return "Excellent! Your resume is highly ATS-optimized and ready to impress recruiters."
    elif score >= 70:
        return "Good resume! A few tweaks will make it stand out even more."
    elif score >= 55:
        return "Average resume. Follow the suggestions below to significantly improve your chances."
    elif score >= 40:
        return "Below average. Your resume needs substantial improvements to pass ATS filters."
    else:
        return "Critical issues found. Your resume may be automatically rejected by ATS systems."
