/**
 * Browse Sorting Models
 *
 * Interface definitions and business logic for browse sorting functionality.
 * Contains the business logic functions that were in SortMethod.ts
 */
import { SortMethod, type SortConfig } from "$domain";

// Predefined sort configurations
export const SORT_CONFIGS: Record<SortMethod, SortConfig> = {
  [SortMethod.ALPHABETICAL]: {
    method: SortMethod.ALPHABETICAL,
    direction: "asc",
    displayName: "Name A-Z",
  },
  [SortMethod.dateAdded]: {
    method: SortMethod.dateAdded,
    direction: "desc",
    displayName: "Recently Added",
  },
  [SortMethod.difficultyLevel]: {
    method: SortMethod.difficultyLevel,
    direction: "asc",
    displayName: "Difficulty",
  },
  [SortMethod.sequenceLength]: {
    method: SortMethod.sequenceLength,
    direction: "asc",
    displayName: "Length",
  },
  [SortMethod.AUTHOR]: {
    method: SortMethod.AUTHOR,
    direction: "asc",
    displayName: "Author",
  },
  [SortMethod.POPULARITY]: {
    method: SortMethod.POPULARITY,
    direction: "desc",
    displayName: "Popularity",
  },
};

// Helper functions
export function getSortConfig(method: SortMethod): SortConfig {
  return SORT_CONFIGS[method];
}

export function getSortDisplayName(method: SortMethod): string {
  return SORT_CONFIGS[method].displayName;
}

export function getAvailableSortMethods(): SortMethod[] {
  return Object.values(SortMethod);
}

export function getAvailableSortConfigs(): SortConfig[] {
  return Object.values(SORT_CONFIGS);
}

export function createCustomSortConfig(
  method: SortMethod,
  direction: "asc" | "desc",
  displayName?: string
): SortConfig {
  return {
    method,
    direction,
    displayName: displayName || getSortDisplayName(method),
  };
}
