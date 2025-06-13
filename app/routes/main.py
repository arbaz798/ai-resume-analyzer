"""
Main routes module.

This module contains the primary routes for the Resume Analyzer application.
"""

import os
import uuid
from datetime import datetime
from flask import (
    Blueprint, flash, redirect, render_template, 
    request, url_for, current_app, jsonify, session, send_file
)
from werkzeug.utils import secure_filename

from app.utils.resume_extractor import extract_text_from_resume
from app.utils.resume_analyzer import analyze_resume
from app.utils.feedback_generator import generate_feedback_report
from app.utils.resume_improver import improve_resume

# Create a Blueprint for the main routes
bp = Blueprint('main', __name__)

def allowed_file(filename):
    """
    Check if the uploaded file has an allowed extension.
    
    Args:
        filename (str): The name of the file to check.
        
    Returns:
        bool: True if file extension is allowed, False otherwise.
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@bp.route('/upload', methods=['POST'])
def upload_resume():
    """
    Handle resume file upload and start the analysis process.
    
    Returns:
        Response: Redirects to the results page or shows an error.
    """
    # Check if a file was uploaded
    if 'resume' not in request.files:
        flash('No file part')
        return redirect(url_for('main.index'))
        
    file = request.files['resume']
    
    # Check if file was selected
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('main.index'))
    
    # Check if file is allowed
    if file and allowed_file(file.filename):
        # Create a unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save the file
        file.save(file_path)
        
        try:
            # Extract text from the resume
            resume_text = extract_text_from_resume(file_path)
            
            # Analyze the resume text
            analysis_results = analyze_resume(resume_text)
            
            # Generate feedback report
            feedback_report = generate_feedback_report(resume_text, analysis_results)
            
            # Store results in session for the results page
            session['feedback_report'] = feedback_report
            session['analysis_results'] = analysis_results
            session['filename'] = file.filename
            session['original_file_path'] = file_path
            
            # Redirect to the results page
            return redirect(url_for('main.results'))
            
        except Exception as e:
            flash(f'Error analyzing resume: {str(e)}')
            # Clean up the uploaded file if there was an error
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(url_for('main.index'))
    else:
        flash('File type not allowed. Please upload a PDF, TXT, or DOCX file.')
        return redirect(url_for('main.index'))

@bp.route('/results')
def results():
    """
    Render the results page showing resume analysis feedback.
    
    Returns:
        Response: Results page with analysis data or redirects to homepage if no data.
    """
    # Check if there is data in the session
    if 'feedback_report' not in session or 'analysis_results' not in session:
        flash('No resume analysis data found. Please upload a resume first.')
        return redirect(url_for('main.index'))
    
    # Get the data from the session
    feedback_report = session.get('feedback_report', {})
    analysis_results = session.get('analysis_results', {})
    filename = session.get('filename', 'Unknown File')
    
    # Render the results template with the data
    return render_template(
        'results.html',
        feedback=feedback_report,
        analysis=analysis_results,
        filename=filename,
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

@bp.route('/about')
def about():
    """Render the about page with information about the app."""
    return render_template('about.html')

@bp.route('/improve_resume')
def improve_resume_route():
    """
    Improve the resume based on analysis results and provide it for download.
    
    Returns:
        Response: The improved resume file for download.
    """
    # Check if there is data in the session
    if 'original_file_path' not in session or 'analysis_results' not in session:
        flash('No resume data found. Please upload a resume first.')
        return redirect(url_for('main.index'))
    
    # Get the data from the session
    original_file_path = session.get('original_file_path')
    analysis_results = session.get('analysis_results', {})
    
    # Create improved resume
    success, result = improve_resume(
        original_file_path, 
        current_app.config['UPLOAD_FOLDER'], 
        analysis_results
    )
    
    if success and result:
        # Get the filename for download
        filename = os.path.basename(result)
        
        # Return the file for download
        return send_file(
            result,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
    else:
        # Show specific error message
        error_msg = result if isinstance(result, str) else 'Failed to improve the resume. Please try again.'
        flash(error_msg)
        return redirect(url_for('main.results'))

@bp.route('/clear')
def clear_session():
    """
    Clear the session data and redirect to the homepage.
    
    Returns:
        Response: Redirect to the homepage.
    """
    # Clear the session data
    session.clear()
    flash('Session data cleared.')
    return redirect(url_for('main.index'))