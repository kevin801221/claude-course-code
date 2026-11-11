import { readFileSync, writeFileSync, renameSync, rmSync } from 'node:fs';
import { randomUUID } from 'node:crypto';

export function loadTasks(path) {
  let text;
  try { text = readFileSync(path, 'utf8'); }
  catch (error) { if (error.code === 'ENOENT') return []; throw error; }
  let tasks;
  try { tasks = JSON.parse(text); }
  catch { throw new Error('tasks.json 不是合法 JSON；請保留原檔並修復。'); }
  if (!Array.isArray(tasks) || tasks.some(t => !t || typeof t.id !== 'string' || typeof t.title !== 'string' || typeof t.done !== 'boolean')) {
    throw new Error('tasks.json 格式錯誤：需要 { id, title, done } 陣列。');
  }
  return tasks;
}

export function saveTasks(path, tasks) {
  // 同一資料夾先寫暫存檔再 rename，避免半份 JSON。此範例不支援多程序同時寫入。
  const temporary = `${path}.${randomUUID()}.tmp`;
  try {
    writeFileSync(temporary, JSON.stringify(tasks, null, 2) + '\n', { flag: 'wx' });
    renameSync(temporary, path);
  } finally {
    rmSync(temporary, { force: true });
  }
}

export function addTask(tasks, title) {
  if (typeof title !== 'string' || !title.trim()) throw new Error('任務標題不可空白。');
  return { id: randomUUID(), title: title.trim(), done: false };
}

export function completeTask(tasks, id) {
  const task = tasks.find(t => t.id === id);
  if (!task) throw new Error(`找不到任務 ID：${id || '（未提供）'}`);
  return tasks.map(t => t.id === id ? { ...t, done: true } : t);
}
