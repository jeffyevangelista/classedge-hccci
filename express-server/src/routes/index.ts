import { Router } from "express";
import publicRoutes from "./public";
import privateRoutes from "./private";

const apiRoutes = Router();

apiRoutes.use(publicRoutes);
apiRoutes.use(privateRoutes);

export default apiRoutes;
