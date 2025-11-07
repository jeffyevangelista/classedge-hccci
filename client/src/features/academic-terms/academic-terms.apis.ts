import api from "@/lib/axios";
import type {
  CreateAcademicTermFormValues,
  UpdateAcademicTermFormValues,
} from "./academic-terms.schemas";

export const getAcademicTerms = async (acadYearId: number) => {
  return (await api.get(`/academic-terms/?academic_year_id=${acadYearId}`))
    .data;
};

export const getAcademicTermCategories = async () => {
  return (await api.get(`/academic-term-categories/all/`)).data;
};

export const createAcademicTerm = async (
  data: CreateAcademicTermFormValues
) => {
  const payload = {
    ...data,
    start_date: data.start_date.toLocaleDateString("en-CA"),
    end_date: data.end_date.toLocaleDateString("en-CA"),
  };

  return (await api.post("/academic-terms/", payload)).data;
};

export const updateAcademicTerm = async (
  data: UpdateAcademicTermFormValues
) => {
  const payload = {
    ...data,
    start_date: data.start_date.toLocaleDateString("en-CA"),
    end_date: data.end_date.toLocaleDateString("en-CA"),
  };

  return (await api.put(`/academic-terms/${data.id}/`, payload)).data;
};
