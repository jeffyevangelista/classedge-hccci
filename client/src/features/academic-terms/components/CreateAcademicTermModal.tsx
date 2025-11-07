import { DatePickerWithInput } from "@/components/date-picker";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { CircleX, Plus, Loader } from "lucide-react";
import { useState } from "react";
import {
  useAcademicTermCategories,
  useCreateAcademicTerm,
} from "../academic-terms.hooks";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { zodResolver } from "@hookform/resolvers/zod";
import type { CreateAcademicTermFormValues } from "../academic-terms.schemas";
import { Controller, useForm } from "react-hook-form";
import { createAcademicTermSchema } from "../academic-terms.schemas";
import { Field, FieldLabel, FieldError } from "@/components/ui/field";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface CreateAcademicTermModalProps {
  academicYearId: number;
}

const CreateAcademicTermModal = ({
  academicYearId,
}: CreateAcademicTermModalProps) => {
  const [open, setOpen] = useState(false);
  const [tooltipOpen, setTooltipOpen] = useState(false);
  const {
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm<CreateAcademicTermFormValues>({
    resolver: zodResolver(createAcademicTermSchema),
    defaultValues: {
      academic_year_id: academicYearId,
      academic_term_category_id: undefined,
      start_date: undefined,
      end_date: undefined,
    },
  });

  const {
    mutateAsync: createAcademicTerm,
    isPending,
    isError,
    error,
  } = useCreateAcademicTerm();

  const {
    isLoading: academicTermIsLoading,
    isError: academicTermIsError,
    error: academicTermError,
    data: academicTermsData,
  } = useAcademicTermCategories();

  const handleDialogChange = (isOpen: boolean) => {
    setOpen(isOpen);
    if (!isOpen) {
      setTooltipOpen(false);
    }
  };

  const onSubmit = async (data: CreateAcademicTermFormValues) => {
    await createAcademicTerm(data);
    console.log(data);

    reset();

    setOpen(false);
  };

  return (
    <Dialog open={open} onOpenChange={handleDialogChange}>
      <Tooltip open={tooltipOpen} onOpenChange={setTooltipOpen}>
        <TooltipTrigger asChild>
          <DialogTrigger asChild>
            <Button variant="default" className="size-9 md:size-auto md:px-4">
              <Plus className="size-4 md:mr-2" />
              <span className="hidden md:inline">Academic Term</span>
            </Button>
          </DialogTrigger>
        </TooltipTrigger>
        <TooltipContent>Create a new academic term</TooltipContent>
      </Tooltip>

      <DialogContent className="sm:max-w-[425px]">
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Create Academic Term</DialogTitle>
            <DialogDescription>
              Provide a date range for the new academic term.
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            {isError && (
              <Alert variant="destructive" className="items-center">
                <CircleX />
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>{error.message}</AlertDescription>
              </Alert>
            )}
            <Field>
              <FieldLabel htmlFor="academic-year">Category</FieldLabel>

              {academicTermIsLoading ? (
                <Skeleton className="w-full h-10" />
              ) : academicTermIsError ? (
                <Alert variant="destructive" className="py-2">
                  <AlertDescription>
                    Failed to load academic years: {academicTermError?.message}
                  </AlertDescription>
                </Alert>
              ) : (
                <Controller
                  control={control}
                  name="academic_term_category_id"
                  render={({ field, fieldState }) => (
                    <Select
                      value={field.value || ""}
                      onValueChange={(value) => field.onChange(value)}
                    >
                      <SelectTrigger
                        className={fieldState.invalid ? "border-red-500" : ""}
                      >
                        <SelectValue placeholder="Select a category" />
                      </SelectTrigger>
                      <SelectContent>
                        {academicTermsData?.map((term: any) => (
                          <SelectItem key={term.id} value={String(term.id)}>
                            {term.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  )}
                />
              )}
              {errors.academic_term_category_id && (
                <FieldError>
                  {errors.academic_term_category_id.message}
                </FieldError>
              )}
            </Field>

            {/* Start Date */}
            <Field>
              <FieldLabel htmlFor="year-start-1">Start Date</FieldLabel>
              <Controller
                control={control}
                name="start_date"
                render={({ field, fieldState }) => (
                  <DatePickerWithInput
                    value={field.value}
                    onChange={(e) => field.onChange(e ?? undefined)}
                    className={
                      fieldState.invalid
                        ? "border-red-500 focus:ring-red-500"
                        : ""
                    }
                  />
                )}
              />
              {errors.start_date && (
                <FieldError>{errors.start_date.message}</FieldError>
              )}
            </Field>

            {/* End Date */}
            <Field>
              <FieldLabel htmlFor="year-end-1">End Date</FieldLabel>
              <Controller
                control={control}
                name="end_date"
                render={({ field, fieldState }) => (
                  <DatePickerWithInput
                    value={field.value}
                    onChange={(e) => field.onChange(e ?? undefined)}
                    className={
                      fieldState.invalid
                        ? "border-red-500 focus:ring-red-500"
                        : ""
                    }
                  />
                )}
              />
              {errors.end_date && (
                <FieldError>{errors.end_date.message}</FieldError>
              )}
            </Field>
          </div>

          <DialogFooter>
            <Button className="w-full" type="submit" disabled={isPending}>
              {isPending ? (
                <>
                  <Loader className="animate-spin" />
                  Submitting...
                </>
              ) : (
                "Submit"
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default CreateAcademicTermModal;
