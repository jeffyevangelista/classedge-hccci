import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import GradingPeriodList from "./GradingPeriodList";
import CreateGradingPeriodModal from "./CreateGradingPeriodModal";

const GradingPeriod = ({ academicTermId }: { academicTermId: number }) => {
  return (
    <Accordion type="single" collapsible>
      <AccordionItem value="grading-periods">
        <AccordionTrigger>Grading Periods</AccordionTrigger>
        <AccordionContent>
          <div className="space-y-3">
            <GradingPeriodList atId={academicTermId} />

            <CreateGradingPeriodModal academicTermId={academicTermId} />
          </div>
        </AccordionContent>
      </AccordionItem>
    </Accordion>
  );
};

export default GradingPeriod;
