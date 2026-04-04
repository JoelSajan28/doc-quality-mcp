from __future__ import annotations

import json
import sys
from typing import Any

from manual_stdio.analyzer import analyze_document


TOOL_DEFINITIONS = [
    {
        "name": "analyze_document",
        "description": "Analyze a markdown or text document and return a quality review.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string"
                }
            },
            "required": ["file_path"],
            "additionalProperties": False
        }
    }
]


def send_response(response: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(response) + "\n")
    sys.stdout.flush()


def make_success_response(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result
    }


def make_error_response(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {
            "code": code,
            "message": message
        }
    }


def handle_initialize(request_id: Any) -> dict[str, Any]:
    return make_success_response(
        request_id,
        {
            "protocolVersion": "2025-03-26",
            "capabilities": {
                "tools": {
                    "listChanged": False
                }
            },
            "serverInfo": {
                "name": "doc-quality-stdio-server",
                "version": "1.0.0"
            }
        }
    )


def handle_tools_list(request_id: Any) -> dict[str, Any]:
    return make_success_response(
        request_id,
        {
            "tools": TOOL_DEFINITIONS
        }
    )


def handle_tools_call(request_id: Any, params: dict[str, Any]) -> dict[str, Any]:
    tool_name = params.get("name")
    arguments = params.get("arguments", {})

    if tool_name != "analyze_document":
        return make_error_response(request_id, -32601, f"Unknown tool: {tool_name}")

    file_path = arguments.get("file_path")
    if not file_path or not isinstance(file_path, str):
        return make_error_response(request_id, -32602, "Missing or invalid 'file_path'")

    try:
        analysis = analyze_document(file_path)
    except FileNotFoundError as exc:
        return make_error_response(request_id, -32001, str(exc))
    except Exception as exc:
        return make_error_response(request_id, -32000, f"Tool execution failed: {exc}")

    return make_success_response(
        request_id,
        {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(analysis, indent=2)
                }
            ],
            "structuredContent": analysis
        }
    )


def handle_request(request: dict[str, Any]) -> dict[str, Any]:
    request_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "initialize":
        return handle_initialize(request_id)

    if method == "tools/list":
        return handle_tools_list(request_id)

    if method == "tools/call":
        return handle_tools_call(request_id, params)

    return make_error_response(request_id, -32601, f"Method not found: {method}")


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            send_response(make_error_response(None, -32700, "Invalid JSON"))
            continue

        response = handle_request(request)
        send_response(response)


if __name__ == "__main__":
    main()