import api from "@/lib/axios";
import type { CreateAcademicYearFormValues } from "./academic-year.schemas";

export const getAcademicYears = async () => {
  return (await api.get(`/academic-years/all/`)).data;
};

export const getAcademicYear = async (id: string) => {
  return (await api.get(`/academic-years/${id}/`)).data;
};

export const getPaginatedAcademicYears = async (
  page: number,
  pageSize: number,
  search: string
) => {
  return (
    await api.get(
      `/academic-years/?page=${page}&page_size=${pageSize}&search=${search}`
    )
  ).data;
};

export const createAcademicYear = async (
  data: CreateAcademicYearFormValues
) => {
  const payload = {
    ...data,
    start_date: data.start_date.toLocaleDateString("en-CA"),
    end_date: data.end_date.toLocaleDateString("en-CA"),
  };
  return (await api.post("/academic-years/", payload)).data;
};

export const updateAcademicYear = async (
  id: number,
  data: CreateAcademicYearFormValues
) => {
  const payload = {
    ...data,
    start_date: data.start_date.toLocaleDateString("en-CA"),
    end_date: data.end_date.toLocaleDateString("en-CA"),
  };
  return (await api.put(`/academic-years/${id}/`, payload)).data;
};
