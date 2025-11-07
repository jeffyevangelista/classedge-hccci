import { useGradingPeriods } from "../grading-period.hooks";
import UpdateGradingPeriodModal from "./UpdateGradingPeriodModal";

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
          <UpdateGradingPeriodModal gradingPeriod={gradingPeriod} />
        </div>
      ))}
    </>
  );
};

export default GradingPeriodList;
