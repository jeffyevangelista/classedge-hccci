import { API_URL } from "@/utils/env";
import axios from "axios";
import useStore from "./store";

const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  const { accessToken } = useStore.getState();

  if (accessToken) config.headers.Authorization = `Bearer ${accessToken}`;

  return config;
});

export default api;
