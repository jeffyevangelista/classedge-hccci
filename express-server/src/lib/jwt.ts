import { sign, verify } from "jsonwebtoken";
import { ACCESS_TOKEN_SECRET, NODE_ENV, REFRESH_TOKEN_SECRET } from "./env";
import { Response } from "express";
import { DecodedToken } from "../types/auth.type";

export const generateAccessToken = (payload: any) => {
  return sign(payload, ACCESS_TOKEN_SECRET, { expiresIn: "15m" });
};

export const generateRefreshToken = (payload: any) => {
  return sign(payload, REFRESH_TOKEN_SECRET, { expiresIn: "7d" });
};

export const verifyAccessToken = (token: string): DecodedToken => {
  try {
    return verify(token, ACCESS_TOKEN_SECRET!) as DecodedToken;
  } catch (err: any) {
    throw new Error(
      err.name === "TokenExpiredError" ? "Token expired" : "Unauthorized"
    );
  }
};

export const verifyRefreshToken = (token: string): DecodedToken => {
  try {
    return verify(token, REFRESH_TOKEN_SECRET!) as DecodedToken;
  } catch (err: any) {
    throw new Error(
      err.name === "TokenExpiredError"
        ? "Refresh token expired"
        : "Unauthorized"
    );
  }
};

export const sendRefreshToken = (res: Response, payload: any) => {
  const refreshToken = generateRefreshToken(payload);

  res.cookie("jwt", refreshToken, {
    httpOnly: true,
    sameSite: "strict",
    secure: NODE_ENV !== "development",
    maxAge: 1000 * 60 * 60 * 24 * 7,
  });
};
