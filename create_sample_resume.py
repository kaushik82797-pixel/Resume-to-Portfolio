"""
create_sample_resume.py
-----------------------
Utility script to create sample resume files (PDF, DOCX, TXT) in the input/ directory
for immediate testing of the AI Resume to Portfolio Generator.
"""

import os

SAMPLE_RESUME_TEXT = """
Alex Morgan
Senior Full-Stack & AI Engineer
Email: alex.morgan@example.com | Phone: +1 (555) 234-5678 | Location: San Francisco, CA
GitHub: https://github.com/alexmorgan-dev | LinkedIn: https://linkedin.com/in/alexmorgandev | Portfolio: https://alexmorgan.dev

PROFESSIONAL SUMMARY
Innovative Senior Full-Stack Engineer with over 6 years of experience building scalable web applications, microservices, and AI-driven platforms. Specialized in Python, TypeScript, React, Cloud Architecture, and Generative AI SDKs. Proven track record of leading high-impact software projects and optimizing performance for millions of users.

TECHNICAL SKILLS
- Programming Languages: Python, TypeScript, JavaScript, SQL, HTML5, CSS3, Go
- Frameworks: React, Next.js, Django, FastAPI, Node.js, Express, TailwindCSS
- Libraries: PyTorch, NumPy, Pandas, Pydantic, Scikit-learn, Jinja2
- Databases: PostgreSQL, MongoDB, Redis, DynamoDB
- Cloud & DevOps: AWS (S3, EC2, Lambda), Docker, Kubernetes, GitHub Actions, Terraform
- Tools: Git, VS Code, Postman, Figma, JIRA
- Soft Skills: Team Leadership, System Architecture, Technical Writing, Problem Solving

WORK EXPERIENCE

Senior Software Engineer | TechNova Solutions | San Francisco, CA
Jan 2022 – Present
- Architected and deployed microservices backend using Python FastAPI and AWS Elastic Beanstalk, improving platform throughput by 40%.
- Led a team of 5 engineers in developing an AI-assisted customer analytics engine integrated with LLM APIs.
- Optimized PostgreSQL database query execution plans, reducing average response latency from 450ms to 85ms.
- Technologies: Python, FastAPI, PostgreSQL, AWS, Docker, React, TypeScript

Full-Stack Developer | CloudScale Innovations | Austin, TX
Jun 2019 – Dec 2021
- Built responsive single-page web applications using React, Redux, and Node.js for B2B enterprise clients.
- Automated CI/CD pipelines using GitHub Actions, cutting release deployment cycle times by 50%.
- Integrated Stripe payment gateways and OAuth2 authentication workflows.
- Technologies: React, Node.js, Express, MongoDB, Docker, AWS S3

EDUCATION

Bachelor of Science in Computer Science
University of California, Berkeley | Berkeley, CA
Aug 2015 – May 2019
- GPA: 3.8 / 4.0 | Dean's Honor List

FEATURED PROJECTS

AI Portfolio Generator
- Developed an automated CLI tool in Python that extracts resume details via Gemini API and renders responsive portfolios.
- Technologies: Python, Google GenAI SDK, Pydantic, Jinja2, HTML5/CSS3
- Link: https://github.com/alexmorgan-dev/resume-to-portfolio

Cloud Metrics Dashboard
- Created a real-time cluster monitoring tool visualizing system metrics using WebSocket and React.
- Technologies: TypeScript, React, Go, Redis, Docker
- Link: https://github.com/alexmorgan-dev/cloud-metrics

CERTIFICATIONS
- AWS Certified Solutions Architect – Associate (Amazon Web Services, 2023)
- Certified Kubernetes Application Developer (CKAD) (Linux Foundation, 2022)

ACHIEVEMENTS
- First Place Winner - Bay Area AI Hackathon 2023 out of 120 participating teams.
- Published technical article on "Scalable LLM Workflows" featured on Hacker News front page.

LANGUAGES
- English (Native)
- Spanish (Professional Working)
"""


def main():
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    # 1. Write TXT sample
    txt_path = "input/resume.txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(SAMPLE_RESUME_TEXT.strip())
    print(f"Created sample text resume: {txt_path}")

    # 2. Write PDF sample using pymupdf if available
    try:
        import pymupdf
        pdf_path = "input/resume.pdf"
        doc = pymupdf.open()
        page = doc.new_page()

        y = 50
        for line in SAMPLE_RESUME_TEXT.strip().split("\n"):
            if y > page.rect.height - 40:
                page = doc.new_page()
                y = 50
            if line.strip():
                page.insert_text((40, y), line.strip(), fontsize=10)
            y += 14

        doc.save(pdf_path)
        doc.close()
        print(f"Created sample PDF resume: {pdf_path}")
    except Exception as e:
        print(f"Could not create PDF sample automatically: {e}")


if __name__ == "__main__":
    main()
