# Module 6 - Provider-Agnostic AI API

This mini project demonstrates a common Python layer that can call:

- OpenAI
- Claude
- Ollama

The FastAPI application exposes one common endpoint:

POST /ai/generate

## Architecture

FastAPI -> AIService -> Provider -> Normalized JSON response

## 1. Create virtual environment

Windows:

    python -m venv venv
    venv\Scripts\activate

## 2. Install dependencies

    pip install -r requirements.txt

## 3. Configure environment

Copy `.env.example` to `.env`.

For OpenAI, add:

    OPENAI_API_KEY=your_key

For Claude, add:

    ANTHROPIC_API_KEY=your_key

Ollama does not need an API key. It requires Ollama running locally.

## 4. Run

    uvicorn main:app --reload

Open:

    http://127.0.0.1:8000/docs

## 5. Test

OpenAI:

    POST /ai/generate

    {
      "provider": "openai",
      "prompt": "Explain PostgreSQL in simple words."
    }

Claude:

    {
      "provider": "claude",
      "prompt": "Explain FastAPI in simple words."
    }

Ollama:

    {
      "provider": "ollama",
      "prompt": "Explain Redis in simple words."
    }

## Assignment requirements covered

- Authentication through environment variables
- Request shaping
- Provider abstraction
- Timeout handling
- SDK retry support
- Response normalization
- Usage/token information where available
- Latency measurement
- Provider switching without changing application logic

## Important

Do not commit `.env` or API keys to GitHub.

If Ollama is not supported on your computer, test OpenAI or Claude and keep the Ollama provider code for the assignment.
