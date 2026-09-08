import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "candidate_history.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS candidate_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id INTEGER,
                candidate_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                human_review TEXT,
                decision TEXT NOT NULL,
                status TEXT NOT NULL
            )
            '''
        )
        conn.commit()

def save_result(state):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            '''
            INSERT INTO candidate_history
            (candidate_id, candidate_name, score, human_review, decision, status)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (
                state.get("candidate_id"),
                state.get("candidate_name"),
                state.get("score", 0),
                state.get("human_review", ""),
                state.get("decision", ""),
                state.get("status", ""),
            ),
        )
        conn.commit()

def get_history():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute(
            '''
            SELECT candidate_id, candidate_name, score, human_review, decision, status
            FROM candidate_history
            ORDER BY id
            '''
        ).fetchall()
