import {
  keepPreviousData,
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import {
  createAcademicTerm,
  getAcademicTermCategories,
  getAcademicTerms,
  updateAcademicTerm,
} from "./academic-terms.apis";
import type {
  CreateAcademicTermFormValues,
  UpdateAcademicTermFormValues,
} from "./academic-terms.schemas";

export const useAcademicTerms = ({ ayId }: { ayId: number }) => {
  return useQuery({
    queryKey: ["academic-terms", ayId],
    queryFn: () => getAcademicTerms(ayId),
    placeholderData: keepPreviousData,
  });
};

export const useAcademicTermCategories = () => {
  return useQuery({
    queryKey: ["academic-term-categories"],
    queryFn: () => getAcademicTermCategories(),
  });
};

export const useCreateAcademicTerm = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["create-academic-term"],
    mutationFn: (payload: CreateAcademicTermFormValues) =>
      createAcademicTerm(payload),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["academic-terms", data.academic_year_id],
      });
    },
  });
};

export const useUpdateAcademicTerm = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: ["update-academic-term"],
    mutationFn: (payload: UpdateAcademicTermFormValues) =>
      updateAcademicTerm(payload),
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["academic-terms", data.academic_year_id],
      });
    },
  });
};
