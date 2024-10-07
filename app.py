import os
import openai
import PyPDF2
import docx
from flask import Flask, request, jsonify

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text() or ""
    return text

# Function to extract text from a DOCX file
def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to extract text based on file extension
def extract_text(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        with open(file_path, 'r') as file:
            return file.read()
    else:
        raise ValueError("Unsupported file format")

# Function to generate matching score using OpenAI API
def generate_matching_score(resume_text, job_description):
    prompt = f"""
    Job Description:
    {job_description}

    Resume:
    {resume_text}
    Please evaluate this resume based on the attached job description. Assess the candidate's
    - qualifications,
    - skills,
    - experience, and
    - cultural fit.

    Provide specific feedback on areas where the resume could be strengthened
    """

    response = openai.chat.completions.create(
        model='gpt-4-0613',
        messages=[
            {'role': 'system', 'content': "You are a helpful assistant."},
            {'role': 'user', 'content': prompt}
        ],
        max_tokens=4000,
        temperature=0.5
    )
    generated_content = response.choices[0].message.content.strip()
    return generated_content

# Function to generate a formatted response based on profile analysis
def generate_response(profile_analysis):
    if "match" in profile_analysis.lower():
        response = "The profile matches the job requirements. Here are the details:\n\n"
        response += f"Profile Analysis:\n{profile_analysis}\n"
    else:
        response = "The profile does not meet the job requirements. Key areas of concern:\n\n"
        response += f"Profile Analysis:\n{profile_analysis}\n"
    
    return response

# Function to process multiple resumes for a given job description
def process_resumes_for_job(resume_file_paths, job_description):
    results = {}
    
    for file_path in resume_file_paths:
        if not os.path.exists(file_path):
            results[file_path] = "File not found"
            continue
        
        try:
            resume_text = extract_text(file_path)
            profile_analysis = generate_matching_score(resume_text, job_description)
            response = generate_response(profile_analysis)
            results[file_path] = response
        except Exception as e:
            results[file_path] = f"Error processing file: {str(e)}"
    
    return results

@app.route('/process_resumes', methods=['POST'])
def api_process_resumes():
    data = request.json
    job_description = data.get('job_description')
    resume_file_paths = data.get('resume_file_paths')

    if not job_description or not resume_file_paths:
        return jsonify({"error": "Missing job description or resume file paths"}), 400

    results = process_resumes_for_job(resume_file_paths, job_description)
    return jsonify(results)

if __name__ == '__main__':
    app.run()