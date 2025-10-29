import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { zodResolver } from "@hookform/resolvers/zod";
import { Controller, useForm } from "react-hook-form";
import {
  forgotPasswordSchema,
  type ForgotPasswordFormValues,
} from "../../auth.schemas";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import { useNavigate } from "react-router";

const ForgotPasswordForm = () => {
  const navigate = useNavigate();
  const {
    handleSubmit,
    control,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: {
      email: "",
    },
  });

  const handleForgotPassword = (data: ForgotPasswordFormValues) => {
    console.log(data);
    navigate("/verify-otp");
  };

  return (
    <form className="space-y-4" onSubmit={handleSubmit(handleForgotPassword)}>
      <Field>
        <FieldLabel className="leading-5" htmlFor="userEmail">
          Email address
        </FieldLabel>
        <Controller
          control={control}
          name="email"
          render={({ field, fieldState }) => (
            <Input
              autoComplete="off"
              id="email"
              placeholder="e.g. juandelacruz@hccci.edu.ph"
              {...field}
              className={
                fieldState.invalid ? "border-red-500 focus:ring-red-500" : ""
              }
            />
          )}
        />
        {errors.email && <FieldError>{errors.email?.message}</FieldError>}
      </Field>

      <Button className="w-full" type="submit">
        Send Reset Link
      </Button>
    </form>
  );
};

export default ForgotPasswordForm;
