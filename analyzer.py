"""
Query Analyzer - Analyzes incoming queries to determine complexity
"""
import re
from typing import Dict


def analyze_query(text: str) -> Dict:
    """
    Analyze a query to determine its complexity and characteristics.
    
    Args:
        text: The user's query text
        
    Returns:
        Dictionary with analysis results
    """
    # Basic metrics
    word_count = len(text.split())
    char_count = len(text)
    
    # Code detection
    has_code = bool(re.search(r'```|function|class|def |import |const |let |var ', text, re.IGNORECASE))
    
    # Complexity keywords
    complex_keywords = r'analyze|compare|explain|evaluate|reasoning|complex|detailed|comprehensive'
    has_complex_keywords = bool(re.search(complex_keywords, text, re.IGNORECASE))
    
    # Simple question detection
    simple_patterns = r'^(what|who|when|where|is|are|can|do|does)\s'
    is_simple_question = bool(re.search(simple_patterns, text, re.IGNORECASE)) and word_count < 20
    
    # Calculate complexity score (1-10)
    complexity = 1
    
    if word_count > 50:
        complexity += 1
    if word_count > 100:
        complexity += 2
    if word_count > 200:
        complexity += 2
        
    if has_code:
        complexity += 3
        
    if has_complex_keywords:
        complexity += 2
        
    if is_simple_question:
        complexity = max(1, complexity - 2)
    
    # Cap at 10
    complexity = min(complexity, 10)
    
    return {
        "word_count": word_count,
        "char_count": char_count,
        "has_code": has_code,
        "has_complex_keywords": has_complex_keywords,
        "is_simple_question": is_simple_question,
        "complexity": complexity
    }


def estimate_tokens(text: str) -> int:
    """
    Rough estimation of token count (chars / 4 is approximate for English)
    """
    return len(text) // 4
