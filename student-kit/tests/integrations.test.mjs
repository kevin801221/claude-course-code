import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
function python(path, input) {
  return spawnSync('python3', [root + path], { cwd: root, encoding: 'utf8', input });
}
test('Hook 拒絕寫入環境秘密檔，正常來源檔放行', () => {
  for (const name of ['.env', '/tmp/demo/.env.production', '/tmp/demo/secrets/token.txt']) {
    const r = python('labs/05-hooks/guard.py', JSON.stringify({ tool_name: 'Write', tool_input: { file_path: name } }));
    assert.equal(r.status, 0, r.stderr);
    assert.equal(JSON.parse(r.stdout).hookSpecificOutput.permissionDecision, 'deny');
  }
  const ok = python('labs/05-hooks/guard.py', JSON.stringify({ tool_name: 'Edit', tool_input: { file_path: 'src/app.mjs' } }));
  assert.equal(ok.status, 0, ok.stderr);
  assert.equal(ok.stdout, '');
});
test('Hook 格式錯誤會阻擋，且不把秘密內容印進訊息', () => {
  const r = python('labs/05-hooks/guard.py', 'bad-json');
  assert.equal(r.status, 2);
  assert.match(r.stderr, /JSON/);
  const empty = python('labs/05-hooks/guard.py', JSON.stringify({ tool_name: 'Write', tool_input: {} }));
  assert.equal(empty.status, 2);
});
test('本機 MCP 完成初始化、工具列舉、課程查詢與未知工具處理', () => {
  const requests = [
    { jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'kit-test', version: '1' } } },
    { jsonrpc: '2.0', method: 'notifications/initialized' },
    { jsonrpc: '2.0', id: 2, method: 'tools/list' },
    { jsonrpc: '2.0', id: 3, method: 'tools/call', params: { name: 'search_lessons', arguments: { query: 'Hooks' } } },
    { jsonrpc: '2.0', id: 4, method: 'tools/call', params: { name: 'missing', arguments: {} } },
    { jsonrpc: '2.0', id: 5, method: 'tools/call', params: { name: 'search_lessons', arguments: { query: 7 } } },
    { jsonrpc: '2.0', id: 6, method: 'ping' }
  ];
  const result = python('labs/06-mcp/lesson-server.py', requests.map(x => JSON.stringify(x)).join('\n') + '\n');
  assert.equal(result.status, 0, result.stderr);
  const replies = result.stdout.trim().split('\n').map(x => JSON.parse(x));
  assert.equal(replies.length, 6);
  assert.equal(replies[0].result.protocolVersion, '2024-11-05');
  assert.equal(replies[1].result.tools[0].name, 'search_lessons');
  assert.match(replies[2].result.content[0].text, /Hooks/);
  assert.equal(replies[3].result.isError, true);
  assert.equal(replies[4].result.isError, true);
  assert.deepEqual(replies[5].result, {});
});
