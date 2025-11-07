import BackForwardButtons from "@/components/back-forward-buttons";
import Breadcrumbs from "@/components/breadcrumbs";
import AcademicTerms from "@/features/academic-terms/components/AcademicTerms";
import AcademicYearDetails from "@/features/academic-year/components/AcademicYearDetails";

const AcademicYearDetailsPage = () => {
  return (
    <div className="flex flex-col space-y-7.5">
      <div className="flex justify-between">
        <BackForwardButtons />
        <Breadcrumbs />
      </div>
      <AcademicYearDetails />
      <AcademicTerms />
    </div>
  );
};

export default AcademicYearDetailsPage;
