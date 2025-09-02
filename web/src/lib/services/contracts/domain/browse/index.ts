/**
 * Browse Service Interfaces
 *
 * Interfaces for browsing, filtering, searching, and managing sequences.
 * This includes navigation, thumbnails, and search functionality.
 */

import type {
  BrowseState,
  BrowseDeleteConfirmationData as DeleteConfirmationData,
  BrowseDeleteResult as DeleteResult,
  FilterType,
  FilterValue,
  SequenceData,
  SortMethod,
} from "$domain";

// ============================================================================
// BROWSE SERVICE INTERFACES
// ============================================================================

/**
 * Main browse service for sequence discovery and filtering
 */
export interface IBrowseService {
  loadSequenceMetadata(): Promise<SequenceData[]>;
  applyFilter(
    sequences: SequenceData[],
    filterType: FilterType,
    filterValue: FilterValue
  ): Promise<SequenceData[]>;
  sortSequences(
    sequences: SequenceData[],
    sortMethod: SortMethod
  ): Promise<SequenceData[]>;
  groupSequencesIntoSections(
    sequences: SequenceData[],
    sortMethod: SortMethod
  ): Promise<Record<string, SequenceData[]>>;
  getUniqueValues(field: keyof SequenceData): Promise<string[]>;
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
  loadSequenceIndex(): Promise<SequenceData[]>;
  buildSearchIndex(sequences: SequenceData[]): Promise<void>;
  searchSequences(query: string): Promise<SequenceData[]>;
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
    sequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<DeleteConfirmationData>;
  deleteSequence(
    sequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<DeleteResult>;
  fixVariationNumbers(
    deletedSequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<SequenceData[]>;
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
    sequences: SequenceData[]
  ): Promise<NavigationSection[]>;
  getNavigationItem(
    sectionId: string,
    itemId: string
  ): Promise<NavigationItem | null>;
  generateNavigationSections(
    sequences: SequenceData[],
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
    allSequences: SequenceData[]
  ): SequenceData[];
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
    sequences: SequenceData[],
    config: SectionConfiguration
  ): Promise<SequenceSection[]>;
  getSectionConfiguration(
    sortMethod: SortMethod
  ): Promise<SectionConfiguration>;
  organizeSections(
    sequences: SequenceData[],
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
// BROWSE DATA TYPES - MOVED TO DOMAIN
// ============================================================================
// These data models have been moved to domain/models/browse/BrowseModels.ts
// Import them from $domain instead

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
  sortOrder?: "asc" | "desc";
  showCounts?: boolean;
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
