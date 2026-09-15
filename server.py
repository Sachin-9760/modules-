from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Annotated

from pydantic import Field
from mcp.server import MCPServer

BASE_DIR = Path(__file__).resolve().parent
TASKS_FILE = BASE_DIR / "data" / "tasks.json"
NOTES_FILE = BASE_DIR / "data" / "project_notes.md"

mcp = MCPServer(
    "Developer Productivity MCP",
    instructions="Use the project tools to manage tasks, search project notes, and perform safe calculations. Read the project resource when you need project context.",
)


def _load_tasks() -> list[dict]:
    if not TASKS_FILE.exists():
        return []
    return json.loads(TASKS_FILE.read_text(encoding="utf-8"))


def _save_tasks(tasks: list[dict]) -> None:
    TASKS_FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


@mcp.tool()
def add_task(
    title: Annotated[str, Field(min_length=1, max_length=120, description="Short task title.")],
    priority: Annotated[str, Field(description="Task priority: low, medium, or high.")] = "medium",
) -> str:
    """Add a development task to the local task list."""
    priority = priority.lower().strip()
    if priority not in {"low", "medium", "high"}:
        return "Invalid priority. Use low, medium, or high."

    tasks = _load_tasks()
    next_id = max((task["id"] for task in tasks), default=0) + 1
    task = {"id": next_id, "title": title.strip(), "priority": priority, "status": "todo"}
    tasks.append(task)
    _save_tasks(tasks)
    return f"Added task #{next_id}: {task['title']} [{priority}]"


@mcp.tool()
def list_tasks(
    status: Annotated[str, Field(description="Filter: all, todo, or done.")] = "all",
) -> list[dict]:
    """List development tasks, optionally filtered by status."""
    status = status.lower().strip()
    if status not in {"all", "todo", "done"}:
        return [{"error": "Invalid status. Use all, todo, or done."}]
    tasks = _load_tasks()
    if status != "all":
        tasks = [task for task in tasks if task["status"] == status]
    return tasks


@mcp.tool()
def complete_task(task_id: Annotated[int, Field(ge=1, description="ID of the task to mark as done.")]) -> str:
    """Mark a development task as completed."""
    tasks = _load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            _save_tasks(tasks)
            return f"Task #{task_id} marked as done."
    return f"Task #{task_id} was not found."


@mcp.tool()
def search_project_notes(
    query: Annotated[str, Field(min_length=1, description="Word or phrase to search for in project notes.")],
) -> list[str]:
    """Search the local project notes and return matching lines with line numbers."""
    needle = query.strip().lower()
    lines = NOTES_FILE.read_text(encoding="utf-8").splitlines()
    matches = [f"{i}: {line}" for i, line in enumerate(lines, 1) if needle in line.lower()]
    return matches[:20]


@mcp.tool()
def ycalculate(expression: Annotated[str, Field(min_length=1, max_length=100, description="Basic arithmetic expression using numbers, +, -, *, /, parentheses, and decimals.")]) -> str:
    """Safely evaluate a basic arithmetic expression without executing arbitrary Python code."""
    expression = expression.strip()
    if not re.fullmatch(r"[0-9+\-*/(). %]+", expression):
        return "Unsupported expression. Use only numbers, +, -, *, /, %, decimal points, and parentheses."
    try:
        result = eval(expression, {"__builtins__": {}}, {})  # noqa: S307 - restricted by strict character allowlist
    except Exception as exc:
        return f"Calculation error: {exc}"
    return str(result)


@mcp.resource("project://overview", mime_type="text/markdown")
def project_overview() -> str:
    """Project overview and guidance for using this MCP server."""
    return NOTES_FILE.read_text(encoding="utf-8")


@mcp.resource("task://{task_id}", mime_type="application/json")
def task_resource(task_id: str) -> dict:
    """Read one task by ID as structured JSON."""
    try:
        wanted = int(task_id)
    except ValueError:
        return {"error": "task_id must be an integer"}
    for task in _load_tasks():
        if task["id"] == wanted:
            return task
    return {"error": f"Task #{wanted} was not found"}


@mcp.prompt()
def code_review(
    code: str,
    focus: str = "correctness, readability, security, and maintainability",
) -> str:
    """Create a focused code-review prompt using the project context."""
    return (
        "You are reviewing code for a small Python MCP project. "
        f"Focus on {focus}. Identify concrete issues, explain why they matter, "
        "and suggest concise fixes.\n\nCODE:\n" + code
    )


if __name__ == "__main__":
    mcp.run()
