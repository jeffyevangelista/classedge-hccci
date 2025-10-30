import { Navigate, Outlet } from "react-router";
import useStore from "@/lib/store";

export const AuthGuard = () => {
  const isAuthenticated = useStore((s) => s.isAuthenticated);
  return isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};
