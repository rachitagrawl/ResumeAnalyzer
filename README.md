# ResumeAnalyzer
This is a Streamlit-based web application that allows users to classify resumes into different job categories and check their compatibility with job roles based on ATS (Applicant Tracking System) keyword matching.

#Features
1. Resume Category Prediction: Predicts the job category (e.g., Data Scientist, Software Engineer, Web Developer, etc.) based on the resume's content.
2. ATS Compatibility Checker: Checks the compatibility of a resume with a specific job role (e.g., Data Scientist, Software Engineer) by comparing the resume's content with job-specific keywords.

#Prerequisites
Before running this app, make sure you have the following installed:
Python 3.x
pip (Python package manager)

#Installation
1. Clone or download the repository.
2. Install the required dependencies by running the following command in the terminal or command prompt:
   pip install streamlit scikit-learn python-docx PyPDF2
3.Ensure the following files are present in the same directory as the app:
       a. clf.pkl - The pre-trained model file.
       b. tfidf.pkl - The TF-IDF vectorizer.
       c. encoder.pkl - The label encoder for job category prediction.

#How to Run the App
1. After installing the dependencies and ensuring the necessary files are in place, run the following command to start the Streamlit app:
            streamlit run app.py
   
2.The app will open in your default web browser. If it doesn't open automatically, navigate to the URL provided by Streamlit (usually http://localhost:8501).

#How to Use the App
1. Resume Category Prediction
  a.Upload your resume in PDF, DOCX, or TXT format.
  b.The app will display the extracted text from the resume.
  c.After the resume is processed, the app will predict the job category based on its content.

2.ATS Compatibility Checker
a. Upload your resume (PDF, DOCX, or TXT format).
b. Select the job role (e.g., Data Scientist, Software Engineer, etc.) from the dropdown.
c. Click on the "Run ATS Check" button to see how compatible your resume is with the selected job role.
d. The app will show you the ATS score, matched keywords, and missing keywords based on the role.

#Troubleshooting
1.If the app doesn't work: Make sure that you have all required files (like the model files) in the correct directory.
2.Error Handling: If the app throws any errors during file upload or processing, make sure the file format is correct (PDF, DOCX, or TXT).

