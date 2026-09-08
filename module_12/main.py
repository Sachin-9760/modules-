import asyncio
import os
from pathlib import Path
import shutil
import sys

from deepagents import create_deep_agent
from deepagents.backends.filesystem import FilesystemBackend
from langchain.agents.middleware import TodoListMiddleware


PROJECT_ROOT = Path(__file__).resolve().parent
WORKSPACE_DIR = PROJECT_ROOT / "workspace"
PROJECT_SKILLS_DIR = PROJECT_ROOT / "skills"
WORKSPACE_SKILLS_DIR = WORKSPACE_DIR / "skills"


async def run_research_pipeline():
    # Ensure workspace exists locally
    WORKSPACE_DIR.mkdir(exist_ok=True)
    shutil.copytree(PROJECT_SKILLS_DIR, WORKSPACE_SKILLS_DIR, dirs_exist_ok=True)
    
    # Establish context engineering over the directory boundaries
    backend = FilesystemBackend(root_dir=str(WORKSPACE_DIR), virtual_mode=True)
    
    # Seed a dummy file to read if none exists
    source_material = WORKSPACE_DIR / "source_material.txt"
    if not source_material.exists():
        source_material.write_text(
            "Deep Agents harness execution details: Planning, context boundaries, and isolation patterns.",
            encoding="utf-8",
        )

    print("Initializing Deep Agent Harness...")
    
    # Builds an execution harness combining declarative planning and progressive disclosure
    agent = create_deep_agent(
        model="anthropic:claude-sonnet-4-6",
        backend=backend,
        skills=["/skills"],
        middleware=[TodoListMiddleware()] # Activates the explicit 'write_todos' tool surface
    )
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Configure it before running a research request."
        )

    prompt = " ".join(sys.argv[1:]).strip()
    if not prompt:
        prompt = "Read the available source material and summarize its key points."

    print(f"Research request: {prompt}")
    result = await agent.ainvoke({"messages": [{"role": "user", "content": prompt}]})
    print("\nResearch result:\n")
    print(result["messages"][-1].content)

if __name__ == "__main__":
    try:
        asyncio.run(run_research_pipeline())
    except RuntimeError as error:
        print(f"Error: {error}")
        raise SystemExit(1)
