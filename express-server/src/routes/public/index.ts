import { Router } from "express";
import authRoutes from "./auth.routes";

const publicRoutes = Router();

publicRoutes.use("/auth", authRoutes);

export default publicRoutes;
