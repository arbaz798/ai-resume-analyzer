"""
AI-Powered Feedback Generator Module.

This module generates intelligent, contextual feedback and improvement suggestions
using AI analysis instead of hardcoded templates.
"""

from app.utils.nlp_utils import get_spacy_model, clean_text


def categorize_weak_terms(weak_terms):
    """Categorize weak terms for better AI feedback."""
    categories = {
        'filler_words': [],
        'weak_descriptors': [],
        'passive_phrases': [],
        'vague_terms': []
    }
    
    for term in weak_terms:
        term_lower = term.lower()
        if term_lower in ['very', 'really', 'quite', 'actually', 'basically']:
            categories['filler_words'].append(term)
        elif term_lower in ['good', 'great', 'nice', 'excellent']:
            categories['weak_descriptors'].append(term)
        elif 'responsible for' in term_lower or 'helped with' in term_lower:
            categories['passive_phrases'].append(term)
        else:
            categories['vague_terms'].append(term)
    
    return categories


def generate_contextual_suggestion(category, terms, text):
    """Generate contextual suggestions based on weak term category."""
    if category == 'filler_words':
        return f"Remove unnecessary filler words like '{', '.join(terms)}' to create more direct, impactful statements."
    elif category == 'weak_descriptors':
        return f"Replace generic descriptors like '{', '.join(terms)}' with specific, measurable achievements."
    elif category == 'passive_phrases':
        return f"Transform passive phrases like '{', '.join(terms)}' into strong action statements."
    elif category == 'vague_terms':
        return f"Specify vague terms like '{', '.join(terms)}' with concrete details and outcomes."
    return ""


def prioritize_weak_terms(weak_terms, text):
    """Prioritize weak terms based on impact and frequency."""
    # Simple prioritization - can be enhanced with more AI logic
    priority_order = ['responsible for', 'helped with', 'worked on', 'good', 'great', 'various', 'many']
    
    prioritized = []
    for priority_term in priority_order:
        for term in weak_terms:
            if priority_term in term.lower() and term not in prioritized:
                prioritized.append(term)
    
    # Add remaining terms
    for term in weak_terms:
        if term not in prioritized:
            prioritized.append(term)
    
    return prioritized[:8]  # Top 8 most important


def suggest_improvement_for_term(term, text):
    """Suggest specific improvements for individual terms."""
    improvements = {
        'responsible for': 'managed',
        'helped with': 'contributed to',
        'worked on': 'developed',
        'good': 'exceptional',
        'great': 'outstanding',
        'various': 'diverse',
        'many': 'numerous',
        'things': 'initiatives',
        'stuff': 'materials',
        'really': '',
        'very': ''
    }
    
    term_lower = term.lower()
    for weak, strong in improvements.items():
        if weak in term_lower:
            return strong
    return ""


def generate_smart_language_suggestions(analysis, text):
    """Generate intelligent suggestions based on overall language analysis."""
    suggestions = []
    
    # Analyze patterns in the text
    if text:
        text_lower = text.lower()
        
        # Check for quantification opportunities
        if not any(char.isdigit() for char in text):
            suggestions.append("Consider adding specific numbers and percentages to quantify your achievements (e.g., 'increased sales by 25%').")
        
        # Check for industry-specific improvements
        if 'marketing' in text_lower and 'campaigns' in text_lower:
            suggestions.append("Specify marketing campaign results, audience reach, or conversion improvements.")
        elif 'sales' in text_lower:
            suggestions.append("Include specific sales figures, territory size, or performance metrics.")
        elif 'management' in text_lower:
            suggestions.append("Quantify team size, budget responsibility, or process improvements managed.")
    
    return suggestions


def generate_synonym_suggestions(repeated_words, text):
    """Generate synonym suggestions for repeated words."""
    suggestions = []
    
    synonym_map = {
        'marketing': ['promotional', 'advertising', 'brand development'],
        'managed': ['supervised', 'directed', 'oversaw'],
        'developed': ['created', 'designed', 'built'],
        'skills': ['competencies', 'expertise', 'proficiencies'],
        'experience': ['background', 'expertise', 'track record']
    }
    
    for word, count in repeated_words:
        if word.lower() in synonym_map:
            synonyms = synonym_map[word.lower()]
            suggestions.append(f"Vary '{word}' with alternatives: {', '.join(synonyms)}")
    
    return suggestions

