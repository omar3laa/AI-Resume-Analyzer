"""
llm_service.py
===============
مكان واحد لكل منطق الـ LLM (بناء الـ Prompt + نداء Gemini + تنضيف الرد).
دي الحاجة الوحيدة اللي backend.py و llm.py المفروض يستوردوا منها،
عشان لو عدّلنا الـ Prompt أو منطق الـ parsing نعدله مرة واحدة بس.
"""

import os
import re
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "Please create a .env file and add GEMINI_API_KEY"
    )

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-2.5-flash"


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

Return ONLY valid JSON. Do not include any text, explanation, or
markdown before or after the JSON object.

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
# Robust JSON Extraction
# ==========================================

def _extract_json(raw_text):
    """
    بيحاول ياخد أي نص JSON من رد الموديل حتى لو حط كلام زيادة
    قبل أو بعد الـ JSON، أو لف الرد بـ ```json ... ``` fences.
    """

    text = raw_text.strip()

    # شيل markdown code fences لو موجودة
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
        if text.endswith("```"):
            text = text[:-3].strip()

    elif text.startswith("```"):
        text = text[3:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()

    # لو لسه فيه كلام زيادة حوالين الـ JSON، دور على أول { وآخر }
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError("Gemini returned invalid JSON")


# ==========================================
# Gemini Call
# ==========================================

def analyze_cv_with_llm(cv_text, job_description, match_score):

    prompt = build_prompt(cv_text, job_description, match_score)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    text = response.text or ""

    result = _extract_json(text)

    # تأكيد إن كل المفاتيح المطلوبة موجودة حتى لو الموديل نسي واحد
    defaults = {
        "summary": "",
        "match_summary": "",
        "strengths": [],
        "weaknesses": [],
        "missing_skills": [],
        "tips": [],
        "hiring_recommendation": ""
    }

    for key, default_value in defaults.items():
        result.setdefault(key, default_value)

    result["match_score"] = match_score

    return result
