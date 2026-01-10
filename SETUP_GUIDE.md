# 🚀 AI Router - Setup Guide

## Quick Setup (5 Steps)

### Step 1: Download and Extract

1. Download the `ai-router` folder
2. Extract to `D:\A\ai-router`
3. Open folder in VS Code or any editor

### Step 2: Create Virtual Environment

Open terminal in `D:\A\ai-router` and run:

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# You should see (venv) in your prompt
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Uvicorn (server)
- HTTPX (async HTTP client)
- Python-dotenv (environment variables)
- Pydantic (data validation)

### Step 4: Configure API Key

1. Open `.env` file
2. Replace `sk-proj-your-openai-key-here` with your actual OpenAI API key
3. Save the file

```env
OPENAI_API_KEY=sk-proj-YOUR-ACTUAL-KEY-HERE
```

### Step 5: Run the Server

```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Server is running!**

Visit: http://localhost:8000

---

## Test It Works

### Option 1: Run Tests

```bash
python tests\test_basic.py
```

Should see: `🎉 ALL TESTS PASSED!`

### Option 2: Run Examples

In a NEW terminal (keep server running):

```bash
cd D:\A\ai-router
venv\Scripts\activate
python example_usage.py
```

### Option 3: Use in Your Code

Create `test.py`:

```python
import httpx

response = httpx.post(
    "http://localhost:8000/v1/chat/completions",
    json={
        "model": "auto",
        "messages": [
            {"role": "user", "content": "What is Python?"}
        ]
    }
)

result = response.json()
print(result['choices'][0]['message']['content'])
print(f"Model used: {result['x-router-info']['selected_model']}")
print(f"Cost: ${result['x-router-info']['cost_usd']}")
```

Run: `python test.py`

---

## View Statistics

While server is running, visit: http://localhost:8000/stats

Or:

```bash
curl http://localhost:8000/stats
```

---

## Next Steps

### Push to GitHub

```bash
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: AI Router MVP"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR-USERNAME/ai-router.git
git branch -M main
git push -u origin main
```

### Deploy to Railway

1. Go to railway.app
2. Sign in with GitHub
3. New Project → Deploy from GitHub
4. Select your `ai-router` repo
5. Add environment variable: `OPENAI_API_KEY`
6. Deploy!

Your API will be at: `https://ai-router-production.up.railway.app`

---

## Troubleshooting

### "python not recognized"

Try: `py` instead of `python`

### "pip not found"

Try: `python -m pip install -r requirements.txt`

### "Can't activate venv"

Try: `.\venv\Scripts\activate.bat`

### "Port 8000 already in use"

Change port in `.env`:
```env
PORT=8001
```

### "OpenAI API error"

Check your API key in `.env` file is correct and has credits.

---

## File Structure

```
ai-router/
├── main.py              # FastAPI server (main file)
├── analyzer.py          # Query complexity analyzer
├── router.py            # Model selection logic
├── requirements.txt     # Python dependencies
├── .env                 # Your API keys (don't commit!)
├── .gitignore          # Files to ignore in git
├── README.md           # Project documentation
├── example_usage.py    # Example code
└── tests/
    └── test_basic.py   # Unit tests
```

---

## What Each File Does

**main.py** - The FastAPI server that receives requests and routes them

**analyzer.py** - Analyzes queries to determine complexity (1-10 scale)

**router.py** - Decides which AI model to use based on complexity

**requirements.txt** - List of Python packages needed

**.env** - Your API keys and configuration (NEVER commit this!)

**.gitignore** - Tells git which files to ignore (protects your secrets)

---

## Success Checklist

- [ ] Virtual environment activated (see `(venv)` in terminal)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] API key added to `.env` file
- [ ] Server running (`python main.py`)
- [ ] Tests passing (`python tests\test_basic.py`)
- [ ] Can make requests to `http://localhost:8000`

---

**Need help? Check README.md or open an issue on GitHub!**
