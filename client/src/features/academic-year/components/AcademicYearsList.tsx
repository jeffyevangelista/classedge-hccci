import { Button } from "@/components/ui/button";
import { ButtonGroup } from "@/components/ui/button-group";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import {
  ChevronLeft,
  ChevronRight,
  Eye,
  Loader2,
  RefreshCw,
  Search,
} from "lucide-react";
import { Link } from "react-router";
import CreateAcademicYearModal from "./CreateAcademicYearModal";
import UpdateAcademicYearModal from "./UpdateAcademicYearModal";
import type { AcademicYear } from "../academic-year.types";
import { usePaginatedAcademicYears } from "../academic-year.hooks";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group";
import { memo, useEffect, useState } from "react";
import { useDebounce } from "use-debounce";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

const AcademicYearsList = () => {
  const {
    data,
    isLoading,
    isError,
    error,
    page,
    setPage,
    search,
    isRefetching,
    refetch,
    setSearch,
    pageSize,
    setPageSize,
  } = usePaginatedAcademicYears();

  const [isButtonLoading, setIsButtonLoading] = useState(false);
  const [isSearchIconLoading, setIsSearchIconLoading] = useState(false);

  const [query, setQuery] = useState(search);
  const [debouncedQuery] = useDebounce(query, 500);

  const handleRefreshTable = async () => {
    setIsButtonLoading(true);
    await refetch();
    setIsButtonLoading(false);
  };

  useEffect(() => {
    setSearch(debouncedQuery.trim());
    setPage(1);
  }, [debouncedQuery]);

  if (isLoading) return <SkeletonTable rows={5} columns={4} />;
  if (isError)
    return (
      <Alert variant="destructive">
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>{error.message}</AlertDescription>
      </Alert>
    );

  const { results = [], next, previous, total_pages } = data || {};

  return (
    <div className="space-y-4 border p-5 rounded-md">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="flex items-center gap-2">
            <InputGroup>
              <InputGroupInput
                placeholder="Search..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <InputGroupAddon align={"inline-end"}>
                {isRefetching ? (
                  <Loader2 className="animate-spin text-muted-foreground" />
                ) : (
                  <Search />
                )}
              </InputGroupAddon>
            </InputGroup>
            <Button
              variant="outline"
              onClick={handleRefreshTable}
              disabled={isButtonLoading}
            >
              <RefreshCw className={isButtonLoading ? "animate-spin" : ""} />
            </Button>
          </div>
        </div>
        <CreateAcademicYearModal />
      </div>

      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead className="hidden md:table-cell">Start Date</TableHead>
            <TableHead className="hidden lg:table-cell">End Date</TableHead>
            <TableHead className="text-center">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {results.length > 0 ? (
            results.map((item: AcademicYear) => (
              <AcademicYearRow key={item.id} item={item} />
            ))
          ) : (
            <TableRow>
              <TableCell colSpan={4} className="h-24 text-center">
                No academic years found.
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>

      {/* Pagination */}
      <div className="flex justify-between items-center ">
        <div className="flex items-center gap-2">
          <p>Items per page</p>
          <Select
            value={String(pageSize)}
            onValueChange={(value) => {
              setPageSize(Number(value));
              setPage(1); // Reset to first page when changing page size
            }}
          >
            <SelectTrigger>
              <SelectValue>{pageSize}</SelectValue>
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="5">5</SelectItem>
              <SelectItem value="10">10</SelectItem>
              <SelectItem value="25">25</SelectItem>
              <SelectItem value="50">50</SelectItem>
              <SelectItem value="100">100</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="flex items-center gap-2">
          <p>
            Page {page} of {total_pages}
          </p>

          <ButtonGroup>
            <Button
              size="icon"
              variant="outline"
              disabled={!previous}
              onClick={() => setPage(Math.max(page - 1, 1))}
            >
              <ChevronLeft />
            </Button>

            <Button
              size="icon"
              variant="outline"
              disabled={!next}
              onClick={() => setPage(page + 1)}
            >
              <ChevronRight />
            </Button>
          </ButtonGroup>
        </div>
      </div>
    </div>
  );
};

/* ------------------ AcademicYearRow (Memoized) ------------------ */

const AcademicYearRow = memo(({ item }: { item: AcademicYear }) => {
  return (
    <TableRow className="hover:bg-muted/50 transition-colors">
      <TableCell>{item.name}</TableCell>
      <TableCell className="hidden md:table-cell">{item.start_date}</TableCell>
      <TableCell className="hidden lg:table-cell">{item.end_date}</TableCell>
      <TableCell className="text-center space-x-2">
        <Tooltip>
          <TooltipTrigger asChild>
            <Button asChild variant="outline" size="sm">
              <Link to={`/academic-years/${item.id}`}>
                <Eye className="mr-1 h-4 w-4" />
                <span className="hidden md:inline">View</span>
              </Link>
            </Button>
          </TooltipTrigger>
          <TooltipContent>View details</TooltipContent>
        </Tooltip>
        <UpdateAcademicYearModal academicYear={item} />
      </TableCell>
    </TableRow>
  );
});
AcademicYearRow.displayName = "AcademicYearRow";

/* ------------------ Pagination (Memoized) ------------------ */

interface PaginationProps {
  page: number;
  totalPages: number;
  hasNext: boolean;
  hasPrevious: boolean;
  pageSize: number;
  onPageChange: (newPage: number) => void;
  onPageSizeChange: (value: string) => void;
}

const Pagination = memo(
  ({
    page,
    totalPages,
    hasNext,
    hasPrevious,
    pageSize,
    onPageChange,
    onPageSizeChange,
  }: PaginationProps) => (
    <div className="flex justify-between items-center pt-2">
      <div className="flex items-center gap-2">
        <p>Items per page</p>
        <Select value={String(pageSize)} onValueChange={onPageSizeChange}>
          <SelectTrigger>
            <SelectValue>{pageSize}</SelectValue>
          </SelectTrigger>
          <SelectContent>
            {[5, 10, 25, 50, 100].map((size) => (
              <SelectItem key={size} value={String(size)}>
                {size}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="flex items-center gap-2">
        <p>
          Page {page} of {totalPages}
        </p>

        <ButtonGroup>
          <Button
            size="icon"
            variant="outline"
            disabled={!hasPrevious}
            onClick={() => onPageChange(Math.max(page - 1, 1))}
          >
            <ChevronLeft />
          </Button>

          <Button
            size="icon"
            variant="outline"
            disabled={!hasNext}
            onClick={() => onPageChange(page + 1)}
          >
            <ChevronRight />
          </Button>
        </ButtonGroup>
      </div>
    </div>
  )
);
Pagination.displayName = "Pagination";

/* ------------------ SkeletonTable ------------------ */

interface SkeletonTableProps {
  columns?: number;
  rows?: number;
}

export const SkeletonTable = memo(
  ({ columns = 4, rows = 5 }: SkeletonTableProps) => (
    <div className="border rounded-md p-5 animate-in fade-in-50">
      <Table>
        <TableHeader>
          <TableRow>
            {Array.from({ length: columns }).map((_, i) => (
              <TableHead key={i}>
                <Skeleton
                  style={{ width: `${Math.floor(Math.random() * 50) + 50}%` }}
                  className="h-4"
                />
              </TableHead>
            ))}
          </TableRow>
        </TableHeader>

        <TableBody>
          {Array.from({ length: rows }).map((_, rowIndex) => (
            <TableRow key={rowIndex}>
              {Array.from({ length: columns }).map((_, colIndex) => (
                <TableCell key={colIndex}>
                  <Skeleton className="h-4 w-full" />
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
);
SkeletonTable.displayName = "SkeletonTable";
export default AcademicYearsList;
