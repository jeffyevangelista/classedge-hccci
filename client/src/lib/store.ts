import type { AuthSlice } from "@/features/auth/auth.slice";
import createAuthSlice from "@/features/auth/auth.slice";
import type { UserSlice } from "@/features/user/user.slice";
import createUserSlice from "@/features/user/user.slice";
import { create } from "zustand";
import { devtools } from "zustand/middleware";

type store = AuthSlice & UserSlice;

const useStore = create<store>()(
  devtools((...a) => ({
    ...createAuthSlice(...a),
    ...createUserSlice(...a),
  }))
);

export default useStore;
