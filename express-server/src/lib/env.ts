import "dotenv/config";

export const DATABASE_URL = process.env.DATABASE_URL || "";
export const PORT = process.env.PORT || "";
export const REFRESH_TOKEN_SECRET = process.env.REFRESH_TOKEN_SECRET || "";
export const ACCESS_TOKEN_SECRET = process.env.ACCESS_TOKEN_SECRET || "";
export const NODE_ENV = process.env.NODE_ENV || "";
