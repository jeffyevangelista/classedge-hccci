import z from "zod";

export const createGradingPeriodSchema = z.object({
  academic_term_id: z.number().min(1, "Academic term is required"),
  start_date: z.date({ message: "Start date is required" }),
  end_date: z.date({ message: "End date is required" }),
  grading_period_category_id: z
    .string()
    .min(1, "Grading Period Category is required"),
});

export type CreateGradingPeriodFormValues = z.infer<
  typeof createGradingPeriodSchema
>;
