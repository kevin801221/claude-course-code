import { db, fill, dataFile } from "./database.mjs";
// Reset only WorkshopFlow's own tables; do not remove a user-supplied file.
db.exec(
  "BEGIN IMMEDIATE; DROP TABLE IF EXISTS registrations; DROP TABLE IF EXISTS seq; DELETE FROM sessions; DELETE FROM participants; COMMIT;",
);
fill();
db.close();
console.log("Seed restored:", dataFile);
