"""
Resume Analyzer Module.

This module provides the core functionality for analyzing resumes.
It evaluates grammar, structure, content quality, and keyword usage.
"""

import re
import statistics
from collections import Counter
from app.utils.nlp_utils import (
    get_spacy_model, check_grammar, tokenize_text, 
    count_words, get_stop_words
)

# List of weak/vague words that should be minimized in a resume
WEAK_WORDS = {
    'good', 'great', 'nice', 'excellent', 'amazing',
    'best', 'better', 'well', 'very', 'really',
    'thing', 'things', 'stuff', 'etc', 'helped',
    'handled', 'responsible', 'responsible for', 
    'various', 'several', 'many', 'some', 'much',
    'a lot', 'kind of', 'sort of', 'type of',
    'worked on', 'worked with', 'was part of',
    'assisted', 'assisted with', 'assisted in'
}

# List of strong action verbs for resumes
ACTION_VERBS = {
    'achieved', 'improved', 'trained', 'managed', 'created',
    'reduced', 'increased', 'negotiated', 'launched', 'developed',
    'designed', 'implemented', 'established', 'coordinated', 'led',
    'presented', 'organized', 'restructured', 'delivered', 'generated',
    'streamlined', 'decreased', 'enhanced', 'expanded', 'optimized',
    'secured', 'integrated', 'innovated', 'authored', 'adapted',
    'resolved', 'revitalized', 'mentored', 'motivated', 'transformed',
    'spearheaded', 'orchestrated'
}

# Industry-specific keywords (can be expanded)
INDUSTRY_KEYWORDS = {
    'technology': {
        'python', 'java', 'javascript', 'react', 'node', 'sql', 'nosql',
        'aws', 'azure', 'cloud', 'docker', 'kubernetes', 'agile', 'scrum',
        'rest api', 'microservices', 'devops', 'ci/cd', 'git', 'machine learning',
        'artificial intelligence', 'data science', 'big data', 'blockchain',
        'frontend', 'backend', 'full stack', 'mobile', 'android', 'ios'
    },
    'business': {
        'management', 'leadership', 'strategy', 'analytics', 'operations',
        'marketing', 'sales', 'finance', 'accounting', 'hr', 'human resources',
        'consulting', 'project management', 'business development', 'client relations',
        'stakeholder', 'roi', 'kpi', 'metrics', 'growth', 'revenue', 'profit',
        'market analysis', 'strategic planning', 'budget', 'forecasting'
    },
    'general': {
        'team', 'leadership', 'communication', 'collaboration', 'problem-solving',
        'analytical', 'detail-oriented', 'project management', 'time management',
        'critical thinking', 'organization', 'planning', 'research', 'writing', 
        'interpersonal', 'multitasking', 'decision-making', 'presentation',
        'negotiation', 'customer service', 'creativity'
    }
}

def analyze_grammar_spelling(text):
    """
    Analyze grammar and spelling in the resume.
    
    This is a simplified version that works without LanguageTool.
    
    Args:
        text (str): The resume text.
        
    Returns:
        dict: Dictionary containing grammar and spelling analysis results.
    """
    # Since LanguageTool is disabled, we're using a simplified approach
    grammar_errors = []
    spelling_errors = []
    
    # Get basic text metrics
    sentences, words = tokenize_text(text)
    total_words = len(words)
    total_sentences = len(sentences)
    
    # Simplified grammar checking (very basic)
    # Check for sentences that don't end with proper punctuation
    for sentence in sentences:
        if sentence and not sentence[-1] in ['.', '!', '?', ':']:
            grammar_errors.append({
                'message': 'Sentence does not end with proper punctuation',
                'context': sentence,
                'offset': 0,
                'length': len(sentence),
                'suggestions': []
            })
    
    # Zero error rates since we can't do proper grammar checking without LanguageTool
    grammar_error_rate = 0
    spelling_error_rate = 0
    
    return {
        'grammar_errors': grammar_errors,
        'spelling_errors': spelling_errors,
        'grammar_error_count': len(grammar_errors),
        'spelling_error_count': len(spelling_errors),
        'grammar_error_rate': grammar_error_rate,
        'spelling_error_rate': spelling_error_rate
    }

