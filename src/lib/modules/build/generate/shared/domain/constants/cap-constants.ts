/**
 * CAP Component Constants
 * Defines the available CAP transformation types with their display metadata
 */

import { CAPComponent, type CAPComponentInfo } from "../models";

/**
 * Complete list of CAP components with their display metadata
 * Used for UI rendering and user selection
 * Note: Descriptions are handled by CAPExplanationTextGenerator service
 * Icons are Font Awesome icon names (without fa- prefix)
 */
export const CAP_COMPONENTS: readonly CAPComponentInfo[] = [
  {
    component: CAPComponent.ROTATED,
    label: "Rotated",
    shortLabel: "Rotated",
    icon: "rotate", // Font Awesome: fa-rotate
    color: "#36c3ff"
  },
  {
    component: CAPComponent.MIRRORED,
    label: "Mirrored",
    shortLabel: "Mirrored",
    icon: "left-right", // Font Awesome: fa-left-right (horizontal flip)
    color: "#6F2DA8"
  },
  {
    component: CAPComponent.SWAPPED,
    label: "Swapped",
    shortLabel: "Swapped",
    icon: "shuffle", // Font Awesome: fa-shuffle
    color: "#26e600"
  },
  {
    component: CAPComponent.COMPLEMENTARY,
    label: "Complementary",
    shortLabel: "Compl.",
    icon: "yin-yang", // Font Awesome: fa-yin-yang
    color: "#eb7d00"
  }
] as const;
