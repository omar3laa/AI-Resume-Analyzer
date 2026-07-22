"""
Career Radar - Backend API
==========================

Responsible for:

1. Receive PDF + Job Description
2. Call Task 1 (PDF Processing)
3. Call Task 2 (Similarity)
4. Call Gemini
5. Return JSON
"""

import os
import json
import traceback

from flask import Flask, request, jsonify
from flask_cors import CORS

from dotenv import load_dotenv
from google import genai

# ==============================
# Person 1 + Person 2
# ==============================

from task1_task2 import run_first_and_second_party_tasks

# ==============================
# Environment Variables
# ==============================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "Please create .env file and add GEMINI_API_KEY"
    )

client = genai.Client(api_key=API_KEY)

# ==============================
# Flask App
# ==============================

app = Flask(__name__)

CORS(app)

# ==============================
# Prompt Builder
# ==============================

def build_prompt(

        cv_text,

        job_description,

        match_score

):

    prompt = f"""
You are a Senior HR Recruiter with more than 15 years of experience.

Compare ONLY the provided CV with the Job Description.

Never invent skills.

Never invent experience.

Candidate Match Score

{match_score}%

===========================================

Candidate CV

{cv_text}

===========================================

Job Description

{job_description}

===========================================

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

Hiring Recommendation MUST be exactly one of:

Strong Match

Good Match

Needs Improvement

Not Recommended
"""

    return prompt


# ==============================
# Gemini Analysis
# ==============================

def analyze_cv_with_llm(

        cv_text,

        job_description,

        match_score

):

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

    # إزالة markdown إن وجد

    if text.startswith("```json"):

        text = text.replace(

            "```json",

            ""

        )

        text = text.replace(

            "```",

            ""

        )

        text = text.strip()

    elif text.startswith("```"):

        text = text.replace(

            "```",

            ""

        )

        text = text.strip()

    try:

        result = json.loads(text)

    except Exception:

        raise ValueError(

            "Gemini returned invalid JSON"

        )

    result["match_score"] = match_score

    return result
# ==========================================
# Analyze Endpoint
# ==========================================

@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        # ----------------------------
        # Validate Request
        # ----------------------------

        if "file" not in request.files:

            return jsonify({

                "error": "No PDF file uploaded."

            }), 400

        pdf_file = request.files["file"]

        job_description = request.form.get(

            "job_description",

            ""

        ).strip()

        if pdf_file.filename == "":

            return jsonify({

                "error": "Please upload a PDF."

            }), 400

        if job_description == "":

            return jsonify({

                "error": "Job Description is required."

            }), 400

        # ==========================================
        # Person 1 + Person 2
        # ==========================================

        result = run_first_and_second_party_tasks(

            pdf_file,

            job_description

        )

        cv_text = result["focused_text"]

        cleaned_text = result["cleaned_text"]

        match_score = result["match_score"]

        # ==========================================
        # Person 3 (Gemini)
        # ==========================================

        llm_result = analyze_cv_with_llm(

            cv_text,

            job_description,

            match_score

        )

        # ==========================================
        # Final JSON
        # ==========================================

        response = {

            "success": True,

            "match_score": match_score,

            "summary":

                llm_result.get(

                    "summary",

                    ""

                ),

            "match_summary":

                llm_result.get(

                    "match_summary",

                    ""

                ),

            "strengths":

                llm_result.get(

                    "strengths",

                    []

                ),

            "weaknesses":

                llm_result.get(

                    "weaknesses",

                    []

                ),

            "missing_skills":

                llm_result.get(

                    "missing_skills",

                    []

                ),

            "tips":

                llm_result.get(

                    "tips",

                    []

                ),

            "hiring_recommendation":

                llm_result.get(

                    "hiring_recommendation",

                    ""

                ),

            "cleaned_text":

                cleaned_text,

            "focused_text":

                cv_text

        }

        return jsonify(response), 200

    except ValueError as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400

    except Exception as e:

        traceback.print_exc()

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ==========================================
# Health Check
# ==========================================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({

        "status": "running",

        "service": "Career Radar Backend"

    })


# ==========================================
# Home
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({

        "project": "Career Radar",

        "backend": "Flask API",

        "status": "Ready"

    })


# ==========================================
# Run Server
# ==========================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=5001,

        debug=True

    )