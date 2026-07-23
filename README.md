# 🎯 Career Radar • AI Resume Analyzer

An intelligent, AI-powered system designed to analyze resumes against specific job descriptions. By leveraging advanced Natural Language Processing (NLP) and Google's Gemini Large Language Models (LLMs), Career Radar provides actionable insights to help candidates optimize their applications and land their dream jobs.

## ✨ Key Features
* **Smart Matching Engine**: Calculates an accurate Match Score using `SentenceTransformers` (all-MiniLM-L6-v2) by measuring the cosine similarity between the resume content and the job description.
* **Deep AI Analysis**: Utilizes Google's Gemini API to generate:
  * 📄 Professional Summary
  * 📈 Comprehensive Match Analysis
  * ✅ Candidate Strengths
  * ⚠️ Potential Weaknesses & Missing Skills
  * 💡 Actionable Improvement Tips
  * 🎯 Final Hiring Recommendation
* **Seamless User Experience**: A clean, interactive, and responsive web interface built with `Streamlit`.
* **Automated PDF Parsing**: Extracts text cleanly from resumes using `PyMuPDF`.

## 🛠️ Tech Stack
* **Frontend**: Streamlit
* **Backend**: Python, Flask
* **AI & NLP**: Google Gemini API (`google-genai`), PyTorch, Sentence Transformers, Numpy
* **Data Extraction**: PyMuPDF (`fitz`)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/Career-Radar.git](https://github.com/YOUR_USERNAME/Career-Radar.git)
cd Career-Radar
