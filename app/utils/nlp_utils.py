"""
NLP Utilities Module.

This module provides Natural Language Processing (NLP) utilities 
for analyzing resume text. It manages initialization of NLP models
and provides common NLP functions used across the application.
"""

import nltk
import spacy
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

# Global variables to hold loaded models
nlp = None

def initialize():
    """
    Initialize NLP components required for resume analysis.
    
    This function loads necessary NLTK data and SpaCy models.
    It should be called once at application startup.
    """
    global nlp
    
    print("Initializing NLP components...")
    
    # Download required NLTK packages
    try:
        # Download necessary NLTK data
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        nltk.download('wordnet', quiet=True)
        
        # Load SpaCy model
        nlp = spacy.load('en_core_web_sm')
        
        print("NLP components initialized successfully")
    except Exception as e:
        print(f"Error initializing NLP components: {str(e)}")
        raise

def get_spacy_model():
    """
    Get the loaded SpaCy model.
    
    Returns:
        spacy.Language: The loaded SpaCy model.
    """
    global nlp
    if nlp is None:
        initialize()
    return nlp

def get_language_tool():
    """
    Get the loaded LanguageTool instance.
    
    Returns:
        None: LanguageTool is disabled in this version.
    """
    return None

def tokenize_text(text):
    """
    Tokenize text into sentences and words.
    
    Args:
        text (str): The text to tokenize.
        
    Returns:
        tuple: A tuple containing (sentences, words)
    """
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    return sentences, words

def clean_text(text):
    """
    Clean the text by removing special characters and normalizing whitespace.
    
    Args:
        text (str): The text to clean.
        
    Returns:
        str: The cleaned text.
    """
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters except for common punctuation
    text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
    
    return text.strip()

def count_words(text):
    """
    Count the number of words in the text.
    
    Args:
        text (str): The text to count words in.
        
    Returns:
        int: The number of words.
    """
    return len(word_tokenize(text))

def get_stop_words():
    """
    Get a set of English stopwords.
    
    Returns:
        set: A set of English stopwords.
    """
    return set(stopwords.words('english'))

def check_grammar(text):
    """
    Simple grammar check without LanguageTool.
    
    This is a simplified version that looks for basic patterns
    since LanguageTool is disabled.
    
    Args:
        text (str): The text to check for grammar issues.
        
    Returns:
        list: List of grammar and spelling errors (simplified).
    """
    # This is a simplified implementation without LanguageTool
    # It returns an empty list as a placeholder
    return []