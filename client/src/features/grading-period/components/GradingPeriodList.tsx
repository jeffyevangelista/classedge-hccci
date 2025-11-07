import { Button } from "@/components/ui/button";
import { Pencil } from "lucide-react";
import { useGradingPeriods } from "../grading-period.hooks";

const GradingPeriodList = ({ atId }: { atId: number }) => {
  const { data, isLoading, isError, error } = useGradingPeriods({
    aTermId: atId,
  });

  if (isLoading) return <p>Loading...</p>;
  if (isError) return <p>Error: {error.message}</p>;
  if (!data || data.length === 0)
    return <p className="text-center">No grading periods found</p>;

  return (
    <>
      {data.map((gradingPeriod: any) => (
        <div
          key={gradingPeriod.id}
          className="flex items-center justify-between rounded-md border p-3"
        >
          <div>
            <p className="font-medium">
              {gradingPeriod.grading_period_category}
            </p>
            <p className="text-sm text-muted-foreground">
              {gradingPeriod.start_date} – {gradingPeriod.end_date}
            </p>
          </div>
          <Button size="icon" variant="ghost">
            <Pencil className="h-4 w-4" />
          </Button>
        </div>
      ))}
    </>
  );
};

export default GradingPeriodList;
