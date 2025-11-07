import { useNavigate } from "react-router";
import { useEffect, useState } from "react";
import { Button } from "./ui/button";
import { ButtonGroup } from "./ui/button-group";
import { ArrowLeft, ArrowRight } from "lucide-react";

const BackForwardButtons = () => {
  const navigate = useNavigate();
  const [canGoBack, setCanGoBack] = useState(false);
  const [canGoForward, setCanGoForward] = useState(false);

  useEffect(() => {
    const updateNavState = () => {
      setCanGoBack(window.history.state?.idx > 0);
      setCanGoForward(
        typeof window.history.state?.idx === "number" &&
          window.history.length - 1 > window.history.state?.idx
      );
    };

    updateNavState();
    window.addEventListener("popstate", updateNavState);

    return () => window.removeEventListener("popstate", updateNavState);
  }, []);

  return (
    <div className="flex gap-2 md:gap-4">
      <ButtonGroup>
        <Button
          className="rounded-full"
          variant="outline"
          onClick={() => navigate(-1)}
          disabled={!canGoBack}
        >
          <ArrowLeft />
          {/* <span className="hidden md:block">Back</span> */}
        </Button>
        <Button
          className="rounded-full"
          variant="outline"
          onClick={() => navigate(1)}
          disabled={!canGoForward}
        >
          {/* <span className="hidden md:block">Forward</span> */}
          <ArrowRight />
        </Button>
      </ButtonGroup>
    </div>
  );
};

export default BackForwardButtons;
