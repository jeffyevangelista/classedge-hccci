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
} from "./academic-terms.apis";
import type { CreateAcademicTermFormValues } from "./academic-terms.schemas";
import { useParams } from "react-router";

export const useAcademicTerms = () => {
  const { ayId } = useParams();

  return useQuery({
    queryKey: ["academic-terms", ayId],
    queryFn: () => getAcademicTerms(Number(ayId)),
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
  const { ayId } = useParams();

  return useMutation({
    mutationKey: ["create-academic-term", ayId],
    mutationFn: (payload: CreateAcademicTermFormValues) =>
      createAcademicTerm(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["academic-terms", ayId] });
    },
  });
};
