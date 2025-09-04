import type { SequenceData } from "../../../../../shared/domain";
import type { FilterValue } from "../../../domain/types";
import type { FilterType, GallerySortMethod } from "../enums";

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

export interface GalleryFilterState {
  activeFilters: Record<FilterType, FilterValue>;
  sortMethod: GallerySortMethod;
  searchQuery: string;
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
