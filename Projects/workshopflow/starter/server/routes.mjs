import express from "express";
import { db } from "./database.mjs";
export const api = express.Router();
api.get("/participants", (_q, r) =>
  r.json(db.prepare("SELECT id,kind FROM participants ORDER BY id").all()),
);
api.get("/sessions", (_q, r) =>
  r.json(db.prepare("SELECT * FROM sessions ORDER BY id").all()),
);
api.use((_q, r) =>
  r.status(501).json({ error: "Starter：請依照 API.md 實作此端點" }),
);
