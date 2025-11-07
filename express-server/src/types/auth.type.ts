import { JwtPayload } from "jsonwebtoken";
import type { UserSelect } from "./user.type";

export type DecodedToken = JwtPayload & {
  user_id: UserSelect["userId"];
  roles: UserSelect["roles"];
  needs_onboarding: UserSelect["needsOnboarding"];
  needs_password_setup: UserSelect["needsPasswordSetup"];
};
