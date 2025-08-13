/**
 * Browse Sort Methods
 *
 * Defines the different ways to sort sequences in the browse tab.
 * Ported from desktop app's SortMethod enum.
 */

export enum SortMethod {
  ALPHABETICAL = "alphabetical",
  DATE_ADDED = "date_added",
  DIFFICULTY_LEVEL = "difficulty_level",
  SEQUENCE_LENGTH = "sequence_length",
  AUTHOR = "author",
  POPULARITY = "popularity",
}

export interface SortConfig {
  method: SortMethod;
  direction: "asc" | "desc";
  displayName: string;
}

// Predefined sort configurations
export const SORT_CONFIGS: Record<SortMethod, SortConfig> = {
  [SortMethod.ALPHABETICAL]: {
    method: SortMethod.ALPHABETICAL,
    direction: "asc",
    displayName: "Name A-Z",
  },
  [SortMethod.DATE_ADDED]: {
    method: SortMethod.DATE_ADDED,
    direction: "desc",
    displayName: "Recently Added",
  },
  [SortMethod.DIFFICULTY_LEVEL]: {
    method: SortMethod.DIFFICULTY_LEVEL,
    direction: "asc",
    displayName: "Difficulty",
  },
  [SortMethod.SEQUENCE_LENGTH]: {
    method: SortMethod.SEQUENCE_LENGTH,
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
  displayName?: string,
): SortConfig {
  return {
    method,
    direction,
    displayName: displayName || getSortDisplayName(method),
  };
}
