import api from "@/lib/axios";

export const getUserDetails = async (userId: string) => {
  return (await api.get(`/profile/me/${userId}`)).data;
};
