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
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { zodResolver } from "@hookform/resolvers/zod";
import { CircleX, Loader, Plus } from "lucide-react";
import { useState } from "react";
import { Controller, useForm } from "react-hook-form";
import { createGradingPeriodSchema } from "../grading-period.schemas";
import type { CreateGradingPeriodFormValues } from "../grading-period.schemas";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import { DatePickerWithInput } from "@/components/date-picker";
import {
  useCreateGradingPeriod,
  useGradingPeriodCategories,
} from "../grading-period.hooks";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface CreateGradingPeriodModalProps {
  academicTermId: number;
}

const CreateGradingPeriodModal = ({
  academicTermId,
}: CreateGradingPeriodModalProps) => {
  const [open, setOpen] = useState(false);
  const [tooltipOpen, setTooltipOpen] = useState(false);

  const {
    mutateAsync: createGradingPeriod,
    isPending,
    isError,
    error,
  } = useCreateGradingPeriod();
  const {
    data: gradingPeriodCategoriesData,
    isLoading: gradingPeriodCategoriesIsLoading,
    isError: gradingPeriodCategoriesIsError,
    error: gradingPeriodCategoriesError,
  } = useGradingPeriodCategories();

  const {
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm<CreateGradingPeriodFormValues>({
    resolver: zodResolver(createGradingPeriodSchema),
    defaultValues: {
      academic_term_id: academicTermId,
      start_date: undefined,
      end_date: undefined,
    },
  });

  const onSubmit = async (data: CreateGradingPeriodFormValues) => {
    await createGradingPeriod(data);
    reset();
    setOpen(false);
  };

  const handleDialogChange = (isOpen: boolean) => {
    setOpen(isOpen);
    if (!isOpen) {
      setTooltipOpen(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={handleDialogChange}>
      <Tooltip open={tooltipOpen} onOpenChange={setTooltipOpen}>
        <TooltipTrigger asChild>
          <DialogTrigger asChild>
            <Button variant="outline" size="sm" className="w-full gap-1">
              <Plus className="size-4 md:mr-2" />
              <span className="hidden md:inline">Grading Period</span>
            </Button>
          </DialogTrigger>
        </TooltipTrigger>
        <TooltipContent>Create a new grading period</TooltipContent>
      </Tooltip>
      <DialogContent className="sm:max-w-[425px]">
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Create Grading Period</DialogTitle>
            <DialogDescription>
              Provide a date range for the new grading period.
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
              <FieldLabel htmlFor="grading-period-category">
                Category
              </FieldLabel>

              {gradingPeriodCategoriesIsLoading ? (
                <Skeleton className="w-full h-10" />
              ) : gradingPeriodCategoriesIsError ? (
                <Alert variant="destructive" className="py-2">
                  <AlertDescription>
                    Failed to load academic years:{" "}
                    {gradingPeriodCategoriesError?.message}
                  </AlertDescription>
                </Alert>
              ) : (
                <Controller
                  control={control}
                  name="grading_period_category_id"
                  render={({ field, fieldState }) => (
                    <Select
                      value={field.value || ""}
                      onValueChange={(value) => field.onChange(value)}
                    >
                      <SelectTrigger
                        className={
                          fieldState.invalid
                            ? "border-red-500 focus:ring-red-500"
                            : ""
                        }
                      >
                        <SelectValue placeholder="Select a category" />
                      </SelectTrigger>
                      <SelectContent>
                        {gradingPeriodCategoriesData?.map((term: any) => (
                          <SelectItem key={term.id} value={String(term.id)}>
                            {term.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  )}
                />
              )}
              {errors.grading_period_category_id && (
                <FieldError>
                  {errors.grading_period_category_id.message}
                </FieldError>
              )}
            </Field>

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

export default CreateGradingPeriodModal;
