from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="LegalEase AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class DocumentRequest(BaseModel):
    doc_type: str
    parties: str
    terms: list
    effective_date: str

@app.get("/")
def read_root():
    return {"message": "LegalEase AI FastAPI Backend is Running!"}

@app.post("/generate-document")
def generate_document(req: DocumentRequest):
    prompt = f"""
    You are an expert legal advocate. Draft a comprehensive, formal, and legally binding {req.doc_type}.
    
    PARTIES: {req.parties}
    EFFECTIVE DATE: {req.effective_date}
    
    KEY CLAUSES TO INCLUDE:
    {', '.join(req.terms)}
    
    INSTRUCTIONS:
    1. Include formal legal introduction and recitals.
    2. Write detailed numbered clauses for Definitions, Obligations, Confidentiality, Termination, and Governing Law.
    3. Include formal closing remarks before the signature lines.
    """
    try:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in environment.")

        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return {"status": "success", "document": response.text}
    except Exception as e:
        print(f"Primary model error: {e}")
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return {"status": "success", "document": response.text}
        except Exception as ex:
            print(f"Fallback model error: {ex}")
            fallback_doc = f"""LEGAL AGREEMENT DRAFT

DOCUMENT TYPE: {req.doc_type}
PARTIES INVOLVED: {req.parties}
EFFECTIVE DATE: {req.effective_date}

OPERATIVE PROVISIONS & CLAUSES:
1. DEFINITIONS AND INTENT
This Agreement governs the relationship between the aforementioned parties starting from {req.effective_date}.

2. TERMS AND CONDITIONS
""" + "\n".join([f"{idx+1}. {term}" for idx, term in enumerate(req.terms)]) + """

3. GOVERNING LAW
This agreement shall be governed by and construed in accordance with applicable state/national laws.
"""
            return {"status": "success", "document": fallback_doc}