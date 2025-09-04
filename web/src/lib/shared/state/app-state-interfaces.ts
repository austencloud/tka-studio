/**
 * State Service Interfaces
 *
 * All interfaces for the refactored state management services.
 * Consolidated into a single file for simplicity since they're small.
 */

import type { IBrowseStatePersister } from "../../modules/browse/services";
import type { AppSettings } from "../domain/models/application/AppSettings";
import type { TabId, Theme, UIPerformanceMetrics } from "../domain/ui/UITypes";

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
export interface IMainTabState {
  // State getters
  readonly activeTab: TabId;
  readonly browseStatePersistence: IBrowseStatePersister;

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
export interface IAppStateInitializer {
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
export interface IPerformanceMetricsState {
  // State getters
  readonly performanceMetrics: UIPerformanceMetrics;

  // Actions
  updateInitializationTime(time: number): void;
  updateLastRenderTime(time: number): void;
  updateMemoryUsage(): void;
  resetMetrics(): void;
}
