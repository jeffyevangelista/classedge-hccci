import { Route, Routes } from "react-router";
import LoginPage from "@/pages/auth/LoginPage";
import RootLayout from "@/components/root-layout";
import DashboardPage from "@/pages/dashboard/DashboardPage";
import ForgotPasswordPage from "@/pages/auth/forgot-password/ForgotPasswordPage";
import VerifyOtpPage from "@/pages/auth/forgot-password/VerifyOtpPage";
import ResetPasswordPage from "@/pages/auth/forgot-password/ResetPasswordPage";
import PersistAuth from "@/features/auth/components/PersistAuth";
import DashboardLayout from "@/components/dashboard-layout";
import AcademicYearsPage from "@/pages/academic-settings/AcademicYearsPage";
import SemestersPage from "@/pages/academic-settings/AcademicTermsPage";
import TermsPage from "@/pages/academic-settings/TermsPage";
import AcademicYearDetailsPage from "@/pages/academic-settings/AcademicYearDetailsPage";

function App() {
  return (
    <Routes>
      <Route element={<PersistAuth />}>
        <Route path="/" element={<RootLayout />}>
          {/* Auth routes */}
          <Route index element={<LoginPage />} />
          <Route path="forgot-password" element={<ForgotPasswordPage />} />
          <Route path="verify-otp" element={<VerifyOtpPage />} />
          <Route path="reset-password" element={<ResetPasswordPage />} />

          {/* Dashboard routes */}

          <Route element={<DashboardLayout />}>
            <Route path="dashboard" element={<DashboardPage />} />

            {/* Academic Settings */}
            <Route path="academic-years">
              <Route index element={<AcademicYearsPage />} />
              <Route path=":ayId">
                <Route index element={<AcademicYearDetailsPage />} />
              </Route>
            </Route>

            <Route path="semesters" element={<SemestersPage />} />
            <Route path="terms" element={<TermsPage />} />
          </Route>
        </Route>
      </Route>
    </Routes>
  );
}

export default App;
