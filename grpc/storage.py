# storage.py
import sqlite3
from typing import Optional, List
from datetime import datetime
from models import TermDB

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS terms (
    keyword TEXT PRIMARY KEY,
    description TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""

class Storage:
    def __init__(self, db_path: str = "glossary.db"):
        self.db_path = db_path
        self._init_db()

    def _conn(self):
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        conn = self._conn()
        conn.executescript(DB_SCHEMA)
        conn.commit()
        conn.close()

    def list_terms(self) -> List[TermDB]:
        conn = self._conn()
        cur = conn.execute("SELECT * FROM terms ORDER BY keyword")
        rows = cur.fetchall()
        conn.close()
        result = []
        for r in rows:
            result.append(TermDB(
                keyword=r["keyword"],
                description=r["description"],
                created_at=datetime.fromisoformat(r["created_at"]),
                updated_at=datetime.fromisoformat(r["updated_at"])
            ))
        return result

    def get_term(self, keyword: str) -> Optional[TermDB]:
        conn = self._conn()
        cur = conn.execute("SELECT * FROM terms WHERE keyword = ?", (keyword,))
        r = cur.fetchone()
        conn.close()
        if not r:
            return None
        return TermDB(
            keyword=r["keyword"],
            description=r["description"],
            created_at=datetime.fromisoformat(r["created_at"]),
            updated_at=datetime.fromisoformat(r["updated_at"])
        )

    def create_term(self, keyword: str, description: str) -> TermDB:
        now = datetime.utcnow().isoformat()
        conn = self._conn()
        conn.execute(
            "INSERT INTO terms (keyword, description, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (keyword, description, now, now)
        )
        conn.commit()
        conn.close()
        return self.get_term(keyword)

    def update_term(self, keyword: str, description: str) -> Optional[TermDB]:
        now = datetime.utcnow().isoformat()
        conn = self._conn()
        cur = conn.execute(
            "UPDATE terms SET description = ?, updated_at = ? WHERE keyword = ?",
            (description, now, keyword)
        )
        conn.commit()
        changed = cur.rowcount
        conn.close()
        if changed:
            return self.get_term(keyword)
        return None

    def delete_term(self, keyword: str) -> bool:
        conn = self._conn()
        cur = conn.execute("DELETE FROM terms WHERE keyword = ?", (keyword,))
        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()
        return deleted
