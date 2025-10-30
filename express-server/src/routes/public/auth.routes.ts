import { Router } from "express";
import {
  handleLogin,
  handleRefresh,
  handleSignup,
} from "../../controllers/auth.controller";

const authRoutes = Router();

authRoutes.route("/login").post(handleLogin);
authRoutes.route("/signup").post(handleSignup);
authRoutes.route("/refresh").get(handleRefresh);

export default authRoutes;
