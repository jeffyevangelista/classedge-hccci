import z from "zod";

export const createAcademicTermSchema = z
  .object({
    academic_year_id: z.number().min(1, "Academic year is required"),
    academic_term_category_id: z
      .string()
      .min(1, "Semester Category is required"),
    start_date: z.date({ message: "Start date is required" }),
    end_date: z.date({ message: "End date is required" }),
  })
  .refine((data) => data.end_date > data.start_date, {
    message: "End date must be after start date (cannot be the same)",
    path: ["end_date"],
  });

export const updateAcademicTermSchema = z.object({
  id: z.number().min(1, "Academic Term ID is required"),
  academic_year_id: z.number().min(1, "Academic Year is required"),
  academic_term_category_id: z.string().min(1, "Semester Category is required"),
  start_date: z.date({ message: "Start date is required" }),
  end_date: z.date({ message: "End date is required" }),
});

export type CreateAcademicTermFormValues = z.infer<
  typeof createAcademicTermSchema
>;

export type UpdateAcademicTermFormValues = z.infer<
  typeof updateAcademicTermSchema
>;
