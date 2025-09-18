/**
 * Refactored Application State - Clean Architecture
 *
 * Orchestrates focused state services following Single Responsibility Principle.
 * Each service handles one specific concern, making the code maintainable and testable.
 *
 * This replaces the 460-line monolith with a clean, focused architecture.
 */

import { browser } from "$app/environment";
import type {
    AppSettings,
    IPersistenceService,
    ISettingsService,
    PerformanceSnapshot,
    SequenceData,
    TabId,
} from "$shared";
import type { IGalleryThumbnailService } from "../../../modules/gallery/display";
import { BackgroundType } from "../../background";
import {
    ensureContainerInitialized,
    resolve,
    resolveAsync,
} from "../../inversify";
import { TYPES } from "../../inversify/types";
import { GridMode } from "../../pictograph";
import { AppTheme } from "./app-state-enums";

// Lazy service resolution - only resolve when needed
let settingsService: ISettingsService | null = null;
let isInitialized = false;

async function getSettingsService(): Promise<ISettingsService> {
  if (!settingsService) {
    settingsService = (await resolveAsync(
      TYPES.ISettingsService
    )) as ISettingsService;
  }
  return settingsService;
}

// Synchronous getter that throws if not initialized
function getSettingsServiceSync(): ISettingsService {
  if (!settingsService) {
    throw new Error(
      "Settings service not initialized. Call initializeAppState first."
    );
  }
  return settingsService;
}

// Initialize the app state
export async function initializeAppState(): Promise<void> {
  if (isInitialized) return;

  try {
    await ensureContainerInitialized();
    settingsService = (await resolveAsync(
      TYPES.ISettingsService
    )) as ISettingsService;
    isInitialized = true;
  } catch (error) {
    console.error("❌ App State: Failed to initialize:", error);
    throw error;
  }
}

let persistenceService: IPersistenceService | null = null;
function getPersistenceService(): IPersistenceService {
  if (!persistenceService) {
    persistenceService = resolve(
      TYPES.IPersistenceService
    ) as IPersistenceService;
  }
  return persistenceService;
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

// Function to get initial tab from localStorage cache (synchronous)
function getInitialTabFromCache(): TabId {
  // Check if we're in a browser environment where localStorage is available
  if (!browser) {
    return "construct";
  }

  try {
    // Try to get saved tab from localStorage cache (synchronous)
    const savedTabData = localStorage.getItem("tka-active-tab-cache");
    if (savedTabData) {
      const parsed = JSON.parse(savedTabData);
      if (parsed && typeof parsed.tabId === "string") {
        return parsed.tabId as TabId;
      }
    }
  } catch (error) {
    console.warn("⚠️ Failed to pre-load saved tab from cache:", error);
  }

  return "construct";
}

// UI state - using Svelte 5 runes for proper reactivity
// Initialize with null to prevent visual jumps during restoration
const uiState = $state({
  activeTab: null as TabId | null, // Start with null, will be set after restoration
  showSettings: false,
  isFullScreen: false,
  isTransitioning: false,
  isWaitingForTabLoad: false,
  // Spotlight state
  showSpotlight: false,
  spotlightSequence: null as SequenceData | null,
  spotlightThumbnailService: null as IGalleryThumbnailService | null,
});

export function getActiveTab(): TabId | null {
  return uiState.activeTab;
}

export function getActiveTabOrDefault(): TabId {
  return uiState.activeTab || "construct";
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
  if (!isInitialized || !settingsService) {
    // Return default settings if not initialized
    return {
      gridMode: GridMode.DIAMOND,
      backgroundType: BackgroundType.NIGHT_SKY,
      backgroundQuality: "medium" as const,
      backgroundEnabled: true,
    };
  }
  return getSettingsServiceSync().settings;
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

// Tab management with persistence
export async function switchTab(tab: TabId): Promise<void> {
  if (uiState.activeTab === tab) {
    return;
  }

  // Handle transition UI
  uiState.isTransitioning = true;

  // Update active tab immediately
  uiState.activeTab = tab;

  // Save tab to persistence (async, don't block UI)
  try {
    const persistence = getPersistenceService();
    await persistence.saveActiveTab(tab);

    // Also save to localStorage cache for immediate access on next load
    if (browser) {
      localStorage.setItem(
        "tka-active-tab-cache",
        JSON.stringify({ tabId: tab })
      );
    }
  } catch (error) {
    console.warn("⚠️ switchTab: Failed to save tab to persistence:", error);
    // Don't throw - tab switching should work even if persistence fails
  }

  // Brief delay to allow transition to complete
  setTimeout(() => {
    uiState.isTransitioning = false;
  }, 300);
}

export function isTabActive(tab: string): boolean {
  return uiState.activeTab === tab;
}

// Initialize persistence and restore saved tab
export async function initializeTabPersistence(): Promise<void> {
  try {
    const persistence = getPersistenceService();

    // Initialize the persistence service
    await persistence.initialize();

    // Restore from database (no cache complexity)
    const savedTab = await persistence.getActiveTab();
    if (savedTab) {
      uiState.activeTab = savedTab;

      // Update localStorage cache to match database
      if (browser) {
        localStorage.setItem(
          "tka-active-tab-cache",
          JSON.stringify({ tabId: savedTab })
        );
      }
    } else {
      // Set default tab and save it
      const defaultTab: TabId = "construct";
      uiState.activeTab = defaultTab;
      await persistence.saveActiveTab(defaultTab);
      if (browser) {
        localStorage.setItem(
          "tka-active-tab-cache",
          JSON.stringify({ tabId: defaultTab })
        );
      }
    }
  } catch (error) {
    console.warn("⚠️ Failed to initialize tab persistence:", error);
    // Don't throw - app should work even if persistence fails
  }
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
export function showSpotlight(
  sequence: SequenceData,
  thumbnailService: IGalleryThumbnailService
): void {
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
  if (!isInitialized || !settingsService) {
    console.warn("Settings service not initialized, cannot update settings");
    return;
  }

  // Update each setting individually using the interface method
  getSettingsServiceSync().updateSettings(newSettings);
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
  try {
    // Initialize tab persistence and restore saved tab
    await initializeTabPersistence();
  } catch (error) {
    console.warn("⚠️ Failed to restore application state:", error);
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
  if (!isInitialized || !settingsService) {
    console.warn("Settings service not initialized, cannot clear settings");
    return;
  }
  getSettingsServiceSync().clearStoredSettings();
}

export function debugSettings(): void {
  if (!isInitialized || !settingsService) {
    console.warn("Settings service not initialized, cannot debug settings");
    return;
  }
  getSettingsServiceSync().debugSettings();
}

// Reset all application state to defaults
export function resetAppState(): void {
  // Reset UI state
  uiState.activeTab = "construct";
  uiState.showSettings = false;
  uiState.theme = AppTheme.DARK;
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
