import { Route, Routes } from "react-router";
import LoginPage from "./pages/auth/LoginPage";
import RootLayout from "@/components/root-layout";
import DashboardPage from "./pages/dashboard/DashboardPage";
import ForgotPasswordPage from "./pages/auth/forgot-password/ForgotPasswordPage";
import VerifyOtpPage from "./pages/auth/forgot-password/VerifyOtpPage";
import ResetPasswordPage from "./pages/auth/forgot-password/ResetPasswordPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<RootLayout />}>
        {/* Auth routes */}
        <Route index element={<LoginPage />} />
        <Route path="forgot-password" element={<ForgotPasswordPage />} />
        <Route path="verify-otp" element={<VerifyOtpPage />} />
        <Route path="reset-password" element={<ResetPasswordPage />} />

        {/* Dashboard routes */}
        <Route path="dashboard" element={<DashboardPage />} />
      </Route>
    </Routes>
  );
}

export default App;
