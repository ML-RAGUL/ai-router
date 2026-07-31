# AI Router

Intelligent query routing system for AI language models with automatic cost optimization.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## Overview

AI Router analyzes incoming queries and routes them to the most cost-effective AI model capable of handling the request. By intelligently selecting between GPT-4o, GPT-3.5-turbo, and GPT-4o-mini based on query complexity, the system is designed to cut API costs while maintaining response quality.

Live instance: https://web-production-a7f5f.up.railway.app

> **Status note:** The routing/complexity-analysis pipeline is fully deployed and live. Live OpenAI completions currently require an active API key with credits on the hosted instance — the routing logic itself runs regardless of key status.

## Key Features

- OpenAI-compatible REST API interface
- Multi-dimensional query complexity analysis
- Automatic model selection based on query characteristics
- Real-time cost tracking and analytics
- Zero-configuration deployment with Railway
- Docker containerization for consistent environments
- Automated CI/CD pipeline with GitHub Actions

## Architecture

The system implements a three-stage processing pipeline:

1. **Query Analysis**: Evaluates incoming requests across six dimensions including vocabulary sophistication, code presence, technical depth, and structural complexity
2. **Model Selection**: Routes queries to appropriate models using a weighted scoring algorithm
3. **Request Forwarding**: Proxies requests to OpenAI API using user-provided credentials

## Installation

### Local Development

```bash
git clone https://github.com/ML-RAGUL/ai-router.git
cd ai-router

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Docker Deployment

```bash
docker build -t ai-router .
docker run -p 8000:8000 -e OPENAI_API_KEY=your-key ai-router
```

### Docker Compose (with PostgreSQL)

```bash
docker-compose up
```

## Usage

The API exposes OpenAI-compatible endpoints. Replace your OpenAI base URL to start using the router:

```python
import openai

client = openai.OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="your-openai-key"
)

response = client.chat.completions.create(
    model="auto",
    messages=[{"role": "user", "content": "Explain Docker containers"}]
)
```

## Routing Logic

Query complexity scores (1-10 scale) determine model selection:

| Complexity Range | Target Model | Use Case | Cost per 1M tokens |
|-----------------|--------------|----------|-------------------|
| 1-3 | GPT-4o-mini | Simple questions, definitions | $0.15 |
| 4-6 | GPT-3.5-turbo | Explanations, medium tasks | $0.50 |
| 7-10 | GPT-4o | Complex analysis, code generation | $2.50 |

Complexity scoring considers:
- Token count and vocabulary diversity
- Presence and complexity of code blocks
- Technical domain indicators
- Task type classification
- Query structure patterns

## API Endpoints

### POST /v1/chat/completions

Standard OpenAI chat completion endpoint with automatic routing.

**Request:**
```json
{
  "model": "auto",
  "messages": [{"role": "user", "content": "your query"}]
}
```

**Response includes routing metadata:**
```json
{
  "choices": [...],
  "x-router-info": {
    "selected_model": "gpt-4o-mini",
    "complexity": 3,
    "cost_usd": 0.000045,
    "saved_usd": 0.000105
  }
}
```

### GET /stats

Returns aggregated usage statistics and model distribution.

### GET /health

Health check endpoint for monitoring and load balancers.

## Cost Analysis

**Projected** savings based on OpenAI's published per-token pricing across complexity tiers — this is a calculated estimate, not measured production traffic (this is a personal/portfolio project, not a deployed production system with real user load):

| Scenario | Monthly Cost (1M tokens, illustrative) | Savings |
|----------|--------------|---------|
| All requests to GPT-4o | $15,000 | Baseline |
| Manual model selection | $8,000 | 47% |
| Automated routing (this system) | $3,000 | 80% |

Actual savings depend on real query distribution and complexity patterns, and would need to be validated against live traffic to confirm.

## Deployment

### Railway

Automatic deployment configured via `railway.json`. Push to main branch triggers rebuild and deployment.

### AWS ECS

Dockerfile supports deployment to AWS Elastic Container Service:

```bash
# Build and tag
docker build -t ai-router .
docker tag ai-router:latest {account}.dkr.ecr.{region}.amazonaws.com/ai-router:latest

# Push to ECR
docker push {account}.dkr.ecr.{region}.amazonaws.com/ai-router:latest

# Deploy to ECS (requires task definition and service configuration)
```

## Development

### Running Tests

```bash
python tests/test_basic.py
```

### CI/CD Pipeline

GitHub Actions workflow runs on every push to main:
- Executes test suite
- Builds Docker image
- Validates container health
- Triggers deployment

## Configuration

Environment variables:

```env
OPENAI_API_KEY=sk-proj-...     # Required: Your OpenAI API key
PORT=8000                       # Optional: Server port (default: 8000)
ENVIRONMENT=production          # Optional: Environment name
LOG_LEVEL=INFO                  # Optional: Logging verbosity
```

## Technical Stack

- **Framework**: FastAPI 0.115+ with async request handling
- **HTTP Client**: HTTPX for async API calls
- **Validation**: Pydantic v2 for request/response schemas
- **Server**: Uvicorn with automatic reloading
- **Containerization**: Docker with multi-stage builds
- **CI/CD**: GitHub Actions for automated testing and deployment

## Project Structure

```
ai-router/
├── main.py              # FastAPI application and routing logic
├── analyzer.py          # Query complexity analysis engine
├── router.py            # Model selection algorithm
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container image definition
├── docker-compose.yml  # Local development environment
└── tests/              # Test suite
```

## Limitations

- Currently supports OpenAI models only
- In-memory request logging (consider database for production)
- No built-in authentication (add reverse proxy or API gateway)
- Rate limiting not implemented (use infrastructure-level controls)
- Cost figures above are projections based on published pricing, not measured production data

## Roadmap

- Support for Anthropic Claude models
- PostgreSQL integration for persistent storage
- Prometheus metrics export
- WebSocket support for streaming responses
- Multi-provider load balancing

## Contributing

Contributions are welcome. Please open an issue to discuss proposed changes before submitting pull requests.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Built with FastAPI framework. Deployed on Railway infrastructure.
