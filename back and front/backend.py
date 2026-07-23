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

import traceback

from flask import Flask, request, jsonify
from flask_cors import CORS

# ==============================
# Person 1 + Person 2
# ==============================

from task1_task2 import run_first_and_second_party_tasks

# ==============================
# Person 3 (shared LLM logic)
# ==============================

from llm_service import analyze_cv_with_llm

# ==============================
# Flask App
# ==============================

app = Flask(__name__)

CORS(app)

# حد أقصى 10MB لأي ملف مرفوع، عشان محدش يرفع PDF ضخم يعلّق السيرفر
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024


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

        if not pdf_file.filename.lower().endswith(".pdf"):
            return jsonify({
                "error": "Only PDF files are supported."
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
            "summary": llm_result.get("summary", ""),
            "match_summary": llm_result.get("match_summary", ""),
            "strengths": llm_result.get("strengths", []),
            "weaknesses": llm_result.get("weaknesses", []),
            "missing_skills": llm_result.get("missing_skills", []),
            "tips": llm_result.get("tips", []),
            "hiring_recommendation": llm_result.get("hiring_recommendation", ""),
            "cleaned_text": cleaned_text,
            "focused_text": cv_text
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
    # debug=False عشان نمنع الـ auto-reloader من تحميل موديل
    # SentenceTransformer مرتين وقت الـ startup
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )
