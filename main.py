from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analyzer import analyze_resume

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeRequest(BaseModel):
    resume: str
    job_description: str

@app.get("/")
def root():
    return {"message": "Resume Analyzer API is running!"}

@app.post("/analyze")
def analyze(request: ResumeRequest):
    result = analyze_resume(request.resume, request.job_description)
    return result
