"""
Basic tests for AI Router
Run with: python tests\test_basic.py
"""
import sys
import os

# Add parent directory to path so we can import analyzer and router
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer import analyze_query, estimate_tokens
from router import select_model, calculate_cost


def test_analyzer():
    """Test query analyzer"""
    print("Testing Analyzer...")
    
    # Test simple query
    result = analyze_query("What is Python?")
    print(f"✓ Simple query: complexity={result['complexity']}")
    assert result['complexity'] <= 3, "Simple query should have low complexity"
    
    # Test complex query
    result = analyze_query("""
    Please analyze the differences between functional programming and object-oriented 
    programming, providing detailed examples of when to use each paradigm, and explain
    the trade-offs in terms of performance, maintainability, and scalability.
    """)
    print(f"✓ Complex query: complexity={result['complexity']}")
    assert result['complexity'] >= 5, "Complex query should have higher complexity"
    
    # Test code query
    result = analyze_query("""
    Here's my Python code:
    ```python
    def hello():
        print("Hello World")
    ```
    Can you improve it?
    """)
    print(f"✓ Code query: has_code={result['has_code']}")
    assert result['has_code'], "Should detect code"
    
    print("✅ Analyzer tests passed!\n")


def test_router():
    """Test model router"""
    print("Testing Router...")
    
    # Test simple routing
    analysis = {"complexity": 2, "has_code": False, "word_count": 5}
    selected = select_model(analysis)
    print(f"✓ Simple route: {selected['model']} - {selected['reason']}")
    assert selected['model'] == "gpt-4o-mini", "Simple queries should route to mini"
    
    # Test complex routing
    analysis = {"complexity": 8, "has_code": False, "word_count": 200}
    selected = select_model(analysis)
    print(f"✓ Complex route: {selected['model']} - {selected['reason']}")
    assert selected['model'] == "gpt-4o", "Complex queries should route to premium"
    
    # Test code routing
    analysis = {"complexity": 6, "has_code": True, "word_count": 100}
    selected = select_model(analysis)
    print(f"✓ Code route: {selected['model']} - {selected['reason']}")
    
    print("✅ Router tests passed!\n")


def test_cost_calculation():
    """Test cost calculation"""
    print("Testing Cost Calculation...")
    
    model_info = {
        "model": "gpt-4o-mini",
        "pricing": {"input": 0.150, "output": 0.600}
    }
    
    # 1000 input tokens, 500 output tokens
    cost = calculate_cost(model_info, 1000, 500)
    expected = (1000/1_000_000 * 0.150) + (500/1_000_000 * 0.600)
    
    print(f"✓ Cost for 1000 in + 500 out: ${cost:.6f}")
    assert abs(cost - expected) < 0.000001, "Cost calculation incorrect"
    
    print("✅ Cost calculation tests passed!\n")


def test_end_to_end():
    """Test full pipeline"""
    print("Testing End-to-End Pipeline...")
    
    query = "Write a Python function to calculate fibonacci numbers"
    
    # Analyze
    analysis = analyze_query(query)
    print(f"✓ Query analyzed: complexity={analysis['complexity']}")
    
    # Route
    selected = select_model(analysis)
    print(f"✓ Model selected: {selected['model']}")
    
    # Estimate cost
    estimated_input_tokens = estimate_tokens(query)
    estimated_output_tokens = 200  # Assume response
    cost = calculate_cost(selected, estimated_input_tokens, estimated_output_tokens)
    print(f"✓ Estimated cost: ${cost:.6f}")
    
    print("✅ End-to-end test passed!\n")


if __name__ == "__main__":
    print("=" * 50)
    print("AI Router - Test Suite")
    print("=" * 50 + "\n")
    
    try:
        test_analyzer()
        test_router()
        test_cost_calculation()
        test_end_to_end()
        
        print("=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 50)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
