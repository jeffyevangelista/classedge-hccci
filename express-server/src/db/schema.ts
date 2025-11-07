import { createId } from "@paralleldrive/cuid2";
import { serial } from "drizzle-orm/pg-core";
import { primaryKey } from "drizzle-orm/pg-core";
import {
  text,
  timestamp,
  boolean,
  varchar,
  pgTable,
} from "drizzle-orm/pg-core";

export const usersTable = pgTable("users", {
  userId: varchar("user_id", { length: 255 }).primaryKey().$defaultFn(createId),
  email: varchar("email", { length: 255 }).notNull().unique(),
  password: text("password").notNull(),
  createdAt: timestamp("created_at").defaultNow(),
  roles: text("roles").array().notNull().default(["student"]),
  active: boolean("active").notNull().default(true),
  needsPasswordSetup: boolean("needs_password_setup").notNull().default(true),
  needsOnboarding: boolean("needs_onboarding").notNull().default(true),
});

export const subjecsTable = pgTable("subjects", {
  subjectId: serial("subject_id").primaryKey(),
  name: varchar("name", { length: 255 }).notNull(),
  description: text("description"),
  code: varchar("code", { length: 255 }).notNull(),
  photo: text("photo"),
  createdAt: timestamp("created_at").defaultNow(),
  teacherId: varchar("teacher_id", { length: 255 }),
  collaborators: varchar("collaborators", { length: 255 }).array(),
});
