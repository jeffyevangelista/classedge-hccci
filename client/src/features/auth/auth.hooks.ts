import { useMutation, useQuery } from "@tanstack/react-query";
import type { LoginCredentials } from "./auth.types";
import { login, msAuth } from "./auth.apis";
import useStore from "@/lib/store";
import { useNavigate } from "react-router";

export const useLogin = () => {
  const navigate = useNavigate();
  const { setCredentials } = useStore.getState();
  return useMutation({
    mutationKey: ["login"],
    mutationFn: (credentials: LoginCredentials) => login(credentials),
    onSuccess: (data) => {
      setCredentials(data.access);
      navigate("/dashboard");
    },
  });
};

export const useMsAuth = (token: string | null) => {
  const navigate = useNavigate();
  const { setCredentials } = useStore.getState();
  return useQuery({
    queryKey: ["ms-auth"],
    queryFn: async () => {
      const data = await msAuth(token);

      if (data) {
        setCredentials(data.access);
      }
      navigate("/dashboard");

      console.log(data);

      return data;
    },
  });
};
