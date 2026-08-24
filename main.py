"""
main.py
-------
AI Resume to Portfolio Generator CLI Application.
Entry point that coordinates resume extraction, Gemini AI structured parsing,
Pydantic model validation, and HTML portfolio rendering.
"""

import sys
import os
from dotenv import load_dotenv

from resume_reader import extract_resume_text, ResumeReaderError
from gemini_parser import parse_resume_with_gemini, GeminiParserError
from portfolio_generator import generate_portfolio, PortfolioGeneratorError


def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 60)
    print(" 🚀 AI RESUME TO PORTFOLIO GENERATOR")
    print("=" * 60)

    # 1. Load environment variables
    load_dotenv()

    # 2. Get resume file path from command line arg or interactive prompt
    if len(sys.argv) > 1:
        resume_path = sys.argv[1].strip()
    else:
        print("\nPlease specify your resume file (PDF, DOCX, TXT).")
        try:
            resume_path = input("Enter the path of your resume [default: input/resume.pdf]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            sys.exit(0)

    if not resume_path:
        resume_path = "input/resume.pdf"

    print(f"\n[1/3] Reading resume from: {resume_path}...")
    try:
        raw_text = extract_resume_text(resume_path)
        print("  ✓ Resume content extracted successfully.")
    except ResumeReaderError as e:
        print(f"\n❌ Error Reading Resume:\n  {str(e)}")
        sys.exit(1)

    print("\n[2/3] Analyzing resume content with Gemini AI...")
    try:
        resume_data = parse_resume_with_gemini(raw_text)
        print("  ✓ Resume successfully analyzed.")
    except GeminiParserError as e:
        print(f"\n❌ Error Analyzing Resume with Gemini API:\n  {str(e)}")
        sys.exit(1)

    print("\n[3/3] Generating responsive HTML portfolio...")
    try:
        output_file = generate_portfolio(resume_data)
        print("  ✓ Portfolio generated successfully.")
    except PortfolioGeneratorError as e:
        print(f"\n❌ Error Generating Portfolio HTML:\n  {str(e)}")
        sys.exit(1)

    # Relative path for user output display
    rel_output = os.path.relpath(output_file, os.getcwd()) if os.path.exists(output_file) else output_file

    print("\n" + "=" * 60)
    print(" SUCCESS! Your professional portfolio is ready.")
    print("=" * 60)
    print(f"\nYour portfolio is available at: {rel_output}")
    print("Open this file in your browser to view your brand new portfolio!\n")


if __name__ == "__main__":
    main()
