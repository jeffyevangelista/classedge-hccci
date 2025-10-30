import { Request, Response } from "express";
import {
  createUserService,
  findUserByEmailService,
  findUserByIdService,
} from "../services/user.service";
import { hashPassword, verifyPassword } from "../lib/pbkdf";
import {
  generateAccessToken,
  sendRefreshToken,
  verifyRefreshToken,
} from "../lib/jwt";

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

  const access = generateAccessToken({
    user_id: newUser.userId,
    roles: newUser.roles,
    needs_onboarding: newUser.needsOnboarding,
    needs_password_setup: newUser.needsPasswordSetup,
  });

  sendRefreshToken(res, { user_id: newUser.userId });

  res.json({
    access,
  });
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

  const access = generateAccessToken({
    user_id: foundUser.userId,
    roles: foundUser.roles,
    needs_onboarding: foundUser.needsOnboarding,
    needs_password_setup: foundUser.needsPasswordSetup,
  });

  sendRefreshToken(res, { user_id: foundUser.userId });

  res.json({
    access,
  });
};

export const handleRefresh = async (req: Request, res: Response) => {
  const { jwt: refreshToken } = req.cookies;

  if (!refreshToken) {
    return res.status(401).json({ message: "Unauthorized" });
  }

  const { user_id } = verifyRefreshToken(refreshToken);

  const foundUser = await findUserByIdService(user_id);

  if (!foundUser) return res.status(401).json({ message: "Unauthorized" });

  const access = generateAccessToken({
    user_id: foundUser.userId,
    roles: foundUser.roles,
    needs_onboarding: foundUser.needsOnboarding,
    needs_password_setup: foundUser.needsPasswordSetup,
  });

  res.json({ access });
};
