/**
 * Reimport type { AppSettings, PerformanceSnapshot } from "../domain/models/application";actored Application State - Clean Architecture
 *
 * Orchestrates focused state services following Single Responsibility Principle.
 * Each service handles one specific concern, making the code maintainable and testable.
 *
 * This replaces the 460-line monolith with a clean, focused architecture.
 */

import type {
    AppSettings,
    ISettingsService,
    PerformanceSnapshot,
    TabId,
    Theme,
} from "$shared";
import { resolve } from "../../inversify";
import { TYPES } from "../../inversify/types";
// Import services from DI container instead of singletons
// import { settingsService } from "./SettingsState.svelte"; // File doesn't exist

// Lazy settings service resolution - only resolve when needed
let settingsService: ISettingsService | null = null;
function getSettingsService(): ISettingsService {
  if (!settingsService) {
    settingsService = resolve(TYPES.ISettingsService) as ISettingsService;
  }
  return settingsService;
}

// Simple reactive store pattern for .svelte.ts files
class ReactiveStore<T> {
  private _value: T;
  private _subscribers = new Set<() => void>();

  constructor(initialValue: T) {
    this._value = initialValue;
  }

  get value(): T {
    return this._value;
  }

  set value(newValue: T) {
    this._value = newValue;
    this._subscribers.forEach((callback) => callback());
  }

  subscribe(callback: () => void): () => void {
    this._subscribers.add(callback);
    return () => this._subscribers.delete(callback);
  }
}

// Import types for proper service resolution

// ============================================================================
// CLEAN API - Delegates to focused services
// ============================================================================

// ============================================================================
// INITIALIZATION STATE
// ============================================================================

// Initialization state - using ReactiveStore for reactivity
const initializationState = new ReactiveStore({
  isInitialized: true,
  isInitializing: false,
  initializationError: null as string | null,
  initializationProgress: 100,
});

export function getIsInitialized() {
  return initializationState.value.isInitialized;
}

export function getIsInitializing() {
  return initializationState.value.isInitializing;
}

export function getInitializationError() {
  return initializationState.value.initializationError;
}

export function getInitializationProgress() {
  return initializationState.value.initializationProgress;
}

export function setInitializationState(
  initialized: boolean,
  initializing: boolean,
  error: string | null = null,
  progress: number = 0
): void {
  initializationState.value = {
    ...initializationState.value,
    isInitialized: initialized,
    isInitializing: initializing,
    initializationError: error,
    initializationProgress: progress,
  };
}

export function setInitializationError(error: string): void {
  initializationState.value = {
    ...initializationState.value,
    initializationError: error,
  };
}

export function setInitializationProgress(progress: number): void {
  initializationState.value = {
    ...initializationState.value,
    initializationProgress: progress,
  };
}

export function getInitializationComplete() {
  return (
    initializationState.value.isInitialized &&
    !initializationState.value.isInitializing
  );
}

// ============================================================================
// UI STATE
// ============================================================================

// UI state - using Svelte 5 runes for proper reactivity
const uiState = $state({
  activeTab: "construct" as TabId,
  showSettings: false,
  theme: "dark" as Theme,
  isFullScreen: false,
  isTransitioning: false,
  // Spotlight state
  showSpotlight: false,
  spotlightSequence: null as any,
  spotlightThumbnailService: null as any,
});

export function getActiveTab() {
  return uiState.activeTab;
}

export function getShowSettings() {
  return uiState.showSettings;
}

export function getTheme() {
  return uiState.theme;
}

export function getIsFullScreen() {
  return uiState.isFullScreen;
}

export function getIsTransitioning() {
  return uiState.isTransitioning;
}

export function getShowSpotlight() {
  return uiState.showSpotlight;
}

export function getSpotlightSequence() {
  return uiState.spotlightSequence;
}

export function getSpotlightThumbnailService() {
  return uiState.spotlightThumbnailService;
}

// ============================================================================
// SETTINGS
// ============================================================================

export function getSettings() {
  return getSettingsService().settings;
}

// ============================================================================
// PERFORMANCE
// ============================================================================

// Performance metrics state - using ReactiveStore for reactivity
const performanceMetrics = new ReactiveStore({
  initializationTime: 0,
  lastRenderTime: 0,
  memoryUsage: 0,
});

export function getPerformanceMetrics() {
  return performanceMetrics.value;
}

// ============================================================================
// DERIVED STATE
// ============================================================================

export function getIsReady() {
  return (
    initializationState.value.isInitialized &&
    !initializationState.value.isInitializing &&
    !initializationState.value.initializationError
  );
}

