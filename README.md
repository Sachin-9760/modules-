# Module 14 — MCP Server SDK for Python

A beginner-friendly MCP assignment built with the **official MCP Python SDK v2**.

## What this project demonstrates

- **5 MCP tools:** task creation, task listing, task completion, note search, and safe arithmetic.
- **2 MCP resources:** project overview and a task resource template.
- **1 MCP prompt:** reusable code-review prompt.
- **Host integration:** ready for Claude Desktop, Claude Code, or Cursor through stdio.
- **Tests:** verifies tools, resource access, and prompt registration.

The official SDK currently requires Python 3.10+ and installs with `mcp[cli]`; this project uses `mcp>=2,<3` so it stays on the current v2 major line.

## 1. Windows setup — easiest way

Open **Command Prompt** inside this folder.

### Option A: using uv (recommended)

```cmd
uv venv
.venv\\Scripts\\activate
uv pip install -r requirements.txt
```

Run the server:

```cmd
uv run mcp run server.py
```

For the interactive MCP Inspector:

```cmd
uv run mcp dev server.py
```

The Inspector lets you see the tools, resources, and prompts and call them manually.

### Option B: using normal Python/pip

```cmd
python -m venv .venv
.venv\\Scripts\\activate
python -m pip install -r requirements.txt
```

Run the server directly with:

```cmd
python server.py
```

Or, after installing the CLI extra, use:

```cmd
mcp run server.py
```

## 2. Test the project

After installing dependencies:

```cmd
pytest
```

Expected result: all tests pass.

## 3. Try the tools

In MCP Inspector, try:

### `add_task`

```text
title = Build MCP client demo
priority = high
```

### `list_tasks`

```text
status = all
```

### `complete_task`

```text
task_id = 1
```

### `search_project_notes`

```text
query = Claude
```

### `calculate`

```text
expression = (100 + 50) / 5
```

## 4. Resources

Open:

- `project://overview`
- `task://1`

Resources are data that the host/application can load as context. Tools are actions the model can call.

## 5. Prompt

Open the `code_review` prompt and provide a small Python function. It creates a reusable code-review request.

## 6. Connect to Cursor (coding tool)

The assignment asks for connection to an agent or coding tool. Cursor is included as the coding-tool example.

1. Copy `.cursor/mcp.json.example` to `.cursor/mcp.json`.
2. Replace the example Windows path with the **absolute path** to this project's `server.py`.
3. Open the project in Cursor.
4. Open Cursor's MCP settings and verify that `developer-productivity-mcp` is connected.
5. Ask the coding agent to use the MCP tools, for example:

> Add a high-priority task called "Review authentication code" using the developer-productivity-mcp server.

Cursor should be able to discover and call `add_task`.

## 7. Claude Desktop alternative

The official SDK can register the server automatically. From this project folder, run:

```cmd
uv run mcp install server.py
```

Then completely quit and reopen Claude Desktop.

On Windows, Claude Desktop's MCP configuration is under `%APPDATA%\\Claude\\claude_desktop_config.json`.

## 8. Claude Code alternative

If Claude Code is installed, register the server with:

```cmd
claude mcp add developer-productivity-mcp -- uv run --with "mcp[cli]" mcp run "C:\\ABSOLUTE\\PATH\\TO\\module14_mcp_server\\server.py"
```

Inside Claude Code, use `/mcp` to verify the server and its tools.

## 9. Architecture

```text
                 +-----------------------+
                 | Claude / Cursor /     |
                 | another MCP host      |
                 +-----------+-----------+
                             |
                         MCP / stdio
                             |
                 +-----------v-----------+
                 | Python MCP Server     |
                 | server.py             |
                 +-----------+-----------+
                    /        |         \\
                   /         |          \\
              Tools      Resources     Prompt
                |             |            |
          tasks/notes     project/task   code review
                |
             data/*.json
```

## 10. Key concept

MCP is **not the whole agent application**. The MCP server provides standardized tools, resources, and prompts. A host such as Cursor or Claude Desktop contains the agent/model and uses an MCP client to communicate with this server.

## 11. Assignment checklist

- [x] Understand what MCP standardizes.
- [x] Build a Python MCP server with the official SDK.
- [x] Expose useful tools.
- [x] Expose resources.
- [x] Expose a prompt.
- [x] Include coding-tool integration instructions for Cursor.
- [x] Include Claude Desktop and Claude Code alternatives.
- [x] Include tests.

## Official references

- MCP SDK docs: https://modelcontextprotocol.io/docs/sdk
- Python SDK: https://github.com/modelcontextprotocol/python-sdk
- MCP organization: https://github.com/modelcontextprotocol
- Anthropic MCP introduction: https://www.anthropic.com/news/model-context-protocol
- LangChain MCP docs: https://docs.langchain.com/oss/python/langchain/mcp
- Reference servers: https://github.com/modelcontextprotocol/servers