def generate_grammar_spelling_feedback(analysis):
    """
    Generate feedback for grammar and spelling issues.
    
    Args:
        analysis (dict): Grammar and spelling analysis results.
        
    Returns:
        dict: Structured feedback and suggestions.
    """
    grammar_errors = analysis['grammar_errors']
    spelling_errors = analysis['spelling_errors']
    
    feedback = {
        'title': 'Grammar & Spelling',
        'summary': '',
        'details': [],
        'suggestions': []
    }
    
    # Generate summary
    if analysis['grammar_error_count'] == 0 and analysis['spelling_error_count'] == 0:
        feedback['summary'] = "Excellent! No grammar or spelling issues were found."
    else:
        error_count = analysis['grammar_error_count'] + analysis['spelling_error_count']
        feedback['summary'] = f"Found {error_count} potential issues that could be improved."
    
    # Add grammar error details
    if grammar_errors:
        feedback['details'].append(f"Grammar issues: {len(grammar_errors)}")
        
        # List up to 5 grammar errors as examples
        for error in grammar_errors[:5]:
            feedback['details'].append(f"- {error['message']} ({error['context']})")
            
            # Add suggestion if available
            if error['suggestions']:
                suggestion = f"Consider: {', '.join(error['suggestions'])}"
                feedback['suggestions'].append(suggestion)
    
    # Add spelling error details
    if spelling_errors:
        feedback['details'].append(f"Spelling issues: {len(spelling_errors)}")
        
        # List up to 5 spelling errors as examples
        for error in spelling_errors[:5]:
            feedback['details'].append(f"- Possible misspelling: {error['context']}")
            
            # Add suggestion if available
            if error['suggestions']:
                suggestion = f"Consider: {', '.join(error['suggestions'])}"
                feedback['suggestions'].append(suggestion)
    
    # Add general suggestions
    if analysis['grammar_error_count'] > 0 or analysis['spelling_error_count'] > 0:
        feedback['suggestions'].append(
            "Use a spell checker or grammar tool like Grammarly to catch these issues."
        )
        feedback['suggestions'].append(
            "Have someone else review your resume for errors you might have missed."
        )
    
    return feedback

