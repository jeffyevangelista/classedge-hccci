import express, { Request, Response } from "express";
import apiRoutes from "./routes";

const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());

// Routes
app.get("/", (req: Request, res: Response) => {
  res.send("Hello, TypeScript with Express!");
});

app.use("/api", apiRoutes);

export default app;
