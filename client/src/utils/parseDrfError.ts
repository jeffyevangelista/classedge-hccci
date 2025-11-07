// src/lib/parseDrfError.ts
export function parseDrfError(errorData: any) {
  const result: Record<string, string[]> = {};

  if (!errorData) return result;

  if (typeof errorData === "string") {
    result.non_field_errors = [errorData];
    return result;
  }

  if (Array.isArray(errorData)) {
    result.non_field_errors = errorData.flatMap((e) =>
      typeof e === "string" ? [e] : Object.values(parseDrfError(e)).flat()
    );
    return result;
  }

  if (errorData.detail) {
    result.non_field_errors = [errorData.detail];
  }

  Object.entries(errorData).forEach(([key, val]) => {
    if (key === "detail") return;

    if (typeof val === "string") {
      result[key] = [val];
    } else if (Array.isArray(val)) {
      result[key] = val.map(String);
    } else if (typeof val === "object" && val !== null) {
      result[key] = Object.values(parseDrfError(val)).flat();
    }
  });

  return result;
}
