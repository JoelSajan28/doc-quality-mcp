# FastMCP Document Quality Server (stdio)

This folder contains a **FastMCP-based stdio MCP server** that exposes a document analysis tool.

The goal of this version is to show how the same MCP server idea can be built using **FastMCP** instead of manually handling JSON-RPC requests.

This version:
- runs over **stdio**
- exposes tools using `@mcp.tool`
- uses the existing `analyzer.py` logic
- can be tested using **MCP Inspector**

---

## What this server does

It exposes a tool that analyzes a local document and returns:

- title
- score
- rating
- strengths
- weaknesses
- suggestions

This is a **rule-based document quality analyzer**, not an LLM-based evaluator.

---

## Project Structure

```text
doc-quality-mcp/
├── fastmcp_stdio/
│   ├── server.py
│   ├── analyzer.py
│   ├── requirements.txt
│   └── docs/
│       └── sample_doc.md
├── manual_stdio/
│   ├── server.py
│   ├── analyzer.py
│   └── docs/
│       └── sample_doc.md
└── README.md
```

---

## Prerequisites

- Python 3.10+
- pip
- Node.js / npm or npx (for MCP Inspector)

---

## Step 1: Go to project root

```bash
cd "<location of project>/doc-quality-mcp"
```

---

## Step 2: (Optional but recommended) create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Step 3: Install dependencies

### Option A: install directly

```bash
pip install fastmcp
```

### Option B: install from requirements file

If `fastmcp_stdio/requirements.txt` contains:

```text
fastmcp
```

then run:

```bash
pip install -r fastmcp_stdio/requirements.txt
```

---

## Step 4: FastMCP server code

Example `fastmcp_stdio/server.py`:

```python
from fastmcp import FastMCP
from analyzer import analyze_document

mcp = FastMCP("Document Quality MCP Server")


@mcp.tool
def analyze_document_tool(file_path: str) -> dict:
    """
    Analyze a markdown or text document and return a quality review.
    """
    return analyze_document(file_path)


@mcp.tool
def suggest_blog_title(file_path: str) -> str:
    """
    Suggest a blog title based on the document content.
    """
    result = analyze_document(file_path)
    title = result.get("title", "Untitled")
    return f"{title}: A Practical Guide"


if __name__ == "__main__":
    mcp.run()
```

---

## Step 5: Analyzer logic

Make sure `fastmcp_stdio/analyzer.py` exists and contains your document analysis logic.

This file is the core business logic. FastMCP only exposes it as a tool.

---

## Step 6: Add a sample document

Create:

```text
fastmcp_stdio/docs/sample_doc.md
```

Example content:

```markdown
# Model Context Protocol Overview

## Introduction
The Model Context Protocol (MCP) is a standardized approach for enabling communication between large language model (LLM) applications and external tools or services. It provides a structured and reliable way to discover, invoke, and manage tools.

## Problem Statement
Modern LLM-based systems often struggle with:
- Fragmented APIs
- Lack of standardization
- Unreliable prompt-based tool usage
- Poor validation of inputs and outputs

## Proposed Solution
MCP introduces a schema-driven approach where:
- Tools are clearly defined with input/output schemas
- Clients can dynamically discover tools
- Servers handle execution and validation

## Architecture
MCP consists of two main components:

### MCP Client
- Handles reasoning and orchestration
- Discovers available tools
- Invokes tools using structured requests

### MCP Server
- Hosts and exposes tools
- Validates inputs
- Executes tool logic
- Returns structured responses

## Example Workflow
1. Client connects to MCP server
2. Client calls `tools/list` to discover tools
3. Client selects appropriate tool
4. Client calls `tools/call` with structured arguments
5. Server executes tool and returns result

## Strengths
- Standardized communication
- Strong validation using schemas
- Clear separation of concerns
- Extensible design

## Weaknesses
- Requires initial setup
- Learning curve for developers
- Dependency on correct schema definitions

## Conclusion
MCP provides a robust framework for integrating LLMs with external systems in a scalable and maintainable way. It significantly improves reliability compared to traditional prompt-based approaches.
```

---

