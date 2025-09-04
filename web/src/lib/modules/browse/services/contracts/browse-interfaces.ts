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

import type { GalleryFilterState, NavigationSectionConfig, NavigationItem, SectionConfig, SequenceSection } from ".";
import type { SequenceData } from "../../../../shared/domain";
import type { FilterType, GallerySortMethod } from "../../gallery/domain/enums";
import type { GalleryFilterValue } from "../../gallery/domain/types/gallery-types";
import type { BrowseDeleteConfirmationData, BrowseDeleteResult } from "../../shared/domain/models/browse-models";
import type { BrowseState } from "../../state";


// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IGalleryService {
  loadSequenceMetadata(): Promise<SequenceData[]>;
  applyFilter(
    sequences: SequenceData[],
    filterType: FilterType,
    filterValue: GalleryFilterValue
  ): Promise<SequenceData[]>;
  sortSequences(
    sequences: SequenceData[],
    sortMethod: GallerySortMethod
  ): Promise<SequenceData[]>;
  groupSequencesIntoSections(
    sequences: SequenceData[],
    sortMethod: GallerySortMethod
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
  saveFilterState(state: GalleryFilterState): Promise<void>;
  loadFilterState(): Promise<GalleryFilterState>;
  saveBrowseState(state: BrowseState): Promise<void>;
  loadBrowseState(): Promise<BrowseState | null>;
}

export interface INavigationService {
  buildNavigationStructure(
    sequences: SequenceData[]
  ): Promise<NavigationSectionConfig[]>;
  getNavigationItem(
    sectionId: string,
    itemId: string
  ): Promise<NavigationItem | null>;
  generateNavigationSections(
    sequences: SequenceData[],
    favorites: string[]
  ): Promise<NavigationSectionConfig[]>;
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
    sections: NavigationSectionConfig[]
  ): NavigationSectionConfig[];
  setActiveItem(
    sectionId: string,
    itemId: string,
    sections: NavigationSectionConfig[]
  ): NavigationSectionConfig[];
}

export interface ISectionService {
  organizeIntoSections(
    sequences: SequenceData[],
    config: SectionConfig
  ): Promise<SequenceSection[]>;
  getSectionConfig(sortMethod: GallerySortMethod): Promise<SectionConfig>;
  organizeSections(
    sequences: SequenceData[],
    config: SectionConfig
  ): Promise<SequenceSection[]>;
  toggleSectionExpansion(
    sectionId: string,
    sections: SequenceSection[]
  ): SequenceSection[];
  updateSectionConfig(
    config: SectionConfig,
    updates: Partial<SectionConfig>
  ): SectionConfig;
}
