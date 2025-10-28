import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import {
  Field,
  FieldGroup,
  FieldLabel,
  FieldSeparator,
} from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import MSLogo from "@/assets/ms-logo.svg";
import { Link, useNavigate } from "react-router";
import { useState } from "react";
import { useLogin } from "../auth.hooks";
import { Loader } from "lucide-react";

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"form">) {
  const navigate = useNavigate();
  const { mutateAsync: login, isPending } = useLogin();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await login({
      email: email,
      password: password,
    });
    navigate("/dashboard");
  };

  return (
    <form
      autoComplete="off"
      onSubmit={handleLogin}
      className={cn("flex flex-col gap-6", className)}
      {...props}
    >
      <FieldGroup>
        <div className="flex flex-col items-center gap-1 text-center">
          <h1 className="text-2xl font-bold">Welcome to Classedge</h1>
          <p className="text-muted-foreground text-sm text-balance">
            A learning Platform of HCCCI
          </p>
        </div>
        <Field>
          <FieldLabel htmlFor="email">Email</FieldLabel>
          <Input
            autoComplete="off"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            id="email"
            type="email"
            placeholder="m@example.com"
            required
          />
        </Field>
        <Field>
          <FieldLabel htmlFor="password">Password</FieldLabel>

          <Input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            id="password"
            type="password"
            required
          />
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
