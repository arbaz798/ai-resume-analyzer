"""
Utilities package initialization.

This package contains utility modules for text extraction, NLP analysis,
and other helper functions for the Resume Analyzer application.
"""

# Import key functions for easier access
from .resume_extractor import extract_text_from_resume
from .resume_analyzer import analyze_resume
from .feedback_generator import generate_feedback_report
from .resume_improver import improve_resume

__all__ = [
    'extract_text_from_resume',
    'analyze_resume',
    'generate_feedback_report',
    'improve_resume'
]