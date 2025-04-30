# Required installations (mention in README or install via terminal):
# pip install streamlit scikit-learn python-docx PyPDF2

import streamlit as st
import pickle
import docx  # Extract text from Word file
import PyPDF2  # Extract text from PDF
import re

# Load pre-trained model and TF-IDF vectorizer
svc_model = pickle.load(open('clf.pkl', 'rb'))
tfidf = pickle.load(open('tfidf.pkl', 'rb'))
le = pickle.load(open('encoder.pkl', 'rb'))

# Sample keyword database for ATS check (can be expanded)
job_keywords = {
    "Data Scientist": [
        "python", "machine learning", "data analysis", "pandas", "numpy", "model", "statistics", "scikit-learn",
        "data cleaning", "visualization", "regression", "classification", "clustering", "tensorflow", "keras",
        "matplotlib", "seaborn", "jupyter", "sql", "data wrangling"
    ],

    "Software Engineer": [
        "java", "spring", "git", "api", "sql", "docker", "microservices", "kubernetes", "oop", "rest",
        "design patterns", "unit testing", "agile", "jenkins", "maven", "linux", "debugging", "version control"
    ],

    "Web Developer": [
        "html", "css", "javascript", "react", "node", "frontend", "backend", "responsive", "bootstrap", "angular",
        "tailwind", "vue", "express", "mongodb", "api integration", "json", "ajax", "dom", "typescript"
    ],

    "DevOps Engineer": [
        "docker", "kubernetes", "jenkins", "ci/cd", "aws", "terraform", "linux", "ansible", "monitoring",
        "cloudwatch", "shell scripting", "infrastructure as code", "nginx", "git", "deployment", "containers"
    ],

    "UI/UX Designer": [
        "figma", "adobe xd", "wireframes", "prototypes", "user research", "design systems", "interaction design",
        "usability testing", "user personas", "responsive design", "typography", "color theory", "aesthetic"
    ],

    "Mobile App Developer": [
        "android", "kotlin", "java", "flutter", "react native", "ios", "swift", "xcode", "play store", "firebase",
        "ui components", "material design", "api integration", "push notifications", "redux"
    ],

    "Machine Learning Engineer": [
        "machine learning", "deep learning", "tensorflow", "keras", "pytorch", "model training", "model evaluation",
        "sklearn", "feature engineering", "mlops", "hyperparameter tuning", "data pipelines", "cloud ai"
    ],

    "Cloud Engineer": [
        "aws", "azure", "gcp", "cloudformation", "terraform", "vm", "ec2", "s3", "cloudwatch", "lambda", "rds",
        "devops", "networking", "vpn", "load balancer", "autoscaling", "cloud storage"
    ],

    "Database Administrator": [
        "sql", "mysql", "postgresql", "mongodb", "oracle", "database design", "indexing", "joins", "stored procedures",
        "database tuning", "backup", "recovery", "replication", "normalization", "query optimization"
    ],

    "Data Analyst": [
        "sql", "excel", "power bi", "tableau", "data visualization", "pandas", "numpy", "statistics",
        "data cleaning", "data wrangling", "python", "dashboards", "business analysis", "insights",
        "kpi", "trend analysis", "reporting", "matplotlib", "seaborn"
    ]
}

# --- Text Cleaning Function ---
def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText.lower()

# --- File Extractors ---
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def extract_text_from_txt(file):
    try:
        text = file.read().decode('utf-8')
    except UnicodeDecodeError:
        text = file.read().decode('latin-1')
    return text

def handle_file_upload(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == 'pdf':
        text = extract_text_from_pdf(uploaded_file)
    elif file_extension == 'docx':
        text = extract_text_from_docx(uploaded_file)
    elif file_extension == 'txt':
        text = extract_text_from_txt(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")
    return text

# --- Prediction Function ---
def pred(input_resume):
    cleaned_text = cleanResume(input_resume)
    vectorized_text = tfidf.transform([cleaned_text]).toarray()
    predicted_category = svc_model.predict(vectorized_text)
    predicted_category_name = le.inverse_transform(predicted_category)
    return predicted_category_name[0]

# --- ATS Checker Function ---
def ats_check(resume_text, selected_role):
    resume_words = set(cleanResume(resume_text).split())
    role_keywords = set(job_keywords.get(selected_role, []))
    matched = resume_words & role_keywords
    missing = role_keywords - resume_words
    score = int((len(matched) / len(role_keywords)) * 100) if role_keywords else 0
    return score, matched, missing

# --- Streamlit Layout ---
def main():
    st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")
    st.title("Resume Classifier + ATS Checker")

    tab1, tab2 = st.tabs(["Resume Category Prediction", "ATS Compatibility Check"])

    with tab1:
        st.subheader("Predict Resume Category")
        uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"], key="cat")
        if uploaded_file is not None:
            try:
                resume_text = handle_file_upload(uploaded_file)
                st.success("Resume text extracted successfully.")
                if st.checkbox("Show extracted text", False):
                    st.text_area("Extracted Resume Text", resume_text, height=300)
                st.subheader("Predicted Category")
                category = pred(resume_text)
                st.write(f"Predicted job category: **{category}**")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    with tab2:
        st.subheader("ATS Compatibility Checker")
        uploaded_file_ats = st.file_uploader("Upload Resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"], key="ats")
        selected_role = st.selectbox("Select Target Job Role", list(job_keywords.keys()), key="role")

        if uploaded_file_ats is not None and selected_role:
            if st.button("Run ATS  Check"):
                try:
                    resume_text = handle_file_upload(uploaded_file_ats)
                    score, matched, missing = ats_check(resume_text, selected_role)

                    st.success("Resume proccessed successfully.")
                    st.write(f"### ATS Score: {score}%")
                    st.markdown(f"**Matched Keywords:** {', '.join(matched) if matched else 'None'}")
                    st.markdown(f"**Missing Keywords:** {', '.join(missing) if missing else 'None'}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()