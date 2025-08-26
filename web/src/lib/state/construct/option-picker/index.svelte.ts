/**
 * Section State Orchestrator - Pure Svelte 5 Runes
 *
 * Combines smaller state modules into a unified section state manager.
 * This replaces the monolithic OptionPickerSectionState with a composable approach.
 */

import type { PictographData } from "$lib/domain/PictographData";
import type {
  ContainerAspect,
  DeviceType,
  ResponsiveLayoutConfig,
} from "./config";
import type { FoldableDetectionResult } from "./utils/deviceDetection";
import { createContainerState } from "./containerState.svelte";
import { createDeviceState } from "./deviceState.svelte";
import { createLayoutState } from "./layoutState.svelte";
import { createUIState } from "./uiState.svelte";

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
 * Create section state manager using composable state modules
 */
export function createSectionState(
  letterType: string,
  initialExpanded: boolean = true
) {
  // Create individual state modules
  const deviceState = createDeviceState();
  const containerState = createContainerState();
  const uiState = createUIState(initialExpanded);

  // Layout state depends on device and container state
  const layoutState = createLayoutState(
    deviceState.state,
    containerState.state,
    0 // Default options count
  );

  // Initialize window listener on mount
  function initializeListeners() {
    deviceState.initializeWindowListener();
  }

  // Cleanup listeners
  function destroyListeners() {
    deviceState.destroyWindowListener();
  }

  return {
    // Delegate to sub-states
    get loadingOptions() {
      return uiState.loadingOptions;
    },
    get uiInitialized() {
      return uiState.uiInitialized;
    },
    get scrollAreaReady() {
      return uiState.scrollAreaReady;
    },
    get isExpanded() {
      return uiState.isExpanded;
    },
    get selectedPictograph() {
      return uiState.selectedPictograph;
    },

    get containerWidth() {
      return containerState.containerWidth;
    },
    get containerHeight() {
      return containerState.containerHeight;
    },
    get containerAspect() {
      return containerState.containerAspect;
    },

    get windowWidth() {
      return deviceState.windowWidth;
    },
    get windowHeight() {
      return deviceState.windowHeight;
    },
    get deviceType() {
      return deviceState.deviceType;
    },
    get isMobile() {
      return deviceState.isMobile;
    },
    get isTablet() {
      return deviceState.isTablet;
    },
    get isPortrait() {
      return deviceState.isPortrait;
    },
    get foldableInfo() {
      return deviceState.foldableInfo;
    },

    get layoutConfig() {
      return layoutState.layoutConfig;
    },

    // Legacy compatibility
    get optionPickerWidth() {
      return containerState.containerWidth;
    },
    get isGroupable() {
      return !deviceState.isMobile;
    },

    // Actions
    setLoadingOptions: uiState.setLoadingOptions,
    setUiInitialized: uiState.setUiInitialized,
    setScrollAreaReady: uiState.setScrollAreaReady,
    toggleExpanded: uiState.toggleExpanded,
    setExpanded: uiState.setExpanded,
    setSelectedPictograph: uiState.setSelectedPictograph,
    updateContainerDimensions: containerState.updateContainerDimensions,

    // Lifecycle
    initializeListeners,
    destroyListeners,

    // Combined state object (for compatibility)
    get state(): SectionState {
      return {
        loadingOptions: uiState.loadingOptions,
        uiInitialized: uiState.uiInitialized,
        scrollAreaReady: uiState.scrollAreaReady,
        isExpanded: uiState.isExpanded,
        selectedPictograph: uiState.selectedPictograph,

        containerWidth: containerState.containerWidth,
        containerHeight: containerState.containerHeight,
        containerAspect: containerState.containerAspect,

        windowWidth: deviceState.windowWidth,
        windowHeight: deviceState.windowHeight,
        deviceType: deviceState.deviceType,
        isMobile: deviceState.isMobile,
        isTablet: deviceState.isTablet,
        isPortrait: deviceState.isPortrait,
        foldableInfo: deviceState.foldableInfo,

        layoutConfig: layoutState.layoutConfig,

        // Legacy compatibility
        optionPickerWidth: containerState.containerWidth,
        isGroupable: !deviceState.isMobile,
      };
    },
  };
}
