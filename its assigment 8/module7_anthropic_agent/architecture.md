# Module 7 Architecture Note

| Architecture | Use when | Example | Complexity |
|---|---|---|---|
| Simple Pipeline | Steps are fixed and predictable | Resume -> Extract -> Validate -> Save | Low |
| Tool-Using Agent | Model must dynamically select actions/tools | Find task -> check data -> summarize | Medium |
| Multi-Agent | Multiple specialized/independent agents have clear value | Researcher + Analyst + Reviewer | High |

## Project choice

This project uses a single Claude tool-using agent.

Claude receives tool definitions and decides whether to call:
- get_task
- list_tasks
- calculate

Python executes the selected tool and sends its result back to Claude.

## Agent loop

1. Receive request.
2. Send request and tools to Claude.
3. Claude returns a final answer OR requests a tool.
4. Execute the tool.
5. Return tool result to Claude.
6. Repeat until a final answer is produced.
7. Stop after a bounded number of iterations.

## Why not multi-agent?

The task does not require independent specialist agents. A multi-agent design would add coordination, latency, cost, and debugging overhead without a clear benefit.
