import json
import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).parent / "document_analysis.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS document_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            title TEXT NOT NULL,
            score REAL NOT NULL,
            rating TEXT NOT NULL,
            strengths_json TEXT NOT NULL,
            weaknesses_json TEXT NOT NULL,
            suggestions_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    conn.commit()
    conn.close()


def save_analysis(file_path: str, analysis: dict[str, Any]) -> dict[str, Any]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO document_analysis (
            file_path,
            title,
            score,
            rating,
            strengths_json,
            weaknesses_json,
            suggestions_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            file_path,
            analysis["title"],
            analysis["score"],
            analysis["rating"],
            json.dumps(analysis.get("strengths", [])),
            json.dumps(analysis.get("weaknesses", [])),
            json.dumps(analysis.get("suggestions", [])),
        ),
    )

    conn.commit()
    saved_id = cursor.lastrowid

    cursor.execute(
        "SELECT * FROM document_analysis WHERE id = ?",
        (saved_id,),
    )
    row = cursor.fetchone()
    conn.close()

    return {
        "id": row["id"],
        "file_path": row["file_path"],
        "title": row["title"],
        "score": row["score"],
        "rating": row["rating"],
        "strengths": json.loads(row["strengths_json"]),
        "weaknesses": json.loads(row["weaknesses_json"]),
        "suggestions": json.loads(row["suggestions_json"]),
        "created_at": row["created_at"],
    }