def analyze_clarity_structure(text):
    """
    Analyze the clarity and structure of the resume.
    
    Args:
        text (str): The resume text.
        
    Returns:
        dict: Dictionary containing clarity and structure analysis.
    """
    nlp = get_spacy_model()
    doc = nlp(text)
    
    # Get sentences
    sentences = [sent.text.strip() for sent in doc.sents]
    
    # Calculate sentence metrics
    sentence_lengths = [len(sent.split()) for sent in sentences]
    avg_sentence_length = statistics.mean(sentence_lengths) if sentence_lengths else 0
    
    # Calculate sentence complexity
    complex_sentences = [sent for sent in sentences if len(sent.split()) > 20]
    
    # Look for bullet points
    bullet_points = re.findall(r'(?:^|\n)[\s]*[•·\-\*][\s]+(.*?)(?:\n|$)', text)
    
    # Identify paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    # Calculate repeated words
    words = [token.text.lower() for token in doc if token.is_alpha]
    word_freq = Counter(words)
    repeated_words = {word: count for word, count in word_freq.items() 
                     if count > 3 and word not in get_stop_words()}
    
    # Check for section headings (all caps or followed by colon)
    potential_headings = re.findall(r'(?:^|\n)([A-Z][A-Z\s]{2,}|.+:)\s*(?:\n|$)', text)
    
    return {
        'avg_sentence_length': avg_sentence_length,
        'complex_sentence_count': len(complex_sentences),
        'complex_sentences': complex_sentences[:5],  # Return only first 5 examples
        'bullet_point_count': len(bullet_points),
        'paragraph_count': len(paragraphs),
        'repeated_words': repeated_words,
        'potential_headings': potential_headings,
        'has_clear_sections': len(potential_headings) >= 3,  # Resume should have at least 3 sections
        'has_bullet_points': len(bullet_points) > 0
    }

def analyze_language_strength(text):
    """
    Analyze the strength of language used in the resume.
    
    Args:
        text (str): The resume text.
        
    Returns:
        dict: Dictionary containing language strength analysis.
    """
    nlp = get_spacy_model()
    doc = nlp(text.lower())
    
    # Extract all words
    words = [token.text.lower() for token in doc if token.is_alpha]
    
    # Debug: Print sample words and WEAK_WORDS
    print(f"DEBUG: Total words extracted: {len(words)}")
    print(f"DEBUG: Sample words: {words[:20]}")
    print(f"DEBUG: WEAK_WORDS set: {WEAK_WORDS}")
    
    # Find weak words
    weak_words_found = [word for word in words if word in WEAK_WORDS]
    weak_phrases_found = []
    
    for phrase in WEAK_WORDS:
        if ' ' in phrase and phrase in text.lower():
            weak_phrases_found.append(phrase)
    
    all_weak_terms = weak_words_found + weak_phrases_found
    
    # Debug: Print weak terms found
    print(f"DEBUG: Weak words found: {weak_words_found[:10]}")
    print(f"DEBUG: Weak phrases found: {weak_phrases_found}")
    print(f"DEBUG: Total weak terms: {len(all_weak_terms)}")
    
    # Find action verbs
    action_verbs_found = [word for word in words if word in ACTION_VERBS]
    
    # Calculate metrics (more lenient scoring)
    weak_words_ratio = len(all_weak_terms) / len(words) if words else 0
    action_verbs_ratio = len(action_verbs_found) / len(words) if words else 0
    
    # More lenient language strength calculation
    # Base score starts at 70% instead of 0%, reduced penalty for weak words
    base_score = 0.70
    weak_penalty = min(0.3, weak_words_ratio * 0.5)  # Max 30% penalty, reduced impact
    action_bonus = min(0.3, action_verbs_ratio * 2.0)  # Up to 30% bonus for action verbs
    
    language_strength_score = base_score - weak_penalty + action_bonus
    language_strength_score = min(1.0, max(0.5, language_strength_score))  # Keep between 50-100%
    
    return {
        'weak_terms': list(set(all_weak_terms)),
        'weak_terms_count': len(all_weak_terms),
        'action_verbs': list(set(action_verbs_found)),
        'action_verbs_count': len(set(action_verbs_found)),
        'weak_words_ratio': weak_words_ratio,
        'action_verbs_ratio': action_verbs_ratio,
        'language_strength_score': language_strength_score
    }

def analyze_keyword_usage(text):
    """
    Analyze the usage of industry keywords in the resume.
    
    Args:
        text (str): The resume text.
        
    Returns:
        dict: Dictionary containing keyword usage analysis.
    """
    text_lower = text.lower()
    
    # Check for keywords in different categories
    found_keywords = {}
    for category, keywords in INDUSTRY_KEYWORDS.items():
        found_in_category = [kw for kw in keywords if kw in text_lower]
        found_keywords[category] = found_in_category
    
    # Flatten the list of found keywords
    all_found_keywords = [kw for sublist in found_keywords.values() for kw in sublist]
    
    # Calculate metrics
    total_unique_keywords = len(set(all_found_keywords))
    
    return {
        'found_keywords': found_keywords,
        'total_unique_keywords': total_unique_keywords,
        'keyword_categories': {category: len(found) for category, found in found_keywords.items()},
        'keyword_density': total_unique_keywords / count_words(text) if count_words(text) > 0 else 0
    }

