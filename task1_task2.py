import re
import os
import fitz
import numpy as np
from datasets import load_dataset
from sentence_transformers import SentenceTransformer, InputExample, losses
from torch.utils.data import DataLoader

# ==========================================
# Train Model (Only if not already trained)
# ==========================================

MODEL_PATH = "./finetuned_model"

if not os.path.exists(MODEL_PATH):

    print("⏳ جاري تدريب الموديل على البيانات (Fine-Tuning)...")

    # 1. تحميل الموديل الأصلي والداتا سيت
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    ds = load_dataset("AzharAli05/Resume-Screening-Dataset", split="train")

    # 2. تجهيز داتا التدريب (تحويل select لـ 1.0 و reject لـ 0.0)
    train_examples = []
    for row in ds:
        # إعطاء قيم مستهدفة (1 للقبول و 0 للرفض)
        label = 1.0 if row["Decision"] == "select" else 0.0
        train_examples.append(
            InputExample(
                texts=[row["Resume"], row["Job_Description"]], label=label
            )
        )

    # 3. إعداد الـ DataLoader والـ Loss Function
    train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=16)
    train_loss = losses.CosineSimilarityLoss(model)

    # 4. بدء التدريب (2 Epochs، الوقت بيعتمد على حجم الداتا والـ CPU/GPU)
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=2,
        warmup_steps=10,
    )

    # 5. حفظ الموديل بعد التدريب عشان مانكررش التدريب في المرات الجاية
    model.save(MODEL_PATH)
    print("✅ تم التدريب بنجاح!")

else:
    print("ℹ️ الموديل المدرب موجود بالفعل، هيتم تخطي التدريب.")

# ==========================================
# Load Embedding Model (Load Once)
# ==========================================

embedding_model = SentenceTransformer(MODEL_PATH)

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

SECTION_KEYWORDS = [
    "skills",
    "technical skills",
    "experience",
    "projects",
    "education",
    "certifications",
    "summary",
    "work history"
]


def extract_skills_and_experience(cv_text):
    """
    بيحاول يعزل أقسام الـ CV المهمة (Skills, Experience, Projects...)
    بدل ما ياخد كل سطر قصير عشوائي (كان بيدخل نويز زي الاسم/التليفون).

    المنطق: نلاقي أي سطر عنوان قسم (heading)، ونضم كل الأسطر اللي
    جاية بعده لحد ما نوصل لعنوان قسم تاني أو سطر فاضي مزدوج.
    """

    lines = cv_text.split("\n")

    important = []
    inside_relevant_section = False

    for line in lines:

        stripped = line.strip()

        if not stripped:
            continue

        is_heading = (
            len(stripped) < 40
            and any(k in stripped.lower() for k in SECTION_KEYWORDS)
        )

        if is_heading:
            inside_relevant_section = True
            important.append(stripped)
            continue

        # لو وصلنا لعنوان قسم تاني مش من الكلمات المفتاحية بتاعتنا،
        # (سطر قصير غالبًا مش جزء من فقرة) نوقف الالتقاط لحد ما نلاقي
        # قسم مهم جديد
        looks_like_other_heading = (
            len(stripped) < 40
            and stripped.isupper()
        )

        if looks_like_other_heading and not is_heading:
            inside_relevant_section = False
            continue

        if inside_relevant_section:
            important.append(stripped)

    text = "\n".join(important)

    # fallback: لو الاستخراج فشل ورجع نص قصير جدًا، استخدم النص الخام كامل
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

    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)

    if norm_product == 0:
        return 0.0

    similarity = np.dot(vec1, vec2) / norm_product

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

def run_first_and_second_party_tasks(pdf_file, job_description):

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
