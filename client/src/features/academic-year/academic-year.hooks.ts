import {
  keepPreviousData,
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import {
  createAcademicYear,
  getAcademicYear,
  getAcademicYears,
  getPaginatedAcademicYears,
  updateAcademicYear,
} from "./academic-year.apis";
import type { CreateAcademicYearFormValues } from "./academic-year.schemas";
import { useParams, useSearchParams } from "react-router";

export const usePaginatedAcademicYears = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  const page = Number(searchParams.get("page") || 1);
  const search = searchParams.get("search") || "";
  const pageSize = Number(searchParams.get("page_size") || 10);

  const query = useQuery({
    queryKey: ["academic-years", page, pageSize, search],
    queryFn: () => getPaginatedAcademicYears(page, pageSize, search),
    placeholderData: keepPreviousData,
  });

  const setPage = (p: number) => {
    searchParams.set("page", String(p));
    setSearchParams(searchParams);
  };

  const setSearch = (term: string) => {
    if (term.trim() === "") {
      searchParams.delete("search");
    } else {
      searchParams.set("search", term);
    }
    searchParams.set("page", "1"); // reset page when filtering
    setSearchParams(searchParams);
  };

  const setPageSize = (size: number) => {
    searchParams.set("page_size", String(size));
    setSearchParams(searchParams);
  };

  return { ...query, page, search, pageSize, setPage, setSearch, setPageSize };
};

export const useAcademicYears = () => {
  return useQuery({
    queryKey: ["academic-years"],
    queryFn: () => getAcademicYears(),
    placeholderData: keepPreviousData,
  });
};

export const useAcademicYear = () => {
  const { ayId } = useParams();

  return useQuery({
    queryKey: ["academic-year", ayId],
    queryFn: () => getAcademicYear(ayId || ""),
    placeholderData: keepPreviousData,
    enabled: !!ayId,
  });
};

export const useCreateAcademicYear = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationKey: ["create-academic-year"],
    mutationFn: (payload: CreateAcademicYearFormValues) =>
      createAcademicYear(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["academic-years"] });
    },
  });
};

export const useUpdateAcademicYear = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationKey: ["update-academic-year"],
    mutationFn: ({
      id,
      payload,
    }: {
      id: number;
      payload: CreateAcademicYearFormValues;
    }) => updateAcademicYear(id, payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["academic-years"] });
      queryClient.invalidateQueries({ queryKey: ["academic-year"] });
    },
  });
};
