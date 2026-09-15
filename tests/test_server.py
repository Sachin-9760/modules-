import pytest
from mcp import Client

from server import mcp


@pytest.mark.anyio
async def test_tools_and_resource() -> None:
    async with Client(mcp) as client:
        tools = await client.list_tools()
        names = {tool.name for tool in tools.tools}
        assert {"add_task", "list_tasks", "complete_task", "search_project_notes", "calculate"} <= names

        result = await client.call_tool("calculate", {"expression": "(10 + 5) * 2"})
        assert result.structured_content == {"result": "30"}

        resource = await client.read_resource("project://overview")
        assert "Developer Productivity MCP" in resource.contents[0].text


@pytest.mark.anyio
async def test_prompt_exists() -> None:
    async with Client(mcp) as client:
        prompts = await client.list_prompts()
        assert any(prompt.name == "code_review" for prompt in prompts.prompts)
