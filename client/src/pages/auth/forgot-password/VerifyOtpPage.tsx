import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import SchoolLogo from "@/assets/school-logo.png";
import VerifyOtpForm from "@/features/auth/components/forgot-password/VerifyOtpForm";

const VerifyOtpPage = () => {
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
            <CardTitle className="mb-1.5 text-2xl">Check your email</CardTitle>
            <CardDescription className="text-base">
              We have sent an OTP to your email. Please enter it below to reset
              your password.
            </CardDescription>
          </div>
        </CardHeader>

        <CardContent className="space-y-4">
          <VerifyOtpForm />
        </CardContent>
      </Card>
    </div>
  );
};

export default VerifyOtpPage;
