import type { SequenceData } from "../../../../shared/domain";
import type { GalleryFilterType, GallerySortMethod } from "../domain/enums";
import type { GalleryFilterValue } from "../domain/types/gallery-types";

export interface IGalleryFilterState {
  setFilter(type: string, value: unknown): void;
  applyCurrentFilter(sequences: SequenceData[]): Promise<SequenceData[]>;
  clearFilter(): void;
  isFilterActive: boolean;
}

export interface IGalleryDisplayState {
  setLoading(loading: boolean, operation?: string): void;
  setError(error: string | null): void;
}

export interface IGalleryState {
  // Core operations
  loadAllSequences(): Promise<void>;
  applyFilter(
    type: GalleryFilterType,
    value: GalleryFilterValue
  ): Promise<void>;
  searchSequences(query: string): Promise<void>;
  updateSort(sortMethod: GallerySortMethod): Promise<void>;
  backToFilters(): Promise<void>;

  // Selection operations
  selectSequence(sequence: SequenceData): Promise<void>;

  // Navigation operations
  generateNavigationSections(): Promise<void>;

  // Filter persistence operations
  restoreSavedState(): Promise<void>;
  clearSavedState(): Promise<void>;

  // Reactive getters
  readonly allSequences: SequenceData[];
  readonly filteredSequences: SequenceData[];
  readonly displayedSequences: SequenceData[];
}
