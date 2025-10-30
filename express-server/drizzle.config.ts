import { defineConfig } from "drizzle-kit";
import { DATABASE_URL } from "./src/utils/env";

export default defineConfig({
  out: "./drizzle",
  dialect: "postgresql",
  schema: "./src/db/schema.ts",
  dbCredentials: {
    url: DATABASE_URL,
  },
});
