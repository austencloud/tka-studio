/**
 * Option UI State - Pure Svelte 5 Runes
 *
 * Handles UI state (sort method, loading, error, tab selection).
 * Extracted from lines 26-44 and 245-290 of optionPickerRunes.svelte.ts
 */

import { OptionPickerSortMethod } from "$lib/domain";
import type { SortMethod } from "../config";

// ===== Types =====
export type LastSelectedTabState = Partial<Record<SortMethod, string | null>>;

interface UIState {
  sortMethod: SortMethod;
  isLoading: boolean;
  error: string | null;
  lastSelectedTab: LastSelectedTabState;
}

// ===== Helper Functions =====
function getStoredState(): UIState {
  if (typeof window === "undefined")
    return {
      sortMethod: OptionPickerSortMethod.LETTER_TYPE,
      isLoading: false,
      error: null,
      lastSelectedTab: {},
    };

  try {
    const stored = localStorage.getItem("optionPickerUIState");

    if (!stored)
      return {
        sortMethod: OptionPickerSortMethod.LETTER_TYPE,
        isLoading: false,
        error: null,
        lastSelectedTab: { [OptionPickerSortMethod.LETTER_TYPE]: "all" },
      };

    const parsed = JSON.parse(stored);

    return {
      sortMethod: parsed.sortMethod || "type",
      isLoading: false,
      error: null,
      lastSelectedTab: parsed.lastSelectedTab || { type: "all" },
    };
  } catch (e) {
    console.error("Error reading from localStorage:", e);
    return {
      sortMethod: OptionPickerSortMethod.LETTER_TYPE,
      isLoading: false,
      error: null,
      lastSelectedTab: { [OptionPickerSortMethod.LETTER_TYPE]: "all" },
    };
  }
}

export function createOptionUIState() {
  // ===== UI State Using Runes =====
  const storedState = getStoredState();
  let uiState = $state<UIState>({
    sortMethod: storedState.sortMethod,
    isLoading: storedState.isLoading,
    error: storedState.error,
    lastSelectedTab: storedState.lastSelectedTab,
  });

  // ===== Actions =====
  function setSortMethod(method: SortMethod): void {
    uiState.sortMethod = method;
  }

  function setLoading(loading: boolean): void {
    uiState.isLoading = loading;
  }

  function setError(error: string | null): void {
    uiState.error = error;
  }

  function setLastSelectedTabForSort(
    sortMethod: SortMethod,
    tabKey: string | null
  ): void {
    // Avoid unnecessary updates if the value hasn't changed
    if (uiState.lastSelectedTab[sortMethod] === tabKey) {
      return;
    }

    uiState.lastSelectedTab = {
      ...uiState.lastSelectedTab,
      [sortMethod]: tabKey,
    };
  }

  function reset(): void {
    // Preserve user preferences
    const currentSortMethod = uiState.sortMethod || "type";
    uiState = {
      sortMethod: currentSortMethod,
      isLoading: false,
      error: null,
      lastSelectedTab: uiState.lastSelectedTab || {},
    };

    // Ensure 'all' is set as the default tab for the current sort method
    setLastSelectedTabForSort(currentSortMethod, "all");
  }

  // ===== Return Interface =====
  return {
    // Getters
    get sortMethod() {
      return uiState.sortMethod;
    },
    get isLoading() {
      return uiState.isLoading;
    },
    get error() {
      return uiState.error;
    },
    get lastSelectedTab() {
      return uiState.lastSelectedTab;
    },

    // Actions
    setSortMethod,
    setLoading,
    setError,
    setLastSelectedTabForSort,
    reset,
  };
}

export type OptionUIState = ReturnType<typeof createOptionUIState>;
