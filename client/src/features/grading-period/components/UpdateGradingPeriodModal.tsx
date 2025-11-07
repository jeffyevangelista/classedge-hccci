import { useState } from "react";
import {
  useGradingPeriodCategories,
  useUpdateGradingPeriod,
} from "../grading-period.hooks";
import {
  updateGradingPeriodSchema,
  type UpdateGradingPeriodFormValues,
} from "../grading-period.schemas";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
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
import { Button } from "@/components/ui/button";

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Controller } from "react-hook-form";
import { Field, FieldError, FieldLabel } from "@/components/ui/field";
import { DatePickerWithInput } from "@/components/date-picker";
import { Skeleton } from "@/components/ui/skeleton";
import { CircleX, Loader, Pencil } from "lucide-react";
import type { GradingPeriod } from "../grading-period.types";

const UpdateGradingPeriodModal = ({
  gradingPeriod,
}: {
  gradingPeriod: GradingPeriod;
}) => {
  const [open, setOpen] = useState(false);
  const [tooltipOpen, setTooltipOpen] = useState(false);

  const {
    mutateAsync: updateGradingPeriod,
    isPending,
    isError,
    error,
  } = useUpdateGradingPeriod();

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
  } = useForm<UpdateGradingPeriodFormValues>({
    resolver: zodResolver(updateGradingPeriodSchema),
    defaultValues: {
      id: Number(gradingPeriod.id),
      academic_term_id: Number(gradingPeriod.academic_term_id),
      start_date: new Date(gradingPeriod.start_date),
      end_date: new Date(gradingPeriod.end_date),
      grading_period_category_id: String(
        gradingPeriod.grading_period_category_id
      ),
    },
  });

  const onSubmit = async (data: UpdateGradingPeriodFormValues) => {
    await updateGradingPeriod(data);
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
            <Button variant="ghost" size="icon">
              <Pencil />
            </Button>
          </DialogTrigger>
        </TooltipTrigger>
        <TooltipContent>Update grading period</TooltipContent>
      </Tooltip>
      <DialogContent className="sm:max-w-[425px]">
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Update Grading Period</DialogTitle>
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

export default UpdateGradingPeriodModal;
