from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def read_document(file_path: str) -> str:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {file_path}")
    return path.read_text(encoding="utf-8")


def extract_title(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return "Untitled Document"


def extract_headings(text: str) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = re.sub(r"^#+\s*", "", stripped).strip()
            if heading:
                headings.append(heading)
    return headings


def extract_paragraphs(text: str) -> list[str]:
    chunks = re.split(r"\n\s*\n", text.strip())
    paragraphs = [chunk.strip() for chunk in chunks if chunk.strip()]
    return paragraphs


def count_long_paragraphs(paragraphs: list[str], threshold: int = 500) -> int:
    return sum(1 for para in paragraphs if len(para) > threshold)


def detect_section_keywords(headings: list[str]) -> dict[str, bool]:
    joined = " | ".join(h.lower() for h in headings)
    return {
        "has_intro": any(word in joined for word in ["introduction", "overview", "purpose"]),
        "has_conclusion": any(word in joined for word in ["conclusion", "summary", "closing"]),
        "has_problem": any(word in joined for word in ["problem", "challenge"]),
        "has_solution": any(word in joined for word in ["solution", "approach"]),
    }


def analyze_document(file_path: str) -> dict[str, Any]:
    text = read_document(file_path)
    title = extract_title(text)
    headings = extract_headings(text)
    paragraphs = extract_paragraphs(text)
    keyword_flags = detect_section_keywords(headings)

    content_length = len(text)
    heading_count = len(headings)
    paragraph_count = len(paragraphs)
    long_paragraph_count = count_long_paragraphs(paragraphs)

    score = 10.0
    strengths: list[str] = []
    weaknesses: list[str] = []
    suggestions: list[str] = []

    # Title
    if title != "Untitled Document":
        strengths.append("Document has a clear title.")
    else:
        score -= 2
        weaknesses.append("Document does not have a clear title.")
        suggestions.append("Add a top-level title to establish the document purpose.")

    # Structure
    if heading_count >= 4:
        strengths.append("Document has a strong section structure.")
    elif heading_count >= 2:
        strengths.append("Document has some section structure.")
    else:
        score -= 2
        weaknesses.append("Document has limited section structure.")
        suggestions.append("Break the document into clearer sections with headings.")

    # Length / completeness
    if content_length >= 500:
        strengths.append("Document has a reasonable amount of content.")
    else:
        score -= 2
        weaknesses.append("Document is too short to feel complete.")
        suggestions.append("Expand the document with more detail, examples, or explanation.")

    # Intro / conclusion
    if keyword_flags["has_intro"]:
        strengths.append("Document includes an introduction or overview section.")
    else:
        score -= 1
        weaknesses.append("Document does not clearly introduce the topic.")
        suggestions.append("Add an introduction to explain the purpose and scope.")

    if keyword_flags["has_conclusion"]:
        strengths.append("Document includes a conclusion or summary.")
    else:
        score -= 2
        weaknesses.append("Document does not include a conclusion.")
        suggestions.append("Add a conclusion to summarize the main takeaways.")

    # Problem/solution clarity
    if keyword_flags["has_problem"] and keyword_flags["has_solution"]:
        strengths.append("Document clearly covers both the problem and the solution.")
    elif keyword_flags["has_problem"] or keyword_flags["has_solution"]:
        strengths.append("Document partially explains the problem/solution flow.")
    else:
        score -= 1
        weaknesses.append("Document does not clearly frame a problem and solution.")
        suggestions.append("Add sections that explain the challenge and the proposed solution.")

    # Paragraph readability
    if long_paragraph_count == 0:
        strengths.append("Paragraphs are reasonably sized and readable.")
    else:
        score -= 1
        weaknesses.append(f"Document has {long_paragraph_count} overly long paragraph(s).")
        suggestions.append("Break long paragraphs into smaller, easier-to-read sections.")

    # Clean up score bounds
    score = max(0.0, min(10.0, round(score, 1)))

    overall_rating = (
        "Excellent" if score >= 9 else
        "Good" if score >= 7 else
        "Average" if score >= 5 else
        "Weak"
    )

    return {
        "title": title,
        "score": score,
        "rating": overall_rating,
        "metrics": {
            "content_length": content_length,
            "heading_count": heading_count,
            "paragraph_count": paragraph_count,
            "long_paragraph_count": long_paragraph_count,
        },
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
    }


if __name__ == "__main__":
    sample_path = "docs/sample_doc.md"
    result = analyze_document(sample_path)

    import json
    print(json.dumps(result, indent=2))