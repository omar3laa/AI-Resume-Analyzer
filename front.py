import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

# إعداد الـ Session State لحفظ اللغة (الافتراضي إنجليزي)
if 'lang' not in st.session_state:
    st.session_state.lang = 'English'

# دالة تبديل اللغة
def toggle_lang():
    if st.session_state.lang == 'English':
        st.session_state.lang = 'العربية'
    else:
        st.session_state.lang = 'English'

# إعدادات اللغات (قواميس النصوص)
translations = {
    "العربية": {
        "title": "📄 محلل السيرة الذاتية (AI Resume Analyzer)",
        "welcome": "أهلاً بك! قم برفع الـ CV الخاص بك وأدخل تفاصيل الوظيفة لمعرفة نسبة التوافق.",
        "upload_cv": "ارفع السيرة الذاتية (PDF)",
        "job_desc": "أدخل تفاصيل الوظيفة (Job Description)",
        "analyze_btn": "تحليل السيرة الذاتية",
        "loading": "جاري تحليل البيانات عبر الذكاء الاصطناعي...",
        "success": "تم التحليل بنجاح!",
        "match_score": "نسبة التوافق",
        "summary_title": "📌 ملخص السيرة الذاتية:",
        "no_summary": "لا يوجد ملخص متاح.",
        "tips_title": "💡 نصائح للتحسين:",
        "no_tips": "السيرة الذاتية مطابقة بشكل ممتاز، لا توجد نصائح حالياً.",
        "server_error": "حدث خطأ في سيرفر التحليل. كود الخطأ:",
        "conn_error": "🚨 تعذر الاتصال بالخادم. يرجى التأكد من تشغيل الـ Flask Backend أولاً.",
        "unexp_error": "حدث خطأ غير متوقع:",
        "missing_inputs": "رجاءً قم برفع ملف الـ CV وأدخل تفاصيل الوظيفة أولاً!",
        "lang_btn": "🌐 English"
    },
    "English": {
        "title": "📄 AI Resume Analyzer",
        "welcome": "Welcome! Upload your CV and enter the job description to get your match score.",
        "upload_cv": "Upload Resume (PDF)",
        "job_desc": "Enter Job Description",
        "analyze_btn": "Analyze Resume",
        "loading": "Analyzing data using AI...",
        "success": "Analysis completed successfully!",
        "match_score": "Match Score",
        "summary_title": "📌 Resume Summary:",
        "no_summary": "No summary available.",
        "tips_title": "💡 Improvement Tips:",
        "no_tips": "Your resume is an excellent match. No tips currently.",
        "server_error": "Server error occurred. Status code:",
        "conn_error": "🚨 Connection failed. Please ensure the Flask Backend is running.",
        "unexp_error": "An unexpected error occurred:",
        "missing_inputs": "Please upload a CV and enter the job description first!",
        "lang_btn": "🌐 العربية"
    }
}

# تحديد القاموس بناءً على اللغة الحالية
t = translations[st.session_state.lang]

# وضع زرار تغيير اللغة في أعلى يمين الشاشة
col1, col2 = st.columns([8, 2])
with col2:
    st.button(t["lang_btn"], on_click=toggle_lang, use_container_width=True)

# تطبيق النصوص على الواجهة
st.title(t["title"])
st.write(t["welcome"])

# 2. قسم المدخلات
uploaded_file = st.file_uploader(t["upload_cv"], type=["pdf"])
job_description = st.text_area(t["job_desc"])

# 3. زرار التحليل والربط الفعلي
if st.button(t["analyze_btn"]):
    if uploaded_file is not None and job_description.strip() != "":
        with st.spinner(t["loading"]):
            try:
                # تجهيز الملف والنص للإرسال إلى الـ API
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'application/pdf')}
                data = {'job_description': job_description}
                
                # الاتصال بالـ Flask Backend
                api_url = 'http://127.0.0.1:5000/analyze'
                response = requests.post(api_url, files=files, data=data)
                
                # التأكد من نجاح الطلب
                if response.status_code == 200:
                    result = response.json()
                    st.success(t["success"])
                    
                    # 4. عرض النتائج
                    match_score = result.get('match_score', 0)
                    st.metric(label=t["match_score"], value=f"{match_score}%")
                    st.progress(match_score / 100.0)
                    
                    st.divider()
                    
                    # عرض الملخص
                    st.subheader(t["summary_title"])
                    st.write(result.get('summary', t["no_summary"]))
                    
                    # عرض النصائح
                    st.subheader(t["tips_title"])
                    tips = result.get('tips', [])
                    if tips:
                        for tip in tips:
                            st.warning(f"- {tip}")
                    else:
                        st.info(t["no_tips"])
                        
                else:
                    st.error(f"{t['server_error']} {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error(t["conn_error"])
            except Exception as e:
                st.error(f"{t['unexp_error']} {e}")
    else:
        st.error(t["missing_inputs"])
