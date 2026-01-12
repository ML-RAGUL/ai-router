"""
Test comparing old analyzer vs improved analyzer
"""
import sys
import os

# Add parent directory to path so we can import analyzer modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import both versions
from analyzer import analyze_query as old_analyze
from analyzer_improved import analyze_query as new_analyze


def compare_analyzers():
    """Compare old vs new analyzer on various queries"""
    
    test_queries = [
        {
            "name": "Simple Question",
            "query": "What is Python?"
        },
        {
            "name": "Medium Explanation",
            "query": "Explain how microservices architecture works and when to use it."
        },
        {
            "name": "Complex Code Task",
            "query": """
            Write a Python function that implements a distributed cache with the following features:
            - Thread-safe operations
            - LRU eviction policy
            - Async support
            - Redis backend
            Include error handling and comprehensive tests.
            """
        },
        {
            "name": "Technical Analysis",
            "query": "Analyze the trade-offs between Kubernetes and Docker Swarm for container orchestration in a microservices architecture."
        },
        {
            "name": "Edge Case - Very Short",
            "query": "Hi"
        },
        {
            "name": "Edge Case - Code Heavy",
            "query": """
            ```python
            def fibonacci(n):
                if n <= 1:
                    return n
                return fibonacci(n-1) + fibonacci(n-2)
            ```
            Optimize this code for better performance.
            """
        }
    ]
    
    print("=" * 80)
    print("ANALYZER COMPARISON: OLD vs NEW")
    print("=" * 80)
    
    for test in test_queries:
        print(f"\n📝 Test: {test['name']}")
        print(f"Query: {test['query'][:60]}...")
        print("-" * 80)
        
        # Old analyzer
        old_result = old_analyze(test['query'])
        print(f"\n🔴 OLD ANALYZER:")
        print(f"   Complexity: {old_result['complexity']}/10")
        print(f"   Word count: {old_result['word_count']}")
        print(f"   Has code: {old_result['has_code']}")
        print(f"   Simple question: {old_result['is_simple_question']}")
        
        # New analyzer
        new_result = new_analyze(test['query'])
        print(f"\n🟢 NEW ANALYZER:")
        print(f"   Complexity: {new_result['complexity']}/10")
        print(f"   Word count: {new_result['word_count']}")
        print(f"   Task type: {new_result['task_type']}")
        print(f"   Recommended tier: {new_result['recommended_model_tier']}")
        print(f"   Score breakdown:")
        for score_name, score_value in new_result['scores'].items():
            print(f"      - {score_name}: {score_value:.1f}/10")
        
        # Comparison
        complexity_diff = new_result['complexity'] - old_result['complexity']
        print(f"\n💡 DIFFERENCE: {complexity_diff:+d} points")
        
        if abs(complexity_diff) >= 2:
            if complexity_diff > 0:
                print(f"   ⚠️  Old analyzer UNDERESTIMATED complexity")
            else:
                print(f"   ⚠️  Old analyzer OVERESTIMATED complexity")
        else:
            print(f"   ✅ Both analyzers agree")
        
        print("\n" + "=" * 80)


if __name__ == "__main__":
    compare_analyzers()