## Step 7: Run the FastMCP server manually

From the project root:

```bash
python3 fastmcp_stdio/server.py
```

Expected result:
- the process starts
- FastMCP shows server startup info
- server runs over **stdio**

Important:
- stdio servers do **not** run on a URL
- stdio servers are launched by a client process

Stop the server with:

```bash
Ctrl + C
```

---

## Step 8: Install MCP Inspector

Run:

```bash
npx @modelcontextprotocol/inspector
```

This opens the MCP Inspector UI in your browser.

---

## Step 9: Configure MCP Inspector for stdio

In MCP Inspector, use:

### Transport Type
```text
STDIO
```

### Command
```text
python3
```

### Arguments
```text
/Users/joelsajan/Desktop/Dev Academy Amplified/Dev Academy Code/doc-quality-mcp/fastmcp_stdio/server.py
```

Important:
- put only `python3` in **Command**
- put the full absolute path to `server.py` in **Arguments**
- do **not** put both in the same field

Authentication:
- leave empty for stdio

Then click:

```text
Connect
```

---

## Step 10: Test in MCP Inspector

### Initialize
Run:

```json
{
  "method": "initialize",
  "params": {}
}
```

### List tools
Run:

```json
{
  "method": "tools/list",
  "params": {}
}
```

Expected tools:
- `analyze_document_tool`
- `suggest_blog_title`

### Call `analyze_document_tool`
Run:

```json
{
  "method": "tools/call",
  "params": {
    "name": "analyze_document_tool",
    "arguments": {
      "file_path": "fastmcp_stdio/docs/sample_doc.md"
    }
  }
}
```

### Call `suggest_blog_title`
Run:

```json
{
  "method": "tools/call",
  "params": {
    "name": "suggest_blog_title",
    "arguments": {
      "file_path": "fastmcp_stdio/docs/sample_doc.md"
    }
  }
}
```

If relative path does not work, use the full absolute path to the sample document.

---

## Expected behavior

### `tools/list`
Should show both tools.

### `analyze_document_tool`
Should return structured analysis with:
- score
- rating
- strengths
- weaknesses
- suggestions

### `suggest_blog_title`
Should return a string such as:

```text
Model Context Protocol Overview: A Practical Guide
```

---

## Common Issues

### 1. `ModuleNotFoundError`
Cause:
- wrong import path
- running from wrong directory
- cross-folder imports not resolving

Fix:
- keep `fastmcp_stdio` self-contained
- use `from analyzer import analyze_document`
- keep `analyzer.py` inside `fastmcp_stdio`

### 2. Inspector connection error
Cause:
- wrong command/arguments split
- wrong path to `server.py`

Fix:
- `Command = python3`
- `Arguments = full absolute path to server.py`

### 3. Tool call fails on file path
Cause:
- wrong relative path

Fix:
- use the full absolute path to `sample_doc.md`

---

## Why this version exists

The project contains two server implementations:

### `manual_stdio`
A manual MCP server built to understand:
- JSON-RPC flow
- `initialize`
- `tools/list`
- `tools/call`
- stdio transport mechanics

### `fastmcp_stdio`
A framework-based MCP server built to understand:
- idiomatic MCP server creation
- automatic tool registration
- schema generation via decorators
- maintainable server design

This side-by-side comparison helps show both:
- how MCP works internally
- how real-world MCP servers are usually built

---

## Current Scope

This version currently supports:
- stdio transport
- local file input
- static analysis
- tool-based interaction

It does not yet include:
- HTTP / SSE transport
- authentication
- database storage
- document upload
- LLM-based semantic review
- GitHub publishing

---

## Future Improvements

- add more tools (`extract_strengths_and_weaknesses`, `export_markdown`, etc.)
- support HTTP transport
- support SSE transport
- integrate SQLite for document tracking
- add optional local LLM support using Ollama
- connect document analysis to blog generation workflow

---

## Summary

This FastMCP version demonstrates how to build a clean stdio-based MCP server for a document analysis workflow.

It is useful for learning:
- MCP server design
- FastMCP tool registration
- client/server interaction over stdio
- testing with MCP Inspector