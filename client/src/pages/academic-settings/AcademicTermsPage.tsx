import AcademicTermsList from "@/features/academic-terms/components/AcademicTermsList";

const AcademicTermsPage = () => {
  return (
    <div>
      <div className="flex justify-between items-center border">
        <p>AcademicTerms</p>
      </div>
      <AcademicTermsList />
    </div>
  );
};

export default AcademicTermsPage;
