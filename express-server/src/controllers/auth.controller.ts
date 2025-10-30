import { Request, Response } from "express";
import {
  createUserService,
  findUserByEmailService,
} from "../services/user.service";
import { hashPassword, verifyPassword } from "../lib/pbkdf";

export const handleSignup = async (req: Request, res: Response) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ message: "Email and password are required" });
  }

  const foundUser = await findUserByEmailService(email);

  if (foundUser) {
    return res.status(409).json({ message: "User already exists" });
  }

  const hashedPassword = hashPassword(password);

  const newUser = await createUserService({ email, password: hashedPassword });

  return res.status(201).json(newUser);
};

export const handleLogin = async (req: Request, res: Response) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ message: "Email and password are required" });
  }

  const foundUser = await findUserByEmailService(email);

  if (
    !foundUser ||
    !foundUser.active ||
    !verifyPassword(password, foundUser.password)
  ) {
    return res.status(401).json({ message: "Incorrect email or password" });
  }

  return res.status(200).json(foundUser);
};
