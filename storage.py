# storage.py
import sqlite3
from typing import Optional, List
from datetime import datetime

from schemas import Term, TermDetailed, Relation

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS terms (
    keyword TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    meta_description TEXT NOT NULL,
    full_description TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_keyword TEXT NOT NULL REFERENCES terms(keyword) ON DELETE CASCADE,
    target_keyword TEXT NOT NULL REFERENCES terms(keyword) ON DELETE CASCADE,
    relation_type TEXT NOT NULL
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

    def list_terms(self) -> List[Term]:
        conn = self._conn()
        cur = conn.execute("SELECT keyword, title, description, created_at, updated_at FROM terms ORDER BY keyword")
        rows = cur.fetchall()
        conn.close()
        result = []
        for r in rows:
            result.append(Term(
                keyword=r["keyword"],
                title=r["title"],
                description=r["description"],
                created_at=datetime.fromisoformat(r["created_at"]),
                updated_at=datetime.fromisoformat(r["updated_at"])
            ))
        return result

    def get_term(self, keyword: str) -> TermDetailed:
        conn = self._conn()
        cur = conn.execute("SELECT * FROM terms WHERE keyword = ?", (keyword,))
        r = cur.fetchone()
        conn.close()
        if not r:
            return None
        return TermDetailed(
            keyword=r["keyword"],
            title=r["title"],
            description=r["description"],
            full_description=r["full_description"],
            meta_description=r["meta_description"],
            created_at=datetime.fromisoformat(r["created_at"]),
            updated_at=datetime.fromisoformat(r["updated_at"])
        )

    def create_term(self, keyword: str, title: str, description: str, meta_description: str, full_description: str) -> TermDetailed:
        now = datetime.utcnow().isoformat()
        conn = self._conn()
        conn.execute(
            "INSERT INTO terms (keyword, title, description, meta_description, full_description, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (keyword, title, description, meta_description, full_description, now, now)
        )
        conn.commit()
        conn.close()
        return self.get_term(keyword)

    def update_term(self, keyword: str, title: str, description: str, meta_description: str, full_description: str) -> TermDetailed:
        now = datetime.utcnow().isoformat()
        conn = self._conn()
        print(title, description, meta_description, full_description)
        cur = conn.execute(
            "UPDATE terms SET title = ?, description = ?, meta_description = ?, full_description = ?, updated_at = ? WHERE keyword = ?",
            (title, description, meta_description, full_description, now, keyword)
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

    def list_relations(self) -> List[Relation]:
        conn = self._conn()
        cur = conn.execute("SELECT * FROM relations")
        rows = cur.fetchall()
        conn.close()
        result = []
        for r in rows:
            result.append(Relation(
                id=r["id"],
                source_keyword=r["source_keyword"],
                target_keyword=r["target_keyword"],
                relation_type=r["relation_type"]
            ))
        return result

    def get_relation(self, relation_id: int) -> Optional[Relation]:
        conn = self._conn()
        cur = conn.execute("SELECT * FROM relations WHERE id = ?", (relation_id, ))
        r = cur.fetchone()
        conn.close()
        if not r:
            return None
        return Relation(
            id=r["id"],
            source_keyword=r["source_keyword"],
            target_keyword=r["target_keyword"],
            relation_type=r["relation_type"]
        )

    def create_relation(self, source_keyword: str, target_keyword: str, relation_type: str) -> Relation:
        conn = self._conn()
        cur = conn.execute(
            "INSERT INTO relations (source_keyword, target_keyword, relation_type) VALUES (?, ?, ?) RETURNING *",
            (source_keyword, target_keyword, relation_type)
        )
        r = cur.fetchone()
        conn.commit()
        conn.close()
        return Relation(
            id=r["id"],
            source_keyword=r["source_keyword"],
            target_keyword=r["target_keyword"],
            relation_type=r["relation_type"]
        )

    def update_relation(self, relation_id: int, source_keyword: str, target_keyword: str, relation_type: str) -> Optional[Relation]:
        conn = self._conn()
        cur = conn.execute(
            "UPDATE relations SET source_keyword = ?, target_keyword = ? relation_type = ? WHERE id = ?",
            (source_keyword, target_keyword, relation_type, relation_id)
        )
        conn.commit()
        changed = cur.rowcount
        conn.close()
        if changed:
            return self.get_relation(relation_id)
        return None

    def delete_relation(self, relation_id: int) -> bool:
        conn = self._conn()
        cur = conn.execute("DELETE FROM relations WHERE id = ?", (relation_id, ))
        conn.commit()
        deleted = cur.rowcount > 0
        conn.close()
        return deleted
