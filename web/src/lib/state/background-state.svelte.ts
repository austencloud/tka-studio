import type { IBackgroundService } from "$contracts";
import {
  BackgroundType,
  type BackgroundSystem,
  type PerformanceMetrics,
  type QualityLevel,
} from "$domain";
import { resolve, TYPES } from "$lib/services/inversify/container";

export function createBackgroundState() {
  // Get services from DI container
  const backgroundService = resolve(
    TYPES.IBackgroundService
  ) as IBackgroundService;

  // Runes-based reactive state
  let backgroundType = $state<BackgroundType>(BackgroundType.NIGHT_SKY);
  let quality = $state<QualityLevel>("medium");
  let isLoading = $state(true);
  let currentSystem = $state<BackgroundSystem | null>(null);
  let metrics = $state<PerformanceMetrics>({ fps: 60, warnings: [] });

  // Derived state
  const isReady = $derived(currentSystem !== null && !isLoading);
  const hasWarnings = $derived(metrics.warnings.length > 0);
  const shouldOptimize = $derived(metrics.fps < 30);

  return {
    // State getters
    get backgroundType() {
      return backgroundType;
    },
    get quality() {
      return quality;
    },
    get isLoading() {
      return isLoading;
    },
    get currentSystem() {
      return currentSystem;
    },
    get metrics() {
      return metrics;
    },
    get isReady() {
      return isReady;
    },
    get hasWarnings() {
      return hasWarnings;
    },
    get shouldOptimize() {
      return shouldOptimize;
    },

    // Actions
    async setBackgroundType(newType: BackgroundType) {
      isLoading = true;
      try {
        backgroundType = newType;
        currentSystem = await backgroundService.createSystem(newType, quality);
      } finally {
        isLoading = false;
      }
    },

    async setQuality(newQuality: QualityLevel) {
      quality = newQuality;
      if (currentSystem) {
        currentSystem.setQuality(newQuality);
      }
    },

    updateMetrics(newMetrics: PerformanceMetrics) {
      metrics = newMetrics;
    },
  };
}
