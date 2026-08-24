"""
models.py
---------
Pydantic data models for validating and structuring resume data extracted by Gemini API.
Ensures strong typing and uniform data structure throughout the application.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    name: str = Field(default="", description="Full name of the candidate")
    title: str = Field(default="", description="Professional job title or headline")
    email: str = Field(default="", description="Primary email address")
    phone: str = Field(default="", description="Contact phone number")
    location: str = Field(default="", description="City, State, or Country of residence")
    profile_image: str = Field(default="", description="URL or placeholder for profile picture if present")


class Skills(BaseModel):
    programming_languages: List[str] = Field(default_factory=list, description="Programming languages (e.g. Python, JS, C++)")
    frameworks: List[str] = Field(default_factory=list, description="Frameworks (e.g. React, Django, Next.js)")
    libraries: List[str] = Field(default_factory=list, description="Libraries and SDKs (e.g. PyTorch, NumPy, Pandas)")
    databases: List[str] = Field(default_factory=list, description="Databases (e.g. PostgreSQL, MongoDB, Redis)")
    cloud: List[str] = Field(default_factory=list, description="Cloud platforms & DevOps (e.g. AWS, GCP, Docker, Kubernetes)")
    tools: List[str] = Field(default_factory=list, description="Tools & software (e.g. Git, VS Code, Figma, JIRA)")
    soft_skills: List[str] = Field(default_factory=list, description="Interpersonal or soft skills (e.g. Leadership, Communication)")
    other: List[str] = Field(default_factory=list, description="Other technical or domain skills")


class ExperienceItem(BaseModel):
    company: str = Field(default="", description="Company or organization name")
    role: str = Field(default="", description="Job title or role held")
    location: str = Field(default="", description="Location of work or 'Remote'")
    start_date: str = Field(default="", description="Start date (e.g. Jan 2022)")
    end_date: str = Field(default="", description="End date or 'Present'")
    description: List[str] = Field(default_factory=list, description="Key responsibilities and accomplishments")
    technologies: List[str] = Field(default_factory=list, description="Technologies used in this role")


class EducationItem(BaseModel):
    institution: str = Field(default="", description="University, college, or school name")
    degree: str = Field(default="", description="Degree or diploma earned (e.g. B.S., M.S.)")
    field: str = Field(default="", description="Field of study or major (e.g. Computer Science)")
    start_date: str = Field(default="", description="Start year/date")
    end_date: str = Field(default="", description="End year/date or graduation year")
    grade: str = Field(default="", description="GPA, marks, or honors if specified")


class ProjectItem(BaseModel):
    name: str = Field(default="", description="Project name")
    description: str = Field(default="", description="Overview of the project")
    technologies: List[str] = Field(default_factory=list, description="Technologies, tools, or languages used")
    url: str = Field(default="", description="URL to live project, repository, or demo")


class CertificationItem(BaseModel):
    name: str = Field(default="", description="Certification title")
    issuer: str = Field(default="", description="Issuing organization (e.g. AWS, Coursera, Google)")
    date: str = Field(default="", description="Date issued or valid until")
    url: str = Field(default="", description="Credential verification link")


class SocialLinks(BaseModel):
    github: str = Field(default="", description="GitHub profile URL")
    linkedin: str = Field(default="", description="LinkedIn profile URL")
    portfolio: str = Field(default="", description="Personal portfolio URL")
    other: List[str] = Field(default_factory=list, description="Other professional links (Medium, Twitter, LeetCode, etc.)")


class ResumeData(BaseModel):
    personal: PersonalInfo = Field(default_factory=PersonalInfo)
    summary: str = Field(default="", description="Professional summary or bio statement")
    skills: Skills = Field(default_factory=Skills)
    experience: List[ExperienceItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    certifications: List[CertificationItem] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list, description="Honors, awards, hackathon wins, or key accomplishments")
    languages: List[str] = Field(default_factory=list, description="Spoken/written languages (e.g. English, Spanish)")
    social_links: SocialLinks = Field(default_factory=SocialLinks)
