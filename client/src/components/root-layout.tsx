import { Outlet } from "react-router";

const RootLayout = () => {
  return (
    <div className="min-h-screen">
      <Outlet />
    </div>
  );
};

export default RootLayout;
