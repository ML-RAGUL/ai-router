"""
Example usage of AI Router

This shows how to use the router in your own code.
Make sure the server is running first: python main.py
"""
import httpx
import asyncio


async def test_router():
    """Test the AI Router with example queries"""
    
    base_url = "http://localhost:8000"
    
    # Test queries of different complexity
    test_queries = [
        {
            "name": "Simple Question",
            "query": "What is Python?",
            "expected_model": "gpt-4o-mini"
        },
        {
            "name": "Medium Question",
            "query": "Explain the differences between lists and tuples in Python, including when to use each.",
            "expected_model": "gpt-3.5-turbo"
        },
        {
            "name": "Complex Analysis",
            "query": """
            Analyze the trade-offs between microservices and monolithic architectures.
            Consider scalability, deployment complexity, team organization, and maintenance.
            Provide specific examples and recommendations for different scenarios.
            """,
            "expected_model": "gpt-4o"
        },
        {
            "name": "Code Request",
            "query": """
            Write a Python function that implements binary search with the following requirements:
            - Handle edge cases
            - Include type hints
            - Add docstring
            - Optimize for performance
            """,
            "expected_model": "gpt-4o"
        }
    ]
    
    print("=" * 70)
    print("AI Router - Example Usage")
    print("=" * 70 + "\n")
    
    async with httpx.AsyncClient() as client:
        for i, test in enumerate(test_queries, 1):
            print(f"{i}. Testing: {test['name']}")
            print(f"   Query: {test['query'][:50]}...")
            
            try:
                response = await client.post(
                    f"{base_url}/v1/chat/completions",
                    json={
                        "model": "auto",
                        "messages": [
                            {"role": "user", "content": test["query"]}
                        ],
                        "max_tokens": 100  # Limit for demo
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    router_info = result.get("x-router-info", {})
                    
                    print(f"   ✓ Selected Model: {router_info.get('selected_model')}")
                    print(f"   ✓ Reason: {router_info.get('reason')}")
                    print(f"   ✓ Complexity: {router_info.get('complexity')}/10")
                    print(f"   ✓ Cost: ${router_info.get('cost_usd'):.6f}")
                    print(f"   ✓ Saved: ${router_info.get('saved_usd'):.6f}")
                    print(f"   ✓ Latency: {router_info.get('latency_seconds')}s")
                    
                    # Show first 100 chars of response
                    content = result['choices'][0]['message']['content']
                    print(f"   Response: {content[:100]}...")
                else:
                    print(f"   ✗ Error: {response.status_code}")
                    print(f"   {response.text}")
                
            except Exception as e:
                print(f"   ✗ Error: {e}")
            
            print()
    
    # Get statistics
    print("=" * 70)
    print("Getting Statistics...")
    print("=" * 70 + "\n")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"Total Requests: {stats['total_requests']}")
            print(f"Total Cost: ${stats['total_cost_usd']:.4f}")
            print(f"Total Saved: ${stats['total_saved_usd']:.4f}")
            print(f"Average Complexity: {stats['average_complexity']:.2f}/10")
            print("\nModel Usage:")
            for model, count in stats['model_usage'].items():
                print(f"  - {model}: {count} requests")
        else:
            print(f"Error getting stats: {response.status_code}")


if __name__ == "__main__":
    print("\n🚀 Starting AI Router Examples...\n")
    print("Make sure the server is running: python main.py\n")
    
    try:
        asyncio.run(test_router())
        print("\n✅ Examples completed!\n")
    except KeyboardInterrupt:
        print("\n\n⏸️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
