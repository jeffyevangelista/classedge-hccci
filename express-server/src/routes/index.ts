import { Router } from "express";
import publicRoutes from "./public";
import privateRoutes from "./private";

const apiRoutes = Router();

apiRoutes.use("/pub", publicRoutes);
apiRoutes.use("/pvt", privateRoutes);

export default apiRoutes;
