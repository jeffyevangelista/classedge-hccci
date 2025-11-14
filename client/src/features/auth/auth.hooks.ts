import { useMutation, useQuery } from "@tanstack/react-query";
import type { LoginCredentials } from "./auth.types";
import { currentUser, login, msAuth, refresh } from "./auth.apis";
import useStore from "@/lib/store";
import { useNavigate } from "react-router";

export const useLogin = () => {
  const navigate = useNavigate();
  return useMutation({
    mutationKey: ["login"],
    mutationFn: (credentials: LoginCredentials) => login(credentials),
    onSuccess: (data) => {
      useStore.getState().setCredentials(data.access);
      navigate("/dashboard");
    },
  });
};

export const useMsAuth = (token: string | null) => {
  const navigate = useNavigate();
  return useQuery({
    queryKey: ["ms-auth"],
    queryFn: async () => {
      const data = await msAuth(token);

      if (data) {
        useStore.getState().setCredentials(data.access);
        navigate("/dashboard");
      }

      return data;
    },
  });
};

export const useCurrentUser = () => {
  return useQuery({
    queryKey: ["current-user"],
    queryFn: currentUser,
    enabled: useStore.getState().isAuthenticated,
  });
};

export const useRefresh = () => {
  return useMutation({
    mutationKey: ["refresh"],
    mutationFn: async () => {
      const data = await refresh();
      useStore.getState().setCredentials(data.access);
    },
  });
};
