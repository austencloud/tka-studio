/**
 * Deep Ocean Background State
 *
 * Domain state management for deep ocean background configuration.
 * Handles user preferences, performance settings, and runtime state.
 *
 * This is PURE STATE - no business logic, just reactive state management.
 */
import type { QualityLevel, AccessibilitySettings, Dimensions } from "$shared";

export interface DeepOceanBackgroundConfig {
  quality: QualityLevel;
  accessibility: AccessibilitySettings;
  paused: boolean;
  autoQualityAdjustment: boolean;
  showPerformanceMetrics: boolean;
}

export function createDeepOceanBackgroundState(
  initialDimensions: Dimensions,
  initialConfig?: Partial<DeepOceanBackgroundConfig>
) {
  // Reactive state
  let dimensions = $state<Dimensions>(initialDimensions);
  let config = $state<DeepOceanBackgroundConfig>({
    quality: "medium",
    accessibility: {
      reducedMotion: false,
      highContrast: false,
      visibleParticleSize: 1,
    },
    paused: false,
    autoQualityAdjustment: true,
    showPerformanceMetrics: false,
    ...initialConfig,
  });

  let isInitialized = $state(false);
  let lastPerformanceCheck = $state(0);
  let performanceWarnings = $state<string[]>([]);

  // Derived state
  const shouldShowMetrics = $derived(
    config.showPerformanceMetrics && !config.accessibility.reducedMotion
  );

  const effectiveQuality = $derived(() => {
    // Reduce quality for accessibility or small screens
    if (config.accessibility.reducedMotion) return "minimal";
    if (dimensions.width < 400 || dimensions.height < 300) return "low";
    return config.quality;
  });

  const isHighPerformanceMode = $derived(
    effectiveQuality() === "high" && !config.accessibility.reducedMotion
  );

  return {
    // Getters
    get dimensions() {
      return dimensions;
    },
    get config() {
      return config;
    },
    get isInitialized() {
      return isInitialized;
    },
    get lastPerformanceCheck() {
      return lastPerformanceCheck;
    },
    get performanceWarnings() {
      return performanceWarnings;
    },

    // Derived getters
    get shouldShowMetrics() {
      return shouldShowMetrics;
    },
    get effectiveQuality() {
      return effectiveQuality();
    },
    get isHighPerformanceMode() {
      return isHighPerformanceMode;
    },

    // State updaters
    updateDimensions: (newDimensions: Dimensions) => {
      dimensions = newDimensions;
    },

    updateQuality: (quality: QualityLevel) => {
      config = { ...config, quality };
    },

    updateAccessibility: (accessibility: Partial<AccessibilitySettings>) => {
      config = {
        ...config,
        accessibility: { ...config.accessibility, ...accessibility },
      };
    },

    togglePause: () => {
      config = { ...config, paused: !config.paused };
    },

    setPaused: (paused: boolean) => {
      config = { ...config, paused };
    },

    togglePerformanceMetrics: () => {
      config = {
        ...config,
        showPerformanceMetrics: !config.showPerformanceMetrics,
      };
    },

    markInitialized: () => {
      isInitialized = true;
    },

    recordPerformanceCheck: (warnings: string[] = []) => {
      lastPerformanceCheck = Date.now();
      performanceWarnings = [...warnings];
    },

    // Configuration helpers
    getCanvasConfig: () => ({
      dimensions,
      quality: effectiveQuality(),
      paused: config.paused,
      accessibility: config.accessibility,
    }),

    // Reset state
    reset: () => {
      isInitialized = false;
      lastPerformanceCheck = 0;
      performanceWarnings = [];
    },
  };
}

export type DeepOceanBackgroundState = ReturnType<
  typeof createDeepOceanBackgroundState
>;
