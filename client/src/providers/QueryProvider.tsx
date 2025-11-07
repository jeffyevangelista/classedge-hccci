import { parseDrfError } from "@/utils/parseDrfError";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { toast } from "sonner";

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
    },
    mutations: {
      onError: (err: any) => handleApiError(err),
    },
  },
});

function handleApiError(err: any) {
  const data = err.response?.data;
  const parsed = parseDrfError(data);

  // Display all errors with field context
  Object.entries(parsed).forEach(([field, errors]) => {
    errors.forEach((msg) => {
      if (field === 'non_field_errors') {
        toast.error(msg);
      } else {
        // Show field name with error message for field-specific errors
        const fieldLabel = field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        toast.error(fieldLabel, { description: msg });
      }
    });
  });
}

const QueryProvider = ({ children }: { children: React.ReactNode }) => {
  return (
    <QueryClientProvider client={queryClient}>
      {children}
      <ReactQueryDevtools />
    </QueryClientProvider>
  );
};

export default QueryProvider;
