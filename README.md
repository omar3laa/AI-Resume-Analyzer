# 🎯 Career Radar • AI Resume Analyzer

An intelligent, AI-powered system designed to analyze resumes against specific job descriptions. By leveraging advanced Natural Language Processing (NLP) and Google's Gemini Large Language Models (LLMs), Career Radar provides actionable insights to help candidates optimize their applications and increase their chances of landing interviews.

---

## 📸 Demo

> Add screenshots or a GIF of your application here.

| Upload Resume | Analysis Results |
|---------------|------------------|
| ![Upload](assets/upload.png) | ![Results](assets/results.png) |

---

## ✨ Key Features

- 🎯 **Smart Matching Engine**
  - Calculates an accurate Resume Match Score using SentenceTransformers (`all-MiniLM-L6-v2`) and Cosine Similarity.

- 🤖 **AI-Powered Resume Analysis**
  - Professional Summary
  - Resume vs Job Description Analysis
  - Candidate Strengths
  - Missing Skills Detection
  - Weakness Analysis
  - Resume Improvement Suggestions
  - Hiring Recommendation

- 📄 **Automatic Resume Parsing**
  - Extracts text from PDF resumes using PyMuPDF.

- ⚡ **Fast & Interactive Interface**
  - Clean and responsive Streamlit web application.

- 🔒 **Secure API Integration**
  - API keys are stored using environment variables.

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python
- Flask

### AI & NLP
- Google Gemini API
- SentenceTransformers
- PyTorch
- NumPy

### PDF Processing
- PyMuPDF

---

## 🏗️ System Architecture

```text
                 PDF Resume
                      │
                      ▼
              PyMuPDF Parser
                      │
                      ▼
              Extract Resume Text
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
Sentence Transformer        Job Description
          │                       │
          └───────────┬───────────┘
                      ▼
              Cosine Similarity
                      │
              Match Percentage
                      │
                      ▼
               Google Gemini API
                      │
                      ▼
      AI Analysis & Recommendations
                      │
                      ▼
                Streamlit Interface
```

---

## 📂 Project Structure

```text
Career-Radar/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── assets/
│   ├── upload.png
│   └── results.png
│
├── utils/
│   ├── parser.py
│   ├── similarity.py
│   ├── gemini.py
│   ├── prompts.py
│   └── helpers.py
│
└── sample_resume.pdf
```

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Career-Radar.git
cd Career-Radar
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate it

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The application will open automatically in your browser.

---

## 📊 Example Output

```text
Resume Match Score
------------------
86%

Professional Summary
--------------------
AI student with strong experience in Python, NLP,
Deep Learning and Machine Learning.

Strengths
---------
✔ Python
✔ Machine Learning
✔ NLP
✔ TensorFlow

Missing Skills
--------------
✖ Docker
✖ AWS
✖ CI/CD

Weaknesses
----------
Limited cloud deployment experience.

Recommendations
---------------
• Add cloud projects.
• Include Docker experience.
• Quantify project achievements.

Final Decision
--------------
Highly Recommended
```

---

## 📈 Performance

| Metric | Value |
|---------|---------|
| Embedding Model | all-MiniLM-L6-v2 |
| Similarity Metric | Cosine Similarity |
| LLM | Google Gemini |
| Framework | Streamlit |
| Average Analysis Time | ~5 Seconds |

---

## 📚 Main Libraries

- Streamlit
- Flask
- SentenceTransformers
- PyTorch
- NumPy
- PyMuPDF
- google-genai
- python-dotenv

---

## 🚀 Future Improvements

- ATS Score Prediction
- Resume Keyword Optimization
- Resume Rewrite with AI
- Cover Letter Generator
- Interview Question Generator
- Resume Ranking for Multiple Candidates
- DOCX Resume Support
- OCR for Scanned Resumes
- Multi-language Resume Analysis
- Skill Gap Dashboard
- Resume History Tracking

---

## ⭐ Project Highlights

- Built an end-to-end AI Resume Analyzer using NLP and Large Language Models.
- Integrated Google Gemini API for intelligent resume evaluation.
- Implemented semantic similarity using SentenceTransformers.
- Automated PDF resume parsing with PyMuPDF.
- Designed an interactive Streamlit interface for real-time analysis.
- Generated AI-powered hiring recommendations and personalized resume improvement suggestions.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Omar Alaa**
- GitHub: https://github.com/omar3laa

**Ahmed Osman**
- GitHub: https://github.com/ahmedosman1542005-al
**Mahmoud khamis**
  - GitHub: https://github.com/Mahmoud70-7
**Hossam Gamal**
  - GitHub: https://github.com/Hossam293


