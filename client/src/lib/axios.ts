import { API_URL } from "@/utils/env";
import axios from "axios";
import useStore from "./store";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const { accessToken } = useStore.getState();

  if (accessToken) config.headers.Authorization = `Bearer ${accessToken}`;

  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    // if (error.message)
    //   error.message = error.response.data.message ?? error.message;
    return Promise.reject(error);
  }
);

export default api;
