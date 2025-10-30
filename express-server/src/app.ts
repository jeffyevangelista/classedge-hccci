import express, { json, Request, Response } from "express";
import apiRoutes from "./routes";
import cookieParser from "cookie-parser";
import cors from "cors";
import corsOptions from "./lib/cors";

const app = express();

// Middleware
app.use(json());
app.use(cookieParser());
app.use(cors(corsOptions));
// Routes
app.get("/", (req: Request, res: Response) => {
  res.send("Hello, TypeScript with Express!");
});

app.use("/api", apiRoutes);

export default app;
