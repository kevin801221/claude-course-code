import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const cli = fileURLToPath(new URL('../bin/tasks.mjs', import.meta.url));
function sandbox(t) {
  const cwd = mkdtempSync(join(tmpdir(), 'course-task-'));
  t.after(() => rmSync(cwd, { recursive: true, force: true }));
  return { cwd, run: (...args) => spawnSync(process.execPath, [cli, ...args], { cwd, encoding: 'utf8' }) };
}
test('第一次列出任務為空陣列', t => {
  const { run } = sandbox(t);
  const result = run('list');
  assert.equal(result.status, 0, result.stderr);
  assert.deepEqual(JSON.parse(result.stdout), []);
});
test('新增繁中任務，重開 CLI 仍可讀到，完成後狀態持久化', t => {
  const { run } = sandbox(t);
  const added = run('add', '  完成 Hooks 練習  ');
  assert.equal(added.status, 0, added.stderr);
  const task = JSON.parse(added.stdout);
  assert.equal(task.title, '完成 Hooks 練習');
  assert.equal(task.done, false);
  assert.equal(run('done', task.id).status, 0);
  assert.deepEqual(JSON.parse(run('list').stdout), [{ ...task, done: true }]);
});
test('空白標題與不存在 ID 回報錯誤且不修改任務', t => {
  const { run, cwd } = sandbox(t);
  run('add', '已有任務');
  const before = readFileSync(join(cwd, 'tasks.json'), 'utf8');
  assert.equal(run('add', '   ').status, 1);
  assert.equal(run('done', 'missing').status, 1);
  assert.equal(readFileSync(join(cwd, 'tasks.json'), 'utf8'), before);
});
test('損壞資料清楚報錯，保留原始檔以便修復', t => {
  const { run, cwd } = sandbox(t);
  writeFileSync(join(cwd, 'tasks.json'), '{broken');
  const result = run('add', '不要覆蓋');
  assert.equal(result.status, 1);
  assert.match(result.stderr, /tasks.json/);
  assert.equal(readFileSync(join(cwd, 'tasks.json'), 'utf8'), '{broken');
});
test('非任務陣列的 JSON 被拒絕', t => {
  const { run, cwd } = sandbox(t);
  writeFileSync(join(cwd, 'tasks.json'), JSON.stringify([{ title: '缺少 id 與 done' }]));
  assert.equal(run('list').status, 1);
});
test('未知指令回傳非零與用法', t => {
  const { run } = sandbox(t);
  const result = run('destroy');
  assert.equal(result.status, 1);
  assert.match(result.stderr, /add|list|done/);
});
