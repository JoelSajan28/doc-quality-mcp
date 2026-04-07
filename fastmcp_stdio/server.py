from fastmcp import FastMCP
from analyzer import analyze_document, read_document
from db import init_db, save_analysis
import requests

mcp = FastMCP("Document Quality MCP Server")

init_db()

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"


def call_ollama(prompt: str, model: str = OLLAMA_MODEL) -> str:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("response", "").strip()


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


@mcp.tool
def generate_blog_intro(file_path: str) -> str:
    """
    Generate a blog-style introduction for the given document using a local Ollama model.
    """
    analysis = analyze_document(file_path)
    document_text = read_document(file_path)

    title = analysis.get("title", "Untitled")
    strengths = analysis.get("strengths", [])
    weaknesses = analysis.get("weaknesses", [])

    prompt = f"""
                You are helping turn a technical document into a blog post.

                Document title:
                {title}

                Document strengths:
                {chr(10).join(f"- {item}" for item in strengths)}

                Document weaknesses:
                {chr(10).join(f"- {item}" for item in weaknesses)}

                Document content:
                \"\"\"
                {document_text}
                \"\"\"

                Write a short blog introduction of 2 short paragraphs.
                Requirements:
                - Make it engaging but clear
                - Keep it concise
                - Do not use bullet points
                - Do not mention that this was generated
                - Focus on why the topic matters and what the reader will learn
                """

    try:
        return call_ollama(prompt)
    except requests.RequestException as exc:
        return f"Ollama call failed: {exc}"


@mcp.tool
def save_document_analysis(file_path: str) -> dict:
    """
    Analyze a document and save the analysis result into a local SQLite database.
    """
    analysis = analyze_document(file_path)
    saved_record = save_analysis(file_path, analysis)
    return {
        "message": "Document analysis saved successfully.",
        "saved_record": saved_record,
    }


if __name__ == "__main__":
    mcp.run()