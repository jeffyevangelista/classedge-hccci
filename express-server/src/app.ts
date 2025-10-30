import express, { Request, Response } from "express";
import apiRoutes from "./routes";
import cookieParser from "cookie-parser";

const app = express();

// Middleware
app.use(express.json());
app.use(cookieParser());
// Routes
app.get("/", (req: Request, res: Response) => {
  res.send("Hello, TypeScript with Express!");
});

app.use("/api", apiRoutes);

export default app;
