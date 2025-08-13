/**
 * Simple Application State - Clean and Predictable
 * Replaces the over-engineered appState.svelte.ts
 */

import type { AppSettings } from "$services/interfaces";

// ============================================================================
// SIMPLE STATE - No over-engineering!
// ============================================================================

type TabId = "construct" | "browse" | "sequence_card" | "write" | "learn";

const appState = $state({
  // Core UI state
  activeTab: "construct" as TabId,
  showSettings: false,
  theme: "dark" as "light" | "dark",

  // Simple transition state (just a flag, no complex orchestration)
  isTransitioning: false,

  // App initialization
  isInitialized: false,
  isInitializing: false,
  initializationError: null as string | null,

  // Settings
  settings: {
    theme: "dark",
    backgroundEnabled: true,
    backgroundType: "aurora",
    backgroundQuality: "medium",
    animationsEnabled: true,
    gridMode: "diamond",
    showBeatNumbers: true,
    autoSave: true,
    exportQuality: "high",
    workbenchColumns: 5,
    // Add any other fields from the interface as needed
    visibility: {
      TKA: true,
      Reversals: true,
      Positions: true,
      Elemental: true,
      VTG: true,
      nonRadialPoints: true,
    },
  } as AppSettings,
});

// ============================================================================
// SIMPLE GETTERS
// ============================================================================

export function getActiveTab() {
  return appState.activeTab;
}
export function getShowSettings() {
  return appState.showSettings;
}
export function getTheme() {
  return appState.theme;
}
export function getSettings() {
  return appState.settings;
}
export function getIsInitialized() {
  return appState.isInitialized;
}
export function getIsInitializing() {
  return appState.isInitializing;
}
export function getInitializationError() {
  return appState.initializationError;
}
export function getIsTransitioning() {
  return appState.isTransitioning;
}

// Derived state
export function getIsReady() {
  return (
    appState.isInitialized &&
    !appState.isInitializing &&
    !appState.initializationError
  );
}

export function getCanUseApp() {
  return getIsReady() && !appState.showSettings;
}

// ============================================================================
// SIMPLE ACTIONS
// ============================================================================

/**
 * Switch tabs - simple and reliable
 */
export async function switchTab(tab: TabId): Promise<void> {
  if (appState.activeTab === tab) return;

  // Simple transition handling
  appState.isTransitioning = true;
  appState.activeTab = tab;

  // Brief delay to allow transition to complete
  setTimeout(() => {
    appState.isTransitioning = false;
  }, 300);
}

/**
 * Check if tab is active
 */
export function isTabActive(tab: string): boolean {
  return appState.activeTab === tab;
}

/**
 * Settings management
 */
export function showSettingsDialog(): void {
  appState.showSettings = true;
}

export function hideSettingsDialog(): void {
  appState.showSettings = false;
}

export function toggleSettingsDialog(): void {
  appState.showSettings = !appState.showSettings;
}

export function updateSettings(newSettings: Partial<AppSettings>): void {
  Object.assign(appState.settings, newSettings);

  if (newSettings.theme) {
    appState.theme = newSettings.theme;
  }
}

export function setTheme(theme: "light" | "dark"): void {
  appState.theme = theme;
  appState.settings.theme = theme;
}

/**
 * Initialization
 */
export function setInitializationState(
  initialized: boolean,
  initializing: boolean,
  error: string | null = null,
): void {
  appState.isInitialized = initialized;
  appState.isInitializing = initializing;
  appState.initializationError = error;
}

/**
 * Get complete state snapshot
 */
export function getAppStateSnapshot() {
  return {
    activeTab: appState.activeTab,
    showSettings: appState.showSettings,
    theme: appState.theme,
    isTransitioning: appState.isTransitioning,
    isInitialized: appState.isInitialized,
    isInitializing: appState.isInitializing,
    initializationError: appState.initializationError,
    settings: { ...appState.settings },
  };
}

/**
 * Reset state
 */
export function resetAppState(): void {
  appState.activeTab = "construct";
  appState.showSettings = false;
  appState.theme = "dark";
  appState.isTransitioning = false;
  appState.isInitialized = false;
  appState.isInitializing = false;
  appState.initializationError = null;
}
