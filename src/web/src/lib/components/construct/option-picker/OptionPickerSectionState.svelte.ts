/**
 * OptionPickerSectionState.svelte.ts - PURE RUNES Advanced section state management
 *
 * Manages sophisticated layout and state including device detection, responsive layouts,
 * and advanced layout context using ONLY Svelte 5 runes - no stores whatsoever.
 */

import type { PictographData } from "$lib/domain/PictographData";
import {
  BREAKPOINTS,
  getContainerAspect,
  type ContainerAspect,
  type DeviceType,
  type ResponsiveLayoutConfig,
} from "./config";
import { createOptionPickerRunes } from "./optionPickerRunes.svelte";
import {
  detectFoldableDevice,
  type FoldableDetectionResult,
} from "./utils/deviceDetection";
import {
  getEnhancedDeviceType,
  getResponsiveLayout,
} from "./utils/layoutUtils";

export interface SectionState {
  // Loading and initialization
  loadingOptions: boolean;
  uiInitialized: boolean;
  scrollAreaReady: boolean;

  // Section-specific state
  isExpanded: boolean;
  selectedPictograph: PictographData | null;

  // Advanced layout state
  containerWidth: number;
  containerHeight: number;
  windowWidth: number;
  windowHeight: number;
  deviceType: DeviceType;
  isMobile: boolean;
  isTablet: boolean;
  isPortrait: boolean;
  containerAspect: ContainerAspect;
  layoutConfig: ResponsiveLayoutConfig;
  foldableInfo: FoldableDetectionResult;

  // Legacy compatibility
  optionPickerWidth: number | null;
  isGroupable: boolean | null;
}

/**
 * Create section state manager using ONLY Svelte 5 runes with sophisticated layout
 */
export function createSectionState(
  letterType: string,
  initialExpanded: boolean = true,
) {
  // Basic state using runes
  let loadingOptions = $state(false);
  let uiInitialized = $state(false);
  let scrollAreaReady = $state(false);
  let isExpanded = $state(initialExpanded);
  let selectedPictograph = $state<PictographData | null>(null);

  // Advanced layout state using runes
  let containerWidth = $state(
    typeof window !== "undefined"
      ? Math.max(300, window.innerWidth * 0.8)
      : BREAKPOINTS.desktop,
  );
  let containerHeight = $state(
    typeof window !== "undefined"
      ? Math.max(200, window.innerHeight * 0.6)
      : 768,
  );
  let windowWidth = $state(
    typeof window !== "undefined" ? window.innerWidth : BREAKPOINTS.desktop,
  );
  let windowHeight = $state(
    typeof window !== "undefined" ? window.innerHeight : 768,
  );

  // Derived sophisticated layout state using runes
  const foldableInfo = $derived(() => detectFoldableDevice());

  const enhancedDeviceInfo = $derived(() => {
    const isMobileUserAgent =
      typeof navigator !== "undefined" &&
      /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
    return getEnhancedDeviceType(containerWidth, isMobileUserAgent);
  });

  const deviceType = $derived(() => enhancedDeviceInfo().deviceType);
  const isMobile = $derived(
    () => deviceType() === "smallMobile" || deviceType() === "mobile",
  );
  const isTablet = $derived(() => deviceType() === "tablet");
  const isPortrait = $derived(() => containerHeight > containerWidth);
  const containerAspect = $derived(() =>
    getContainerAspect(containerWidth, containerHeight),
  );

  // Calculate responsive layout configuration
  const layoutConfig = $derived(() => {
    // For section state, we use a default count of 10 for layout calculations
    // This will be overridden by actual option counts in the components
    const defaultCount = 10;

    return getResponsiveLayout(
      defaultCount,
      containerHeight,
      containerWidth,
      isMobile(),
      isPortrait(),
      foldableInfo(),
    );
  });

  // Legacy compatibility derived state
  const optionPickerWidth = $derived(() => containerWidth);
  const isGroupable = $derived(() =>
    ["Type4", "Type5", "Type6"].includes(letterType),
  );

  // Additional derived state
  const canLoadOptions = $derived(() => {
    return uiInitialized && scrollAreaReady && !loadingOptions;
  });

  const isReady = $derived(() => {
    return uiInitialized && scrollAreaReady;
  });

  // Debounced dimension updates using pure functions
  const debouncedUpdateDimensions = (() => {
    let timeoutId: ReturnType<typeof setTimeout> | null = null;

    return (newContainerWidth: number, newContainerHeight: number) => {
      if (timeoutId !== null) {
        clearTimeout(timeoutId);
      }

      timeoutId = setTimeout(() => {
        // Ensure we never set invalid dimensions
        if (newContainerWidth > 0 && newContainerHeight > 0) {
          containerWidth = newContainerWidth;
          containerHeight = newContainerHeight;
        } else {
          // Use fallback values based on window size
          if (newContainerWidth <= 0) {
            const fallbackWidth =
              typeof window !== "undefined"
                ? Math.max(300, window.innerWidth * 0.8)
                : BREAKPOINTS.desktop;
            containerWidth = fallbackWidth;
          }

          if (newContainerHeight <= 0) {
            const fallbackHeight =
              typeof window !== "undefined"
                ? Math.max(200, window.innerHeight * 0.6)
                : 768;
            containerHeight = fallbackHeight;
          }
        }
        timeoutId = null;
      }, 100);
    };
  })();

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

  function updateContainerDimensions(width: number, height: number) {
    debouncedUpdateDimensions(width, height);
  }

  function updateWindowDimensions(width: number, height: number) {
    windowWidth = width;
    windowHeight = height;
  }

  // Legacy compatibility function
  function updateOptionPickerWidth(width: number) {
    updateContainerDimensions(width, containerHeight);
  }

  function resetState() {
    loadingOptions = false;
    selectedPictograph = null;
    // Keep UI initialization and expansion state
  }

  // Return reactive state and functions
  return {
    // Basic reactive state (getters)
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

    // Advanced layout reactive state
    get containerWidth() {
      return containerWidth;
    },
    get containerHeight() {
      return containerHeight;
    },
    get windowWidth() {
      return windowWidth;
    },
    get windowHeight() {
      return windowHeight;
    },
    get deviceType() {
      return deviceType;
    },
    get isMobile() {
      return isMobile;
    },
    get isTablet() {
      return isTablet;
    },
    get isPortrait() {
      return isPortrait;
    },
    get containerAspect() {
      return containerAspect;
    },
    get layoutConfig() {
      return layoutConfig;
    },
    get foldableInfo() {
      return foldableInfo;
    },

    // Legacy compatibility
    get optionPickerWidth() {
      return optionPickerWidth;
    },
    get isGroupable() {
      return isGroupable;
    },

    // Derived state
    get canLoadOptions() {
      return canLoadOptions;
    },
    get isReady() {
      return isReady;
    },

    // State management functions
    setLoadingOptions,
    setUiInitialized,
    setScrollAreaReady,
    toggleExpanded,
    setExpanded,
    setSelectedPictograph,
    updateContainerDimensions,
    updateWindowDimensions,
    updateOptionPickerWidth, // Legacy compatibility
    resetState,
  };
}

