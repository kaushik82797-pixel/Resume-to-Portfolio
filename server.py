"""
server.py
---------
FastAPI web server for the AI Resume to Portfolio Generator SaaS application.
Exposes REST API endpoints for resume upload, Gemini parsing, live rendering,
and serving the single-page application.
"""

import os
import shutil
from typing import Dict, Any
from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from models import ResumeData
from resume_reader import extract_resume_text, ResumeReaderError
from gemini_parser import parse_resume_with_gemini, GeminiParserError
from portfolio_generator import generate_portfolio, PortfolioGeneratorError

load_dotenv()

app = FastAPI(
    title="PortfolioAI - AI Resume to Portfolio Generator",
    description="SaaS Web Application for transforming resumes into professional portfolios using Gemini AI.",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
WEB_DIR = os.path.join(BASE_DIR, "web")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(WEB_DIR, exist_ok=True)

# Mount static directories
app.mount("/css", StaticFiles(directory=os.path.join(WEB_DIR, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(WEB_DIR, "js")), name="js")
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_landing_page():
    """Serves the main single-page SaaS application."""
    index_path = os.path.join(WEB_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="SaaS frontend file 'web/index.html' not found.")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()


@app.post("/api/upload")
async def upload_and_parse_resume(file: UploadFile = File(...)):
    """
    Endpoint for uploading resume file (PDF, DOCX, TXT),
    extracting text, and parsing with Gemini API into structured JSON.
    """
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    if ext not in [".pdf", ".docx", ".txt", ".md"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file extension '{ext}'. Please upload a PDF, DOCX, or TXT document."
        )

    # Save uploaded file safely
    saved_path = os.path.join(INPUT_DIR, filename)
    try:
        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file on server: {str(e)}")

    # Step 1: Extract text
    try:
        raw_text = extract_resume_text(saved_path)
    except ResumeReaderError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Step 2: Parse text with Gemini API
    try:
        resume_data = parse_resume_with_gemini(raw_text)
    except GeminiParserError as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI Extraction Failed: {str(e)}"
        )

    # Step 3: Render initial portfolio HTML
    try:
        portfolio_path = generate_portfolio(resume_data)
    except PortfolioGeneratorError as e:
        raise HTTPException(status_code=500, detail=f"Portfolio Generation Failed: {str(e)}")

    return {
        "status": "success",
        "message": "Resume analyzed and portfolio generated successfully.",
        "data": resume_data.model_dump(),
        "preview_url": "/api/preview-portfolio"
    }


@app.post("/api/render-portfolio")
async def render_portfolio_data(data: Dict[str, Any] = Body(...)):
    """
    Endpoint for re-rendering portfolio HTML when user edits fields in live editor.
    """
    try:
        resume_data = ResumeData.model_validate(data)
        portfolio_path = generate_portfolio(resume_data)
        return {
            "status": "success",
            "message": "Portfolio updated successfully.",
            "preview_url": "/api/preview-portfolio"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to update portfolio: {str(e)}")


@app.get("/api/preview-portfolio", response_class=HTMLResponse)
async def preview_portfolio():
    """Serves the generated portfolio HTML for live preview inside an iframe."""
    portfolio_file = os.path.join(OUTPUT_DIR, "portfolio.html")
    if not os.path.exists(portfolio_file):
        return HTMLResponse("<h3>No portfolio generated yet. Please upload a resume first.</h3>")
    with open(portfolio_file, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/api/download-portfolio")
async def download_portfolio():
    """Returns generated portfolio.html as a downloadable file attachment."""
    portfolio_file = os.path.join(OUTPUT_DIR, "portfolio.html")
    if not os.path.exists(portfolio_file):
        raise HTTPException(status_code=404, detail="Generated portfolio file not found.")
    return FileResponse(
        portfolio_file,
        media_type="text/html",
        filename="portfolio.html"
    )


if __name__ == "__main__":
    import sys
    import uvicorn
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    port = int(os.getenv("PORT", 8000))
    print(f"🚀 Launching PortfolioAI SaaS Server on http://127.0.0.1:{port}")
    uvicorn.run("server:app", host="127.0.0.1", port=port, reload=True)
