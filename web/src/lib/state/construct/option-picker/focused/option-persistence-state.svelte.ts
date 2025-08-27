/**
 * Option Persistence State - Pure Svelte 5 Runes
 *
 * Handles localStorage operations, preloaded options, and state persistence.
 * Extracted from the original optionPickerRunes.svelte.ts
 */

import type { PictographData } from "$lib/domain/PictographData";
import type { IPositionMapper } from "$lib/services/interfaces/positioning-interfaces";
import { resolve, TYPES } from "$lib/services/inversify/container";
import type { SortMethod } from "../config";
import type { LastSelectedTabState } from "./option-ui-state.svelte";

interface UIState {
  sortMethod: SortMethod;
  isLoading: boolean;
  error: string | null;
  lastSelectedTab: LastSelectedTabState;
}

export function createOptionPersistenceState() {
  // ===== Helper Functions =====

  /**
   * Helper function to compute endPosition from motion data
   */
  function getEndPosition(pictographData: PictographData): string | null {
    if (pictographData.motions?.blue && pictographData.motions?.red) {
      const positionService = resolve(TYPES.IPositionMapper) as IPositionMapper;
      const position = positionService.getPositionFromLocations(
        pictographData.motions.blue.endLocation,
        pictographData.motions.red.endLocation
      );
      return position?.toString() || null;
    }
    return null;
  }

  // ===== Cache Operations =====

  /**
   * Check for preloaded options from localStorage
   */
  function checkPreloadedOptions(): PictographData[] | null {
    try {
      const preloadedData = localStorage.getItem("preloaded_options");
      if (preloadedData) {
        const preloadedOptions = JSON.parse(preloadedData);
        localStorage.removeItem("preloaded_options");
        return preloadedOptions || [];
      }
    } catch (error) {
      console.error("Error checking preloaded options:", error);
    }
    return null;
  }

  /**
   * Check for bulk preloaded options for a specific end position
   */
  function checkBulkPreloadedOptions(
    targetEndPosition: string
  ): PictographData[] | null {
    try {
      const allPreloadedData = localStorage.getItem("all_preloaded_options");
      if (allPreloadedData) {
        const allOptions = JSON.parse(allPreloadedData);
        return (
          allOptions.filter((option: PictographData) => {
            const endPos = getEndPosition(option);
            return endPos === targetEndPosition;
          }) || []
        );
      }
    } catch (error) {
      console.error("Error checking bulk preloaded options:", error);
    }
    return null;
  }

  /**
   * Get target end position from sequence
   */
  function getTargetEndPosition(sequence: PictographData[]): string | null {
    if (sequence.length === 0) return null;
    const lastPictograph = sequence[sequence.length - 1];
    return getEndPosition(lastPictograph);
  }

  // ===== State Persistence =====

  /**
   * Save last selected tab state
   */
  function saveLastSelectedTab(state: LastSelectedTabState): void {
    try {
      localStorage.setItem("lastSelectedTab", JSON.stringify(state));
    } catch (error) {
      console.error("Error saving last selected tab:", error);
    }
  }

  /**
   * Load stored UI state from localStorage
   */
  function loadStoredUIState(): UIState {
    try {
      const savedSort = localStorage.getItem("optionPickerSortMethod");
      const savedTabs = localStorage.getItem("lastSelectedTab");

      return {
        sortMethod: (savedSort as SortMethod) || "by-family",
        isLoading: false,
        error: null,
        lastSelectedTab: savedTabs ? JSON.parse(savedTabs) : {},
      };
    } catch (error) {
      console.error("Error loading stored UI state:", error);
      return {
        sortMethod: "by-family" as SortMethod,
        isLoading: false,
        error: null,
        lastSelectedTab: {},
      };
    }
  }

  /**
   * Persist UI state to localStorage
   */
  function persistState(state: UIState): void {
    try {
      localStorage.setItem("optionPickerSortMethod", state.sortMethod);
      localStorage.setItem(
        "lastSelectedTab",
        JSON.stringify(state.lastSelectedTab)
      );
    } catch (error) {
      console.error("Error persisting state:", error);
    }
  }

  /**
   * Clear preloaded data from localStorage
   */
  function clearPreloadedData(): void {
    try {
      localStorage.removeItem("preloaded_options");
      localStorage.removeItem("all_preloaded_options");
    } catch (error) {
      console.error("Error clearing preloaded data:", error);
    }
  }

  // ===== Return Interface =====
  return {
    checkPreloadedOptions,
    checkBulkPreloadedOptions,
    getTargetEndPosition,
    saveLastSelectedTab,
    loadStoredUIState,
    persistState,
    clearPreloadedData,
  };
}

export type OptionPersistenceState = ReturnType<
  typeof createOptionPersistenceState
>;
