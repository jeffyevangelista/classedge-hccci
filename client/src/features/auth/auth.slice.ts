import type { StateCreator } from "zustand";
import { jwtDecode } from "jwt-decode";
import type { AuthUser, DecodedToken } from "./auth.types";

type AuthState = {
  accessToken: string | null;
  isAuthenticated: boolean;
  authUser: AuthUser | null;
  role: string[] | null;
};

type AuthAction = {
  setCredentials: (token: string) => void;
  clearCredentials: () => void;
};

export type AuthSlice = AuthState & AuthAction;

const initialState: AuthState = {
  accessToken: null,
  isAuthenticated: false,
  authUser: null,
  role: null,
};

const createAuthSlice: StateCreator<AuthSlice> = (set) => ({
  ...initialState,
  setCredentials: async (token: string) => {
    const { role, user_id } = jwtDecode<DecodedToken>(token);
    set({
      authUser: { userId: user_id, role },
    });
  },
  clearCredentials: async () => {
    set({ ...initialState });
  },
});

export default createAuthSlice;
