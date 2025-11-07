import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import GradingPeriod from "@/features/grading-period/components/GradingPeriod";
import { useAcademicTerms } from "../academic-terms.hooks";
import type { AcademicTerm } from "../academic-terms.types";
import UpdateAcademicTermModal from "./UpdateAcademicTermModal";

const AcademicTermsList = ({ ayId }: { ayId: number }) => {
  const { data, isLoading, isError, error } = useAcademicTerms({ ayId });

  if (isLoading) return <p>Loading...</p>;
  if (isError) return <p>Error: {error.message}</p>;
  if (!data || data.length === 0)
    return <p className="text-center">No academic terms found</p>;

  return (
    <>
      {data.map((academicTerm: AcademicTerm) => (
        <Card key={academicTerm.id}>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>{academicTerm.academic_term_category}</CardTitle>
                <CardDescription>
                  {academicTerm.start_date} – {academicTerm.end_date}
                </CardDescription>
              </div>
              <UpdateAcademicTermModal academicTerm={academicTerm} />
            </div>
          </CardHeader>

          <CardContent>
            <GradingPeriod academicTermId={academicTerm.id} />
          </CardContent>
        </Card>
      ))}
    </>
  );
};

export default AcademicTermsList;
