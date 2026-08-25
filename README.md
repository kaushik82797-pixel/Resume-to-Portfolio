# AI Resume to Portfolio Generator 🚀

An intelligent, Python-based application that parses resume files (PDF, DOCX, TXT) using **Google GenAI SDK (Gemini API)** with strict structured JSON output and Pydantic validation, automatically transforming unstructured resumes into beautiful, responsive, modern developer web portfolios (`portfolio.html`).

---

## 📌 Project Overview

Traditional resume builders require manual copy-pasting into complex templates. **AI Resume to Portfolio Generator** automates this entire process:
1. It extracts raw text from your resume file.
2. It sends the unstructured text to Gemini AI using a zero-hallucination instruction prompt.
3. Gemini returns strict structured JSON validated by Pydantic models.
4. Python populates a clean, modern HTML5/CSS3 portfolio template using Jinja2.
5. Empty resume sections and missing links are dynamically omitted.
6. A single, standalone `portfolio.html` file is generated, complete with a dark/light mode toggle.

---

## ✨ Key Features

- **Multi-Format Extraction**: Supports `.pdf` (via PyMuPDF), `.docx` (via python-docx), and `.txt` files automatically.
- **Zero Hallucination AI Parsing**: Uses strict Gemini system instructions and Pydantic structured output (`response_schema`).
- **Dynamic Section Hiding**: Intelligently hides empty skill categories, missing social buttons, or empty experience timelines.
- **Single-File Output**: Generates a self-contained, highly portable `portfolio.html` with embedded CSS and JS.
- **Modern Responsive Design**: Features sleek typography, card glassmorphism, interactive badges, timeline views, and theme toggling (Dark/Light).
- **Secure Key Management**: Strictly isolation of API keys inside `.env` (never exposed in generated HTML or code).
- **Beginner-Friendly CLI**: Clean error messaging and progress tracking.

---

## 🛠️ Technology Stack

- **Core**: Python 3.9+
- **AI / LLM SDK**: `google-genai` (Google GenAI Python SDK)
- **Model**: `gemini-2.5-flash`
- **Data Validation**: Pydantic v2
- **Document Extractors**: PyMuPDF (`fitz`), `python-docx`
- **Template Engine**: Jinja2
- **Frontend Stack**: HTML5, Vanilla CSS3 (with CSS Variables), Lightweight Vanilla JavaScript (Theme Toggle)

---

## 📁 Project Structure

```
resume-to-portfolio/
│
├── main.py                   # Main CLI entry point & user interaction workflow
├── gemini_parser.py          # Gemini API integration with Pydantic structured output
├── resume_reader.py          # Document reader for PDF, DOCX, and TXT files
├── portfolio_generator.py    # Jinja2 template rendering engine
├── models.py                 # Pydantic schemas enforcing strict JSON structure
├── create_sample_resume.py   # Helper script to generate sample resume files
├── requirements.txt          # Minimal required Python dependencies
├── .env.example              # Template for Gemini API credentials
├── .gitignore                # Excludes secrets (.env) and generated artifacts
├── README.md                 # Project documentation and viva guide
│
├── templates/
│   └── portfolio_template.html # Semantic HTML5 portfolio template
│
├── static/
│   └── style.css             # Polished CSS3 stylesheet with light/dark variables
│
├── input/
│   └── resume.pdf            # Input directory for user resumes
│
└── output/
    └── portfolio.html        # Output directory for generated portfolios
```

### Explanation of Files

- `models.py`: Defines Pydantic data schemas (`ResumeData`, `PersonalInfo`, `Skills`, `ExperienceItem`, etc.) ensuring strict field typing.
- `resume_reader.py`: Handles multi-format file ingestion (.pdf, .docx, .txt) and returns raw text while catching corrupt/unsupported files.
- `gemini_parser.py`: Connects to `google-genai` API, sends system instructions, applies `response_schema`, and returns validated Pydantic objects.
- `portfolio_generator.py`: Loads Jinja2 template (`portfolio_template.html`), embeds `style.css`, evaluates dynamic visibility, and writes `portfolio.html`.
- `main.py`: Interactive CLI tool orchestrating the step-by-step pipeline.
- `templates/portfolio_template.html`: Jinja2 template with GFM-inspired dark/light theme structure and dynamic section rendering.
- `static/style.css`: Design system CSS containing custom variables, fluid typography, card elevation, and responsive breakpoints.

