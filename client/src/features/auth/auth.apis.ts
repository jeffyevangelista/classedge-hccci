import api from "@/lib/axios";
import type { LoginCredentials } from "./auth.types";

export const login = async (credentials: LoginCredentials) => {
  return (await api.post("/auth/login/", credentials)).data;
};
