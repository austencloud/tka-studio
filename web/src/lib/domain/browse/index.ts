/**
 * Browse Domain Models - Main Export
 *
 * Central export for all browse-related domain models and types.
 */

// Filter Types
export {
  createFilterConfig,
  FilterType,
  formatFilterDisplayName,
  isMultiValueFilter,
  isRangeFilter,
} from "./FilterType";
export type { FilterConfig, FilterValue } from "./FilterType";

// Sort Methods
export {
  createCustomSortConfig,
  getAvailableSortConfigs,
  getAvailableSortMethods,
  getSortConfig,
  getSortDisplayName,
  SORT_CONFIGS,
  SortMethod,
} from "./SortMethod";
export type { SortConfig } from "./SortMethod";

// Browse State
export {
  createDefaultBrowseState,
  createDefaultDisplayState,
  createDefaultLoadingState,
  NavigationMode,
  updateBrowseState,
} from "./BrowseState";
export type {
  BrowseDisplayState,
  BrowseLoadingState,
  BrowseState,
  SequenceFilterResult,
} from "./BrowseState";

// Main browse types including legacy ones from types.ts
export type {
  BrowseConfig,
  BrowseDeleteConfirmationData,
  BrowseDeleteResult,
  BrowseResult,
  FilterOption,
  FilterState,
  NavigationItem,
  NavigationSection,
  SearchCriteria,
  SectionConfiguration,
  SequenceSection,
  SortOption,
} from "./types";

// Re-export GridMode from main enums to maintain compatibility
export { GridMode } from "../enums";

// Metadata types for Browse functionality
export * from "./metadata";

// Favorites types
export type { FavoriteItem, FavoritesCollection } from "./favorites";

// Animation types
export type { AnimationConfig, AnimationState } from "./animation/types";
