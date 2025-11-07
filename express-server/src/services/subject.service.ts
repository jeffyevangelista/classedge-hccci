import { eq } from "drizzle-orm";
import db from "../db";
import { subjecsTable } from "../db/schema";
import { SubjectInsert } from "../types/subject.type";

export const findAllSubjects = async () => {
  return await db.select().from(subjecsTable);
};

export const findSubjectById = async (subjectId: string) => {
  const [subject] = await db
    .select()
    .from(subjecsTable)
    .where(eq(subjecsTable.subjectId, parseInt(subjectId)));
  return subject;
};

export const createSubject = async (subject: SubjectInsert) => {
  return await db.insert(subjecsTable).values(subject);
};

export const updateSubject = async (
  subjectId: string,
  subject: SubjectInsert
) => {
  const numericSubjectId = Number(subjectId);

  if (Number.isNaN(numericSubjectId)) {
    throw new Error("Invalid subject id provided");
  }

  return await db
    .update(subjecsTable)
    .set(subject)
    .where(eq(subjecsTable.subjectId, numericSubjectId));
};

export const deleteSubject = async (subjectId: string) => {
  const numericSubjectId = Number(subjectId);

  if (Number.isNaN(numericSubjectId)) {
    throw new Error("Invalid subject id provided");
  }

  return await db
    .delete(subjecsTable)
    .where(eq(subjecsTable.subjectId, numericSubjectId));
};
