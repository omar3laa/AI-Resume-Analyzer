import os
import json
from dotenv import load_dotenv
from google import genai

from task1_task2 import run_first_and_second_party_tasks

# ==========================================
# Load API Key
# ==========================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

# ==========================================
# Prompt Builder
# ==========================================

def build_prompt(cv_text, job_description, match_score):

    prompt = f"""
You are a Senior HR Recruiter with over 15 years of experience.

Analyze ONLY the provided information.

Never invent skills.

Never invent experience.

Candidate Match Score

{match_score}%

Candidate CV

{cv_text}

==================================================

Job Description

{job_description}

==================================================

Return ONLY valid JSON.

JSON Format

{{
"summary":"",
"match_summary":"",
"strengths":[],
"weaknesses":[],
"missing_skills":[],
"tips":[],
"hiring_recommendation":""
}}

Hiring Recommendation MUST be exactly one of

Strong Match

Good Match

Needs Improvement

Not Recommended
"""

    return prompt

# ==========================================
# Gemini Analysis
# ==========================================

def analyze_resume(pdf_file, job_description):

    result = run_first_and_second_party_tasks(
        pdf_file,
        job_description
    )

    cv_text = result["focused_text"]

    match_score = result["match_score"]

    prompt = build_prompt(
        cv_text,
        job_description,
        match_score
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    ai_result = json.loads(text)

    ai_result["match_score"] = match_score

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