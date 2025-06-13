# AI-Powered Resume Analyzer

A web application that analyzes resumes to provide personalized feedback and suggestions for improvement using artificial intelligence and natural language processing techniques.

## Features

- **Grammar & Spelling Check:** Identifies grammar errors and typos that could hurt your credibility
- **Structure Analysis:** Evaluates the organization and formatting of your resume
- **Language Strength Evaluation:** Identifies weak phrases and suggests stronger alternatives
- **Keyword Optimization:** Checks for industry-relevant keywords that ATS systems look for
- **Comprehensive Scoring:** Provides an overall score and component scores to track improvements
- **Actionable Suggestions:** Offers specific recommendations to enhance your resume

## Technologies Used

- **Backend:** Python, Flask
- **NLP Libraries:** NLTK, SpaCy, LanguageTool
- **PDF/Text Processing:** PyMuPDF, pdfminer.six
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Deployment:** Ready for Heroku, AWS, or Render

## Detailed Local Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step 1: Set Up the Project

```bash
# Navigate to the project directory where you have saved/extracted the files
cd resume_analyzer
```

### Step 2: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 4: Download SpaCy Language Model

```bash
# Download the English language model
python -m spacy download en_core_web_sm
```

### Step 5: Create Uploads Directory

Ensure the uploads directory exists:

```bash
# Create the uploads directory if it doesn't exist
mkdir -p app/uploads
```

### Step 6: Run the Application

```bash
# Start the Flask development server
python run.py
```

### Step 7: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

You should now see the Resume Analyzer interface and be able to upload and analyze resumes.

### Troubleshooting Common Issues

- **Missing Dependencies**: If you encounter import errors, ensure all packages are installed with `pip install -r requirements.txt`
- **SpaCy Model Issues**: If you get errors about missing SpaCy models, verify installation with `python -m spacy validate`
- **File Permission Errors**: Ensure the app has write permissions to the uploads directory
- **Port Already in Use**: If port 5000 is already in use, modify the `port` parameter in `run.py`

## GitHub Setup and Deployment Instructions

### Step 1: Create a GitHub Account (if you don't have one)

