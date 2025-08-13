/**
 * Modern Pictograph Service using Svelte 5 Runes
 *
 * Provides reactive pictograph data and rendering coordination using pure runes.
 * This complements the existing class-based services.
 */

import { ensureModernPictographData } from "$lib/components/pictograph/dataAdapter";
import type { BeatData, PictographData } from "$lib/domain";

interface PictographServiceConfig {
  defaultGridMode: "diamond" | "box";
  debugMode: boolean;
  loadingTimeout: number;
}

/**
 * Create a reactive pictograph service using runes
 */
export function createPictographService(
  config: Partial<PictographServiceConfig> = {},
) {
  // Configuration with defaults
  const serviceConfig: PictographServiceConfig = {
    defaultGridMode: "diamond",
    debugMode: false,
    loadingTimeout: 5000,
    ...config,
  };

  // Reactive state using runes
  let currentPictographData = $state<PictographData | null>(null);
  let isLoading = $state(false);
  let errorMessage = $state<string | null>(null);
  const loadedComponents = $state(new Set<string>());

  // Derived state
  const hasValidData = $derived(() => currentPictographData != null);
  const loadingProgress = $derived(() => {
    if (!hasValidData()) return 0;
    // Calculate based on required components
    const requiredComponents = getRequiredComponents();
    if (requiredComponents.length === 0) return 100;
    return Math.round(
      (loadedComponents.size / requiredComponents.length) * 100,
    );
  });

  // Helper function to determine required components
  function getRequiredComponents(): string[] {
    if (!currentPictographData) return [];

    const components = ["grid"];

    if (currentPictographData.arrows?.blue) components.push("blue-arrow");
    if (currentPictographData.arrows?.red) components.push("red-arrow");
    if (currentPictographData.props?.blue) components.push("blue-prop");
    if (currentPictographData.props?.red) components.push("red-prop");

    return components;
  }

  // Public methods
  const service = {
    // Getters (reactive)
    get currentData() {
      return currentPictographData;
    },
    get isLoading() {
      return isLoading;
    },
    get errorMessage() {
      return errorMessage;
    },
    get loadingProgress() {
      return loadingProgress();
    },
    get hasValidData() {
      return hasValidData();
    },

    // Methods
    setPictographData(data: unknown) {
      try {
        errorMessage = null;
        const modernData = ensureModernPictographData(
          data as Record<string, unknown>,
        );

        if (modernData) {
          currentPictographData = modernData;
          loadedComponents.clear();
          isLoading = true;

          if (serviceConfig.debugMode) {
            console.log("📊 PictographService: Data set", modernData);
          }
        } else {
          throw new Error("Invalid pictograph data provided");
        }
      } catch (error) {
        errorMessage = error instanceof Error ? error.message : "Unknown error";
        currentPictographData = null;
        isLoading = false;
      }
    },

    setBeatData(beat: BeatData) {
      if (beat.pictograph_data) {
        this.setPictographData(beat.pictograph_data);
      } else {
        currentPictographData = null;
        isLoading = false;
        loadedComponents.clear();
      }
    },

    markComponentLoaded(componentName: string) {
      loadedComponents.add(componentName);

      if (serviceConfig.debugMode) {
        console.log(`📦 Component loaded: ${componentName}`, {
          loaded: loadedComponents.size,
          required: getRequiredComponents().length,
        });
      }

      // Check if all components are loaded
      const required = getRequiredComponents();
      if (required.every((comp) => loadedComponents.has(comp))) {
        isLoading = false;

        if (serviceConfig.debugMode) {
          console.log("✅ All components loaded");
        }
      }
    },

    markComponentError(componentName: string, error: string) {
      errorMessage = `${componentName}: ${error}`;

      if (serviceConfig.debugMode) {
        console.error(`❌ Component error: ${componentName}`, error);
      }

      // Still mark as loaded to prevent blocking
      this.markComponentLoaded(componentName);
    },

    reset() {
      currentPictographData = null;
      isLoading = false;
      errorMessage = null;
      loadedComponents.clear();
    },

    // Configuration
    setDebugMode(enabled: boolean) {
      serviceConfig.debugMode = enabled;
    },

    getConfig() {
      return { ...serviceConfig };
    },
  };

  return service;
}

/**
 * Global instance for shared use (optional)
 */
export const globalPictographService = createPictographService();

/**
 * Helper function to create a pictograph service bound to a specific beat
 */
export function createBeatPictographService(
  beat: BeatData,
  config?: Partial<PictographServiceConfig>,
) {
  const service = createPictographService(config);
  service.setBeatData(beat);
  return service;
}