/**
 * Create global option picker state using ONLY Svelte 5 runes with sophisticated layout
 * This is the main state manager that coordinates everything
 */
export function createOptionPickerState() {
  // Use the main runes-based store
  const optionPickerRunes = createOptionPickerRunes();

  // Advanced layout state using runes
  let containerWidth = $state(
    typeof window !== "undefined"
      ? Math.max(300, window.innerWidth * 0.8)
      : BREAKPOINTS.desktop,
  );
  let containerHeight = $state(
    typeof window !== "undefined"
      ? Math.max(200, window.innerHeight * 0.6)
      : 768,
  );
  let windowWidth = $state(
    typeof window !== "undefined" ? window.innerWidth : BREAKPOINTS.desktop,
  );
  let windowHeight = $state(
    typeof window !== "undefined" ? window.innerHeight : 768,
  );

  // Derived sophisticated state using runes
  const foldableInfo = $derived(() => detectFoldableDevice());

  const enhancedDeviceInfo = $derived(() => {
    const isMobileUserAgent =
      typeof navigator !== "undefined" &&
      /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
    return getEnhancedDeviceType(containerWidth, isMobileUserAgent);
  });

  const deviceType = $derived(() => enhancedDeviceInfo().deviceType);
  const isMobile = $derived(
    () => deviceType() === "smallMobile" || deviceType() === "mobile",
  );
  const isTablet = $derived(() => deviceType() === "tablet");
  const isPortrait = $derived(() => containerHeight > containerWidth);
  const containerAspect = $derived(() =>
    getContainerAspect(containerWidth, containerHeight),
  );

  // Calculate layout for current options
  const currentLayoutConfig = $derived(() => {
    const optionsCount = optionPickerRunes.optionsData.length;

    return getResponsiveLayout(
      optionsCount,
      containerHeight,
      containerWidth,
      isMobile(),
      isPortrait(),
      foldableInfo(),
    );
  });

  // Section states for each letter type using Map with runes
  const sectionStates = new Map<
    string,
    ReturnType<typeof createSectionState>
  >();

  // Initialize section states
  function initializeSectionStates() {
    const letterTypes = ["Type1", "Type2", "Type3", "Type4", "Type5", "Type6"];
    letterTypes.forEach((letterType) => {
      if (!sectionStates.has(letterType)) {
        sectionStates.set(letterType, createSectionState(letterType));
      }
    });
  }

  // Get section state
  function getSectionState(letterType: string) {
    if (!sectionStates.has(letterType)) {
      sectionStates.set(letterType, createSectionState(letterType));
    }
    const sectionState = sectionStates.get(letterType);
    if (!sectionState) {
      throw new Error(`Failed to create section state for ${letterType}`);
    }
    return sectionState;
  }

  // Debounced dimension updates
  const debouncedUpdateDimensions = (() => {
    let timeoutId: ReturnType<typeof setTimeout> | null = null;

    return (newContainerWidth: number, newContainerHeight: number) => {
      if (timeoutId !== null) {
        clearTimeout(timeoutId);
      }

      timeoutId = setTimeout(() => {
        // Ensure we never set invalid dimensions
        if (newContainerWidth > 0 && newContainerHeight > 0) {
          containerWidth = newContainerWidth;
          containerHeight = newContainerHeight;
        } else {
          // Use fallback values
          if (newContainerWidth <= 0) {
            const fallbackWidth =
              typeof window !== "undefined"
                ? Math.max(300, window.innerWidth * 0.8)
                : BREAKPOINTS.desktop;
            containerWidth = fallbackWidth;
          }

          if (newContainerHeight <= 0) {
            const fallbackHeight =
              typeof window !== "undefined"
                ? Math.max(200, window.innerHeight * 0.6)
                : 768;
            containerHeight = fallbackHeight;
          }
        }

        // Update all section states with new dimensions
        sectionStates.forEach((sectionState) => {
          sectionState.updateContainerDimensions(
            containerWidth,
            containerHeight,
          );
        });

        timeoutId = null;
      }, 100);
    };
  })();

  // Global state management functions
  function setContainerDimensions(width: number, height: number) {
    debouncedUpdateDimensions(width, height);
  }

  function setWindowDimensions(width: number, height: number) {
    windowWidth = width;
    windowHeight = height;

    // Update all section states with new window dimensions
    sectionStates.forEach((sectionState) => {
      sectionState.updateWindowDimensions(width, height);
    });
  }

  function resetAllStates() {
    optionPickerRunes.reset();

    // Reset all section states
    sectionStates.forEach((sectionState) => {
      sectionState.resetState();
    });
  }

  // Initialize section states
  initializeSectionStates();

  return {
    // ✅ FIXED: Explicitly expose reactive getters instead of spreading
    // This ensures reactivity is preserved when wrapping the runes
    get optionsData() {
      return optionPickerRunes.optionsData;
    },
    get sequenceData() {
      return optionPickerRunes.sequenceData;
    },
    get selectedPictograph() {
      return optionPickerRunes.selectedPictograph;
    },
    get filteredOptions() {
      return optionPickerRunes.filteredOptions;
    },
    get groupedOptions() {
      return optionPickerRunes.groupedOptions;
    },
    get categoryKeys() {
      return optionPickerRunes.categoryKeys;
    },

    // Expose other runes interface methods
    get sequence() {
      return optionPickerRunes.sequence;
    },
    get allOptions() {
      return optionPickerRunes.allOptions;
    },
    get isLoading() {
      return optionPickerRunes.isLoading;
    },
    get error() {
      return optionPickerRunes.error;
    },
    get sortMethod() {
      return optionPickerRunes.sortMethod;
    },
    get lastSelectedTab() {
      return optionPickerRunes.lastSelectedTab;
    },

    // Actions
    loadOptions: optionPickerRunes.loadOptions,
    setSortMethod: optionPickerRunes.setSortMethod,
    setReversalFilter: optionPickerRunes.setReversalFilter,
    setLastSelectedTabForSort: optionPickerRunes.setLastSelectedTabForSort,
    selectOption: optionPickerRunes.selectOption,
    reset: optionPickerRunes.reset,
    setLoading: optionPickerRunes.setLoading,
    setError: optionPickerRunes.setError,
    setSequence: optionPickerRunes.setSequence,
    setOptions: optionPickerRunes.setOptions,

    // Advanced layout reactive state
    get containerWidth() {
      return containerWidth;
    },
    get containerHeight() {
      return containerHeight;
    },
    get windowWidth() {
      return windowWidth;
    },
    get windowHeight() {
      return windowHeight;
    },
    get deviceType() {
      return deviceType;
    },
    get isMobile() {
      return isMobile;
    },
    get isTablet() {
      return isTablet;
    },
    get isPortrait() {
      return isPortrait;
    },
    get containerAspect() {
      return containerAspect;
    },
    get layoutConfig() {
      return currentLayoutConfig;
    },
    get foldableInfo() {
      return foldableInfo;
    },

    // Section state management
    getSectionState,

    // Enhanced state management
    setContainerDimensions,
    setWindowDimensions,
    resetAllStates,
  };
}
