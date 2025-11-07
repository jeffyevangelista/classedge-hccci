"use client";

import { useState, useEffect, useRef } from "react";
import { Plus, Edit, Trash2, Share2 } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function SpeedDial() {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  const actions = [
    {
      icon: <Edit size={16} />,
      label: "Edit",
      onClick: () => alert("Edit clicked"),
    },
    {
      icon: <Share2 size={16} />,
      label: "Share",
      onClick: () => alert("Share clicked"),
    },
    {
      icon: <Trash2 size={16} />,
      label: "Delete",
      onClick: () => alert("Delete clicked"),
    },
  ];

  // 🔒 Close when clicking outside
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node))
        setOpen(false);
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div
      ref={ref}
      className="fixed bottom-6 right-6 flex flex-col items-end space-y-2"
    >
      {/* Speed Dial Actions */}
      <div
        className={`flex flex-col items-end space-y-2 mb-2 transition-all duration-200 ${
          open
            ? "opacity-100 translate-y-0"
            : "opacity-0 translate-y-2 pointer-events-none"
        }`}
      >
        {actions.map((action, i) => (
          <Button
            key={i}
            variant="outline"
            size="sm"
            className="flex items-center gap-2 shadow-md bg-background hover:bg-accent text-foreground"
            onClick={() => {
              action.onClick();
              setOpen(false);
            }}
          >
            {action.icon}
            <span className="text-sm">{action.label}</span>
          </Button>
        ))}
      </div>

      {/* Main FAB */}
      <div className="relative">
        <Button
          size="icon"
          onClick={() => setOpen(!open)}
          className={
            "relative w-14 h-14 rounded-full bg-primary text-primary-foreground shadow-lg hover:bg-primary/90 active:scale-95 transition"
          }
        >
          <Plus
            size={26}
            className={`transition-transform duration-300 ${
              open ? "rotate-45" : "rotate-0"
            }`}
          />
          {/* Smooth Ping */}
          <span
            className={`absolute inset-0 rounded-full bg-primary opacity-30 ${
              open ? "hidden" : "animate-smooth-ping"
            }`}
          ></span>
        </Button>
      </div>
    </div>
  );
}