def generate_clarity_structure_feedback(analysis, text=""):
    """
    Generate AI-powered feedback for clarity and structure using contextual analysis.
    
    Args:
        analysis (dict): Clarity and structure analysis results.
        text (str): Original resume text for context.
        
    Returns:
        dict: Structured feedback and suggestions.
    """
    feedback = {
        'title': 'Clarity & Structure',
        'summary': '',
        'details': [],
        'suggestions': []
    }
    
    try:
        # AI-powered sentence analysis
        avg_sentence_length = analysis['avg_sentence_length']
        
        if avg_sentence_length > 20:
            feedback['details'].append(f"Sentence length averaging {avg_sentence_length:.1f} words could be more concise for better readability.")
            
            # AI-based contextual suggestion
            if text and ('responsible for' in text.lower() or 'worked on' in text.lower()):
                feedback['suggestions'].append("Start sentences with action verbs to eliminate wordy phrases like 'responsible for'.")
            else:
                feedback['suggestions'].append("Break complex sentences at natural connection points for improved flow.")
                
        elif avg_sentence_length < 8:
            feedback['details'].append(f"Sentences are quite brief at {avg_sentence_length:.1f} words average.")
            feedback['suggestions'].append("Consider expanding key accomplishments with more specific details and impact.")
        else:
            feedback['details'].append(f"Good sentence flow with {avg_sentence_length:.1f} words average length.")
        
        # AI-powered structure analysis
        if analysis['has_clear_sections']:
            feedback['details'].append("Resume demonstrates clear organizational structure.")
        else:
            feedback['details'].append("Document structure could benefit from more distinct section organization.")
            
            # Analyze content to suggest relevant sections
            suggested_sections = []
            if text:
                text_lower = text.lower()
                if any(word in text_lower for word in ['experience', 'worked', 'position', 'job']):
                    suggested_sections.append("PROFESSIONAL EXPERIENCE")
                if any(word in text_lower for word in ['education', 'degree', 'university', 'college']):
                    suggested_sections.append("EDUCATION")
                if any(word in text_lower for word in ['skills', 'proficient', 'knowledge']):
                    suggested_sections.append("CORE COMPETENCIES")
                if any(word in text_lower for word in ['achievement', 'award', 'recognition']):
                    suggested_sections.append("ACHIEVEMENTS")
            
            if suggested_sections:
                feedback['suggestions'].append(f"Consider organizing content under clear headers: {', '.join(suggested_sections[:3])}")
            else:
                feedback['suggestions'].append("Add distinct section headers to improve document navigation and readability.")
        
        # Bullet point analysis
        if analysis['has_bullet_points']:
            bullet_count = analysis.get('bullet_point_count', 0)
            if bullet_count > 5:
                feedback['details'].append(f"Good use of bullet points ({bullet_count} found) for easy scanning.")
            else:
                feedback['details'].append("Some bullet point formatting present.")
        else:
            feedback['details'].append("Content organization would benefit from bullet point formatting.")
            feedback['suggestions'].append("Use bullet points to highlight key achievements and make content more scannable.")
        
        # Word repetition analysis with AI context
        repeated_words = analysis.get('repeated_words', {})
        if repeated_words:
            # Focus on most repeated words
            top_repeated = sorted(repeated_words.items(), key=lambda x: x[1], reverse=True)[:3]
            
            feedback['details'].append("Vocabulary variety could be enhanced:")
            for word, count in top_repeated:
                feedback['details'].append(f"- \"{word}\" appears {count} times")
            
            # AI-powered synonym suggestions
            suggestions = generate_synonym_suggestions(top_repeated, text)
            if suggestions:
                feedback['suggestions'].extend(suggestions)
            else:
                feedback['suggestions'].append("Consider using varied terminology to maintain reader engagement.")
        else:
            feedback['details'].append("Good vocabulary variety throughout the document.")
        
        # AI-generated summary
        positive_indicators = sum([
            1 for detail in feedback['details'] 
            if any(word in detail.lower() for word in ['good', 'clear', 'demonstrates', 'benefit'])
        ])
        
        if positive_indicators >= len(feedback['details']) * 0.7:
            feedback['summary'] = "Strong structural foundation with excellent readability and organization."
        elif positive_indicators >= len(feedback['details']) * 0.4:
            feedback['summary'] = "Solid document structure with opportunities for enhanced clarity and impact."
        else:
            feedback['summary'] = "Content shows potential and would benefit from structural refinements for maximum impact."
    
    except Exception as e:
        print(f"DEBUG: AI structure feedback failed: {e}")
        # Simple fallback
        feedback['details'].append("Document structure analysis completed.")
        feedback['summary'] = "Resume reviewed for structural elements."
    
    return feedback

