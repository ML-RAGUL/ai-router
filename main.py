"""
AI Router - FastAPI server for intelligent AI model routing
"""
import os
import time
from datetime import datetime
from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import httpx
from dotenv import load_dotenv
from pydantic import BaseModel

from analyzer import analyze_query, estimate_tokens
from router import select_model, calculate_cost, calculate_savings

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(
    title="AI Router",
    description="Intelligent routing for AI models - automatically choose the cheapest model for each query",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory storage for MVP (replace with DB later)
request_log = []


class ChatRequest(BaseModel):
    """OpenAI-compatible chat completion request"""
    model: str = "auto"  # "auto" triggers our routing
    messages: list
    temperature: Optional[float] = 1.0
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "AI Router",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/v1/chat/completions",
            "stats": "/stats",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/stats")
async def get_stats():
    """Get routing statistics"""
    if not request_log:
        return {
            "total_requests": 0,
            "total_cost": 0,
            "total_saved": 0,
            "average_complexity": 0
        }
    
    total_requests = len(request_log)
    total_cost = sum(log.get("cost", 0) for log in request_log)
    total_saved = sum(log.get("savings", {}).get("saved_usd", 0) for log in request_log)
    avg_complexity = sum(log.get("analysis", {}).get("complexity", 0) for log in request_log) / total_requests
    
    # Model usage breakdown
    model_usage = {}
    for log in request_log:
        model = log.get("selected_model", {}).get("model", "unknown")
        model_usage[model] = model_usage.get(model, 0) + 1
    
    return {
        "total_requests": total_requests,
        "total_cost_usd": round(total_cost, 4),
        "total_saved_usd": round(total_saved, 4),
        "average_complexity": round(avg_complexity, 2),
        "model_usage": model_usage,
        "recent_requests": request_log[-10:]  # Last 10 requests
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    """
    OpenAI-compatible chat completions endpoint with intelligent routing
    """
    start_time = time.time()
    
    try:
        # Extract the user's query
        if not request.messages:
            raise HTTPException(status_code=400, detail="Messages cannot be empty")
        
        last_message = request.messages[-1]
        user_query = last_message.get("content", "")
        
        # Analyze the query
        analysis = analyze_query(user_query)
        
        # Select optimal model (unless user specified a specific model)
        if request.model == "auto" or request.model.startswith("auto"):
            selected = select_model(analysis)
        else:
            # User specified a model, use it directly
            selected = {
                "provider": "openai",
                "model": request.model,
                "pricing": {"input": 0, "output": 0},
                "reason": "User-specified model"
            }
        
        # Get API key from environment
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key or openai_key == "sk-proj-your-openai-key-here":
            raise HTTPException(
                status_code=500, 
                detail="OpenAI API key not configured. Please set OPENAI_API_KEY in .env file"
            )
        
        # Forward request to OpenAI
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openai_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": selected["model"],
                    "messages": request.messages,
                    "temperature": request.temperature,
                    "max_tokens": request.max_tokens,
                    "stream": request.stream
                }
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"OpenAI API error: {response.text}"
            )
        
        result = response.json()
        
        # Calculate costs
        usage = result.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        cost = calculate_cost(selected, input_tokens, output_tokens)
        savings = calculate_savings(cost)
        
        # Log the request
        latency = time.time() - start_time
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "selected_model": selected,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
            "savings": savings,
            "latency_seconds": round(latency, 3)
        }
        request_log.append(log_entry)
        
        # Add custom headers with routing info
        result["x-router-info"] = {
            "selected_model": selected["model"],
            "reason": selected["reason"],
            "complexity": analysis["complexity"],
            "cost_usd": round(cost, 6),
            "saved_usd": round(savings["saved_usd"], 6),
            "latency_seconds": round(latency, 3)
        }
        
        return result
        
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request to AI provider timed out")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"Error communicating with AI provider: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/models")
async def list_models():
    """List available models"""
    return {
        "object": "list",
        "data": [
            {
                "id": "auto",
                "object": "model",
                "created": 1234567890,
                "owned_by": "ai-router",
                "description": "Automatically select the best model based on query complexity"
            },
            {
                "id": "gpt-4o-mini",
                "object": "model",
                "created": 1234567890,
                "owned_by": "openai"
            },
            {
                "id": "gpt-4o",
                "object": "model",
                "created": 1234567890,
                "owned_by": "openai"
            },
            {
                "id": "gpt-3.5-turbo",
                "object": "model",
                "created": 1234567890,
                "owned_by": "openai"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
