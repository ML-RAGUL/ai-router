"""
Router - Selects the optimal AI model based on query analysis
"""
from typing import Dict


# Model pricing (USD per 1M tokens)
MODEL_PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.150, "output": 0.600},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
    "claude-haiku-3-5-20241022": {"input": 0.80, "output": 4.00},
}


def select_model(analysis: Dict) -> Dict:
    """
    Select the optimal model based on query analysis.
    
    Strategy:
    - Complexity 1-3: Use cheapest models (gpt-4o-mini)
    - Complexity 4-6: Use mid-tier models (gpt-3.5-turbo)
    - Complexity 7-10: Use premium models (gpt-4o)
    - Code queries: Prefer models good at code
    
    Args:
        analysis: Query analysis from analyzer.py
        
    Returns:
        Dictionary with selected model info
    """
    complexity = analysis["complexity"]
    has_code = analysis["has_code"]
    
    # Route based on complexity
    if complexity <= 3 and not has_code:
        # Simple queries -> cheapest model
        selected = {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "pricing": MODEL_PRICING["gpt-4o-mini"],
            "reason": "Simple query - using most cost-effective model"
        }
    
    elif complexity <= 6:
        # Medium complexity -> mid-tier
        selected = {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "pricing": MODEL_PRICING["gpt-3.5-turbo"],
            "reason": "Medium complexity - balanced model"
        }
    
    else:
        # Complex queries -> premium model
        selected = {
            "provider": "openai",
            "model": "gpt-4o",
            "pricing": MODEL_PRICING["gpt-4o"],
            "reason": "Complex query - using premium model"
        }
    
    # Override for code
    if has_code and complexity >= 5:
        selected = {
            "provider": "openai",
            "model": "gpt-4o",
            "pricing": MODEL_PRICING["gpt-4o"],
            "reason": "Code-heavy query - using best reasoning model"
        }
    
    return selected


def calculate_cost(model_info: Dict, input_tokens: int, output_tokens: int) -> float:
    """
    Calculate the cost of a request.
    
    Args:
        model_info: Model information from select_model()
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        
    Returns:
        Cost in USD
    """
    pricing = model_info["pricing"]
    
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]
    
    return input_cost + output_cost


def calculate_savings(actual_cost: float, baseline_model: str = "gpt-4o") -> Dict:
    """
    Calculate savings compared to always using baseline model.
    
    Args:
        actual_cost: Actual cost of routed request
        baseline_model: Model to compare against (default: gpt-4o)
        
    Returns:
        Dictionary with savings info
    """
    # This is simplified - in real scenario you'd calculate based on actual tokens
    baseline_pricing = MODEL_PRICING[baseline_model]
    avg_baseline_cost = (baseline_pricing["input"] + baseline_pricing["output"]) / 2
    avg_actual_cost = actual_cost
    
    saved = max(0, avg_baseline_cost - avg_actual_cost)
    percent_saved = (saved / avg_baseline_cost * 100) if avg_baseline_cost > 0 else 0
    
    return {
        "saved_usd": round(saved, 6),
        "percent_saved": round(percent_saved, 2),
        "baseline_model": baseline_model
    }
