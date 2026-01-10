"""
Mock Demo - Shows how AI Router works without using OpenAI credits
"""

from analyzer import analyze_query, estimate_tokens
from router import select_model, calculate_cost, calculate_savings


def mock_ai_response(query: str) -> str:
    """Generate a mock AI response"""
    if "what is" in query.lower():
        return "Python is a high-level programming language known for simplicity and readability."
    elif "explain" in query.lower():
        return "Lists are mutable and use [], tuples are immutable and use (). Lists for changing data, tuples for fixed data."
    elif "analyze" in query.lower():
        return "Microservices offer scalability and flexibility but add complexity. Monoliths are simpler initially but harder to scale."
    else:
        return "Here's a Python function with type hints and documentation as requested."


def run_mock_demo():
    print("\n" + "=" * 70)
    print("🎭 AI ROUTER - MOCK DEMO")
    print("=" * 70)
    
    test_queries = [
        {"name": "Simple", "query": "What is Python?"},
        {"name": "Medium", "query": "Explain lists vs tuples in Python"},
        {"name": "Complex", "query": "Analyze microservices vs monolithic architectures with examples"},
        {"name": "Code", "query": "Write a Python binary search function with type hints"}
    ]
    
    total_cost = 0
    total_saved = 0
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n{i}. {test['name']} Query")
        print("-" * 70)
        print(f"Query: {test['query'][:60]}...")
        
        # Analyze
        analysis = analyze_query(test['query'])
        print(f"\n📊 Analysis: Complexity {analysis['complexity']}/10")
        
        # Route
        selected = select_model(analysis)
        print(f"🎯 Selected: {selected['model']}")
        print(f"💡 Reason: {selected['reason']}")
        
        # Mock response
        response = mock_ai_response(test['query'])
        
        # Calculate cost
        input_tokens = estimate_tokens(test['query'])
        output_tokens = estimate_tokens(response)
        cost = calculate_cost(selected, input_tokens, output_tokens)
        savings = calculate_savings(cost)
        
        total_cost += cost
        total_saved += savings['saved_usd']
        
        print(f"💰 Cost: ${cost:.6f} | Saved: ${savings['saved_usd']:.6f} ({savings['percent_saved']:.0f}%)")
        print(f"💬 Response: {response[:100]}...")
    
    # Summary
    print("\n" + "=" * 70)
    print("📈 SUMMARY")
    print("=" * 70)
    print(f"Total Requests: {len(test_queries)}")
    print(f"Total Cost: ${total_cost:.6f}")
    print(f"Total Saved: ${total_saved:.6f}")
    print(f"Savings Rate: {(total_saved / (total_cost + total_saved) * 100):.0f}%")
    print("\n✅ Your AI Router works perfectly!")
    print("💳 Add OpenAI credits to test with real responses\n")


if __name__ == "__main__":
    run_mock_demo()