---

## 🔑 How to Get a Gemini API Key

1. Go to **[Google AI Studio](https://aistudio.google.com/)**.
2. Sign in with your Google account.
3. Click on **"Get API key"** -> **"Create API key"**.
4. Copy your newly generated API key.

---

## ⚙️ Installation & Setup

### 1. Clone or Open the Project Directory

```bash
cd resume-to-portfolio
```

### 2. Configure Environment Variables (`.env`)

Create a `.env` file in the project root directory (you can copy `.env.example`):

```bash
cp .env.example .env
```

Open `.env` in a text editor and insert your Gemini API Key:

```env
GEMINI_API_KEY=AIzaSyYourActualGeminiApiKeyHere
```

### 3. Install Python Dependencies

It is recommended to use a virtual environment:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

---

## 🚀 How to Run the Project

### Option A: Generate Sample Resumes First (Quick Test)

Run the included helper script to create sample resumes (`input/resume.pdf` and `input/resume.txt`):

```bash
python create_sample_resume.py
```

### Option B: Use Your Own Resume

Place your PDF, DOCX, or TXT resume into the `input/` folder (e.g. `input/my_resume.pdf`).

### Execute the Generator

Run the main application:

```bash
python main.py
```

When prompted:
```text
Enter the path of your resume [default: input/resume.pdf]:
```
Press `Enter` to use the default sample, or type your custom path (e.g. `input/my_resume.pdf`).

---

## 📊 Complete Data Flow Architecture

For college project demonstrations and viva examinations, the data flow follows this linear architecture:

```
[Resume File (.pdf/.docx/.txt)]
            │
            ▼
┌─────────────────────────┐
│   resume_reader.py      │ ── (Extracts raw text via PyMuPDF / docx)
└─────────────────────────┘
            │
            ▼
┌─────────────────────────┐
│   gemini_parser.py      │ ── (Sends text to Gemini API with System Prompt)
└─────────────────────────┘
            │
            ▼
┌─────────────────────────┐
│  Structured JSON (API)  │ ── (Returned by Gemini using response_schema)
└─────────────────────────┘
            │
            ▼
┌─────────────────────────┐
│       models.py         │ ── (Pydantic validates fields into ResumeData)
└─────────────────────────┘
            │
            ▼
┌─────────────────────────┐
│ portfolio_generator.py │ ── (Jinja2 renders template & embeds style.css)
└─────────────────────────┘
            │
            ▼
[output/portfolio.html]   ── (Standalone, interactive browser portfolio)
```

---

## 🎯 Example Terminal Output

```text
============================================================
 🚀 AI RESUME TO PORTFOLIO GENERATOR
============================================================

Please specify your resume file (PDF, DOCX, TXT).
Enter the path of your resume [default: input/resume.pdf]: input/resume.pdf

[1/3] Reading resume from: input/resume.pdf...
  ✓ Resume content extracted successfully.

[2/3] Analyzing resume content with Gemini AI...
  ✓ Resume successfully analyzed.

[3/3] Generating responsive HTML portfolio...
  ✓ Portfolio generated successfully.

============================================================
 SUCCESS! Your professional portfolio is ready.
============================================================

Your portfolio is available at: output/portfolio.html
Open this file in your browser to view your brand new portfolio!
```

---

## ❓ Common Errors & Solutions

| Error | Cause | Solution |
| :--- | :--- | :--- |
| `GEMINI_API_KEY is missing` | `.env` file not created or key missing | Create `.env` file and set `GEMINI_API_KEY=your_key` |
| `PyMuPDF library is missing` | Missing PDF extraction dependency | Run `pip install pymupdf` |
| `File not found` | Incorrect file path entered | Ensure resume file is located in `input/` or provide full path |
| `Older .doc format not supported` | Document in legacy binary .doc format | Save document as `.docx` or export as `.pdf` |
| `403 / Invalid API Key` | Incorrect key copied from AI Studio | Verify API key active at [AI Studio](https://aistudio.google.com/) |

---


