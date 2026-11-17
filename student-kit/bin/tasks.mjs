#!/usr/bin/env node
import { resolve } from 'node:path';
import { loadTasks, saveTasks, addTask, completeTask } from '../src/task-board.mjs';

const [command = 'list', ...args] = process.argv.slice(2);
const usage = '用法：npm run tasks -- list | add "任務標題" | done <id>';
try {
  if (!['list', 'add', 'done'].includes(command)) throw new Error(usage);
  const path = resolve('tasks.json');
  const tasks = loadTasks(path);
  let result = tasks;
  if (command === 'add') {
    result = addTask(tasks, args.join(' '));
    saveTasks(path, [...tasks, result]);
  } else if (command === 'done') {
    result = completeTask(tasks, args[0]);
    saveTasks(path, result);
  }
  console.log(JSON.stringify(result, null, 2));
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