1. Go to [GitHub.com](https://github.com)
2. Click "Sign up" and follow the instructions to create your account
3. Verify your email address when prompted

### Step 2: Install Git on Your Computer

#### For Windows:
1. Download Git from [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Run the installer with default settings
3. Open Command Prompt or Git Bash to verify installation by typing: `git --version`

#### For macOS:
1. If you have Homebrew, run: `brew install git`
2. Otherwise, download Git from [https://git-scm.com/download/mac](https://git-scm.com/download/mac)
3. Open Terminal and verify installation: `git --version`

#### For Linux:
1. For Debian/Ubuntu: `sudo apt-get update && sudo apt-get install git`
2. For Fedora: `sudo dnf install git`
3. Verify installation: `git --version`

### Step 3: Configure Git

Open Terminal or Command Prompt and run:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 4: Create a New GitHub Repository

1. Log in to GitHub
2. Click the "+" icon in the top right corner and select "New repository"
3. Enter "resume-analyzer" as the repository name
4. Add a description (optional)
5. Select "Public" or "Private" depending on your preference
6. Check "Add a README file" (optional)
7. Click "Create repository"

### Step 5: Upload Project Files to GitHub

#### Option 1: Using GitHub Desktop (Easiest Method)
1. Download and install [GitHub Desktop](https://desktop.github.com/)
2. Sign in with your GitHub account
3. Click "File" > "Add local repository"
4. Browse to your resume_analyzer project folder and select it
5. Add a summary message for your first commit (e.g., "Initial commit")
6. Click "Commit to main"
7. Click "Publish repository" (or "Push origin" if the repository already exists)

#### Option 2: Using Command Line
1. Open Terminal or Command Prompt
2. Navigate to your project directory:
   ```bash
   cd path/to/resume_analyzer
   ```
3. Initialize git repository:
   ```bash
   git init
   ```
4. Add all files to git:
   ```bash
   git add .
   ```
5. Commit the files:
   ```bash
   git commit -m "Initial commit"
   ```
6. Connect to your GitHub repository:
   ```bash
   git remote add origin https://github.com/yourusername/resume-analyzer.git
   ```
7. Push the files to GitHub:
   ```bash
   git push -u origin main
   ```
   (If you're using an older Git version, you might need to use `master` instead of `main`)

### Step 6: Verify Your Repository

1. Go to your GitHub account and navigate to your repositories
2. Click on "resume-analyzer"
3. Ensure all your files have been uploaded correctly

## Heroku Deployment Instructions

### Prerequisites

- Heroku account (sign up at [heroku.com](https://www.heroku.com) if you don't have one)
- Heroku CLI installed ([installation guide](https://devcenter.heroku.com/articles/heroku-cli))
- Project uploaded to GitHub (follow GitHub instructions above)

### Step 1: Ensure Your Application has Required Files

The project should include these files for Heroku deployment:

1. **requirements.txt**: Lists all Python dependencies, including gunicorn:
   ```
   # Check if gunicorn is in your requirements.txt, if not, add:
   gunicorn==20.1.0
   ```

2. **Procfile**: Create this file in the root directory with the following content:
   ```
   web: gunicorn run:app
   ```

### Step 2: Create a Heroku Application

1. Sign in to your Heroku account on the [Heroku website](https://dashboard.heroku.com)
2. Click the "New" button in the top right corner and select "Create new app"
3. Enter a unique app name (e.g., "resume-analyzer-app") and select your region
4. Click "Create app"

### Step 3: Connect Your GitHub Repository

1. In your app's dashboard, go to the "Deploy" tab
2. Under "Deployment method", select "GitHub"
3. Click "Connect to GitHub" and sign in if prompted
4. In the search field, type "resume-analyzer" and click "Search"
5. Find your repository in the list and click "Connect"

### Step 4: Configure Your Application

1. Go to the "Settings" tab in your app's dashboard
2. Under "Config Vars", click "Reveal Config Vars"
3. Add a variable with key `SECRET_KEY` and a secure random value
4. Add a variable with key `PYTHONPATH` and value `/app`

### Step 5: Add the Python Buildpack

1. Still in the "Settings" tab, scroll down to "Buildpacks"
2. Click "Add buildpack"
3. Select "Python" and click "Save changes"

### Step 6: Deploy Your Application

1. Go back to the "Deploy" tab
2. Scroll down to the "Manual deploy" section
3. Make sure "main" (or "master") branch is selected
4. Click "Deploy Branch"
5. Wait for the build process to complete (this may take a few minutes)
6. Once complete, click "View" to see your deployed application

### Step 7: Enable Automatic Deployments (Optional)

1. In the "Deploy" tab, scroll to the "Automatic deploys" section
2. Click "Enable Automatic Deploys"
3. This will automatically deploy new changes when you push to your GitHub repository

### Step 8: Monitor Your Application

1. Go to the "More" dropdown in the top right and select "View logs"
2. Check for any errors or issues that might occur
3. Use these logs for troubleshooting if needed

### Troubleshooting Heroku Deployment

- **Application Error**: Check logs by clicking "More" → "View logs" in your app dashboard
- **Build Failures**: Ensure all dependencies are correctly listed in requirements.txt
- **SpaCy Model Issues**: After deploying, you might need to run `heroku run python -m spacy download en_core_web_sm`
- **Memory Limitations**: If your app crashes, you might need to upgrade to a paid dyno for more resources
- **Port Configuration**: Make sure your app listens on the port specified by the environment variable `PORT`

## Project Structure

```
resume_analyzer/
├── app/
│   ├── __init__.py         # Flask application factory
│   ├── routes/             # Route definitions
│   │   ├── __init__.py
│   │   └── main.py         # Main route handlers
│   ├── static/             # Static files (CSS, JS, images)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/          # HTML templates
│   │   ├── base.html       # Base template
│   │   ├── index.html      # Home page
│   │   ├── results.html    # Results page
│   │   └── about.html      # About page
│   ├── uploads/            # Folder for uploaded resumes
│   └── utils/              # Utility modules
│       ├── __init__.py
│       ├── nlp_utils.py            # NLP utilities
│       ├── resume_extractor.py     # Text extraction from documents
│       ├── resume_analyzer.py      # Core resume analysis
│       └── feedback_generator.py   # Feedback generation
├── requirements.txt        # Project dependencies
├── Procfile               # For Heroku deployment
├── run.py                 # Main entry point
└── README.md              # Project documentation
```

## Usage

1. **Upload Resume:** Select or drag & drop your resume file (PDF, DOCX, or TXT format)
2. **Analyze:** The system will extract text and analyze your resume using AI
3. **Review Results:** Examine the overall score, component scores, and detailed feedback
4. **Implement Suggestions:** Use the recommendations to improve your resume

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- NLTK and SpaCy for NLP capabilities
- Flask for the web framework
- PyMuPDF and pdfminer.six for document processing
- Bootstrap for frontend design