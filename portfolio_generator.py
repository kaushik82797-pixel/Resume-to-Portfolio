"""
portfolio_generator.py
----------------------
Renders validated ResumeData Pydantic objects into a responsive, modern HTML portfolio
using Jinja2 templating and embedded CSS styling. Automatically hides empty sections.
"""

import os
from typing import Optional
from jinja2 import Environment, FileSystemLoader
from models import ResumeData


class PortfolioGeneratorError(Exception):
    """Custom exception raised during portfolio generation."""
    pass


def check_has_skills(data: ResumeData) -> bool:
    """Returns True if any skill category in the ResumeData has at least one skill."""
    skills = data.skills
    return bool(
        skills.programming_languages or
        skills.frameworks or
        skills.libraries or
        skills.databases or
        skills.cloud or
        skills.tools or
        skills.soft_skills or
        skills.other
    )


def generate_portfolio(
    resume_data: ResumeData,
    template_dir: str = "templates",
    template_file: str = "portfolio_template.html",
    css_file_path: str = "static/style.css",
    output_path: str = "output/portfolio.html"
) -> str:
    """
    Renders the portfolio HTML using Jinja2 template and writes to output_path.

    :param resume_data: Validated ResumeData Pydantic object
    :param template_dir: Path to directory containing Jinja2 templates
    :param template_file: Name of template file
    :param css_file_path: Path to stylesheet to embed in HTML
    :param output_path: Destination HTML file path
    :return: Absolute path to generated portfolio HTML
    """
    try:
        # Resolve absolute paths
        base_dir = os.path.dirname(os.path.abspath(__file__))
        abs_template_dir = os.path.join(base_dir, template_dir)
        abs_css_path = os.path.join(base_dir, css_file_path)
        abs_output_path = os.path.join(base_dir, output_path)

        if not os.path.exists(abs_template_dir):
            raise PortfolioGeneratorError(f"Templates directory not found: '{abs_template_dir}'")

        full_template_path = os.path.join(abs_template_dir, template_file)
        if not os.path.exists(full_template_path):
            raise PortfolioGeneratorError(f"Template file not found: '{full_template_path}'")

        # Read CSS content for single-file self-contained HTML rendering
        css_content = ""
        if os.path.exists(abs_css_path):
            with open(abs_css_path, "r", encoding="utf-8") as f:
                css_content = f.read()
        else:
            print(f"Warning: Stylesheet not found at '{abs_css_path}'. Portfolio will render with fallback inline styles.")

        # Set up Jinja2 environment
        env = Environment(
            loader=FileSystemLoader(abs_template_dir),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True
        )

        template = env.get_template(template_file)

        # Check if skills section has content
        has_skills = check_has_skills(resume_data)

        # Render HTML
        rendered_html = template.render(
            data=resume_data,
            css_content=css_content,
            has_skills=has_skills
        )

        # Ensure output directory exists
        out_dir = os.path.dirname(abs_output_path)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        # Write output file
        with open(abs_output_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)

        return abs_output_path

    except Exception as e:
        if isinstance(e, PortfolioGeneratorError):
            raise e
        raise PortfolioGeneratorError(f"Failed to generate portfolio HTML: {str(e)}")
