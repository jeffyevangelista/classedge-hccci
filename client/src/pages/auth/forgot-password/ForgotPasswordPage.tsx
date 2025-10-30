import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import SchoolLogo from "@/assets/school-logo.png";
import ForgotPasswordForm from "@/features/auth/components/forgot-password/ForgotPasswordForm";
import { Link } from "react-router";
import { Button } from "@/components/ui/button";

const ForgotPasswordPage = () => {
  return (
    <div className="relative flex h-auto min-h-screen items-center justify-center overflow-x-hidden px-4 py-10 sm:px-6 lg:px-8">
      <Card className="z-1 w-full border-none shadow sm:max-w-md">
        <CardHeader className="gap-6">
          <div className="flex items-center justify-center sm:justify-start gap-2">
            <img className="size-9" src={SchoolLogo} alt="School Logo" />
            <span className="text-sm font-semibold hidden sm:block">
              Holy Child Central Colleges Inc.
            </span>
          </div>

          <div>
            <CardTitle className="mb-1.5 text-2xl">Forgot Password?</CardTitle>
            <CardDescription className="text-base">
              Enter your email to receive an OTP for password reset.
            </CardDescription>
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          <ForgotPasswordForm />

          <Link to="/" className="group mx-auto flex w-fit items-center gap-2">
            <Button variant={"link"}>Back to login</Button>
          </Link>
        </CardContent>
      </Card>
    </div>
  );
};

export default ForgotPasswordPage;