export function getCanUseApp() {
  return getIsReady() && !uiState.showSettings;
}

// ============================================================================
// ACTIONS
// ============================================================================

// Tab management
export async function switchTab(tab: TabId): Promise<void> {
  console.log("🔄 switchTab called with:", tab, "current:", uiState.activeTab);
  if (uiState.activeTab === tab) {
    console.log("🔄 switchTab: Already on tab", tab, "- skipping");
    return;
  }

  // Handle transition UI
  uiState.isTransitioning = true;
  console.log("🔄 switchTab: Set transitioning to true");

  // Update active tab
  uiState.activeTab = tab;
  console.log(
    "🔄 switchTab: Updated activeTab to",
    tab,
    "new state:",
    uiState.activeTab
  );

  // Brief delay to allow transition to complete
  setTimeout(() => {
    uiState.isTransitioning = false;
    console.log("🔄 switchTab: Set transitioning to false");
  }, 300);
}

export function isTabActive(tab: string): boolean {
  return uiState.activeTab === tab;
}

export function setFullScreen(fullScreen: boolean): void {
  uiState.isFullScreen = fullScreen;
}

// Settings management
export function showSettingsDialog(): void {
  uiState.showSettings = true;
}

export function hideSettingsDialog(): void {
  uiState.showSettings = false;
}

export function toggleSettingsDialog(): void {
  uiState.showSettings = !uiState.showSettings;
}

// Spotlight management
export function showSpotlight(sequence: any, thumbnailService: any): void {
  uiState.spotlightSequence = sequence;
  uiState.spotlightThumbnailService = thumbnailService;
  uiState.showSpotlight = true;
}

export function hideSpotlight(): void {
  uiState.showSpotlight = false;
  uiState.spotlightSequence = null;
  uiState.spotlightThumbnailService = null;
}

export async function updateSettings(
  newSettings: Partial<AppSettings>
): Promise<void> {
  // Update each setting individually using the interface method
  getSettingsService().updateSettings(newSettings);

  // Update theme in UI state if theme changed
  if (newSettings.theme) {
    uiState.theme = newSettings.theme;
  }
}

export async function setTheme(theme: Theme): Promise<void> {
  uiState.theme = theme;
  getSettingsService().updateSettings({ theme });
}

// Performance tracking
export function updateInitializationTime(time: number): void {
  performanceMetrics.value = {
    ...performanceMetrics.value,
    initializationTime: time,
  };
}

export function updateLastRenderTime(time: number): void {
  performanceMetrics.value = {
    ...performanceMetrics.value,
    lastRenderTime: time,
  };
}

export function updateMemoryUsage(): void {
  if (typeof performance !== "undefined" && "memory" in performance) {
    const memory = (performance as { memory: { usedJSHeapSize: number } })
      .memory;
    performanceMetrics.value = {
      ...performanceMetrics.value,
      memoryUsage: Math.round(memory.usedJSHeapSize / 1048576),
    };
  }
}

// ============================================================================
// APPLICATION LIFECYCLE
// ============================================================================

export async function restoreApplicationState(): Promise<void> {
  // Restore application state from localStorage or other persistence
  // For now, this is a no-op since we're using local state
  console.log("Restoring application state...");
}

// ============================================================================
// UTILITIES & DEBUG
// ============================================================================

// Performance snapshot for debugging
export function createPerformanceSnapshot(): PerformanceSnapshot {
  return {
    timestamp: Date.now(),
    metrics: performanceMetrics.value,
    appState: {
      isFullScreen: uiState.isFullScreen,
      isTransitioning: uiState.isTransitioning,
      showSettings: uiState.showSettings,
      theme: uiState.theme,
    },
    memoryUsage: performanceMetrics.value.memoryUsage,
  };
}

export function resetMetrics(): void {
  performanceMetrics.value = {
    initializationTime: 0,
    lastRenderTime: 0,
    memoryUsage: 0,
  };
}

export function clearStoredSettings(): void {
  getSettingsService().clearStoredSettings();
}

export function debugSettings(): void {
  getSettingsService().debugSettings();
}

// Reset all application state to defaults
export function resetAppState(): void {
  // Reset UI state
  uiState.activeTab = "construct";
  uiState.showSettings = false;
  uiState.theme = "dark";
  uiState.isFullScreen = false;
  uiState.isTransitioning = false;

  // Reset initialization state
  initializationState.value = {
    isInitialized: true,
    isInitializing: false,
    initializationError: null,
    initializationProgress: 100,
  };

  // Reset performance metrics
  performanceMetrics.value = {
    initializationTime: 0,
    lastRenderTime: 0,
    memoryUsage: 0,
  };

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
