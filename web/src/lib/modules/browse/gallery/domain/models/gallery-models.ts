import type { SequenceData } from "$shared/domain";
import type { GalleryFilterType, GallerySortMethod } from "../enums";
import type { GalleryFilterValue } from "../types";

export interface GallerySection {
  id: string;
  title: string;
  count: number;
  sequences: SequenceData[];
  isExpanded: boolean;
  sortOrder: number;
}
export interface GalleryDisplayState {
  currentView: "filter_selection" | "sequence_browser";
  selectedSequence: SequenceData | null;
  isSequenceDetailOpen: boolean;
}

export interface GalleryLoadingState {
  isLoading: boolean;
  hasError: boolean;
  errorMessage: string | null;
}

// Renamed to be more specific about its purpose
export interface GalleryFilterConfiguration {
  activeFilters: Record<GalleryFilterType, GalleryFilterValue>;
  sortMethod: GallerySortMethod;
  searchQuery: string;
}

// Factory functions for default states
export function createDefaultDisplayState(): GalleryDisplayState {
  return {
    currentView: "filter_selection",
    selectedSequence: null,
    isSequenceDetailOpen: false,
  };
}

export function createDefaultLoadingState(): GalleryLoadingState {
  return {
    isLoading: false,
    hasError: false,
    errorMessage: null,
  };
}

export interface GalleryNavigationItem {
  id: string;
  label: string;
  value: string | number;
  count: number;
  isActive: boolean;
  sequences: SequenceData[];
}

export interface GalleryNavigationConfig {
  id: string;
  title: string;
  type: "date" | "length" | "letter" | "level" | "author" | "favorites";
  items: GalleryNavigationItem[];
  isExpanded: boolean;
  totalCount: number;
}

export interface GallerySectionConfig {
  groupBy:
    | keyof SequenceData
    | "letter"
    | "length"
    | "difficulty"
    | "date"
    | "none";
  sortMethod: GallerySortMethod;
  showEmptySections: boolean;
  expandedSections?: Set<string>;
}

export interface GalleryDisplayPreferences {
  itemsPerPage: number;
  sortOptions: string[];
  filterOptions: string[];
  viewModes: string[];
}

export interface GallerySearchResult {
  sequences: SequenceData[];
  totalCount: number;
  hasMore: boolean;
  nextPage?: number;
}

export interface GallerySearchCriteria {
  query: string;
  filters: Record<string, unknown>;
  sortBy: string;
  sortOrder: "asc" | "desc";
}

export interface GalleryFilterOption {
  id: string;
  label: string;
  value: unknown;
  count?: number;
}

export interface GallerySortOption {
  id: string;
  label: string;
  field: string;
  direction: "asc" | "desc";
}
export interface GalleryFilterConfig {
  type: GalleryFilterType;
  value: GalleryFilterValue;
  displayName: string;
}
export interface SequenceSection {
  id: string;
  title: string;
  count: number;
  sequences: SequenceData[];
  isExpanded: boolean;
  sortOrder: number;
  metadata?: Record<string, unknown>;
}
// Renamed to be more specific about its purpose
export interface CompleteFilterState {
  activeFilters: Record<GalleryFilterType, GalleryFilterValue>;
  sortMethod: GallerySortMethod;
  searchQuery: string;
}

// Note: BrowseState moved to browse-state-factory.svelte.ts as the canonical reactive version

export interface NavigationItem {
  id: string;
  label: string;
  value: string | number;
  count: number;
  isActive: boolean;
  sequences: SequenceData[];
}

export interface NavigationSectionConfig {
  id: string;
  title: string;
  type: "date" | "length" | "letter" | "level" | "author" | "favorites";
  items: NavigationItem[];
  isExpanded: boolean;
  totalCount: number;
}

export interface SectionConfig {
  groupBy:
    | keyof SequenceData
    | "letter"
    | "length"
    | "difficulty"
    | "date"
    | "none";
  sortMethod: GallerySortMethod;
  showEmptySections: boolean;
  expandedSections?: Set<string>;
  sortOrder?: "asc" | "desc";
  showCounts?: boolean;
}
// Renamed to be more specific about its purpose
export interface FilterHistoryEntry {
  type: string | null;
  value: unknown;
  appliedAt: Date;
}

export interface GalleryViewState {
  mode: "grid" | "list";
  gridColumns?: number;
  thumbnailSize?: "small" | "medium" | "large";
}

export interface GalleryScrollState {
  scrollTop: number;
  scrollLeft: number;
  containerHeight: number;
  containerWidth: number;
}

export interface GallerySelectionState {
  selectedSequenceId: string | null;
  selectedVariationIndex: number | null;
  lastSelectedAt: Date | null;
}

export interface GallerySortState {
  method:
    | "name_asc"
    | "name_desc"
    | "difficulty"
    | "length"
    | "recent"
    | "author";
  direction: "asc" | "desc";
  appliedAt: Date;
}

export interface CompleteGalleryState {
  filter: FilterHistoryEntry | null;
  sort: GallerySortState;
  view: GalleryViewState;
  scroll: GalleryScrollState;
  selection: GallerySelectionState;
  lastUpdated: Date;
  version: number; // For handling state migration
}

export interface ApplicationTabState {
  activeTab: string;
  lastActiveTab: string | null;
  tabStates: Record<string, unknown>;
  lastUpdated: Date;
}
