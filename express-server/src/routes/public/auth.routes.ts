import { Router } from "express";
import { handleLogin } from "../../controllers/auth.controller";

const authRoutes = Router();

authRoutes.route("/login").post(handleLogin);

export default authRoutes;
