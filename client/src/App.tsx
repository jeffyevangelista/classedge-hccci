import { Route, Routes } from "react-router";
import LoginPage from "./pages/auth/LoginPage";
import RootLayout from "@/components/root-layout";
import DashboardPage from "./pages/dashboard/DashboardPage";

function App() {
  return (
    <Routes>
      <Route path="/" element={<RootLayout />}>
        <Route index element={<LoginPage />} />

        <Route path="dashboard" element={<DashboardPage />} />
      </Route>
    </Routes>
  );
}

export default App;
