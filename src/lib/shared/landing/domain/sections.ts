/**
 * Landing Sections
 *
 * Defines the tab navigation structure for the landing experience.
 */

import type { LandingSection, LandingTab } from "./types";

export const LANDING_SECTIONS: LandingSection[] = [
  {
    id: "resources" satisfies LandingTab,
    label: "Resources",
    icon: '<i class="fas fa-book"></i>',
    color: "rgba(102, 126, 234, 1)",
    gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
  },
  {
    id: "community" satisfies LandingTab,
    label: "Community",
    icon: '<i class="fas fa-users"></i>',
    color: "rgba(56, 189, 248, 1)",
    gradient: "linear-gradient(135deg, #38bdf8 0%, #06b6d4 100%)",
  },
  {
    id: "support" satisfies LandingTab,
    label: "Support",
    icon: '<i class="fas fa-heart"></i>',
    color: "rgba(244, 63, 94, 1)",
    gradient: "linear-gradient(135deg, #f43f5e 0%, #ec4899 100%)",
  },
  {
    id: "dev" satisfies LandingTab,
    label: "Dev",
    icon: '<i class="fas fa-code"></i>',
    color: "rgba(34, 197, 94, 1)",
    gradient: "linear-gradient(135deg, #22c55e 0%, #16a34a 100%)",
  },
];
