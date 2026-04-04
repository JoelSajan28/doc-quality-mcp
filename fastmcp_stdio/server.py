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