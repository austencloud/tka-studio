/**
 * OptionPickerScrollState - Svelte 5 runes-based state management for scroll container
 *
 * Extracted from OptionPickerScroll.svelte to provide clean state management using runes.
 * Follows the established patterns from optionPickerRunes.svelte.ts.
 */

import type { PictographData } from "$lib/domain/PictographData";
import type { ResponsiveLayoutConfig } from "./config";
import {
  createPictographOrganizer,
  type OrganizedPictographs,
} from "./services/PictographOrganizerService";
import type { FoldableDetectionResult } from "./utils/deviceDetection";
import {
  createLayoutMetricsCalculator,
  type DeviceInfo,
  type LayoutMetrics,
  type ScrollBehaviorConfig,
} from "./utils/scrollLayoutMetrics";

// ===== Types =====
export interface ScrollContainerProps {
  pictographs: PictographData[];
  onPictographSelected: (pictograph: PictographData) => void;
  containerWidth: number;
  containerHeight: number;
  layoutConfig: ResponsiveLayoutConfig;
  deviceInfo: DeviceInfo;
  foldableInfo: FoldableDetectionResult;
}

export interface ScrollContainerState {
  // Core data
  pictographs: PictographData[];
  organizedPictographs: OrganizedPictographs;

  // Layout state
  layoutMetrics: LayoutMetrics;
  scrollBehavior: ScrollBehaviorConfig;
  cssProperties: Record<string, string | number>;
  cssClasses: string[];

  // UI state
  isEmpty: boolean;
  hasIndividualSections: boolean;
  hasGroupedSections: boolean;
  debugInfo?: () => Record<string, unknown> | null; // For development debugging
}

// ===== Main State Creator =====
/**
 * Creates reactive state for the option picker scroll container using Svelte 5 runes
 */
export function createOptionPickerScrollState(
  initialProps: ScrollContainerProps
) {
  // ===== Core State Using Runes =====
  let pictographs = $state<PictographData[]>(initialProps.pictographs);
  let containerWidth = $state(initialProps.containerWidth);
  let containerHeight = $state(initialProps.containerHeight);
  let layoutConfig = $state<ResponsiveLayoutConfig>(initialProps.layoutConfig);
  let deviceInfo = $state<DeviceInfo>(initialProps.deviceInfo);
  let foldableInfo = $state<FoldableDetectionResult>(initialProps.foldableInfo);

  // ===== Services =====
  const pictographOrganizer = createPictographOrganizer();

  // ===== Derived State Using Runes =====

  // Organized pictographs
  const organizedPictographs = $derived.by(() => {
    return pictographOrganizer.organizePictographs(pictographs);
  });

  // Layout metrics calculator
  const layoutCalculator = createLayoutMetricsCalculator(
    () => containerWidth,
    () => containerHeight,
    () => deviceInfo,
    () => layoutConfig
  );

  // Layout metrics
  const layoutMetrics = $derived(() => layoutCalculator.metrics);
  const scrollBehavior = $derived(() => layoutCalculator.scrollBehavior);
  const cssProperties = $derived(() => layoutCalculator.cssProperties);
  const cssClasses = $derived(() => layoutCalculator.cssClasses);

  // UI state derived values
  const isEmpty = $derived(() => pictographs.length === 0);
  const hasIndividualSections = $derived(
    () => organizedPictographs.hasIndividual
  );
  const hasGroupedSections = $derived(() => organizedPictographs.hasGrouped);

  // Debug info for development
  const debugInfo = $derived(() => {
    if (import.meta.env.DEV) {
      return {
        pictographCount: pictographs.length,
        containerDimensions: { width: containerWidth, height: containerHeight },
        deviceType: deviceInfo.deviceType,
        isFoldable: foldableInfo.isFoldable,
        organizedSections: {
          individual: Object.keys(organizedPictographs.individual).filter(
            (key) => (organizedPictographs.individual?.[key]?.length ?? 0) > 0
          ),
          grouped: Object.keys(organizedPictographs.grouped).filter(
            (key) => (organizedPictographs.grouped?.[key]?.length ?? 0) > 0
          ),
        },
        layoutMetrics: {
          aspectRatio: layoutMetrics().aspectRatio.toFixed(3),
          isLandscape: layoutMetrics().isLandscape,
          shouldUseMobileLayout: layoutMetrics().shouldUseMobileLayout,
          contentPadding: layoutMetrics().contentPadding,
        },
      };
    }
    return null;
  });

  // ===== Actions =====

  /**
   * Updates the pictographs data
   */
  function updatePictographs(newPictographs: PictographData[]) {
    pictographs = newPictographs;
  }

  /**
   * Updates container dimensions
   */
  function updateContainerDimensions(width: number, height: number) {
    containerWidth = width;
    containerHeight = height;
  }

  /**
   * Updates layout configuration
   */
  function updateLayoutConfig(newConfig: ResponsiveLayoutConfig) {
    layoutConfig = newConfig;
  }

  /**
   * Updates device information
   */
  function updateDeviceInfo(newDeviceInfo: DeviceInfo) {
    deviceInfo = newDeviceInfo;
  }

  /**
   * Updates foldable device information
   */
  function updateFoldableInfo(newFoldableInfo: FoldableDetectionResult) {
    foldableInfo = newFoldableInfo;
  }

  /**
   * Bulk update of all props (useful for prop changes)
   */
  function updateProps(newProps: Partial<ScrollContainerProps>) {
    if (newProps.pictographs !== undefined) {
      pictographs = newProps.pictographs;
    }
    if (newProps.containerWidth !== undefined) {
      containerWidth = newProps.containerWidth;
    }
    if (newProps.containerHeight !== undefined) {
      containerHeight = newProps.containerHeight;
    }
    if (newProps.layoutConfig !== undefined) {
      layoutConfig = newProps.layoutConfig;
    }
    if (newProps.deviceInfo !== undefined) {
      deviceInfo = newProps.deviceInfo;
    }
    if (newProps.foldableInfo !== undefined) {
      foldableInfo = newProps.foldableInfo;
    }
  }

  /**
   * Gets current state snapshot
   */
  function getStateSnapshot(): ScrollContainerState {
    return {
      pictographs,
      organizedPictographs,
      layoutMetrics: layoutMetrics(),
      scrollBehavior: scrollBehavior(),
      cssProperties: cssProperties(),
      cssClasses: cssClasses(),
      isEmpty: isEmpty(),
      hasIndividualSections: hasIndividualSections(),
      hasGroupedSections: hasGroupedSections(),
      debugInfo,
    };
  }

  // ===== Effects for Development Debugging =====
  // DISABLED: This was causing ResizeObserver loop errors and performance issues
  // The constant logging during layout changes was triggering infinite resize loops
  /*
	if (import.meta.env.DEV) {
		$effect(() => {
			// Log significant state changes in development
			if (pictographs.length > 0) {
				console.log('🔄 OptionPickerScrollState: State updated', {
					pictographCount: pictographs.length,
					hasIndividual: hasIndividualSections,
					hasGrouped: hasGroupedSections,
					layoutMetrics: {
						mobile: layoutMetrics().shouldUseMobileLayout,
						foldable: layoutMetrics().isFoldableDevice,
						aspectRatio: layoutMetrics().aspectRatio.toFixed(3),
					},
				});
			}
		});
	}
	*/

  // ===== Return Reactive Interface =====
  return {
    // Reactive getters
    get pictographs() {
      return pictographs;
    },
    get organizedPictographs() {
      return organizedPictographs;
    },
    get layoutMetrics() {
      return layoutMetrics;
    },
    get scrollBehavior() {
      return scrollBehavior;
    },
    get cssProperties() {
      return cssProperties;
    },
    get cssClasses() {
      return cssClasses;
    },
    get isEmpty() {
      return isEmpty;
    },
    get hasIndividualSections() {
      return hasIndividualSections;
    },
    get hasGroupedSections() {
      return hasGroupedSections;
    },
    get debugInfo() {
      return debugInfo;
    },

    // Container dimensions
    get containerWidth() {
      return containerWidth;
    },
    get containerHeight() {
      return containerHeight;
    },
    get layoutConfig() {
      return layoutConfig;
    },
    get deviceInfo() {
      return deviceInfo;
    },
    get foldableInfo() {
      return foldableInfo;
    },

    // Actions
    updatePictographs,
    updateContainerDimensions,
    updateLayoutConfig,
    updateDeviceInfo,
    updateFoldableInfo,
    updateProps,
    getStateSnapshot,

    // Direct access to services (for advanced usage)
    pictographOrganizer,
  };
}

