/**
 * Refactored Application State - Clean Architecture
 *
 * Orchestrates focused state services following Single Responsibility Principle.
 * Each service handles one specific concern, making the code maintainable and testable.
 *
 * This replaces the 460-line monolith with a clean, focused architecture.
 */

import type { AppSettings, PerformanceSnapshot } from "$shared";
import { BackgroundType } from "../../background";
import { GridMode } from "../../pictograph";
import {
  areServicesInitialized,
  getSettingsServiceSync,
} from "./services.svelte";

export {
  getInitializationComplete,
  getInitializationError,
  getInitializationProgress,
  getIsInitialized,
  getIsInitializing,
  initializeAppState,
  setInitializationError,
  setInitializationProgress,
  setInitializationState,
} from "./initialization-state.svelte";

export {
  // Primary module API
  getActiveModule,
  getActiveModuleOrDefault,
  isModuleActive,
  setActiveModule,
  // Legacy tab API (deprecated)
  getActiveTab,
  getActiveTabOrDefault,
  isTabActive,
  setActiveTab,
  // UI state
  getIsFullScreen,
  getIsTransitioning,
  getShowSettings,
  getShowSpotlight,
  getSpotlightSequence,
  getSpotlightThumbnailService,
  hideSettingsDialog,
  closeSpotlightViewer,
  setFullScreen,
  showSettingsDialog,
  openSpotlightViewer,
  toggleSettingsDialog,
} from "./ui/ui-state.svelte";

export {
  getInitialTabFromCache,
  initializeTabPersistence,
  switchTab,
} from "./ui/tab-state";

import {
  getInitializationError,
  getIsInitialized,
  getIsInitializing,
  resetInitializationState,
} from "./initialization-state.svelte";
import { initializeTabPersistence as initializeTabPersistenceInternal } from "./ui/tab-state";
import {
  getIsFullScreen,
  getIsTransitioning,
  getShowSettings,
  resetUIState,
} from "./ui/ui-state.svelte";

// ============================================================================
// SETTINGS
// ============================================================================
export function getSettings() {
  const initialized = areServicesInitialized();
  // Debug logging removed - this function is called hundreds of times during reactive updates
  // console.log("🔍 getSettings called, servicesInitialized:", initialized);

  if (!initialized) {
    // console.log("🔍 Returning default settings (services not initialized yet)");
    // Return default settings if not initialized
    return {
      gridMode: GridMode.DIAMOND,
      backgroundType: BackgroundType.NIGHT_SKY,
      backgroundQuality: "medium" as const,
      backgroundEnabled: true,
    };
  }
  // Return the reactive settings object directly (NOT a snapshot)
  // This ensures components using $derived(getSettings()) will re-render when settings change
  const settings = getSettingsServiceSync().settings;
  // console.log("🔍 Returning reactive settings, backgroundType:", settings.backgroundType);
  return settings;
}

// ============================================================================
// PERFORMANCE
// ============================================================================

const performanceMetrics = $state({
  initializationTime: 0,
  lastRenderTime: 0,
  memoryUsage: 0,
});

export function getPerformanceMetrics() {
  return performanceMetrics;
}

// ============================================================================
// DERIVED STATE
// ============================================================================

export function getIsReady() {
  return (
    getIsInitialized() && !getIsInitializing() && !getInitializationError()
  );
}

export function getCanUseApp() {
  return getIsReady() && !getShowSettings();
}

// ============================================================================
export async function updateSettings(
  newSettings: Partial<AppSettings>
): Promise<void> {
  console.log(
    "📝 app-state.updateSettings called with:",
    JSON.stringify(newSettings, null, 2)
  );

  if (!areServicesInitialized()) {
    console.warn("Settings service not initialized, cannot update settings");
    return;
  }

  // Update each setting individually using the interface method
  console.log("📝 Calling getSettingsServiceSync().updateSettings...");
  getSettingsServiceSync().updateSettings(newSettings);
  console.log("📝 updateSettings completed");
}

// Performance tracking
export function updateInitializationTime(time: number): void {
  performanceMetrics.initializationTime = time;
}

export function updateLastRenderTime(time: number): void {
  performanceMetrics.lastRenderTime = time;
}

export function updateMemoryUsage(): void {
  if (typeof performance !== "undefined" && "memory" in performance) {
    const memory = (performance as { memory: { usedJSHeapSize: number } })
      .memory;
    performanceMetrics.memoryUsage = Math.round(
      memory.usedJSHeapSize / 1048576
    );
  }
}

// ============================================================================
// APPLICATION LIFECYCLE
// ============================================================================

export async function restoreApplicationState(): Promise<void> {
  try {
    // Initialize tab persistence and restore saved tab
    await initializeTabPersistenceInternal();
  } catch (error) {
    console.warn("?? Failed to restore application state:", error);
    // Don't throw - app should work even if persistence fails
  }
}

// ============================================================================
// UTILITIES & DEBUG
// ============================================================================

// Performance snapshot for debugging
export function createPerformanceSnapshot(): PerformanceSnapshot {
  return {
    timestamp: Date.now(),
    metrics: performanceMetrics,
    appState: {
      isFullScreen: getIsFullScreen(),
      isTransitioning: getIsTransitioning(),
      showSettings: getShowSettings(),
    },
    memoryUsage: performanceMetrics.memoryUsage,
  };
}

export function resetMetrics(): void {
  performanceMetrics.initializationTime = 0;
  performanceMetrics.lastRenderTime = 0;
  performanceMetrics.memoryUsage = 0;
}

export function clearStoredSettings(): void {
  if (!areServicesInitialized()) {
    console.warn("Settings service not initialized, cannot clear settings");
    return;
  }
  getSettingsServiceSync().clearStoredSettings();
}

export function debugSettings(): void {
  if (!areServicesInitialized()) {
    console.warn("Settings service not initialized, cannot debug settings");
    return;
  }
  getSettingsServiceSync().debugSettings();
}

// Reset all application state to defaults
export function resetAppState(): void {
  // Reset UI state
  resetUIState();

  // Reset initialization state
  resetInitializationState();

  // Reset performance metrics
  resetMetrics();

  // Reset settings
  // TODO: Implement resetToDefaults in ISettingsService interface
  console.warn("resetToDefaults not implemented in ISettingsService");
}

// ============================================================================
// DEVELOPMENT HELPERS
// ============================================================================

declare global {
  interface Window {
    debugSettings?: typeof debugSettings;
    resetAppState?: typeof resetAppState;
    clearStoredSettings?: typeof clearStoredSettings;
  }
}

if (typeof window !== "undefined") {
  window.debugSettings = debugSettings;
  window.resetAppState = resetAppState;
  window.clearStoredSettings = clearStoredSettings;
}
