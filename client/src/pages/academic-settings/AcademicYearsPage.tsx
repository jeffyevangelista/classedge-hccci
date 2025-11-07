import BackForwardButtons from "@/components/back-forward-buttons";
import Breadcrumbs from "@/components/breadcrumbs";
import AcademicYearsList from "@/features/academic-year/components/AcademicYearsList";

const AcademicYearsPage = () => {
  return (
    <div>
      <div className="flex justify-between items-center">
        <BackForwardButtons />
        <Breadcrumbs />
      </div>

      <AcademicYearsList />
    </div>
  );
};

export default AcademicYearsPage;
