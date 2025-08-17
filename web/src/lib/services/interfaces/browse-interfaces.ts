/**
 * Browse Service Interfaces
 *
 * Interfaces for browsing, filtering, searching, and managing sequences.
 * This includes navigation, thumbnails, and search functionality.
 */

import type {
  BrowseSequenceMetadata,
  FilterType,
  FilterValue,
  SortMethod,
} from "./domain-types";

// ============================================================================
// BROWSE SERVICE INTERFACES
// ============================================================================

/**
 * Main browse service for sequence discovery and filtering
 */
export interface IBrowseService {
  loadSequenceMetadata(): Promise<BrowseSequenceMetadata[]>;
  applyFilter(
    sequences: BrowseSequenceMetadata[],
    filterType: FilterType,
    filterValue: FilterValue
  ): Promise<BrowseSequenceMetadata[]>;
  sortSequences(
    sequences: BrowseSequenceMetadata[],
    sortMethod: SortMethod
  ): Promise<BrowseSequenceMetadata[]>;
  groupSequencesIntoSections(
    sequences: BrowseSequenceMetadata[],
    sortMethod: SortMethod
  ): Promise<Record<string, BrowseSequenceMetadata[]>>;
  getUniqueValues(field: keyof BrowseSequenceMetadata): Promise<string[]>;
  getFilterOptions(filterType: FilterType): Promise<string[]>;
}

/**
 * Thumbnail management service
 */
export interface IThumbnailService {
  getThumbnailUrl(sequenceId: string, thumbnailPath: string): string;
  preloadThumbnail(sequenceId: string, thumbnailPath: string): Promise<void>;
  getThumbnailMetadata(
    sequenceId: string
  ): Promise<{ width: number; height: number } | null>;
  clearThumbnailCache(): void;
}

/**
 * Sequence indexing and search service
 */
export interface ISequenceIndexService {
  loadSequenceIndex(): Promise<BrowseSequenceMetadata[]>;
  buildSearchIndex(sequences: BrowseSequenceMetadata[]): Promise<void>;
  searchSequences(query: string): Promise<BrowseSequenceMetadata[]>;
  refreshIndex(): Promise<void>;
}

// ============================================================================
// BROWSE MANAGEMENT SERVICES
// ============================================================================

/**
 * Service for managing sequence deletion operations
 */
export interface IDeleteService {
  prepareDeleteConfirmation(
    sequence: BrowseSequenceMetadata,
    allSequences: BrowseSequenceMetadata[]
  ): Promise<DeleteConfirmationData>;
  deleteSequence(
    sequence: BrowseSequenceMetadata,
    allSequences: BrowseSequenceMetadata[]
  ): Promise<DeleteResult>;
  fixVariationNumbers(
    deletedSequence: BrowseSequenceMetadata,
    allSequences: BrowseSequenceMetadata[]
  ): Promise<BrowseSequenceMetadata[]>;
}

/**
 * Service for managing user favorites
 */
export interface IFavoritesService {
  addToFavorites(sequenceId: string): Promise<void>;
  removeFromFavorites(sequenceId: string): Promise<void>;
  toggleFavorite(sequenceId: string): Promise<void>;
  getFavorites(): Promise<string[]>;
  isFavorite(sequenceId: string): Promise<boolean>;
}

/**
 * Service for persisting filter and browse state
 */
export interface IFilterPersistenceService {
  saveFilterState(state: FilterState): Promise<void>;
  loadFilterState(): Promise<FilterState>;
  saveBrowseState(state: BrowseState): Promise<void>;
  loadBrowseState(): Promise<BrowseState | null>;
}

/**
 * Service for managing navigation structure
 */
export interface INavigationService {
  buildNavigationStructure(
    sequences: BrowseSequenceMetadata[]
  ): Promise<NavigationSection[]>;
  getNavigationItem(
    sectionId: string,
    itemId: string
  ): Promise<NavigationItem | null>;
  generateNavigationSections(
    sequences: BrowseSequenceMetadata[],
    favorites: string[]
  ): Promise<NavigationSection[]>;
  getSequencesForNavigationItem(
    item: NavigationItem,
    sectionType:
      | "letter"
      | "author"
      | "level"
      | "length"
      | "favorites"
      | "date",
    allSequences: BrowseSequenceMetadata[]
  ): BrowseSequenceMetadata[];
  toggleSectionExpansion(
    sectionId: string,
    sections: NavigationSection[]
  ): NavigationSection[];
  setActiveItem(
    sectionId: string,
    itemId: string,
    sections: NavigationSection[]
  ): NavigationSection[];
}

/**
 * Service for organizing sequences into sections
 */
export interface ISectionService {
  organizeIntoSections(
    sequences: BrowseSequenceMetadata[],
    config: SectionConfiguration
  ): Promise<SequenceSection[]>;
  getSectionConfiguration(
    sortMethod: SortMethod
  ): Promise<SectionConfiguration>;
  organizeSections(
    sequences: BrowseSequenceMetadata[],
    config: SectionConfiguration
  ): Promise<SequenceSection[]>;
  toggleSectionExpansion(
    sectionId: string,
    sections: SequenceSection[]
  ): SequenceSection[];
  updateSectionConfiguration(
    config: SectionConfiguration,
    updates: Partial<SectionConfiguration>
  ): SectionConfiguration;
}

// ============================================================================
// BROWSE DATA TYPES
// ============================================================================

export interface DeleteConfirmationData {
  sequence: BrowseSequenceMetadata;
  relatedSequences: BrowseSequenceMetadata[];
  hasVariations: boolean;
  willFixVariationNumbers: boolean;
}

export interface DeleteResult {
  success: boolean;
  deletedSequence: BrowseSequenceMetadata | null;
  affectedSequences: BrowseSequenceMetadata[];
  error?: string;
}

export interface BrowseDisplayState {
  currentView: "filter_selection" | "sequence_browser";
  selectedSequence: BrowseSequenceMetadata | null;
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

export interface BrowseState {
  displayState: BrowseDisplayState;
  loadingState: BrowseLoadingState;
  filterState: FilterState;
}

export interface NavigationItem {
  id: string;
  label: string;
  value: string | number;
  count: number;
  isActive: boolean;
  sequences: BrowseSequenceMetadata[];
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
    | keyof BrowseSequenceMetadata
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
  sequences: BrowseSequenceMetadata[];
  isExpanded: boolean;
  metadata?: Record<string, unknown>;
}
