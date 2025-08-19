/**
 * Sophisticated Option Picker State using ONLY Svelte 5 Runes
 *
 * Complete port of the legacy system with advanced features using pure runes:
 * - Advanced state management
 * - Sophisticated filtering and grouping
 * - Real option data service integration
 * - Performance optimizations
 * - Complex reactive state derivations
 */

import type { PictographData } from "$lib/domain/PictographData";
import { resolve } from "$services/bootstrap";
import { createBeatData } from "$lib/domain/BeatData";
import type { ReversalFilter, SortMethod } from "./config";
import {
  determineGroupKey,
  getSortedGroupKeys,
  getSorter,
} from "./services/OptionsService";

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
      sortMethod: "type",
      isLoading: false,
      error: null,
      lastSelectedTab: {},
    };

  try {
    const stored = localStorage.getItem("optionPickerUIState");

    if (!stored)
      return {
        sortMethod: "type",
        isLoading: false,
        error: null,
        lastSelectedTab: { type: "all" },
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
      sortMethod: "type",
      isLoading: false,
      error: null,
      lastSelectedTab: { type: "all" },
    };
  }
}



/**
 * Create sophisticated option picker state using ONLY Svelte 5 runes
 */
export function createOptionPickerRunes() {
  // ===== Core State Using Runes =====
  let sequenceData = $state<PictographData[]>([]);
  let optionsData = $state<PictographData[]>([]);
  let selectedPictograph = $state<PictographData | null>(null);

  // ===== UI State Using Runes =====
  const storedState = getStoredState();
  let uiState = $state<UIState>({
    sortMethod: storedState.sortMethod,
    isLoading: storedState.isLoading,
    error: storedState.error,
    lastSelectedTab: storedState.lastSelectedTab,
  });

  // ===== Derived State Using Runes =====

  // Filtered and sorted options
  const filteredOptions = $derived(() => {
    const options = [...optionsData];
    options.sort(getSorter(uiState.sortMethod, sequenceData));
    return options;
  });

  // Simplified grouped options - compute only when explicitly needed
  let cachedGroupedOptions = $state<Record<string, PictographData[]>>({});

  function computeGroupedOptions(): Record<string, PictographData[]> {
    const groups: Record<string, PictographData[]> = {};
    const options = filteredOptions();
    options.forEach((option) => {
      const groupKey = determineGroupKey(
        option,
        uiState.sortMethod,
        sequenceData
      );
      if (!groups[groupKey]) groups[groupKey] = [];
      groups[groupKey].push(option);
    });

    const sortedKeys = getSortedGroupKeys(
      Object.keys(groups),
      uiState.sortMethod
    );
    const sortedGroups: Record<string, PictographData[]> = {};
    sortedKeys.forEach((key) => {
      if (groups[key]) {
        sortedGroups[key] = groups[key];
      }
    });
    cachedGroupedOptions = sortedGroups;
    return sortedGroups;
  }

  // Category keys available - simplified
  const categoryKeys = $derived(() => Object.keys(cachedGroupedOptions));

  // ===== State Persistence Effect =====
  // Disable automatic state persistence to prevent reactive cascades
  // Only save state on explicit user actions
  // $effect(() => {
  //   // Save state changes to localStorage
  //   saveStateToLocalStorage(uiState);
  // });

  // ===== Actions =====
  async function loadOptions(sequence: PictographData[]) {
    sequenceData = sequence;

    // **Check for preloaded options first to avoid loading state**
    try {
      // First check for specific preloaded options (from individual clicks)
      const preloadedData = localStorage.getItem("preloaded_options");
      if (preloadedData) {
        const preloadedOptions = JSON.parse(preloadedData);
        optionsData = preloadedOptions || [];
        uiState.isLoading = false;
        uiState.error = null;

        // Clear preloaded data so it's only used once
        localStorage.removeItem("preloaded_options");

        // Set default tab if needed
        if (
          !uiState.lastSelectedTab[uiState.sortMethod] ||
          uiState.lastSelectedTab[uiState.sortMethod] === null
        ) {
          setLastSelectedTabForSort(uiState.sortMethod, "all");
        }

        return; // Skip the loading process
      }

      // Check for bulk preloaded options (from component load)
      const allPreloadedData = localStorage.getItem("all_preloaded_options");
      if (allPreloadedData) {
        const allPreloadedOptions = JSON.parse(allPreloadedData);

        // Determine the current end position we need options for
        let targetEndPosition: string | null = null;

        if (sequence && sequence.length > 0) {
          const lastBeat = sequence[sequence.length - 1];
          const endPosition =
            lastBeat?.endPosition || lastBeat?.metadata?.endPosition;
          targetEndPosition =
            typeof endPosition === "string" ? endPosition : null;
        } else {
          // For empty sequence, get from start position
          const startPositionData = localStorage.getItem("startPosition");
          if (startPositionData) {
            const startPosition = JSON.parse(startPositionData);
            targetEndPosition = startPosition.endPosition || null;
          }
        }

        // If we have preloaded options for this end position, use them
        if (targetEndPosition && allPreloadedOptions[targetEndPosition]) {
          const optionsForPosition = allPreloadedOptions[targetEndPosition];
          optionsData = optionsForPosition || [];
          uiState.isLoading = false;
          uiState.error = null;

          // Set default tab if needed
          if (
            !uiState.lastSelectedTab[uiState.sortMethod] ||
            uiState.lastSelectedTab[uiState.sortMethod] === null
          ) {
            setLastSelectedTabForSort(uiState.sortMethod, "all");
          }

          return; // Skip the loading process
        }
      }
    } catch (error) {
      console.warn(
        "Failed to load preloaded options, falling back to normal loading:",
        error
      );
    }

    // Normal loading process (only if no preloaded options)
    uiState.isLoading = true;
    uiState.error = null;

    try {
      // Extract end position from sequence for the real OptionDataService
      let nextOptions: PictographData[] = [];

      if (sequence && sequence.length > 0) {
        const lastBeat = sequence[sequence.length - 1];
        const endPosition =
          lastBeat?.endPosition || lastBeat?.metadata?.endPosition;

        if (endPosition && typeof endPosition === "string") {
          // Get the option data service through DI
          const optionDataService = resolve("IOptionDataService") as {
            getNextOptions(sequence: unknown[]): Promise<PictographData[]>;
          };

          // Create a minimal sequence with a beat that has the end position
          const minimalSequence = [
            createBeatData({
              beatNumber: 1,
              metadata: { endPosition: endPosition },
            }),
          ];

          nextOptions = await optionDataService.getNextOptions(minimalSequence);
        } else {
          console.warn("No end position found in sequence");
        }
      } else {
        // For empty sequence, try to get start position from localStorage
        const startPositionData = localStorage.getItem("startPosition");
        if (startPositionData) {
          const startPosition = JSON.parse(startPositionData);
          const endPosition =
            typeof startPosition.endPosition === "string"
              ? startPosition.endPosition
              : null;
          if (endPosition) {
            // Get the option data service through DI
            const optionDataService = resolve("IOptionDataService") as {
              getNextOptions(sequence: unknown[]): Promise<PictographData[]>;
            };

            // Create a minimal sequence with a beat that has the end position
            const minimalSequence = [
              createBeatData({
                beatNumber: 1,
                metadata: { endPosition: endPosition },
              }),
            ];

            nextOptions =
              await optionDataService.getNextOptions(minimalSequence);
          }
        }
      }

      // If we got no options, log a warning but don't treat it as an error
      if (!nextOptions || nextOptions.length === 0) {
        console.warn("No options available for the current sequence");
      }

      optionsData = nextOptions || [];
      uiState.isLoading = false;

      // Only set default tab if we don't have a selected tab yet
      if (
        !uiState.lastSelectedTab[uiState.sortMethod] ||
        uiState.lastSelectedTab[uiState.sortMethod] === null
      ) {
        setLastSelectedTabForSort(uiState.sortMethod, "all");

        if (typeof document !== "undefined") {
          const viewChangeEvent = new CustomEvent("viewchange", {
            detail: { mode: "all" },
            bubbles: true,
          });
          document.dispatchEvent(viewChangeEvent);
        }
      }
    } catch (error) {
      console.error("Error loading options:", error);
      uiState.isLoading = false;
      uiState.error =
        error instanceof Error
          ? error.message
          : "Unknown error loading options";
      optionsData = [];
    }
  }

  function setSortMethod(method: SortMethod) {
    uiState.sortMethod = method;
  }

  function setReversalFilter(_filter: ReversalFilter) {
    // Note: ReversalFilter would need to be added to UIState if needed
  }

  function setLastSelectedTabForSort(
    sortMethod: SortMethod,
    tabKey: string | null
  ) {
    // Avoid unnecessary updates if the value hasn't changed
    if (uiState.lastSelectedTab[sortMethod] === tabKey) {
      return;
    }

    uiState.lastSelectedTab = {
      ...uiState.lastSelectedTab,
      [sortMethod]: tabKey,
    };
  }

  async function selectOption(option: PictographData) {
    // Update selected pictograph
    selectedPictograph = option;

    // Dispatch custom events
    if (typeof document !== "undefined") {
      const beatAddedEvent = new CustomEvent("beat-added", {
        detail: { beat: option },
        bubbles: true,
      });
      document.dispatchEvent(beatAddedEvent);

      const optionSelectedEvent = new CustomEvent("option-selected", {
        detail: { option },
        bubbles: true,
      });
      document.dispatchEvent(optionSelectedEvent);
    }
  }

  function reset() {
    optionsData = [];
    sequenceData = [];

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
    selectedPictograph = null;
  }

  function setLoading(loading: boolean) {
    uiState.isLoading = loading;
  }

  function setError(error: string | null) {
    uiState.error = error;
  }

  // ===== Return Reactive Interface =====
  return {
    // ✅ FIXED: Use getters that access the state directly for reactivity
    get optionsData() {
      return optionsData;
    },
    get sequenceData() {
      return sequenceData;
    },
    get selectedPictograph() {
      return selectedPictograph;
    },
    get filteredOptions() {
      return filteredOptions();
    },
    get groupedOptions() {
      return computeGroupedOptions();
    },
    get categoryKeys() {
      return categoryKeys();
    },

    // ✅ Keep getters for backward compatibility, but prefer direct access above
    get sequence() {
      return sequenceData;
    },
    get allOptions() {
      return optionsData;
    },
    get isLoading() {
      return uiState.isLoading;
    },
    get error() {
      return uiState.error;
    },
    get sortMethod() {
      return uiState.sortMethod;
    },
    get lastSelectedTab() {
      return uiState.lastSelectedTab;
    },

    // Actions
    loadOptions,
    setSortMethod,
    setReversalFilter,
    setLastSelectedTabForSort,
    selectOption,
    reset,
    setLoading,
    setError,

    // Direct state setters (for advanced use)
    setSequence: (seq: PictographData[]) => {
      sequenceData = seq;
    },
    setOptions: (opts: PictographData[]) => {
      optionsData = opts;
    },
    setSelectedPictograph: (opt: PictographData | null) => {
      selectedPictograph = opt;
    },
  };
}
/**
 * Type for the option picker runes instance
 */
export type OptionPickerRunes = ReturnType<typeof createOptionPickerRunes>;
