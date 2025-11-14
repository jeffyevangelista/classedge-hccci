import db from "../db";
import { usersTable } from "../db/schema";
import { eq } from "drizzle-orm";
import { UserInsert } from "../types/user.type";

export const findUserByEmailService = async (email: string) => {
  const [user] = await db
    .select()
    .from(usersTable)
    .where(eq(usersTable.email, email));

  return user;
};

export const findUserByIdService = async (userId: string) => {
  const [user] = await db
    .select()
    .from(usersTable)
    .where(eq(usersTable.userId, userId));

  return user;
};

export const createUserService = async (payload: UserInsert) => {
  const [createdUser] = await db.insert(usersTable).values(payload).returning();

  return createdUser;
};
