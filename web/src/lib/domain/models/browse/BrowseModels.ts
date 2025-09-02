import type {
  FilterType,
  FilterValue,
  SortMethod,
  SequenceData,
} from "$domain";

export interface SequenceMetadata {
  word: string;
  author: string;
  totalBeats: number;
}

export interface SequenceSection {
  id: string;
  title: string;
  count: number;
  sequences: SequenceData[];
  isExpanded: boolean;
  sortOrder: number;
}

/**
 * Browse Service Interfaces
 *
 * Interfaces for browsing, filtering, searching, and managing sequences.
 * This includes navigation, thumbnails, and search functionality.
 */
// ============================================================================
// BROWSE SERVICE INTERFACES
// ============================================================================
/**
 * Main browse service for sequence discovery and filtering
 */

// ============================================================================
// DATA CONTRACTS (Domain Models)
// ============================================================================

export interface BrowseDeleteConfirmationData {
  sequence: SequenceData;
  relatedSequences: SequenceData[];
  hasVariations: boolean;
  willFixVariationNumbers: boolean;
}

export interface BrowseDeleteResult {
  success: boolean;
  deletedSequence: SequenceData | null;
  affectedSequences: SequenceData[];
  error?: string;
}

export interface BrowseDisplayState {
  currentView: "filter_selection" | "sequence_browser";
  selectedSequence: SequenceData | null;
  isSequenceDetailOpen: boolean;
}

export interface BrowseLoadingState {
  isLoading: boolean;
  hasError: boolean;
  errorMessage: string | null;
}

export interface FilterState {
  activeFilters: Record<FilterType, FilterValue>;
  sortMethod: SortMethod;
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

export interface NavigationSection {
  id: string;
  title: string;
  type: "date" | "length" | "letter" | "level" | "author" | "favorites";
  items: NavigationItem[];
  isExpanded: boolean;
  totalCount: number;
}

export interface SectionConfiguration {
  groupBy:
    | keyof SequenceData
    | "letter"
    | "length"
    | "difficulty"
    | "date"
    | "none";
  sortMethod: SortMethod;
  showEmptySections: boolean;
  expandedSections?: Set<string>;
}

export interface SequenceSection {
  id: string;
  title: string;
  count: number;
  sequences: SequenceData[];
  isExpanded: boolean;
  metadata?: Record<string, unknown>;
}

export interface BrowseConfig {
  itemsPerPage: number;
  sortOptions: string[];
  filterOptions: string[];
  viewModes: string[];
}

export interface BrowseResult {
  sequences: SequenceData[];
  totalCount: number;
  hasMore: boolean;
  nextPage?: number;
}

export interface SearchCriteria {
  query: string;
  filters: Record<string, unknown>;
  sortBy: string;
  sortOrder: "asc" | "desc";
}

export interface FilterOption {
  id: string;
  label: string;
  value: unknown;
  count?: number;
}

export interface SortOption {
  id: string;
  label: string;
  field: string;
  direction: "asc" | "desc";
}
