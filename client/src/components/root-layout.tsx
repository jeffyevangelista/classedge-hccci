import { Outlet } from "react-router";

const RootLayout = () => {
  return (
    <div className="flex flex-col w-full min-h-screen ">
      <Outlet />
    </div>
  );
};

export default RootLayout;
