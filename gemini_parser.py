"""
gemini_parser.py
----------------
Sends extracted resume text to the Gemini API using the official Google GenAI Python SDK.
Utilizes structured output capabilities with Pydantic validation to guarantee clean,
factually accurate, zero-hallucination JSON extraction.
"""

import os
from typing import Optional
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

from models import ResumeData


class GeminiParserError(Exception):
    """Custom exception for errors during Gemini API parsing."""
    pass


SYSTEM_PROMPT = """You are an expert resume parser and professional career-profile extraction AI.

Analyze the supplied resume carefully.

Extract ONLY information explicitly present in the resume.

Never invent:
- employment
- skills
- dates
- education
- projects
- certifications
- achievements
- URLs
- contact information

Normalize formatting where appropriate while preserving factual accuracy.
Categorize skills intelligently into:
- programming_languages
- frameworks
- libraries
- databases
- cloud
- tools
- soft_skills
- other

Separate internships from full-time experience when possible.
Identify projects and their technologies.
Extract professional URLs accurately (GitHub, LinkedIn, portfolio, etc.).

If information is unavailable or not mentioned in the resume, return an empty string or empty list for that field. Do NOT guess or hallucinate.
Return the information strictly according to the supplied JSON schema.
"""


def parse_resume_with_gemini(resume_text: str, api_key: Optional[str] = None) -> ResumeData:
    """
    Sends raw resume text to Gemini API and parses it into a validated ResumeData Pydantic object.

    :param resume_text: Plain text extracted from resume file
    :param api_key: Optional explicit API key, defaults to GEMINI_API_KEY from .env
    :return: ResumeData Pydantic instance
    """
    if genai is None:
        raise GeminiParserError(
            "The 'google-genai' package is not installed. Please install it with: pip install google-genai"
        )

    # Ensure environment variables are loaded
    load_dotenv()

    final_api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not final_api_key or final_api_key.strip() == "" or "your_api_key_here" in final_api_key:
        raise GeminiParserError(
            "GEMINI_API_KEY is missing or unconfigured.\n"
            "Please create a '.env' file in the project root with your valid API key:\n"
            "  GEMINI_API_KEY=your_actual_gemini_api_key\n"
            "You can obtain a key from https://aistudio.google.com/"
        )

    if not resume_text or not resume_text.strip():
        raise GeminiParserError("Provided resume text is empty. Cannot process with Gemini.")

    try:
        # Initialize Google GenAI client
        client = genai.Client(api_key=final_api_key)

        prompt = f"Resume Content:\n\n{resume_text}"

        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=ResumeData,
            temperature=0.1,  # Low temperature for factual extraction
        )

        # Call Gemini API
        # Using gemini-3.6-flash as primary structured output model
        model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config,
            )
        except Exception as api_err:
            if "404" in str(api_err) or "NOT_FOUND" in str(api_err):
                # Fallback to gemini-flash-latest
                response = client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=prompt,
                    config=config,
                )
            else:
                raise api_err

        if not response or not response.text:
            raise GeminiParserError("Received an empty response from Gemini API.")

        raw_json = response.text.strip()

        # Validate with Pydantic model
        resume_data = ResumeData.model_validate_json(raw_json)
        return resume_data

    except Exception as e:
        if isinstance(e, GeminiParserError):
            raise e
        # Catch GenAI client errors or JSON validation issues
        raise GeminiParserError(f"Error while parsing resume with Gemini API: {str(e)}")
