import useStore from "@/lib/store";
import { useQuery } from "@tanstack/react-query";
import { jwtDecode } from "jwt-decode";
import { getUserDetails } from "./user.apis";

export const useProfileDetails = () => {
  const { accessToken } = useStore.getState();

  const { data: user } = useQuery({
    queryKey: ["user"],
    queryFn: async () => {
      const { userId } = jwtDecode<{ userId: string }>(accessToken!);
      const res = await getUserDetails(userId);
      return res;
    },
    enabled: !!accessToken,
  });
  return user;
};
