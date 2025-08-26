/**
 * State Service Interfaces
 *
 * All interfaces for the refactored state management services.
 * Consolidated into a single file for simplicity since they're small.
 */

import type { AppSettings } from "$services/interfaces/application-interfaces";

// ============================================================================
// SHARED TYPES
// ============================================================================

export type TabId =
  | "construct"
  | "browse"
  | "sequence_card"
  | "write"
  | "learn"
  | "about"
  | "motion-tester";

export type Theme = "light" | "dark";

export interface PerformanceMetrics {
  initializationTime: number;
  lastRenderTime: number;
  memoryUsage: number;
}

// ============================================================================
// SERVICE INTERFACES
// ============================================================================

/**
 * Core application state management (UI state, transitions, etc.)
 */
export interface IApplicationStateService {
  // State getters
  readonly isFullScreen: boolean;
  readonly isTransitioning: boolean;
  readonly showSettings: boolean;
  readonly theme: Theme;

  // Derived state
  readonly isReady: boolean;
  readonly canUseApp: boolean;

  // Actions
  setFullScreen(fullScreen: boolean): void;
  setTransitioning(isTransitioning: boolean): void;
  showSettingsDialog(): void;
  hideSettingsDialog(): void;
  toggleSettingsDialog(): void;
  setTheme(theme: Theme): void;

  // State management
  getStateSnapshot(): object;
  resetState(): void;
}

/**
 * Settings management and persistence
 */
export interface ISettingsService {
  // State getters
  readonly settings: AppSettings;

  // Actions
  updateSettings(newSettings: Partial<AppSettings>): void;
  loadSettings(): Promise<void>;
  saveSettings(): void;
  clearStoredSettings(): void;
  resetToDefaults(): void;

  // Debug
  debugSettings(): void;
}

/**
 * Tab navigation and state persistence
 */
export interface ITabStateService {
  // State getters
  readonly activeTab: TabId;

  // Actions
  switchTab(tab: TabId): Promise<void>;
  isTabActive(tab: string): boolean;

  // Persistence
  saveCurrentTabState(tab: TabId): Promise<void>;
  restoreApplicationState(): Promise<void>;
}

/**
 * Application initialization state
 */
export interface IInitializationService {
  // State getters
  readonly isInitialized: boolean;
  readonly isInitializing: boolean;
  readonly initializationError: string | null;
  readonly initializationProgress: number;

  // Derived state
  readonly initializationComplete: boolean;

  // Actions
  setInitializationState(
    initialized: boolean,
    initializing: boolean,
    error?: string | null,
    progress?: number
  ): void;
  setInitializationError(error: string): void;
  setInitializationProgress(progress: number): void;
  resetInitializationState(): void;
}

/**
 * Performance metrics tracking
 */
export interface IPerformanceMetricsService {
  // State getters
  readonly performanceMetrics: PerformanceMetrics;

  // Actions
  updateInitializationTime(time: number): void;
  updateLastRenderTime(time: number): void;
  updateMemoryUsage(): void;
  resetMetrics(): void;
}