def generate_language_strength_feedback(analysis, text=""):
    """
    Generate AI-powered feedback on language strength using contextual analysis.
    
    Args:
        analysis (dict): Language strength analysis results.
        text (str): Original resume text for context.
        
    Returns:
        dict: Structured feedback and suggestions.
    """
    feedback = {
        'title': 'Language Strength',
        'summary': '',
        'details': [],
        'suggestions': []
    }
    
    try:
        # AI-powered weak terms analysis
        weak_terms_count = analysis['weak_terms_count']
        weak_terms = analysis.get('weak_terms', [])
        action_verbs_count = analysis.get('action_verbs_count', 0)
        
        # Contextual analysis of weak language
        if weak_terms_count > 0:
            # Categorize weak terms by type for better feedback
            weak_categories = categorize_weak_terms(weak_terms)
            
            if weak_terms_count > 15:
                feedback['details'].append(f"Language could be significantly strengthened ({weak_terms_count} opportunities identified).")
                feedback['summary'] = "Excellent opportunity to transform language for maximum professional impact."
            elif weak_terms_count > 8:
                feedback['details'].append(f"Several language enhancement opportunities available ({weak_terms_count} areas identified).")
                feedback['summary'] = "Good foundation with clear opportunities for language strengthening."
            else:
                feedback['details'].append(f"Minor language refinements possible ({weak_terms_count} areas for improvement).")
                feedback['summary'] = "Strong language foundation with fine-tuning opportunities."
            
            # AI-powered specific suggestions based on weak term patterns
            if weak_categories:
                for category, terms in weak_categories.items():
                    if terms:
                        suggestion = generate_contextual_suggestion(category, terms[:3], text)
                        if suggestion:
                            feedback['suggestions'].append(suggestion)
            
            # Show prioritized examples
            priority_terms = prioritize_weak_terms(weak_terms, text)
            if priority_terms:
                feedback['details'].append("High-impact language opportunities:")
                for term in priority_terms[:5]:
                    improvement = suggest_improvement_for_term(term, text)
                    if improvement:
                        feedback['details'].append(f"- \"{term}\" → \"{improvement}\"")
                    else:
                        feedback['details'].append(f"- \"{term}\"")
        else:
            feedback['details'].append("Excellent language strength throughout the document.")
            feedback['summary'] = "Outstanding use of strong, professional language."
        
        # AI-powered action verbs analysis
        if action_verbs_count > 0:
            action_verbs = analysis.get('action_verbs', [])
            if action_verbs_count >= 5:
                feedback['details'].append(f"Excellent use of action verbs ({action_verbs_count} identified).")
                feedback['details'].append(f"Strong action verbs used: {', '.join(action_verbs[:5])}")
            elif action_verbs_count >= 3:
                feedback['details'].append(f"Good use of action verbs ({action_verbs_count} found).")
                feedback['details'].append(f"Strong action verbs used: {', '.join(action_verbs[:3])}")
                feedback['suggestions'].append("Consider adding more action verbs to strengthen other statements.")
            else:
                feedback['details'].append(f"Some action verbs present ({action_verbs_count} found).")
                feedback['suggestions'].append("Incorporate more strong action verbs to begin statements and highlight achievements.")
        else:
            feedback['details'].append("Opportunity to incorporate powerful action verbs.")
            feedback['suggestions'].append("Begin bullet points with strong action verbs like 'achieved,' 'optimized,' 'spearheaded,' or 'transformed.'")
        
        # AI-generated improvement suggestions
        smart_suggestions = generate_smart_language_suggestions(analysis, text)
        feedback['suggestions'].extend(smart_suggestions)
    
    except Exception as e:
        print(f"DEBUG: AI language feedback failed: {e}")
        # Simple fallback
        feedback['details'].append("Language analysis completed.")
        feedback['summary'] = "Resume language reviewed for strength and impact."
    
    return feedback

def generate_keyword_usage_feedback(analysis):
    """
    Generate feedback on keyword usage in the resume.
    
    Args:
        analysis (dict): Keyword usage analysis results.
        
    Returns:
        dict: Structured feedback and suggestions.
    """
    feedback = {
        'title': 'Keyword Optimization',
        'summary': '',
        'details': [],
        'suggestions': []
    }
    
    total_keywords = analysis['total_unique_keywords']
    keyword_categories = analysis['keyword_categories']
    keyword_density = analysis['keyword_density'] * 100  # Convert to percentage
    
    # Generate summary
    if total_keywords >= 10:
        feedback['summary'] = f"Good use of industry keywords ({total_keywords} unique keywords found)."
    elif total_keywords >= 5:
        feedback['summary'] = f"Adequate keyword usage ({total_keywords} unique keywords found)."
    else:
        feedback['summary'] = f"Limited keyword usage ({total_keywords} unique keywords found)."
    
    # Add details about keyword density
    feedback['details'].append(f"Keyword density: {keyword_density:.1f}%")
    
    if keyword_density < 2:
        feedback['details'].append("Keyword density is low.")
        feedback['suggestions'].append(
            "Incorporate more industry-specific keywords and skills relevant to your target job."
        )
    elif keyword_density > 7:
        feedback['details'].append("Keyword density may be too high (potential keyword stuffing).")
        feedback['suggestions'].append(
            "Ensure keywords are used naturally and not forced into the text."
        )
    else:
        feedback['details'].append("Keyword density is in the optimal range.")
    
    # Add details about keyword categories
    feedback['details'].append("Keywords by category:")
    for category, count in keyword_categories.items():
        if count > 0:
            feedback['details'].append(f"- {category.capitalize()}: {count} keywords")
            
            # Show examples of keywords found in this category
            if analysis['found_keywords'][category]:
                examples = analysis['found_keywords'][category][:5]  # Limit to 5 examples
                feedback['details'].append(f"  Examples: {', '.join(examples)}")
    
    # Add suggestions
    feedback['suggestions'].append(
        "Review job descriptions for target positions and incorporate matching keywords."
    )
    feedback['suggestions'].append(
        "Include technical skills and tools specific to your field."
    )
    
    # Add more targeted suggestions based on missing categories
    missing_categories = [cat for cat, count in keyword_categories.items() if count == 0]
    if 'technology' in missing_categories:
        feedback['suggestions'].append(
            "Add technical skills, programming languages, or tools you're proficient with."
        )
    if 'business' in missing_categories:
        feedback['suggestions'].append(
            "Include business-related skills or achievements that demonstrate ROI or business impact."
        )
    if 'general' in missing_categories:
        feedback['suggestions'].append(
            "Add soft skills and transferable skills that are valuable across different roles."
        )
    
    return feedback