// ===== Type Export =====
export type OptionPickerScrollState = ReturnType<
  typeof createOptionPickerScrollState
>;

// ===== Utility Functions =====

/**
 * Creates state with default values for testing or fallback scenarios
 */
export function createDefaultScrollState(): OptionPickerScrollState {
  const defaultProps: ScrollContainerProps = {
    pictographs: [],
    onPictographSelected: () => {},
    containerWidth: 800,
    containerHeight: 600,
    layoutConfig: {
      gridColumns: "repeat(4, minmax(0, 1fr))",
      optionSize: "100px",
      gridGap: "8px",
      gridClass: "",
      aspectClass: "",
      scaleFactor: 1.0,
    },
    deviceInfo: {
      deviceType: "desktop",
      isFoldable: false,
      foldableInfo: {
        isFoldable: false,
        isUnfolded: false,
        foldableType: "unknown",
        confidence: 0,
      },
    },
    foldableInfo: {
      isFoldable: false,
      isUnfolded: false,
      foldableType: "unknown",
      confidence: 0,
    },
  };

  return createOptionPickerScrollState(defaultProps);
}

/**
 * Validates scroll state props
 */
export function validateScrollStateProps(
  props: Partial<ScrollContainerProps>
): {
  isValid: boolean;
  errors: string[];
  warnings: string[];
} {
  const errors: string[] = [];
  const warnings: string[] = [];

  if (props.containerWidth !== undefined && props.containerWidth <= 0) {
    errors.push("Container width must be positive");
  }

  if (props.containerHeight !== undefined && props.containerHeight <= 0) {
    errors.push("Container height must be positive");
  }

  if (props.pictographs && !Array.isArray(props.pictographs)) {
    errors.push("Pictographs must be an array");
  }

  if (props.containerWidth !== undefined && props.containerWidth < 200) {
    warnings.push("Container width is very narrow, consider minimum 200px");
  }

  if (props.containerHeight !== undefined && props.containerHeight < 300) {
    warnings.push("Container height is very short, consider minimum 300px");
  }

  return {
    isValid: errors.length === 0,
    errors,
    warnings,
  };
}
