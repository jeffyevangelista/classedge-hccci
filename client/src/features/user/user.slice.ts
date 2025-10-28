import type { StateCreator } from "zustand";
import { persist } from "zustand/middleware";

type UserState = {
  user: any | null;
};

type UserAction = {
  setUser: (user: any) => void;
  clearUser: () => void;
};

export type UserSlice = UserState & UserAction;

const initialState = {
  user: null,
};

const createUserSlice: StateCreator<
  UserSlice,
  [],
  [["zustand/persist", UserSlice]]
> = persist(
  (set) => ({
    ...initialState,
    setUser: (user: any) => set({ user }),
    clearUser: () => set({ user: null }),
  }),
  {
    name: "user",
  }
);

export default createUserSlice;
