import { API_URL } from "@/utils/env";
import axios from "axios";
import useStore from "./store";
import { refresh } from "@/features/auth/auth.apis";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const accessToken = useStore.getState().accessToken;

  if (accessToken) config.headers.Authorization = `Bearer ${accessToken}`;

  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const { accessToken, setCredentials, clearCredentials } =
      useStore.getState();
    if (
      (error.response.status == 401 || error.response.status == 403) &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;

      if (accessToken) {
        try {
          const { access } = await refresh();
          setCredentials(access);
          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        } catch (error) {
          console.log("Session expired");
          clearCredentials();
          return Promise.reject(error);
        }
      }
    }

    if (error.message) {
      error.message = error.response.data.detail ?? error.message;
    }

    return Promise.reject(error);
  }
);

export default api;
