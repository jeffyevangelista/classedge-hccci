import { useRefresh } from "@/features/auth/auth.hooks";
import useStore from "@/lib/store";
import { Loader } from "lucide-react";
import { useEffect, useState } from "react";
import { Outlet } from "react-router";

const PersistAuth = () => {
  const { accessToken } = useStore();
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const { mutateAsync: refresh, isPending } = useRefresh();

  useEffect(() => {
    let isMounted = true;

    const verifyRefreshToken = async () => {
      console.log("verifying refresh token");
      try {
        await refresh();
      } catch (err) {
        console.log(err);
        // navigate("/", { replace: true }); // Redirect to login if refresh fails
      } finally {
        if (isMounted) setIsCheckingAuth(false); // Allow rendering to continue
      }
    };

    if (!accessToken) {
      verifyRefreshToken();
    } else {
      setIsCheckingAuth(false);
    }

    return () => {
      isMounted = false;
    };
  }, []);

  if (isCheckingAuth || isPending)
    return (
      <div className="flex h-screen items-center">
        <Loader className="mx-auto animate-spin" />
      </div>
    );

  return <Outlet />;
};

export default PersistAuth;
