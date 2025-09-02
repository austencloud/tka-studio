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

import type {
  BrowseDeleteConfirmationData,
  BrowseDeleteResult,
  BrowseState,
  FilterState,
  FilterType,
  FilterValue,
  NavigationItem,
  NavigationSection,
  SectionConfiguration,
  SequenceData,
  SequenceSection,
  SortMethod,
} from "$domain";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

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

export interface IThumbnailService {
  getThumbnailUrl(sequenceId: string, thumbnailPath: string): string;
  preloadThumbnail(sequenceId: string, thumbnailPath: string): Promise<void>;
  getThumbnailMetadata(
    sequenceId: string
  ): Promise<{ width: number; height: number } | null>;
  clearThumbnailCache(): void;
}

export interface ISequenceIndexService {
  loadSequenceIndex(): Promise<SequenceData[]>;
  buildSearchIndex(sequences: SequenceData[]): Promise<void>;
  searchSequences(query: string): Promise<SequenceData[]>;
  refreshIndex(): Promise<void>;
}

export interface IDeleteService {
  prepareDeleteConfirmation(
    sequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<BrowseDeleteConfirmationData>;
  deleteSequence(
    sequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<BrowseDeleteResult>;
  fixVariationNumbers(
    deletedSequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<SequenceData[]>;
}

export interface IFavoritesService {
  addToFavorites(sequenceId: string): Promise<void>;
  removeFromFavorites(sequenceId: string): Promise<void>;
  toggleFavorite(sequenceId: string): Promise<void>;
  getFavorites(): Promise<string[]>;
  isFavorite(sequenceId: string): Promise<boolean>;
}

export interface IFilterPersistenceService {
  saveFilterState(state: FilterState): Promise<void>;
  loadFilterState(): Promise<FilterState>;
  saveBrowseState(state: BrowseState): Promise<void>;
  loadBrowseState(): Promise<BrowseState | null>;
}

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
