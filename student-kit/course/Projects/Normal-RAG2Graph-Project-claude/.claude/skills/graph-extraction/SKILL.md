---
name: graph-extraction
description: 從 chunk 萃取 canonical entities + relations 存 SQLite。Use when implementing knowledge graph extraction, building the SQLite schema for entities/relations, or whenever the user says「GraphRAG」「knowledge graph」「entity extraction」「KG 萃取」.
---

## Schema（5 張表）

```sql
CREATE TABLE documents (
    doc_id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    uploaded_at TIMESTAMP NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE chunks (
    chunk_id TEXT PRIMARY KEY,
    doc_id TEXT NOT NULL REFERENCES documents(doc_id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL
);

CREATE TABLE entities (
    entity_id TEXT PRIMARY KEY,  -- slug(canonical_name)
    canonical_name TEXT NOT NULL,
    aliases TEXT NOT NULL,       -- JSON array
    "group" TEXT NOT NULL,       -- Person/Concept/Org/Event/Location
    summary TEXT,
    val INTEGER NOT NULL DEFAULT 0,
    created_from_doc_id TEXT REFERENCES documents(doc_id),
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE links (
    link_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_entity_id TEXT NOT NULL REFERENCES entities(entity_id) ON DELETE CASCADE,
    target_entity_id TEXT NOT NULL REFERENCES entities(entity_id) ON DELETE CASCADE,
    label TEXT NOT NULL,
    confidence REAL NOT NULL,
    source_chunk_id TEXT NOT NULL REFERENCES chunks(chunk_id) ON DELETE CASCADE
);

CREATE TABLE entity_chunks (
    entity_id TEXT NOT NULL REFERENCES entities(entity_id) ON DELETE CASCADE,
    chunk_id TEXT NOT NULL REFERENCES chunks(chunk_id) ON DELETE CASCADE,
    salience REAL NOT NULL DEFAULT 0.5,
    PRIMARY KEY (entity_id, chunk_id)
);
```

PRAGMA foreign_keys = ON，ON DELETE CASCADE。

## 萃取 Prompt 樣板
只輸出 JSON，欄位：canonical_name / aliases / group(5 種) / summary / salience。
group 只能是：Person / Concept / Org / Event / Location。
每 chunk 至多 8 個 entity、10 個 relation。

## 合併策略
- entity_id = slug(canonical_name)
- 同名自動聯集 aliases
- 每個 chunk 失敗獨立 skip，不中斷整份文件
- 完成後重算 entities.val = COUNT(*) FROM entity_chunks

## 刪除策略（級聯）
DELETE document → CASCADE chunks → CASCADE entity_chunks + links
→ 清除無 entity_chunks 的孤立 entities → 重算 val
