/**
 * Browse Domain Exports
 *
 * All types, models, and enums related to browsing functionality.
 */

// Types (no conflicts)
export * from "./types";

// Models - Selective exports to avoid conflicts
export type {
  BrowseDeleteConfirmationData,
  BrowseDeleteResult,
  BrowseDisplayState,
  BrowseLoadingState,
  BrowsePanelConfig,
  BrowsePanelState,
  BrowseState,
  FilterConfig,
  FilterState,
  MetadataAnalysisResult,
  NavigationItem,
  NavigationSectionConfig,
  ResizeOperation,
  SectionConfig,
  SequenceFilterResult,
  SequenceSection,
  SortConfig,
  ThumbnailFile,
} from "./models";

// Functions
export { createDefaultDisplayState, createDefaultLoadingState } from "./models";

// Enums (exported as values)
export { NavigationMode } from "./models";

// Browse-specific SortMethod to avoid conflicts with core SortMethod
export { SortMethod as BrowseSortMethod } from "./models";

// Additional commonly needed types for browse services
