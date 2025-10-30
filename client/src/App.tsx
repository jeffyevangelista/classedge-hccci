import { Route, Routes } from "react-router";
import LoginPage from "./pages/auth/LoginPage";
import RootLayout from "@/components/root-layout";
import DashboardPage from "./pages/dashboard/DashboardPage";
import ForgotPasswordPage from "./pages/auth/forgot-password/ForgotPasswordPage";
import VerifyOtpPage from "./pages/auth/forgot-password/VerifyOtpPage";
import ResetPasswordPage from "./pages/auth/forgot-password/ResetPasswordPage";
import useStore from "@/lib/store";
import { useEffect } from "react";
import { refresh } from "./features/auth/auth.apis";
import { AuthGuard } from "./features/auth/components/AuthGuard";

export const useAuthInit = () => {
  const setAuth = useStore((s) => s.setCredentials);
  const clearAuth = useStore((s) => s.clearCredentials);

  useEffect(() => {
    const initialize = async () => {
      try {
        const { access } = await refresh();
        setAuth(access);
      } catch {
        clearAuth();
      }
    };
    initialize();
  }, []);
};

function App() {
  useAuthInit();
  return (
    <Routes>
      <Route path="/" element={<RootLayout />}>
        {/* Auth routes */}
        <Route index element={<LoginPage />} />
        <Route path="forgot-password" element={<ForgotPasswordPage />} />
        <Route path="verify-otp" element={<VerifyOtpPage />} />
        <Route path="reset-password" element={<ResetPasswordPage />} />

        {/* Dashboard routes */}

        <Route element={<AuthGuard />}>
          <Route path="dashboard" element={<DashboardPage />} />
        </Route>
      </Route>
    </Routes>
  );
}

export default App;
