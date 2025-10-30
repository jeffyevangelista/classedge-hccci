import { useState } from "react";
import { useMsal } from "@azure/msal-react";
import { InteractionRequiredAuthError } from "@azure/msal-browser";
import { Button } from "@/components/ui/button";
import { Field, FieldLabel } from "@/components/ui/field";
import MSLogo from "@/assets/ms-logo.svg";
import { MICROSOFT_CLIENT_ID, MICROSOFT_TENANT_ID } from "@/utils/env";
import { useMsAuth } from "../auth.hooks";

// 🔧 Configuration
export const msalConfig = {
  auth: {
    clientId: MICROSOFT_CLIENT_ID,
    authority: `https://login.microsoftonline.com/${MICROSOFT_TENANT_ID}`,
    redirectUri: window.location.origin, // safer than hardcoding localhost
  },
};

export const loginRequest = {
  scopes: ["User.Read"],
};

const MSAuthButton = () => {
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const { instance, accounts } = useMsal();
  const { isLoading } = useMsAuth(accessToken);

  const acquireToken = async (account: any) => {
    try {
      const response = await instance.acquireTokenSilent({
        ...loginRequest,
        account,
      });
      setAccessToken(response.accessToken);
      console.log("✅ Microsoft token acquired & sent to backend!");
    } catch (error) {
      if (error instanceof InteractionRequiredAuthError) {
        console.warn("🔄 Silent token failed, trying popup...");
        const loginResponse = await instance.loginPopup(loginRequest);
        const tokenResponse = await instance.acquireTokenSilent({
          ...loginRequest,
          account: loginResponse.account,
        });
        setAccessToken(tokenResponse.accessToken);
      } else {
        console.error("❌ Microsoft Auth Error:", error);
      }
    }
  };

  const handleMicrosoftLogin = async () => {
    try {
      let account = accounts[0];

      // Login if needed
      if (!account) {
        const loginResponse = await instance.loginPopup(loginRequest);
        account = loginResponse.account;
      }

      await acquireToken(account);
    } catch (error) {
      console.error("❌ Microsoft login failed:", error);
    }
  };

  return (
    <Field>
      <FieldLabel>Sign in with</FieldLabel>
      <Button
        variant="outline"
        type="button"
        onClick={handleMicrosoftLogin}
        disabled={isLoading}
        className="flex items-center gap-2"
      >
        <img src={MSLogo} alt="Microsoft logo" className="w-4 h-4" />
        Microsoft
      </Button>
    </Field>
  );
};

export default MSAuthButton;
