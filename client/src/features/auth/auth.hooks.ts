import { useMutation } from "@tanstack/react-query";
import type { LoginCredentials } from "./auth.types";
import { login } from "./auth.apis";
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
