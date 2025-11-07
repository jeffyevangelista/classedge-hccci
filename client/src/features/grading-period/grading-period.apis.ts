import api from "@/lib/axios";
import type {
  CreateGradingPeriodFormValues,
  UpdateGradingPeriodFormValues,
} from "./grading-period.schemas";

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

export const updateGradingPeriod = async (
  data: UpdateGradingPeriodFormValues
) => {
  const payload = {
    ...data,
    start_date: data.start_date.toLocaleDateString("en-CA"),
    end_date: data.end_date.toLocaleDateString("en-CA"),
  };
  return (await api.patch(`/grading-periods/${data.id}/`, payload)).data;
};
