/**
 * Browse State Models
 *
 * Domain models for browse functionality state management.
 * Ported from desktop app's browse models.
 */

import type { SequenceData } from "../SequenceData";
import type { FilterType, FilterValue } from "./FilterType";
import { SortMethod } from "./SortMethod";

export interface BrowseState {
  filterType: FilterType | null;
  filterValues: FilterValue;
  selectedSequence: string | null;
  selectedVariation: number | null;
  navigationMode: NavigationMode;
  sortMethod: SortMethod;
}

export enum NavigationMode {
  FILTER_SELECTION = "filter_selector",
  SEQUENCE_BROWSER = "sequence_picker",
}

export interface BrowseSequenceMetadata {
  id: string;
  name: string;
  word: string;
  thumbnails: string[];
  sequenceLength?: number;
  author?: string;
  level?: number;
  dateAdded?: Date;
  gridMode?: string;
  propType?: string;
  isFavorite: boolean;
  isCircular: boolean;
  startingPosition?: string;
  difficultyLevel?: string;
  tags: string[];
  metadata: Record<string, unknown>;
}

export interface SequenceFilterResult {
  sequences: BrowseSequenceMetadata[];
  totalCount: number;
  filterApplied: {
    type: FilterType;
    value: FilterValue;
  };
}

export interface BrowseLoadingState {
  isLoading: boolean;
  loadedCount: number;
  totalCount: number;
  currentOperation: string;
  error: string | null;
}

export interface BrowseDisplayState {
  sequences: BrowseSequenceMetadata[];
  sortedSections: Record<string, BrowseSequenceMetadata[]>;
  currentSection: string | null;
  thumbnailWidth: number;
  gridColumns: number;
}

// Helper functions for state management
export function createDefaultBrowseState(): BrowseState {
  return {
    filterType: null,
    filterValues: null,
    selectedSequence: null,
    selectedVariation: null,
    navigationMode: NavigationMode.FILTER_SELECTION,
    sortMethod: SortMethod.ALPHABETICAL,
  };
}

export function createBrowseSequenceMetadata(
  sequence: SequenceData,
): BrowseSequenceMetadata {
  return {
    id: sequence.id,
    name: sequence.name,
    word: sequence.word,
    thumbnails: [...sequence.thumbnails],
    ...(sequence.sequence_length !== undefined && {
      sequenceLength: sequence.sequence_length,
    }),
    ...(sequence.author !== undefined && { author: sequence.author }),
    ...(sequence.level !== undefined && { level: sequence.level }),
    ...(sequence.date_added !== undefined && {
      dateAdded: sequence.date_added,
    }),
    ...(sequence.grid_mode !== undefined && { gridMode: sequence.grid_mode }),
    ...(sequence.prop_type !== undefined && { propType: sequence.prop_type }),
    isFavorite: sequence.is_favorite,
    isCircular: sequence.is_circular,
    ...(sequence.starting_position !== undefined && {
      startingPosition: sequence.starting_position,
    }),
    ...(sequence.difficulty_level !== undefined && {
      difficultyLevel: sequence.difficulty_level,
    }),
    tags: [...sequence.tags],
    metadata: { ...sequence.metadata },
  };
}

export function createDefaultLoadingState(): BrowseLoadingState {
  return {
    isLoading: false,
    loadedCount: 0,
    totalCount: 0,
    currentOperation: "",
    error: null,
  };
}

export function createDefaultDisplayState(): BrowseDisplayState {
  return {
    sequences: [],
    sortedSections: {},
    currentSection: null,
    thumbnailWidth: 200,
    gridColumns: 3,
  };
}

export function updateBrowseState(
  state: BrowseState,
  updates: Partial<BrowseState>,
): BrowseState {
  return { ...state, ...updates };
}
