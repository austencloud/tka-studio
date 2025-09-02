/**
 * Browse State Models
 *
 * Domain models for browse functionality state management.
 * Ported from desktop app's browse models.
 */

import type { FilterType, FilterValue, SequenceData } from "$domain";
import { SortMethod } from "$domain";

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

// SequenceData eliminated - using SequenceData directly
// This eliminates 95% duplication and clarifies starting position types

export interface SequenceFilterResult {
  sequences: SequenceData[];
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
  sequences: SequenceData[];
  sortedSections: Record<string, SequenceData[]>;
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

// createSequenceData function removed - using SequenceData directly
// No conversion needed since SequenceData was eliminated

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
  updates: Partial<BrowseState>
): BrowseState {
  return { ...state, ...updates };
}
