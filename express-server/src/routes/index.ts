import { Router } from "express";
import publicRoutes from "./public";
import privateRoutes from "./private";

const apiRoutes = Router();

apiRoutes.use("/public", publicRoutes);
apiRoutes.use("/private", privateRoutes);

export default apiRoutes;
