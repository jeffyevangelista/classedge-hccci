import { type JwtPayload } from "jwt-decode";

export type LoginCredentials = {
  email: string;
  password: string;
};

export type DecodedToken = JwtPayload & {
  role: string[];
  user_id: string;
  token_type: string;
  exp: number;
  iat: number;
  jti: string;
  needs_password_setup: boolean;
  needs_onboarding: boolean;
};

export type AuthUser = {
  userId: string;
  role: string[];
};
