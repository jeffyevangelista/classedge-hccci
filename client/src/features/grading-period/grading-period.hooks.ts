import {
  keepPreviousData,
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import {
  getGradingPeriodCategories,
  getGradingPeriods,
  updateGradingPeriod,
} from "./grading-period.apis";
import { createGradingPeriod } from "./grading-period.apis";
import type {
  CreateGradingPeriodFormValues,
  UpdateGradingPeriodFormValues,
} from "./grading-period.schemas";

export const useGradingPeriodCategories = () => {
  return useQuery({
    queryKey: ["grading-period-categories"],
    queryFn: () => getGradingPeriodCategories(),
    placeholderData: keepPreviousData,
  });
};

export const useGradingPeriods = ({ aTermId }: { aTermId: number }) => {
  return useQuery({
    queryKey: ["grading-periods", aTermId],
    queryFn: () => getGradingPeriods(aTermId),
    placeholderData: keepPreviousData,
  });
};

export const useCreateGradingPeriod = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateGradingPeriodFormValues) =>
      createGradingPeriod(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["grading-periods", data.academic_term_id],
      });
    },
  });
};

export const useUpdateGradingPeriod = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: UpdateGradingPeriodFormValues) =>
      updateGradingPeriod(data),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["grading-periods", data.academic_term_id],
      });
    },
  });
};
