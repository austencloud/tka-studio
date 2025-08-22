/**
 * Browse Filter Types
 *
 * Defines the different ways to filter sequences in the browse tab.
 * Ported from desktop app's FilterType enum.
 */

export enum FilterType {
  STARTING_LETTER = "starting_letter",
  CONTAINS_LETTERS = "contains_letters",
  LENGTH = "length",
  DIFFICULTY = "difficulty",
  startPosition = "startPosition",
  AUTHOR = "author",
  GRID_MODE = "gridMode",
  ALL_SEQUENCES = "all_sequences",
  FAVORITES = "favorites",
  RECENT = "recent",
}

export type FilterValue = string | number | string[] | null;

export interface FilterConfig {
  type: FilterType;
  value: FilterValue;
  displayName: string;
}

// Helper functions for filter operations
export function createFilterConfig(
  type: FilterType,
  value: FilterValue,
  displayName?: string
): FilterConfig {
  return {
    type,
    value,
    displayName: displayName || formatFilterDisplayName(type, value),
  };
}

export function formatFilterDisplayName(
  type: FilterType,
  value: FilterValue
): string {
  switch (type) {
    case FilterType.STARTING_LETTER:
      return typeof value === "string" && value.includes("-")
        ? `Letters ${value}`
        : `Letter ${value}`;
    case FilterType.CONTAINS_LETTERS:
      return `Contains "${value}"`;
    case FilterType.LENGTH:
      return value === "all" ? "All Lengths" : `${value} beats`;
    case FilterType.DIFFICULTY:
      return value === "all" ? "All Levels" : `${value} level`;
    case FilterType.startPosition:
      return value === "all" ? "All Positions" : `Position ${value}`;
    case FilterType.AUTHOR:
      return value === "all" ? "All Authors" : `By ${value}`;
    case FilterType.GRID_MODE:
      return value === "all" ? "All Styles" : `${value} style`;
    case FilterType.ALL_SEQUENCES:
      return "All Sequences";
    case FilterType.FAVORITES:
      return "Favorites";
    case FilterType.RECENT:
      return "Recently Added";
    default:
      return String(value || "Unknown");
  }
}

export function isRangeFilter(type: FilterType): boolean {
  return type === FilterType.STARTING_LETTER;
}

export function isMultiValueFilter(type: FilterType): boolean {
  return type === FilterType.CONTAINS_LETTERS;
}