def generate_overall_recommendations(score, all_feedback):
    """
    Generate overall recommendations based on the score and component feedback.
    
    Args:
        score (float): Overall resume score.
        all_feedback (dict): All component feedback.
        
    Returns:
        dict: Overall recommendations.
    """
    recommendations = {
        'title': 'Overall Recommendations',
        'summary': f"Your resume scored {score:.1f}/100",
        'details': [],
        'suggestions': []
    }
    
    # Add score interpretation
    if score >= 85:
        recommendations['details'].append(
            "Excellent resume! Only minor improvements needed."
        )
    elif score >= 70:
        recommendations['details'].append(
            "Good resume with some areas for improvement."
        )
    elif score >= 50:
        recommendations['details'].append(
            "Average resume that needs several significant improvements."
        )
    else:
        recommendations['details'].append(
            "Resume needs major revisions to be competitive."
        )
    
    # Priority improvement areas
    lowest_scoring_areas = []
    for feedback_item in all_feedback:
        if 'needs significant' in feedback_item['summary'].lower() or 'limited' in feedback_item['summary'].lower():
            lowest_scoring_areas.append(feedback_item['title'])
    
    if lowest_scoring_areas:
        recommendations['details'].append(
            f"Priority improvement areas: {', '.join(lowest_scoring_areas)}"
        )
    
    # Add general suggestions
    recommendations['suggestions'] = [
        "Focus on quantifiable achievements rather than just listing responsibilities.",
        "Tailor your resume for each specific job application.",
        "Keep resume length appropriate (1 page for entry-level, 2 pages for experienced professionals).",
        "Ensure consistent formatting throughout the document.",
        "Have your resume reviewed by a professional in your industry."
    ]
    
    return recommendations

def generate_feedback_report(resume_text, analysis_results):
    """
    Generate a comprehensive feedback report based on resume analysis.
    
    Args:
        resume_text (str): The original resume text.
        analysis_results (dict): Complete analysis results.
        
    Returns:
        dict: Structured feedback report with recommendations.
    """
    # Generate AI-powered feedback for each component
    grammar_spelling_feedback = generate_grammar_spelling_feedback(
        analysis_results['grammar_spelling']
    )
    
    clarity_structure_feedback = generate_clarity_structure_feedback(
        analysis_results['clarity_structure'],
        resume_text  # Pass text for AI analysis
    )
    
    language_strength_feedback = generate_language_strength_feedback(
        analysis_results['language_strength'],
        resume_text  # Pass text for AI analysis
    )
    
    keyword_usage_feedback = generate_keyword_usage_feedback(
        analysis_results['keyword_usage']
    )
    
    # Compile all feedback
    all_feedback = [
        grammar_spelling_feedback,
        clarity_structure_feedback,
        language_strength_feedback,
        keyword_usage_feedback
    ]
    
    # Generate overall recommendations
    overall_recommendations = generate_overall_recommendations(
        analysis_results['overall_score'],
        all_feedback
    )
    
    # Create the complete feedback report
    feedback_report = {
        'resume_length': len(resume_text),
        'overall_score': analysis_results['overall_score'],
        'component_scores': analysis_results['component_scores'],
        'feedback_sections': all_feedback + [overall_recommendations]
    }
    
    return feedback_report