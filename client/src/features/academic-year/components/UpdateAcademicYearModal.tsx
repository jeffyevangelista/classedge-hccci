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
import { Input } from "@/components/ui/input";
import { CircleX, Pencil } from "lucide-react";
import { useState } from "react";
import { useUpdateAcademicYear } from "../academic-year.hooks";
import { Loader } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { zodResolver } from "@hookform/resolvers/zod";
import type { CreateAcademicYearFormValues } from "../academic-year.schemas";
import { Controller, useForm } from "react-hook-form";
import { createAcademicYearSchema } from "../academic-year.schemas";
import { Field, FieldLabel, FieldError } from "@/components/ui/field";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import type { AcademicYear } from "../academic-year.types";

const UpdateAcademicYearModal = ({
  academicYear,
}: {
  academicYear: AcademicYear;
}) => {
  const [open, setOpen] = useState(false);
  const [tooltipOpen, setTooltipOpen] = useState(false);
  const {
    handleSubmit,
    control,
    reset,
    formState: { errors },
  } = useForm<CreateAcademicYearFormValues>({
    resolver: zodResolver(createAcademicYearSchema),
    defaultValues: {
      name: academicYear.name,
      start_date: new Date(academicYear.start_date),
      end_date: new Date(academicYear.end_date),
    },
  });
  const {
    mutateAsync: updateAcademicYear,
    isPending,
    isError,
    error,
  } = useUpdateAcademicYear();

  const onSubmit = async (data: CreateAcademicYearFormValues) => {
    await updateAcademicYear({
      id: academicYear.id,
      payload: data,
    });

    // Reset form to original academic year values
    reset({
      name: academicYear.name,
      start_date: new Date(academicYear.start_date),
      end_date: new Date(academicYear.end_date),
    });

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
      <Tooltip
        open={tooltipOpen}
        onOpenChange={setTooltipOpen}
        delayDuration={150}
      >
        <TooltipTrigger asChild>
          <DialogTrigger asChild>
            <Button
              className="cursor-pointer"
              variant={"ghost"}
              onFocus={() => setTooltipOpen(false)} // prevent focus re-opening
            >
              <Pencil />
              <span className="hidden md:block">Edit</span>
            </Button>
          </DialogTrigger>
        </TooltipTrigger>
        <TooltipContent>Edit academic year</TooltipContent>
      </Tooltip>

      <DialogContent className="sm:max-w-[425px]">
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Update Academic Year</DialogTitle>
            <DialogDescription>
              Provide a name and date range for the academic year.
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
              <FieldLabel htmlFor="name-1">Name</FieldLabel>
              <Controller
                control={control}
                name="name"
                render={({ field, fieldState }) => (
                  <Input
                    id="name-1"
                    {...field}
                    className={
                      fieldState.invalid
                        ? "border-red-500 focus:ring-red-500"
                        : ""
                    }
                  />
                )}
              />
              {errors.name && <FieldError>{errors.name?.message}</FieldError>}
            </Field>
            <Field>
              <FieldLabel htmlFor="year-start-1">Start Date</FieldLabel>
              <Controller
                control={control}
                name="start_date"
                render={({ field, fieldState }) => (
                  <DatePickerWithInput
                    value={field.value}
                    onChange={(e) => field.onChange(e)}
                    className={
                      fieldState.invalid
                        ? "border-red-500 focus:ring-red-500"
                        : ""
                    }
                  />
                )}
              />
              {errors.start_date && (
                <FieldError>{errors.start_date?.message}</FieldError>
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
                    onChange={(e) => field.onChange(e)}
                    className={
                      fieldState.invalid
                        ? "border-red-500 focus:ring-red-500"
                        : ""
                    }
                  />
                )}
              />
              {errors.end_date && (
                <FieldError>{errors.end_date?.message}</FieldError>
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

export default UpdateAcademicYearModal;
