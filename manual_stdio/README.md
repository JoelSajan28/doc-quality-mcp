# 📄 Document Quality MCP Server (stdio)

This project is a **minimal MCP (Model Context Protocol) server** that analyzes a document and evaluates its quality based on structure and completeness.

It is built as a **learning-focused MVP** to understand:
- how MCP servers work
- how tools are exposed via JSON-RPC
- how stdio transport behaves
- how structured outputs are returned

---

## 🚀 What this server does

Given a local document (`.md` or `.txt`), it:

- extracts the title  
- analyzes structure (headings, sections)  
- checks completeness (intro, conclusion, etc.)  
- evaluates readability  
- assigns a **score out of 10**  
- returns:
  - strengths
  - weaknesses
  - improvement suggestions

---

## 🏗️ Project Structure

```text
doc-quality-mcp/
├── server.py          # MCP stdio server
├── analyzer.py        # Core document analysis logic
├── docs/
│   └── sample_doc.md  # Sample input document
├── README.md
└── .gitignore
```

---

## ⚙️ How it works

```text
Client
  ↓
MCP JSON-RPC request (stdio)
  ↓
server.py
  ↓
analyzer.py
  ↓
Structured analysis response
```

---

## 🧰 Available Tool

### analyze_document

#### Input

```json
{
  "file_path": "docs/sample_doc.md"
}
```

#### Output

```json
{
  "title": "Model Context Protocol Overview",
  "score": 10.0,
  "rating": "Excellent",
  "metrics": {
    "content_length": 890,
    "heading_count": 6,
    "paragraph_count": 6,
    "long_paragraph_count": 0
  },
  "strengths": [
    "Document has a clear title.",
    "Document has a strong section structure.",
    "Document has a reasonable amount of content.",
    "Document includes an introduction or overview section.",
    "Document includes a conclusion or summary.",
    "Document clearly covers both the problem and the solution.",
    "Paragraphs are reasonably sized and readable."
  ],
  "weaknesses": [],
  "suggestions": []
}
```

---

## ▶️ How to run

### 1. Run the server

```bash
python3 server.py
```

### 2. Send requests manually (stdin)

Paste one JSON request per line.

#### Initialize

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
```

#### List tools

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

#### Call tool

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"analyze_document","arguments":{"file_path":"docs/sample_doc.md"}}}
```

---

## 📊 How scoring works

The document is evaluated based on:

- presence of title  
- number of headings  
- document length  
- introduction presence  
- conclusion presence  
- problem/solution clarity  
- paragraph readability  

The score starts at **10** and is reduced when key structural elements are missing.

---

## ⚠️ Limitations

- only supports local file paths  
- no file upload support  
- no authentication  
- no streaming  
- no LLM integration  
- single tool only  
- expects one JSON request per line in stdio mode  

---

## 🔭 Future Improvements

- [ ] Add multiple tools (summary, title suggestion, etc.)  
- [ ] Support file upload instead of file path  
- [ ] Add SQLite for document tracking  
- [ ] Integrate local LLM (Ollama)  
- [ ] Export blog-ready markdown  
- [ ] GitHub publishing integration  
- [ ] Support HTTP / SSE transports  

---

## 🎯 Purpose of this project

This project was created to:
- test stdio config locally
- understand MCP deeply (not just use it)  
- experiment with different MCP configurations (stdio, HTTP, SSE)  
- build a realistic but simple MCP tool  
- serve as a base for future document-analysis workflows  

---

## 🧪 Status

- ✅ Analyzer logic working  
- ✅ MCP stdio server working  
- 🚧 Expanding tooling and transport  

---

## 👨‍💻 Author

Joel Ukran Sajan