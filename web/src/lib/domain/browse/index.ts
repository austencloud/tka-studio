/**
 * Browse Domain Models - Main Export
 *
 * Central export for all browse-related domain models and types.
 */

// Filter Types
export {
  FilterType,
  createFilterConfig,
  formatFilterDisplayName,
  isMultiValueFilter,
  isRangeFilter,
} from "./FilterType";
export type { FilterConfig, FilterValue } from "./FilterType";

// Sort Methods
export {
  SORT_CONFIGS,
  SortMethod,
  createCustomSortConfig,
  getAvailableSortConfigs,
  getAvailableSortMethods,
  getSortConfig,
  getSortDisplayName,
} from "./SortMethod";
export type { SortConfig } from "./SortMethod";

// Browse State
export {
  NavigationMode,
  createDefaultBrowseState,
  createDefaultDisplayState,
  createDefaultLoadingState,
  updateBrowseState,
} from "./BrowseState";
export type {
  BrowseDisplayState,
  BrowseLoadingState,
  BrowseState,
  SequenceFilterResult,
} from "./BrowseState";

// Re-export GridMode from main enums to maintain compatibility
export { GridMode } from "../enums";
