import test from "node:test";
import { chromium } from "playwright";
import { fixture } from "./harness.mjs";
test("13–15 瀏覽器：新外部申請 → HR 核准 → 學員看到正取", async (t) => {
  const a = await fixture(t, "cr");
  const b = await chromium.launch(
    process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {},
  );
  t.after(() => b.close());
  const p = await b.newPage();
  p.setDefaultTimeout(5000);
  await p.goto(a.base);
  await p.getByLabel("目前身分").selectOption("e1");
  await p.getByRole("link", { name: "最後一席" }).click();
  await p.getByRole("button", { name: "報名", exact: true }).click();
  await p.getByText("我的狀態：待審核").waitFor();
  await p.getByLabel("目前身分").selectOption("hr");
  await p.getByRole("link", { name: "HR 管理" }).click();
  await p.getByRole("button", { name: "核准" }).click();
  await p.getByText("正取", { exact: true }).waitFor();
  await p.getByLabel("目前身分").selectOption("e1");
  await p.getByRole("link", { name: "我的報名" }).click();
  await p.getByText("正取", { exact: true }).waitFor();
});
