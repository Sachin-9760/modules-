import json
import time
import anthropic
from tools.task_tools import get_task, list_tasks
from tools.calculator import calculate

SYSTEM_PROMPT = """
You are a helpful task-management agent.

You can use tools when the user's request requires task data or arithmetic.
Available tools:
- get_task: retrieve one task by ID
- list_tasks: list available tasks
- calculate: perform basic arithmetic

Rules:
1. Decide whether a tool is actually needed.
2. Use the minimum number of tools needed.
3. After a tool result, continue and answer the user.
4. Never invent task information.
5. Keep the final answer concise and clear.
"""

class TaskAgent:
    def __init__(self, api_key: str, model: str):
        self.client = anthropic.AsyncAnthropic(
            api_key=api_key, timeout=60.0, max_retries=2
        )
        self.model = model
        self.tool_functions = {
            "get_task": get_task,
            "list_tasks": list_tasks,
            "calculate": calculate,
        }
        self.tools = [
            {
                "name": "get_task",
                "description": "Get a task by its numeric ID.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "integer", "description": "The task ID."}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "list_tasks",
                "description": "List all available tasks.",
                "input_schema": {
                    "type": "object", "properties": {}, "required": []
                }
            },
            {
                "name": "calculate",
                "description": "Calculate a basic arithmetic expression such as 10 + 5 or 20 * 3.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "expression": {"type": "string", "description": "A basic arithmetic expression."}
                    },
                    "required": ["expression"]
                }
            }
        ]

    async def run(self, user_prompt: str):
        start = time.perf_counter()
        messages = [{"role": "user", "content": user_prompt}]
        tool_calls = []

        for _ in range(5):
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=800,
                system=SYSTEM_PROMPT,
                tools=self.tools,
                messages=messages,
            )

            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                final_text = "".join(
                    block.text for block in response.content
                    if block.type == "text"
                )
                latency_ms = round((time.perf_counter() - start) * 1000, 2)
                usage = {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                }
                return {
                    "model": self.model,
                    "response": final_text,
                    "tool_calls": tool_calls,
                    "latency_ms": latency_ms,
                    "usage": usage,
                }

            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue

                tool_name = block.name
                tool_input = block.input
                tool_calls.append({"tool": tool_name, "input": tool_input})

                function = self.tool_functions.get(tool_name)
                if not function:
                    result = {"error": f"Unknown tool: {tool_name}"}
                else:
                    try:
                        result = function(**tool_input)
                    except Exception as exc:
                        result = {"error": str(exc)}

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result)
                })

            messages.append({"role": "user", "content": tool_results})

        raise RuntimeError("Agent reached the maximum number of tool-use steps.")
