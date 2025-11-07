import { subjecsTable } from "../db/schema";

export type SubjectInsert = typeof subjecsTable.$inferInsert;
export type SubjectSelect = typeof subjecsTable.$inferSelect;
