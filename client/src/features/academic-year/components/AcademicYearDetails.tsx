import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useAcademicYear } from "../academic-year.hooks";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import UpdateAcademicYearModal from "./UpdateAcademicYearModal";

const AcademicYearDetails = () => {
  const { data, isLoading, isError, error } = useAcademicYear();

  if (isLoading) return <p>loading...</p>;

  if (isError) return <div>Error: {error.message}</div>;

  return (
    <div>
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Academic Year: {data.name}</CardTitle>
              <CardDescription>
                {data.start_date} – {data.end_date}
              </CardDescription>
            </div>
            <Badge variant="default">Active</Badge>
          </div>
        </CardHeader>
        <CardFooter className="flex gap-2 justify-end">
          <UpdateAcademicYearModal academicYear={data} />
          <Button variant="destructive">Deactivate</Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default AcademicYearDetails;
