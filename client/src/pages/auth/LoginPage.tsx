"use client";

import { LoginForm } from "@/features/auth/components/LoginForm";
import SchoolLogo from "@/assets/school-logo.png";
import useEmblaCarousel from "embla-carousel-react";
import Autoplay from "embla-carousel-autoplay";
import Fade from "embla-carousel-fade";
import HCCCI1 from "@/assets/HCCCI-1.jpg";
import HCCCI2 from "@/assets/HCCCI-2.jpg";
import HCCCI3 from "@/assets/HCCCI-3.jpg";
import HCCCI4 from "@/assets/HCCCI-4.jpg";
import HCCCI5 from "@/assets/HCCCI-5.jpg";

const IMAGES = [HCCCI1, HCCCI2, HCCCI3, HCCCI4, HCCCI5];

const LoginPage = () => {
  const [emblaRef] = useEmblaCarousel({ loop: true }, [
    Fade(), // Fade transition plugin
    Autoplay({ delay: 8000, stopOnInteraction: false }),
  ]);

  return (
    <div className="grid min-h-svh md:p-2.5 lg:grid-cols-2 bg-background">
      {/* LEFT: Carousel section */}
      <div className="relative hidden lg:block">
        <div
          className="overflow-hidden h-full w-full rounded-md"
          ref={emblaRef}
        >
          <div className="flex h-full">
            {IMAGES.map((src, i) => (
              <div key={i} className="flex-[0_0_100%] relative h-full">
                <img
                  src={src}
                  alt={`Campus ${i + 1}`}
                  className="absolute inset-0 h-full w-full object-cover rounded-md brightness-90 transition-opacity duration-1000"
                />
              </div>
            ))}
          </div>
        </div>

        {/* Optional dark overlay for contrast */}
        <div className="absolute inset-0" />
      </div>

      {/* RIGHT: Login section */}
      <div className="flex flex-col gap-4 p-6 md:p-10 lg:p-16">
        <div className="flex justify-center md:justify-start items-center gap-3">
          <img src={SchoolLogo} alt="School Logo" className="h-14 w-14" />
          <span className="hidden md:block text-lg font-semibold leading-tight">
            Holy Child Central Colleges Inc.
          </span>
        </div>

        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-xs">
            <LoginForm />
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
