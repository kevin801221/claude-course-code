import test from 'node:test';import assert from 'node:assert/strict';import {chromium} from 'playwright';import {fixture} from './harness.mjs';
test('1/9/12 四個畫面實際操作、重整、狀態與 API 對照',async t=>{
 const a=await fixture(t);const browser=await chromium.launch(process.env.CHROME_PATH?{executablePath:process.env.CHROME_PATH}:{});t.after(()=>browser.close());
 const p=await browser.newPage();p.setDefaultTimeout(5000);await p.goto(a.base);await p.getByRole('link',{name:'最後一席'}).click();
 await p.getByRole('button',{name:'報名',exact:true}).click();await p.getByText('我的狀態：正取').waitFor();await p.reload();await p.getByText('我的狀態：正取').waitFor();
 await p.getByRole('link',{name:'我的報名'}).click();await p.getByText('正取',{exact:true}).waitFor();await a.join('i2');await Promise.all([a.cancel('i1'),a.join('i3')]);await p.reload();await p.getByText('已取消',{exact:true}).waitFor();
 await p.getByLabel('目前身分').selectOption('hr');await p.getByRole('link',{name:'HR 管理'}).click();await p.getByText('正取',{exact:true}).waitFor();await p.getByText('候補',{exact:true}).waitFor();
 const s=p.getByRole('article').filter({has:p.getByRole('heading',{name:'最後一席'})});await s.getByLabel('容量').fill('2');await s.getByRole('button',{name:'更新容量'}).click();await s.getByText('開放 · 剩餘 0 / 2').waitFor();assert.equal((await a.session()).capacity,2);
 await s.getByLabel('容量').fill('1');await s.getByRole('button',{name:'更新容量'}).click();await p.getByRole('alert').waitFor();assert.equal((await a.session()).capacity,2);
});
