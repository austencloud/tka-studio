/**
 * UI State - Pure Svelte 5 Runes
 *
 * Handles basic UI state like loading, expansion, and selection
 */

import type { PictographData } from "$lib/domain/PictographData";

export interface UIState {
  loadingOptions: boolean;
  uiInitialized: boolean;
  scrollAreaReady: boolean;
  isExpanded: boolean;
  selectedPictograph: PictographData | null;
}

export function createUIState(initialExpanded: boolean = true) {
  // Basic UI state using runes
  let loadingOptions = $state(false);
  let uiInitialized = $state(false);
  let scrollAreaReady = $state(false);
  let isExpanded = $state(initialExpanded);
  let selectedPictograph = $state<PictographData | null>(null);

  // State management functions
  function setLoadingOptions(loading: boolean) {
    loadingOptions = loading;
  }

  function setUiInitialized(initialized: boolean) {
    uiInitialized = initialized;
  }

  function setScrollAreaReady(ready: boolean) {
    scrollAreaReady = ready;
  }

  function toggleExpanded() {
    isExpanded = !isExpanded;
  }

  function setExpanded(expanded: boolean) {
    isExpanded = expanded;
  }

  function setSelectedPictograph(pictograph: PictographData | null) {
    selectedPictograph = pictograph;
  }

  return {
    // State accessors
    get loadingOptions() {
      return loadingOptions;
    },
    get uiInitialized() {
      return uiInitialized;
    },
    get scrollAreaReady() {
      return scrollAreaReady;
    },
    get isExpanded() {
      return isExpanded;
    },
    get selectedPictograph() {
      return selectedPictograph;
    },

    // Actions
    setLoadingOptions,
    setUiInitialized,
    setScrollAreaReady,
    toggleExpanded,
    setExpanded,
    setSelectedPictograph,

    // Derived state object
    get state(): UIState {
      return {
        loadingOptions,
        uiInitialized,
        scrollAreaReady,
        isExpanded,
        selectedPictograph,
      };
    },
  };
}
