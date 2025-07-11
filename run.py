"""
Run script for the Resume Analyzer application.

This is the main entry point for running the Flask application.
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)