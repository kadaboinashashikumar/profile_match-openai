# Resume Matcher API

The Resume Matcher API is a Python-based application that processes resumes and compares them against job descriptions using OpenAI's GPT model. It provides an automated way to evaluate candidate profiles for job openings.

## Features

- Extract text from PDF, DOCX, and TXT files
- Generate matching scores and analysis using OpenAI's GPT model
- Process multiple resumes for a given job description
- RESTful API endpoint for easy integration

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- OpenAI API key

## Installation

1. Clone the repository:
  
2. Install the required dependencies:
   ```
   pip install flask openai PyPDF2 python-docx
   ```

3. Set up your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

## Usage

1. Start the Flask server:
   ```
   python resume_matcher_api.py
   ```

2. The API will be available at `http://localhost:5000/process_resumes`

3. Send a POST request to the API endpoint with the following JSON payload:
   ```json
   {
     "job_description": "We need a candidate with Python, Django, and data analysis skills, with at least 0-1 years of experience.",
     "resume_file_paths": [
       "/path/to/resume1.pdf",
       "/path/to/resume2.docx",
       "/path/to/resume3.txt"
     ]
   }
   ```

4. The API will return a JSON response with the analysis for each resume.

## API Reference

### POST /process_resumes

Process multiple resumes against a job description.

**Request Body:**

| Parameter | Type | Description |
|-----------|------|-------------|
| job_description | string | The job description text |
| resume_file_paths | array | Array of file paths to the resumes |

**Response:**

A JSON object where keys are the file paths and values are the analysis results.

## Contributing

Contributions to the Resume Matcher API are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

