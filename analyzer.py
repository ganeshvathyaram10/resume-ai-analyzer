import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_resume(resume_text: str, job_description: str) -> dict:
    prompt = f"""
You are an expert resume coach and recruiter.

Analyze the resume against the job description and return ONLY a JSON object with this exact structure:
{{
  "match_score": <number 0 to 100>,
  "strengths": [<3 things the resume does well>],
  "missing_skills": [<skills in job description missing from resume>],
  "improved_bullets": [<3 improved resume bullet points tailored to this job>],
  "summary": "<one sentence overall assessment>"
}}

Return ONLY the JSON. No explanation, no markdown, no extra text.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    text = response.choices[0].message.content.strip()

    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]

    return json.loads(text.strip())


if __name__ == "__main__":
    sample_resume = """
    John Doe | john@email.com
    Skills: Python, SQL, Excel, data analysis
    Experience:
    - Analyzed sales data using Excel and created monthly reports
    - Built Python scripts to automate data cleaning tasks
    - Collaborated with marketing team on campaign performance tracking
    """

    sample_job = """
    Data Analyst – Acme Corp
    Requirements:
    - 2+ years experience with Python and SQL
    - Experience with data visualization tools (Tableau, Power BI)
    - Strong communication and presentation skills
    - Familiarity with machine learning concepts
    - Cloud platforms (AWS, GCP) experience preferred
    """

    print("Analyzing resume... ⏳\n")
    result = analyze_resume(sample_resume, sample_job)
    print(json.dumps(result, indent=2))
