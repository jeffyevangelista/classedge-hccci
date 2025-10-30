import { Router } from "express";
import { handleLogin, handleSignup } from "../../controllers/auth.controller";

const authRoutes = Router();

authRoutes.route("/login").post(handleLogin);
authRoutes.route("/signup").post(handleSignup);

export default authRoutes;
