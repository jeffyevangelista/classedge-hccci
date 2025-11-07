import { Button } from "@/components/ui/button";
import { zodResolver } from "@hookform/resolvers/zod";
import { Controller, useForm } from "react-hook-form";
import { verifyOtpSchema, type VerifyOtpFormValues } from "../../auth.schemas";
import {
  Field,
  FieldDescription,
  FieldError,
  FieldGroup,
  FieldLabel,
} from "@/components/ui/field";
import { useNavigate } from "react-router";
import {
  InputOTP,
  InputOTPGroup,
  InputOTPSlot,
} from "@/components/ui/input-otp";

const ForgotPasswordForm = () => {
  const navigate = useNavigate();
  const {
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<VerifyOtpFormValues>({
    resolver: zodResolver(verifyOtpSchema),
    defaultValues: {
      otp: "",
    },
  });

  const handleVerifyOtp = (data: VerifyOtpFormValues) => {
    console.log(data);
    navigate("/reset-password");
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit(handleVerifyOtp)}>
      <FieldGroup>
        <Field>
          <FieldLabel htmlFor="otp" className="sr-only">
            Verification code
          </FieldLabel>
          <Controller
            control={control}
            name="otp"
            render={({ field, fieldState }) => (
              <InputOTP
                id="otp"
                maxLength={6}
                value={field.value ?? ""}
                onChange={(value) => field.onChange(value)}
                aria-invalid={fieldState.invalid}
              >
                <InputOTPGroup className=" mx-auto gap-2.5 *:data-[slot=input-otp-slot]:rounded-md *:data-[slot=input-otp-slot]:border">
                  <InputOTPSlot index={0} />
                  <InputOTPSlot index={1} />
                  <InputOTPSlot index={2} />
                  <InputOTPSlot index={3} />
                  <InputOTPSlot index={4} />
                  <InputOTPSlot index={5} />
                </InputOTPGroup>
              </InputOTP>
            )}
          />
          <FieldDescription className="text-center">
            Enter the 6-digit code sent to your email.
          </FieldDescription>
          {errors.otp && (
            <FieldError className="text-center">
              {errors.otp.message}
            </FieldError>
          )}
        </Field>
        <Button type="submit">Verify</Button>
        <FieldDescription className="text-center">
          Didn&apos;t receive the code?{" "}
          <Button size={"sm"} variant="link">
            Resend
          </Button>
        </FieldDescription>
      </FieldGroup>
    </form>
  );
};

export default ForgotPasswordForm;
