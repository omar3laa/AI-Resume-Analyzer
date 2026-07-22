import re
import fitz
import numpy as np
from sentence_transformers import SentenceTransformer

# ==========================================
# Load Embedding Model (Load Once)
# ==========================================

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================
# PDF Extraction
# ==========================================

def extract_text_from_pdf(uploaded_file):

    if isinstance(uploaded_file, str):
        doc = fitz.open(uploaded_file)

    elif hasattr(uploaded_file, "read"):
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    else:
        doc = fitz.open(stream=uploaded_file, filetype="pdf")

    text = ""

    for page in doc:
        text += page.get_text()

    doc.close()

    return text

# ==========================================
# Text Cleaning
# ==========================================

def clean_text(text):

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s.,@+\-/#()]", " ", text)

    return text.strip()

# ==========================================
# Extract Important Sections
# ==========================================

def extract_skills_and_experience(cv_text):

    lower = cv_text.lower()

    keywords = [
        "skills",
        "technical skills",
        "experience",
        "projects",
        "education",
        "certifications",
        "summary",
        "work history"
    ]

    important = []

    for line in cv_text.split("\n"):

        if any(k in line.lower() for k in keywords):

            important.append(line)

        elif len(line.strip()) < 60:

            important.append(line)

    text = "\n".join(important)

    if len(text) < 100:
        return cv_text

    return text

# ==========================================
# CV Processing
# ==========================================

def process_cv(uploaded_file):

    raw_text = extract_text_from_pdf(uploaded_file)

    cleaned_text = clean_text(raw_text)

    focused_text = extract_skills_and_experience(raw_text)

    cleaned_focused = clean_text(focused_text)

    return {

        "raw_text": raw_text,

        "cleaned_text": cleaned_text,

        "focused_text": cleaned_focused

    }

# ==========================================
# Embedding
# ==========================================

def generate_embedding(text):

    return embedding_model.encode(text)

# ==========================================
# Cosine Similarity
# ==========================================

def calculate_cosine_similarity(vec1, vec2):

    similarity = np.dot(vec1, vec2)

    similarity /= (
        np.linalg.norm(vec1)
        *
        np.linalg.norm(vec2)
    )

    return float(similarity)

# ==========================================
# Match Score
# ==========================================

def get_match_score(cv_text, job_description):

    cv_clean = clean_text(cv_text)

    jd_clean = clean_text(job_description)

    cv_embedding = generate_embedding(cv_clean)

    jd_embedding = generate_embedding(jd_clean)

    similarity = calculate_cosine_similarity(
        cv_embedding,
        jd_embedding
    )

    score = similarity * 100

    score = max(0, min(100, score))

    return round(score, 2)

# ==========================================
# Integration Function
# ==========================================

def run_first_and_second_party_tasks(
        pdf_file,
        job_description
):

    cv = process_cv(pdf_file)

    match_score = get_match_score(

        cv["focused_text"],

        job_description

    )

    return {

        "raw_text": cv["raw_text"],

        "cleaned_text": cv["cleaned_text"],

        "focused_text": cv["focused_text"],

        "match_score": match_score

    }

# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    pdf_path = "test.pdf"

    job_description = """
    Machine Learning Engineer

    Requirements

    Python

    TensorFlow

    Docker

    SQL

    AWS

    Flask

    Git
    """

    result = run_first_and_second_party_tasks(

        pdf_path,

        job_description

    )

    print("=" * 50)

    print("Match Score:", result["match_score"])

    print("=" * 50)

    print(result["focused_text"][:1000])