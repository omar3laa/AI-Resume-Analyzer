import streamlit as st
import requests

# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="Career Radar",
    page_icon="📄",
    layout="wide"
)

st.title("🎯 Career Radar")
st.markdown("### AI Resume Analyzer")

st.divider()

BACKEND_URL = "http://127.0.0.1:5001/analyze"

# ==========================================
# Session State (عشان النتيجة تفضل ظاهرة بعد أي rerun)
# ==========================================

if "result" not in st.session_state:
    st.session_state.result = None

# ==========================================
# Upload PDF
# ==========================================

uploaded_file = st.file_uploader(
    "Upload Your Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste the Job Description here..."
)

analyze = st.button(
    "Analyze Resume",
    type="primary",
    use_container_width=True
)

# ==========================================
# Call Backend
# ==========================================

if analyze:

    if uploaded_file is None:
        st.error("Please upload your resume.")
        st.stop()

    if job_description.strip() == "":
        st.error("Please enter Job Description.")
        st.stop()

    with st.spinner("Analyzing Resume..."):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file,
                "application/pdf"
            )
        }

        data = {
            "job_description": job_description
        }

        try:
            response = requests.post(
                BACKEND_URL,
                files=files,
                data=data,
                timeout=60  # عشان الواجهة متعلقش لو الباك إند أو Gemini بطيئين
            )
            result = response.json()

        except requests.exceptions.Timeout:
            st.error("Backend took too long to respond. Please try again.")
            st.stop()

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to Backend. Make sure it's running on port 5001.")
            st.stop()

        except Exception:
            st.error("Unexpected error while contacting the backend.")
            st.stop()

        if not response.ok:
            st.error(
                result.get(
                    "error",
                    "Unknown Error"
                )
            )
            st.stop()

        # نخزن النتيجة في session_state عشان تفضل ظاهرة
        # حتى بعد إعادة تشغيل السكريبت (rerun) بتاعة Streamlit
        st.session_state.result = result

# ==========================================
# Display Results (بيتنفذ بس لو فيه نتيجة محفوظة)
# ==========================================

if st.session_state.result is not None:

    result = st.session_state.result

    st.divider()

    st.subheader("📊 Analysis Result")

    score = result.get("match_score", 0)

    st.progress(min(int(score), 100))

    st.metric(
        label="Match Score",
        value=f"{score}%"
    )

    st.divider()

    # ==========================================
    # Summary
    # ==========================================

    st.subheader("📄 Professional Summary")

    st.info(
        result.get(
            "summary",
            "No summary available."
        )
    )

    # ==========================================
    # Match Summary
    # ==========================================

    st.subheader("📈 Match Analysis")

    st.write(
        result.get(
            "match_summary",
            "No analysis available."
        )
    )

    st.divider()

    col1, col2 = st.columns(2)

    # ==========================================
    # Strengths
    # ==========================================

    with col1:

        st.subheader("✅ Strengths")

        strengths = result.get("strengths", [])

        if strengths:
            for item in strengths:
                st.success(item)
        else:
            st.write("No strengths found.")

    # ==========================================
    # Weaknesses
    # ==========================================

    with col2:

        st.subheader("⚠️ Weaknesses")

        weaknesses = result.get("weaknesses", [])

        if weaknesses:
            for item in weaknesses:
                st.warning(item)
        else:
            st.write("No weaknesses found.")

    st.divider()

    # ==========================================
    # Missing Skills
    # ==========================================

    st.subheader("❌ Missing Skills")

    missing = result.get("missing_skills", [])

    if missing:
        for skill in missing:
            st.error(skill)
    else:
        st.success("No missing skills detected.")

    st.divider()

    # ==========================================
    # Improvement Tips
    # ==========================================

    st.subheader("💡 Improvement Tips")

    tips = result.get("tips", [])

    if tips:
        for i, tip in enumerate(tips, start=1):
            st.write(f"**{i}.** {tip}")
    else:
        st.write("No tips available.")

    st.divider()

    # ==========================================
    # Hiring Recommendation
    # ==========================================

    recommendation = result.get("hiring_recommendation", "")

    if recommendation == "Strong Match":
        st.success(f"🎉 {recommendation}")
    elif recommendation == "Good Match":
        st.info(f"👍 {recommendation}")
    elif recommendation == "Needs Improvement":
        st.warning(f"⚡ {recommendation}")
    elif recommendation:
        st.error(f"❌ {recommendation}")

    st.divider()

    st.caption("Career Radar • AI Resume Analyzer")
