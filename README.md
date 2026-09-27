# LegalEase AI - Smart Legal Document Generator

LegalEase AI is an automated platform designed to simplify legal document generation, agreement formatting, and contract creation. Built with a FastAPI backend and a Streamlit frontend, it generates clean, formal, downloadable legal PDFs.

## Features
- AI-Powered Draft Generation: Generates legal agreements, contracts, and NDAs dynamically.
- Custom Visual Branding: Includes a custom Metallic Rose Gold seal with Scales of Justice logo integration.
- Automated Formatting: Dynamic page-break logic, structured legal clauses, and organized signature layouts.
- PDF Export: One-click PDF document generation using ReportLab.

## Tech Stack
- Backend: Python, FastAPI
- Frontend: Streamlit
- PDF Generation: ReportLab, Pillow (PIL)
- AI Integration: Google Gemini API

## File Structure
- app.py: Streamlit frontend interface
- main.py: FastAPI backend services
- utils/: Document formatters
- assets/: Custom logo and branding visual assets
