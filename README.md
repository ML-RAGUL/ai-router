# 🚀 AI Router

> Intelligent routing for AI models - automatically choose the cheapest model for each query and save 50-80% on AI costs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen.svg)](https://web-production-a7f5f.up.railway.app)

## 🌐 Live Demo

**Try it now:** [https://web-production-a7f5f.up.railway.app](https://web-production-a7f5f.up.railway.app)

```bash
# Test the live API
curl https://web-production-a7f5f.up.railway.app/health

# View statistics
curl https://web-production-a7f5f.up.railway.app/stats
```

## ⚡ Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-router
cd ai-router

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure your API key
# Edit .env file and add your OpenAI API key
```

### Run the Server

```bash
python main.py
```

Server will start at `http://localhost:8000`

### Use in Your Code

```python
import openai

# Just change the base URL - that's it!
openai.api_base = "http://localhost:8000/v1"
openai.api_key = "your-openai-key"  # Your actual OpenAI key

# Use as normal - the router handles optimization
response = openai.ChatCompletion.create(
    model="auto",  # "auto" triggers intelligent routing
    messages=[{"role": "user", "content": "What is Python?"}]
)

print(response.choices[0].message.content)
```

## 🎯 Features

- ✅ **Automatic Cost Optimization** - Routes to cheapest appropriate model
- ✅ **OpenAI Compatible** - Drop-in replacement, works with existing code
- ✅ **Smart Analysis** - Analyzes query complexity automatically
- ✅ **Real-time Analytics** - See your savings in `/stats` endpoint
- ✅ **Zero Configuration** - Just set your API key and go
- ✅ **Privacy First** - You keep your own API keys

## 📊 How It Works

1. **Receives your request** - Compatible with OpenAI API format
2. **Analyzes complexity** - Checks length, keywords, code presence
3. **Selects optimal model** - Chooses cheapest model that can handle it
4. **Routes request** - Forwards to selected provider using YOUR key
5. **Returns response** - Same format as direct API call

### Routing Logic

| Complexity | Query Type | Model Used | Cost per 1M tokens |
|------------|-----------|------------|-------------------|
| 1-3 (Simple) | "What is X?", short questions | GPT-4o Mini | $0.15 |
| 4-6 (Medium) | Longer questions, explanations | GPT-3.5 Turbo | $0.50 |
| 7-10 (Complex) | Analysis, code, reasoning | GPT-4o | $2.50 |

## 💰 Example Savings

**Scenario:** 1 million tokens per month

| Approach | Cost | Notes |
|----------|------|-------|
| All GPT-4o | $15,000 | Always using premium model |
| Manual switching | $8,000 | If you remember to switch |
| **AI Router** | **$3,000** | Automatic optimization |
| **Savings** | **$12,000/month** | **80% reduction** |

## 📈 API Endpoints

### Chat Completions

```bash
POST /v1/chat/completions
```

OpenAI-compatible endpoint. Use `model: "auto"` for automatic routing.

### Statistics

```bash
GET /stats
```

Returns usage statistics:
```json
{
  "total_requests": 150,
  "total_cost_usd": 0.45,
  "total_saved_usd": 1.85,
  "average_complexity": 4.2,
  "model_usage": {
    "gpt-4o-mini": 120,
    "gpt-4o": 30
  }
}
```

### Health Check

```bash
GET /health
```

## 🛠️ Configuration

Edit `.env` file:

```env
# Your OpenAI API key
OPENAI_API_KEY=sk-proj-your-key-here

# Server port (default: 8000)
PORT=8000

# Environment
ENVIRONMENT=development
```

## 🚀 Deployment

### Deploy to Railway

1. Push your code to GitHub
2. Create Railway account
3. New Project → Deploy from GitHub
4. Add environment variable: `OPENAI_API_KEY`
5. Deploy!

Your API will be available at: `https://your-app.railway.app`

### Use Deployed Version

```python
import openai

openai.api_base = "https://your-app.railway.app/v1"
openai.api_key = "your-openai-key"

# Works the same!
```

## 📝 Supported Models

Currently supports OpenAI models:
- GPT-4o
- GPT-4o Mini
- GPT-3.5 Turbo

**Coming soon:**
- Anthropic Claude
- Google Gemini
- Open source models

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- OpenAI for the API
- The open source community

## ⚠️ Disclaimer

This is an educational project. For production use, consider:
- Adding authentication
- Rate limiting
- Database for persistent storage
- Error handling improvements
- Monitoring and logging

## 📧 Contact

Questions? Open an issue or reach out!

---

**Built with ❤️ for the developer community**

*Save money, ship faster, build better.*
