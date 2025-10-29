import { Request, Response } from "express";
import createError from "http-errors";

export const handleLogin = async (req: Request, res: Response) => {
  const { email, password } = req.body;

  if (!email || !password) {
    throw createError(400, "Email and password are required");
  }
};
