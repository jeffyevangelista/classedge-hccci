import { CorsOptions } from "cors";
import { CORS_WHITELIST } from "./env";

const corsOptions: CorsOptions = {
  origin(origin, callback) {
    // Allow requests with no origin (like curl or mobile apps)
    if (!origin) return callback(null, true);

    if (CORS_WHITELIST.includes(origin)) {
      callback(null, true);
    } else {
      console.warn("❌ Blocked by CORS:", origin);
      callback(new Error("Not allowed by CORS"));
    }
  },
  credentials: true,
  optionsSuccessStatus: 200,
};

export default corsOptions;
