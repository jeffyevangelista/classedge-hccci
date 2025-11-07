export type AcademicTerm = {
  id: number;
  academic_term_category_id: number;
  academic_term_category: string;
  academic_year_id: number;
  academic_year: string;
  calculation_method: string;
  start_date: string; // ISO date string (e.g., "2025-01-01")
  end_date: string; // ISO date string (e.g., "2025-12-30")
  created_at: string; // ISO timestamp (e.g., "2025-11-05T14:09:31.082467+08:00")
  updated_at: string | null;
};
