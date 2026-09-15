# Module 7 - Introduction to Agents Using Anthropic

A simple Claude tool-using agent with FastAPI.

## Architecture

User -> FastAPI -> Claude Agent -> decide -> Tool (if needed) -> tool result -> Claude -> final answer

Tools:
- get_task
- list_tasks
- calculate

## Setup on Windows / VS Code

1. Open this folder in VS Code.
2. Create environment:
   python -m venv venv
3. Activate:
   venv\Scripts\activate
4. Install:
   pip install -r requirements.txt
5. Copy `.env.example` to `.env`.
6. Add your Anthropic API key:
   ANTHROPIC_API_KEY=your_key_here
7. Run:
   python -m uvicorn main:app --reload
8. Open:
   http://127.0.0.1:8000/docs

## Test

POST /agent/run

Simple:
{
  "prompt": "What is an AI agent in one sentence?"
}

Tool use:
{
  "prompt": "What is the status of task 2?"
}

List tasks:
{
  "prompt": "Show me all tasks and identify the high priority ones."
}

Calculation:
{
  "prompt": "Calculate 25 * 4 + 10."
}

## Module 7 concepts

- Agent vs single prompt
- Tool use / function calling
- Agent decision loop
- Context passed between turns
- Bounded tool-use steps
- Timeout and retry configuration
- Token tracking
- FastAPI integration
- Structured JSON response

## Architecture decision

Use a simple pipeline when steps are fixed and predictable.

Use a tool-using agent when the system must dynamically decide which action/tool to take.

Use multiple agents only when specialization or parallel independent work clearly justifies extra cost, latency, and coordination complexity.

The demo intentionally uses one Claude agent instead of a multi-agent system.

Never commit `.env` or API keys to GitHub.
