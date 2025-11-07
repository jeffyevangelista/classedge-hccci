import "dotenv/config";

export const DATABASE_URL: string = process.env.DATABASE_URL || "";
export const PORT: string = process.env.PORT || "";
export const REFRESH_TOKEN_SECRET: string =
  process.env.REFRESH_TOKEN_SECRET || "";
export const ACCESS_TOKEN_SECRET: string =
  process.env.ACCESS_TOKEN_SECRET || "";
export const NODE_ENV: string = process.env.NODE_ENV || "";
export const CORS_WHITELIST = process.env.CORS_WHITELIST
  ? process.env.CORS_WHITELIST.split(",")
  : [];
