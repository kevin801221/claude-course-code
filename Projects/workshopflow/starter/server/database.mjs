import { DatabaseSync } from 'node:sqlite';
import { mkdirSync, readFileSync } from 'node:fs';
import path from 'node:path';
export const seed = JSON.parse(readFileSync(new URL('../fixtures/seed.json', import.meta.url)));
export const dataFile = process.env.WORKSHOP_DB || path.resolve('data/workshop.sqlite');
mkdirSync(path.dirname(dataFile), {recursive:true});
export const db = new DatabaseSync(dataFile);
db.exec(`PRAGMA foreign_keys=ON; PRAGMA busy_timeout=5000; PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS participants(id TEXT PRIMARY KEY,kind TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS sessions(id TEXT PRIMARY KEY,title TEXT NOT NULL,description TEXT NOT NULL,starts TEXT NOT NULL,capacity INTEGER NOT NULL CHECK(capacity>0),open INTEGER NOT NULL DEFAULT 1);`);
export function fill() {
  db.exec('BEGIN IMMEDIATE');
  try {
    if (!db.prepare('SELECT 1 FROM participants LIMIT 1').get()) {
      for (const p of seed.participants) db.prepare('INSERT INTO participants VALUES(?,?)').run(p.id,p.kind);
      for (const s of seed.sessions) db.prepare('INSERT INTO sessions(id,title,description,starts,capacity) VALUES(?,?,?,?,?)').run(s.id,s.title,s.description,s.starts,s.capacity);
    }
    db.exec('COMMIT');
  } catch(e) { db.exec('ROLLBACK'); throw e; }
}
fill();
