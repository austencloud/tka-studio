/**
 * Browse models exports
 *
 * Selective exports to avoid conflicts between files
 */

// From BrowseState.ts (primary source for BrowseDisplayState and BrowseLoadingState)
export {
  NavigationMode,
  createDefaultDisplayState,
  createDefaultLoadingState,
} from "./BrowseState";
export type {
  BrowseDisplayState,
  BrowseLoadingState,
  BrowseState,
  SequenceFilterResult,
} from "./BrowseState";

// From FilterModels.ts (primary source for filter types)
export type { FilterConfig } from "./FilterModels";

// From BrowseModels.ts (avoid conflicts with BrowseState) - exclude conflicting types
export type {
  BrowseDeleteConfirmationData,
  BrowseDeleteResult,
  FilterState,
  NavigationItem,
  NavigationSectionConfig,
  SectionConfig,
  SequenceSection,
} from "./BrowseModels";

// Export the extended types from BrowseModels with different names to avoid conflicts
export type {
  BrowseDisplayState as ExtendedBrowseDisplayState,
  BrowseLoadingState as ExtendedBrowseLoadingState,
} from "./BrowseModels";

// From BrowseSorting.ts (functions only)
export {
  SORT_CONFIGS,
  createCustomSortConfig,
  getAvailableSortConfigs,
  getAvailableSortMethods,
  getSortConfig,
  getSortDisplayName,
} from "./BrowseSorting";

// From other files (no conflicts)
export * from "./FavoritesModels";
export * from "./Metadata";
export * from "./PanelManagement";
export * from "./SequenceState";
export * from "./SortModels";
