/**
 * Browse Sort Methods
 *
 * Defines the different ways to sort sequences in the browse tab.
 * Ported from desktop app's GallerySortMethod enum.
 */

import { GallerySortMethod } from "../enums/gallery-enums";

export interface SortConfig {
  method: GallerySortMethod;
  direction: "asc" | "desc";
  displayName: string;
}

// Helper functions moved to gallery-sorting-models.ts to avoid duplicates
// Import from gallery-sorting-models.ts if needed
