import api from "@/lib/axios";
import type { LoginCredentials } from "./auth.types";

export const login = async (credentials: LoginCredentials) => {
  return (await api.post("/auth/login/", credentials)).data;
};

export const msAuth = async (token: string | null) => {
  return (
    await api.get("/microsoft/login/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  ).data;
};

export const refresh = async () => {
  return (await api.get("/auth/refresh/")).data;
};

export const currentUser = async () => {
  return (await api.get("/profiles/me/")).data;
};
