"""
Resume Analyzer App Initialization Module.

This module initializes the Flask application and configures it with all 
necessary components for the Resume Analyzer web application.
"""

import os
from flask import Flask
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

def create_app(test_config=None):
    """
    Create and configure the Flask application.
    
    Args:
        test_config (dict, optional): Test configuration to override default configs.
    
    Returns:
        Flask: Configured Flask application instance.
    """
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        UPLOAD_FOLDER=os.path.join(app.root_path, 'uploads'),
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,  # 5MB max file size
        ALLOWED_EXTENSIONS={'pdf', 'txt', 'docx'}
    )
    
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register blueprints
    from app.routes import main
    app.register_blueprint(main.bp)
    
    # Initialize NLP components
    from app.utils import nlp_utils
    nlp_utils.initialize()
    
    return app