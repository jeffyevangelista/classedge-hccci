import { Calendar } from "lucide-react";
import AcademicTermsList from "./AcademicTermsList";
import CreateAcademicTermModal from "./CreateAcademicTermModal";
import { useParams } from "react-router";

const AcademicTerms = () => {
  const { ayId } = useParams();
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-medium flex items-center gap-2">
          <Calendar className="h-5 w-5 text-muted-foreground" />
          Academic Terms
        </h2>
        <CreateAcademicTermModal academicYearId={Number(ayId)} />
      </div>

      <AcademicTermsList ayId={Number(ayId)} />
    </div>
  );
};

export default AcademicTerms;
