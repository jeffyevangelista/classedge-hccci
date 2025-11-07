import api from "@/lib/axios";
import type { CreateGradingPeriodFormValues } from "./grading-period.schemas";

export const getGradingPeriodCategories = async () => {
  return (await api.get("/grading-period-categories/all/")).data;
};

export const getGradingPeriods = async (id: number) => {
  return (await api.get(`/grading-periods/?academic_term_id=${id}`)).data;
};

export const createGradingPeriod = async (
  data: CreateGradingPeriodFormValues
) => {
  const payload = {
    ...data,
    start_date: data.start_date.toLocaleDateString("en-CA"),
    end_date: data.end_date.toLocaleDateString("en-CA"),
  };
  return (await api.post("/grading-periods/", payload)).data;
};
