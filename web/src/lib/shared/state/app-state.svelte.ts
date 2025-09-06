/**
 * Reimport type { AppSettings, PerformanceSnapshot } from "../domain/models/application";actored Application State - Clean Architecture
 *
 * Orchestrates focused state services following Single Responsibility Principle.
 * Each service handles one specific concern, making the code maintainable and testable.
 *
 * This replaces the 460-line monolith with a clean, focused architecture.
 */

import type { PerformanceSnapshot, TabId, Theme } from "$shared/domain";
import type { AppSettings } from "../domain/models/application/AppSettings";
// Import services from DI container instead of singletons
import { settingsService } from "./SettingsState.svelte";

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

// UI state - using ReactiveStore for reactivity
const uiState = new ReactiveStore({
  activeTab: "construct" as TabId,
  showSettings: false,
  theme: "dark" as Theme,
  isFullScreen: false,
  isTransitioning: false,
});

export function getActiveTab() {
  return uiState.value.activeTab;
}

export function getShowSettings() {
  return uiState.value.showSettings;
}

export function getTheme() {
  return uiState.value.theme;
}

export function getIsFullScreen() {
  return uiState.value.isFullScreen;
}

export function getIsTransitioning() {
  return uiState.value.isTransitioning;
}

// ============================================================================
// SETTINGS
// ============================================================================

export function getSettings() {
  return settingsService.settings;
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
  return getIsReady() && !uiState.value.showSettings;
}

// ============================================================================
// ACTIONS
// ============================================================================

// Tab management
export async function switchTab(tab: TabId): Promise<void> {
  if (uiState.value.activeTab === tab) return;

  // Handle transition UI
  uiState.value = { ...uiState.value, isTransitioning: true };

  // Update active tab
  uiState.value = { ...uiState.value, activeTab: tab };

  // Brief delay to allow transition to complete
  setTimeout(() => {
    uiState.value = { ...uiState.value, isTransitioning: false };
  }, 300);
}

export function isTabActive(tab: string): boolean {
  return uiState.value.activeTab === tab;
}

export function setFullScreen(fullScreen: boolean): void {
  uiState.value = { ...uiState.value, isFullScreen: fullScreen };
}

// Settings management
export function showSettingsDialog(): void {
  uiState.value = { ...uiState.value, showSettings: true };
}

export function hideSettingsDialog(): void {
  uiState.value = { ...uiState.value, showSettings: false };
}

export function toggleSettingsDialog(): void {
  uiState.value = {
    ...uiState.value,
    showSettings: !uiState.value.showSettings,
  };
}

export function updateSettings(newSettings: Partial<AppSettings>): void {
  settingsService.updateSettings(newSettings);

  // Update theme in UI state if theme changed
  if (newSettings.theme) {
    uiState.value = { ...uiState.value, theme: newSettings.theme };
  }
}

export function setTheme(theme: Theme): void {
  uiState.value = { ...uiState.value, theme };
  settingsService.updateSettings({ theme });
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
      isFullScreen: uiState.value.isFullScreen,
      isTransitioning: uiState.value.isTransitioning,
      showSettings: uiState.value.showSettings,
      theme: uiState.value.theme,
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
  settingsService.clearStoredSettings();
}

export function debugSettings(): void {
  settingsService.debugSettings();
}

// Reset all application state to defaults
export function resetAppState(): void {
  // Reset UI state
  uiState.value = {
    activeTab: "construct",
    showSettings: false,
    theme: "dark",
    isFullScreen: false,
    isTransitioning: false,
  };

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
  settingsService.resetToDefaults();
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
