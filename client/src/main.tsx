import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { BrowserRouter } from "react-router";
import QueryProvider from "./providers/QueryProvider.tsx";
import ToastProvider from "./providers/ToastProvider.tsx";
import { MsalProvider } from "@azure/msal-react";
import { PublicClientApplication } from "@azure/msal-browser";
import { msalConfig } from "./features/auth/components/MSAuthButton.tsx";

const msalInstance = new PublicClientApplication(msalConfig);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      <MsalProvider instance={msalInstance}>
        <QueryProvider>
          <ToastProvider>
            <App />
          </ToastProvider>
        </QueryProvider>
      </MsalProvider>
    </BrowserRouter>
  </StrictMode>
);
