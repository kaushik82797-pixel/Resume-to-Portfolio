"""
test_pipeline.py
----------------
Offline verification test for resume extraction and HTML portfolio generation.
"""

from resume_reader import extract_resume_text
from models import (
    ResumeData, PersonalInfo, Skills, ExperienceItem,
    EducationItem, ProjectItem, CertificationItem, SocialLinks
)
from portfolio_generator import generate_portfolio


def test_extraction():
    print("Testing text extraction from input/resume.pdf...")
    pdf_text = extract_resume_text("input/resume.pdf")
    print(f"Extracted {len(pdf_text)} characters from PDF.")
    assert "Alex Morgan" in pdf_text, "Failed to extract name from PDF"

    print("Testing text extraction from input/resume.txt...")
    txt_text = extract_resume_text("input/resume.txt")
    print(f"Extracted {len(txt_text)} characters from TXT.")
    assert "Alex Morgan" in txt_text, "Failed to extract name from TXT"


def test_generator():
    print("Testing portfolio HTML generation with mock ResumeData...")
    mock_data = ResumeData(
        personal=PersonalInfo(
            name="Alex Morgan",
            title="Senior Full-Stack & AI Engineer",
            email="alex.morgan@example.com",
            phone="+1 (555) 234-5678",
            location="San Francisco, CA"
        ),
        summary="Innovative Senior Full-Stack Engineer with over 6 years of experience building scalable web applications, microservices, and AI-driven platforms.",
        skills=Skills(
            programming_languages=["Python", "TypeScript", "JavaScript", "SQL", "Go"],
            frameworks=["React", "Next.js", "Django", "FastAPI"],
            libraries=["PyTorch", "NumPy", "Pandas", "Pydantic"],
            databases=["PostgreSQL", "MongoDB", "Redis"],
            cloud=["AWS", "Docker", "Kubernetes"],
            tools=["Git", "VS Code", "Postman"],
            soft_skills=["Leadership", "System Architecture", "Communication"]
        ),
        experience=[
            ExperienceItem(
                company="TechNova Solutions",
                role="Senior Software Engineer",
                location="San Francisco, CA",
                start_date="Jan 2022",
                end_date="Present",
                description=[
                    "Architected microservices backend using Python FastAPI and AWS Elastic Beanstalk.",
                    "Led a team of 5 engineers developing AI-assisted analytics engine.",
                    "Optimized PostgreSQL database queries, reducing response latency by 80%."
                ],
                technologies=["Python", "FastAPI", "PostgreSQL", "AWS", "Docker"]
            )
        ],
        education=[
            EducationItem(
                institution="University of California, Berkeley",
                degree="B.S.",
                field="Computer Science",
                start_date="2015",
                end_date="2019",
                grade="3.8 GPA"
            )
        ],
        projects=[
            ProjectItem(
                name="AI Portfolio Generator",
                description="CLI tool in Python extracting resume details via Gemini API and rendering responsive portfolios.",
                technologies=["Python", "Google GenAI SDK", "Pydantic", "Jinja2"],
                url="https://github.com/alexmorgan-dev/resume-to-portfolio"
            )
        ],
        certifications=[
            CertificationItem(
                name="AWS Certified Solutions Architect",
                issuer="Amazon Web Services",
                date="2023",
                url="https://aws.amazon.com"
            )
        ],
        achievements=["First Place Winner - Bay Area AI Hackathon 2023"],
        languages=["English", "Spanish"],
        social_links=SocialLinks(
            github="https://github.com/alexmorgan-dev",
            linkedin="https://linkedin.com/in/alexmorgandev",
            portfolio="https://alexmorgan.dev"
        )
    )

    out_file = generate_portfolio(mock_data)
    print(f"Portfolio generated at: {out_file}")
    with open(out_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    assert "Alex Morgan" in html_content
    assert "Senior Full-Stack &amp; AI Engineer" in html_content or "Senior Full-Stack & AI Engineer" in html_content
    assert "TechNova Solutions" in html_content
    assert "Technical Expertise" in html_content
    print("[OK] Offline verification test passed successfully!")


if __name__ == "__main__":
    test_extraction()
    test_generator()
