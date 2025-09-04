/**
 * Browse Sorting Models
 *
 * Interface definitions and business logic for browse sorting functionality.
 * Contains the business logic functions that were in GallerySortMethod.ts
 */
import { SORT_CONFIGS } from "../../gallery/domain/constants/gallery-constants";
import { GallerySortMethod } from "../../gallery/domain/enums";
import type { SortConfig } from "./SortModels";

// Helper functions
export function getSortConfig(method: GallerySortMethod): SortConfig {
  return SORT_CONFIGS[method];
}

export function getSortDisplayName(method: GallerySortMethod): string {
  return SORT_CONFIGS[method].displayName;
}

export function getAvailableSortMethods(): GallerySortMethod[] {
  return Object.values(GallerySortMethod);
}

export function getAvailableSortConfigs(): SortConfig[] {
  return Object.values(SORT_CONFIGS);
}

export function createCustomSortConfig(
  method: GallerySortMethod,
  direction: "asc" | "desc",
  displayName?: string
): SortConfig {
  return {
    method,
    direction,
    displayName: displayName || getSortDisplayName(method),
  };
}
