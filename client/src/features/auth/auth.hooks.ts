import { useMutation } from "@tanstack/react-query";
import type { LoginCredentials } from "./auth.types";
import { login } from "./auth.apis";
import useStore from "@/lib/store";
import { toast } from "sonner";

export const useLogin = () => {
  const { setCredentials } = useStore.getState();
  return useMutation({
    mutationKey: ["login"],
    mutationFn: (credentials: LoginCredentials) => login(credentials),
    onSuccess: (data) => {
      setCredentials(data.access);
      toast.success("Login successful");
    },
    onError: (error) => {
      toast.error(error.message);
    },
  });
};
