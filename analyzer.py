"""
Enhanced Query Analyzer - Professional complexity analysis with ML-inspired scoring
"""
import re
import math
from typing import Dict, List
from collections import Counter


class QueryAnalyzer:
    """Advanced query analyzer with multi-dimensional complexity scoring"""
    
    # Complexity indicators with weights
    COMPLEXITY_KEYWORDS = {
        'high': ['analyze', 'evaluate', 'compare', 'design', 'architect', 'implement', 
                 'optimize', 'refactor', 'debug', 'comprehensive', 'detailed', 'thorough'],
        'medium': ['explain', 'describe', 'summarize', 'create', 'build', 'write', 'develop'],
        'low': ['what', 'when', 'where', 'who', 'is', 'are', 'can', 'does', 'define']
    }
    
    # Technical indicators
    CODE_PATTERNS = [
        (r'```[\w]*\n', 3),  # Code blocks (highest weight)
        (r'\bclass\s+\w+', 2),  # Class definitions
        (r'\bdef\s+\w+', 2),  # Function definitions
        (r'\bimport\s+\w+', 2),  # Imports
        (r'\bfunction\s+\w+', 2),  # JS functions
        (r'SELECT|INSERT|UPDATE|DELETE', 2),  # SQL
        (r'\{[\s\S]*:[^\}]*\}', 1),  # JSON-like structures
        (r'\$\w+|\@\w+', 1),  # Variables
    ]
    
    # Domain complexity indicators
    TECHNICAL_DOMAINS = [
        'algorithm', 'database', 'architecture', 'system', 'network',
        'security', 'optimization', 'distributed', 'concurrent', 'async',
        'microservice', 'kubernetes', 'docker', 'cloud', 'scalability'
    ]
    
    def analyze(self, text: str) -> Dict:
        """
        Perform multi-dimensional analysis of query complexity
        
        Returns complexity score (1-10) based on:
        - Length (non-linear scaling)
        - Vocabulary sophistication
        - Code presence and complexity
        - Task type (creative vs analytical)
        - Technical domain depth
        """
        # Basic metrics
        words = text.split()
        word_count = len(words)
        char_count = len(text)
        sentence_count = len(re.split(r'[.!?]+', text))
        
        # Initialize scoring components
        scores = {
            'length_score': self._calculate_length_score(word_count),
            'vocabulary_score': self._calculate_vocabulary_score(text, words),
            'code_score': self._calculate_code_score(text),
            'task_complexity_score': self._calculate_task_complexity(text),
            'technical_depth_score': self._calculate_technical_depth(text),
            'structure_score': self._calculate_structure_score(text, sentence_count)
        }
        
        # Weighted combination
        weights = {
            'length_score': 0.15,
            'vocabulary_score': 0.20,
            'code_score': 0.25,
            'task_complexity_score': 0.25,
            'technical_depth_score': 0.10,
            'structure_score': 0.05
        }
        
        final_complexity = sum(scores[key] * weights[key] for key in weights)
        final_complexity = max(1, min(10, round(final_complexity)))
        
        return {
            'complexity': final_complexity,
            'word_count': word_count,
            'char_count': char_count,
            'sentence_count': sentence_count,
            'scores': scores,
            'has_code': scores['code_score'] > 2,
            'is_simple_question': final_complexity <= 3 and sentence_count == 1,
            'estimated_tokens': self._estimate_tokens_accurate(text),
            'task_type': self._classify_task_type(text),
            'recommended_model_tier': self._recommend_tier(final_complexity)
        }
    
    def _calculate_length_score(self, word_count: int) -> float:
        """Non-linear length scoring using logarithmic scale"""
        if word_count <= 5:
            return 1.0
        elif word_count <= 20:
            return 2.0 + (word_count - 5) / 15 * 2  # 2-4
        elif word_count <= 50:
            return 4.0 + (word_count - 20) / 30 * 2  # 4-6
        elif word_count <= 100:
            return 6.0 + (word_count - 50) / 50 * 2  # 6-8
        else:
            return min(10.0, 8.0 + math.log10(word_count - 99))
    
    def _calculate_vocabulary_score(self, text: str, words: List[str]) -> float:
        """Analyze vocabulary sophistication"""
        score = 5.0  # Base score
        
        text_lower = text.lower()
        
        # Check for complexity keywords
        high_complexity_count = sum(1 for word in self.COMPLEXITY_KEYWORDS['high'] if word in text_lower)
        medium_complexity_count = sum(1 for word in self.COMPLEXITY_KEYWORDS['medium'] if word in text_lower)
        low_complexity_count = sum(1 for word in self.COMPLEXITY_KEYWORDS['low'] if word in text_lower)
        
        score += high_complexity_count * 0.8
        score += medium_complexity_count * 0.4
        score -= low_complexity_count * 0.3
        
        # Vocabulary diversity (unique words / total words)
        if len(words) > 0:
            diversity = len(set(w.lower() for w in words)) / len(words)
            score += diversity * 2  # Higher diversity = more complex
        
        return max(1.0, min(10.0, score))
    
    def _calculate_code_score(self, text: str) -> float:
        """Detect and score code presence and complexity"""
        score = 0.0
        
        for pattern, weight in self.CODE_PATTERNS:
            matches = len(re.findall(pattern, text, re.IGNORECASE | re.MULTILINE))
            score += matches * weight
        
        # Code block bonus
        code_blocks = re.findall(r'```[\s\S]*?```', text)
        if code_blocks:
            # Longer code blocks = more complex
            avg_block_length = sum(len(block) for block in code_blocks) / len(code_blocks)
            score += min(3, avg_block_length / 100)
        
        return min(10.0, score)
    
    def _calculate_task_complexity(self, text: str) -> float:
        """Determine task type complexity"""
        text_lower = text.lower()
        
        # High complexity tasks
        if any(word in text_lower for word in ['design', 'architect', 'implement', 'build system']):
            return 9.0
        
        # Analysis tasks
        if any(word in text_lower for word in ['analyze', 'compare', 'evaluate', 'assess']):
            return 7.0
        
        # Creation tasks
        if any(word in text_lower for word in ['create', 'write', 'generate', 'develop']):
            return 6.0
        
        # Explanation tasks
        if any(word in text_lower for word in ['explain', 'describe', 'tell me about']):
            return 4.0
        
        # Simple queries
        if re.match(r'^(what|who|when|where|why|how)\s', text_lower):
            return 2.0
        
        return 5.0  # Default
    
    def _calculate_technical_depth(self, text: str) -> float:
        """Assess technical domain complexity"""
        text_lower = text.lower()
        
        domain_count = sum(1 for domain in self.TECHNICAL_DOMAINS if domain in text_lower)
        
        if domain_count >= 3:
            return 9.0
        elif domain_count == 2:
            return 7.0
        elif domain_count == 1:
            return 5.0
        else:
            return 3.0
    
    def _calculate_structure_score(self, text: str, sentence_count: int) -> float:
        """Analyze query structure complexity"""
        # Multiple sentences = more complex
        if sentence_count > 5:
            return 8.0
        elif sentence_count > 3:
            return 6.0
        elif sentence_count > 1:
            return 4.0
        else:
            return 2.0
    
    def _estimate_tokens_accurate(self, text: str) -> int:
        """
        More accurate token estimation using heuristics
        Based on OpenAI's tokenization patterns
        """
        # Rough approximation: 1 token ≈ 4 characters for English
        # But adjust for special cases
        
        base_estimate = len(text) / 4
        
        # Code uses more tokens (worse compression)
        if '```' in text:
            base_estimate *= 1.3
        
        # Special characters use more tokens
        special_char_count = len(re.findall(r'[^\w\s]', text))
        base_estimate += special_char_count * 0.5
        
        # Numbers and technical terms use more tokens
        number_count = len(re.findall(r'\d+', text))
        base_estimate += number_count * 0.3
        
        return int(base_estimate)
    
    def _classify_task_type(self, text: str) -> str:
        """Classify the type of task being requested"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['write', 'create', 'generate', 'build']):
            return 'generation'
        elif any(word in text_lower for word in ['analyze', 'evaluate', 'compare']):
            return 'analysis'
        elif any(word in text_lower for word in ['explain', 'describe', 'what is']):
            return 'explanation'
        elif any(word in text_lower for word in ['fix', 'debug', 'error', 'problem']):
            return 'debugging'
        elif any(word in text_lower for word in ['optimize', 'improve', 'refactor']):
            return 'optimization'
        else:
            return 'general'
    
    def _recommend_tier(self, complexity: int) -> str:
        """Recommend model tier based on complexity"""
        if complexity <= 3:
            return 'mini'  # GPT-4o-mini
        elif complexity <= 6:
            return 'standard'  # GPT-3.5-turbo
        else:
            return 'premium'  # GPT-4o


# Backwards compatibility - keep old function signature
def analyze_query(text: str) -> Dict:
    """Legacy function for backwards compatibility"""
    analyzer = QueryAnalyzer()
    return analyzer.analyze(text)


def estimate_tokens(text: str) -> int:
    """Legacy function for backwards compatibility"""
    analyzer = QueryAnalyzer()
    return analyzer._estimate_tokens_accurate(text)
