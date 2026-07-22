import json

from task1_task2 import run_first_and_second_party_tasks
from llm_service import analyze_cv_with_llm

# ==========================================
# Gemini Analysis (standalone/manual test entrypoint)
# ==========================================

def analyze_resume(pdf_file, job_description):

    result = run_first_and_second_party_tasks(
        pdf_file,
        job_description
    )

    cv_text = result["focused_text"]
    match_score = result["match_score"]

    ai_result = analyze_cv_with_llm(
        cv_text,
        job_description,
        match_score
    )

    ai_result["cleaned_text"] = result["cleaned_text"]
    ai_result["focused_text"] = result["focused_text"]

    return ai_result


# ==========================================
# Test
# ==========================================

if __name__ == "__main__":

    pdf = "test.pdf"

    job = """
Machine Learning Engineer

Requirements

Python

TensorFlow

SQL

AWS

Docker

Git

Flask
"""

    analysis = analyze_resume(
        pdf,
        job
    )

    print(json.dumps(
        analysis,
        indent=4,
        ensure_ascii=False
    ))
