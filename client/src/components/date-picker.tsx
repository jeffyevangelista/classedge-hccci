"use client";

import * as React from "react";
import { format } from "date-fns";
import { Calendar as CalendarIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Input } from "@/components/ui/input";

interface DatePickerProps {
  value?: Date | null;
  onChange?: (date: Date | null) => void;
  placeholder?: string;
  label?: string;
  disabled?: boolean;
  className?: string;
}

export function DatePickerWithInput({
  value,
  onChange,
  placeholder = "Pick a date",
  disabled,
  className,
}: DatePickerProps) {
  const [open, setOpen] = React.useState(false);
  const [internalValue, setInternalValue] = React.useState<Date | null>(
    value ?? null
  );

  React.useEffect(() => {
    if (value) setInternalValue(value);
  }, [value]);

  const handleSelect = (date: Date | undefined) => {
    const newDate = date ?? null;
    setInternalValue(newDate);
    onChange?.(newDate);
    setOpen(false);
  };

  return (
    <div className={cn("flex flex-col gap-1", className)}>
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <div className="relative">
            <Input
              value={internalValue ? format(internalValue, "PPP") : ""}
              placeholder={placeholder}
              disabled={disabled}
              readOnly
              className={cn("cursor-pointer pr-10", className)}
              onClick={() => setOpen(!open)}
            />
            <CalendarIcon className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          </div>
        </PopoverTrigger>
        <PopoverContent align="start" className="w-auto p-0">
          <Calendar
            mode="single"
            selected={internalValue ?? undefined}
            onSelect={handleSelect}
            initialFocus
          />
        </PopoverContent>
      </Popover>
    </div>
  );
}
