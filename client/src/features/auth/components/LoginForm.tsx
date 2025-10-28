import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Field,
  FieldError,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import MSLogo from "@/assets/ms-logo.svg";
import { Link, useNavigate } from "react-router";
import { useLogin } from "../auth.hooks";
import { Loader } from "lucide-react";
import ReCAPTCHA from "react-google-recaptcha";
import { SITE_KEY } from "@/utils/env";
import { Controller, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema, type LoginFormValues } from "../auth.schemas";
import type { LoginCredentials } from "../auth.types";

export function LoginForm() {
  const navigate = useNavigate();
  const { mutateAsync: login, isPending } = useLogin();

  const {
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<LoginCredentials>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
      recaptcha: "",
    },
  });

  const handleLogin = async (data: LoginFormValues) => {
    await login({ ...data, recaptcha: "dev-bypass-token" });

    navigate("/dashboard");
  };

  return (
    <form autoComplete="off" onSubmit={handleSubmit(handleLogin)}>
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Welcome to Classedge</h1>
          <p className="text-muted-foreground text-sm text-balance">
            A learning Platform of HCCCI
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="email">Email</FieldLabel>
          <Controller
            control={control}
            name="email"
            render={({ field, fieldState }) => (
              <Input
                autoComplete="off"
                id="email"
                placeholder="juandelacruz@hccci.edu.ph"
                {...field}
                className={
                  fieldState.invalid ? "border-red-500 focus:ring-red-500" : ""
                }
              />
            )}
          />
          {errors.email && <FieldError>{errors.email?.message}</FieldError>}
        </Field>
        <Field>
          <FieldLabel htmlFor="password">Password</FieldLabel>
          <Controller
            control={control}
            name="password"
            render={({ field, fieldState }) => (
              <Input
                id="password"
                type="password"
                {...field}
                className={
                  fieldState.invalid ? "border-red-500 focus:ring-red-500" : ""
                }
              />
            )}
          />
          {errors.password && (
            <FieldError>{errors.password?.message}</FieldError>
          )}
          <div className="flex items-center">
            <Link
              to="/forgot-password"
              className="ml-auto text-sm underline-offset-4 hover:underline"
            >
              Forgot your password?
            </Link>
          </div>
        </Field>

        <Field>
          <div className="flex justify-center">
            <Controller
              control={control}
              name="recaptcha"
              render={({ field }) => (
                <ReCAPTCHA sitekey={SITE_KEY} {...field} />
              )}
            />
          </div>
          {errors.recaptcha && (
            <FieldError>{errors.recaptcha?.message}</FieldError>
          )}
        </Field>

        <Field>
          <Button type="submit" disabled={isPending}>
            {isPending ? <Loader className="animate-spin" /> : "Login"}
          </Button>
        </Field>
        <FieldSeparator>or continue with</FieldSeparator>
        <Field>
          <Button
            variant="outline"
            type="button"
            onClick={() => navigate("/dashboard")}
          >
            <img src={MSLogo} alt="ms-logo" className="size-4" />
            Microsoft
          </Button>
        </Field>
      </FieldGroup>
    </form>
  );
}