def calculate_overall_score(analysis_results):
    """
    Calculate an overall score based on the analysis results.
    
    Args:
        analysis_results (dict): The complete analysis results.
        
    Returns:
        float: The overall score (0-100).
    """
    # Define weights for each component
    weights = {
        'grammar_spelling': 0.25,
        'clarity_structure': 0.25,
        'language_strength': 0.30,
        'keyword_usage': 0.20
    }
    
    scores = {}
    
    # Grammar & Spelling Score (lower error rates = higher score)
    grammar_error_rate = analysis_results['grammar_spelling']['grammar_error_rate']
    spelling_error_rate = analysis_results['grammar_spelling']['spelling_error_rate']
    
    # Max error rates that would give a score of 0
    max_grammar_error_rate = 0.5  # More than 0.5 errors per sentence is bad
    max_spelling_error_rate = 0.1  # More than 10% of words with spelling errors is bad
    
    grammar_score = max(0, 1 - (grammar_error_rate / max_grammar_error_rate))
    spelling_score = max(0, 1 - (spelling_error_rate / max_spelling_error_rate))
    scores['grammar_spelling'] = (grammar_score * 0.5 + spelling_score * 0.5) * 100
    
    # Clarity & Structure Score (more lenient)
    clarity_results = analysis_results['clarity_structure']
    has_sections = clarity_results['has_clear_sections']
    has_bullets = clarity_results['has_bullet_points']
    avg_sentence_length = clarity_results['avg_sentence_length']
    
    # More lenient sentence length scoring (accept 8-20 words as good)
    if 8 <= avg_sentence_length <= 20:
        sentence_length_score = 1.0
    else:
        sentence_length_score = max(0.6, 1 - min(1, abs(avg_sentence_length - 14) / 20))
    
    # More lenient structure scoring - start with higher base scores
    structure_score = (
        (1.0 if has_sections else 0.75) * 0.4 +  # 75% even without clear sections
        (1.0 if has_bullets else 0.70) * 0.3 +   # 70% even without bullets
        sentence_length_score * 0.3              # Higher weight on sentence length
    )
    
    # Ensure minimum score of 60%
    structure_score = max(0.60, structure_score)
    scores['clarity_structure'] = structure_score * 100
    
    # Language Strength Score
    language_strength = analysis_results['language_strength']['language_strength_score']
    scores['language_strength'] = language_strength * 100
    
    # Keyword Usage Score (more lenient)
    keyword_results = analysis_results['keyword_usage']
    keyword_density = keyword_results['keyword_density']
    total_keywords = keyword_results['total_unique_keywords']
    
    # More lenient keyword density scoring (accept 1-8% as good)
    if 0.01 <= keyword_density <= 0.08:
        keyword_density_score = 1.0
    else:
        keyword_density_score = max(0.6, 1 - min(1, abs(keyword_density - 0.04) / 0.08))
    
    # More lenient keyword count - 5+ keywords is considered good
    keyword_count_score = min(1, total_keywords / 8)  # Reduced from 15 to 8
    keyword_count_score = max(0.5, keyword_count_score)  # Minimum 50%
    
    keyword_score = keyword_density_score * 0.4 + keyword_count_score * 0.6
    # Ensure minimum score of 55%
    keyword_score = max(0.55, keyword_score)
    scores['keyword_usage'] = keyword_score * 100
    
    # Calculate weighted average for overall score
    overall_score = sum(scores[component] * weight for component, weight in weights.items())
    
    # Apply a more encouraging curve - boost scores slightly
    overall_score = min(100, overall_score * 1.1)  # 10% boost, capped at 100
    
    # Return both component scores and overall score
    return {
        'component_scores': scores,
        'overall_score': round(overall_score, 1)
    }

def analyze_resume(text):
    """
    Perform comprehensive analysis of a resume.
    
    Args:
        text (str): The extracted text from the resume.
        
    Returns:
        dict: Complete analysis results.
    """
    # Check if the text is empty (allow any length for improvement)
    if not text or not text.strip():
        raise ValueError("Resume text is empty.")
    
    # Perform various analyses
    grammar_spelling_results = analyze_grammar_spelling(text)
    clarity_structure_results = analyze_clarity_structure(text)
    language_strength_results = analyze_language_strength(text)
    keyword_usage_results = analyze_keyword_usage(text)
    
    # Compile all results
    analysis_results = {
        'grammar_spelling': grammar_spelling_results,
        'clarity_structure': clarity_structure_results,
        'language_strength': language_strength_results,
        'keyword_usage': keyword_usage_results,
    }
    
    # Calculate overall score
    score_results = calculate_overall_score(analysis_results)
    analysis_results.update(score_results)
    
    return analysis_results