import { Request, Response } from "express";
import {
  findAllSubjects,
  findSubjectById,
  createSubject,
  updateSubject,
  deleteSubject,
} from "../services/subject.service";

export const handleGetSubjects = async (req: Request, res: Response) => {
  const subjects = await findAllSubjects();
  return res.status(200).json(subjects);
};

export const handleGetSubject = async (req: Request, res: Response) => {
  const { subjectId } = req.params;
  const subject = await findSubjectById(subjectId);
  return res.status(200).json(subject);
};

export const handleCreateSubject = async (req: Request, res: Response) => {
  const { subject } = req.body;
  const createdSubject = await createSubject(subject);
  return res.status(200).json(createdSubject);
};

export const handleUpdateSubject = async (req: Request, res: Response) => {
  const { subjectId } = req.params;
  const updatedSubject = await updateSubject(subjectId, req.body);
  return res.status(200).json(updatedSubject);
};

export const handleDeleteSubject = async (req: Request, res: Response) => {
  const { subjectId } = req.params;
  const deletedSubject = await deleteSubject(subjectId);
  return res.status(200).json(deletedSubject);
};
