import { cpSync, mkdirSync, existsSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
const root = fileURLToPath(new URL(".", import.meta.url));
const [mode, target] = process.argv.slice(2);
if (!["groups", "reference"].includes(mode) || !target)
  throw Error("node prepare.mjs groups|reference NEW_DIRECTORY");
const dest = path.resolve(target);
if (existsSync(dest) || dest.startsWith(path.resolve(root) + path.sep))
  throw Error("請指定教材之外尚不存在的新目錄；不會覆寫原有專案。");
mkdirSync(dest, { recursive: true });
for (const name of mode === "groups"
  ? ["A-subagents", "B-agent-teams", "C-workflow"]
  : ["reference"]) {
  const out = mode === "groups" ? path.join(dest, name) : dest;
  cpSync(path.join(root, "starter"), out, {
    recursive: true,
    filter: (p) => !["node_modules", "dist", "data"].includes(path.basename(p)),
  });
  if (mode === "reference") {
    cpSync(path.join(root, "reference"), out, { recursive: true });
    for (const f of ["cr.test.mjs", "cr-ui.test.mjs"])
      cpSync(path.join(root, "grading", f), path.join(out, "tests", f));
  }
  writeFileSync(
    path.join(out, "BASELINE.txt"),
    "WorkshopFlow classroom baseline 1\n",
  );
  console.log(out);
}
