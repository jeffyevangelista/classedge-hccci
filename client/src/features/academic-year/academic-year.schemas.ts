import z from "zod";

export const createAcademicYearSchema = z
  .object({
    name: z.string().min(1, "Name is required"),
    start_date: z.date({ message: "Start date is required" }),
    end_date: z.date({ message: "End date is required" }),
  })
  .refine((data) => data.end_date > data.start_date, {
    message: "End date must be after start date (cannot be the same)",
    path: ["end_date"],
  });

export type CreateAcademicYearFormValues = z.infer<
  typeof createAcademicYearSchema
>;
