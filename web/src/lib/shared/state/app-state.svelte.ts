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
import { initializationService } from "./app-state-initializer.svelte";
import { applicationStateService } from "./application-state.svelte";
import { tabStateService } from "./main-tab-state.svelte";
import { performanceMetricsService } from "./PerformanceMetricsState.svelte";
import { settingsService } from "./SettingsState.svelte";

// ============================================================================
// CLEAN API - Delegates to focused services
// ============================================================================

// ============================================================================
// INITIALIZATION STATE
// ============================================================================

export function getIsInitialized() {
  return initializationService.isInitialized;
}

export function getIsInitializing() {
  return initializationService.isInitializing;
}

export function getInitializationError() {
  return initializationService.initializationError;
}

export function getInitializationProgress() {
  return initializationService.initializationProgress;
}

export function setInitializationState(
  initialized: boolean,
  initializing: boolean,
  error: string | null = null,
  progress: number = 0
): void {
  initializationService.setInitializationState(
    initialized,
    initializing,
    error,
    progress
  );
}

export function setInitializationError(error: string): void {
  initializationService.setInitializationError(error);
}

export function setInitializationProgress(progress: number): void {
  initializationService.setInitializationProgress(progress);
}

export function getInitializationComplete() {
  return initializationService.initializationComplete;
}

// ============================================================================
// UI STATE
// ============================================================================

export function getActiveTab() {
  return tabStateService.activeTab;
}

export function getShowSettings() {
  return applicationStateService.showSettings;
}

export function getTheme() {
  return applicationStateService.theme;
}

export function getIsFullScreen() {
  return applicationStateService.isFullScreen;
}

export function getIsTransitioning() {
  return applicationStateService.isTransitioning;
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

export function getPerformanceMetrics() {
  return performanceMetricsService.performanceMetrics;
}

// ============================================================================
// DERIVED STATE
// ============================================================================

export function getIsReady() {
  return (
    initializationService.isInitialized &&
    !initializationService.isInitializing &&
    !initializationService.initializationError
  );
}

export function getCanUseApp() {
  return getIsReady() && !applicationStateService.showSettings;
}

// ============================================================================
// ACTIONS
// ============================================================================

// Tab management
export async function switchTab(tab: TabId): Promise<void> {
  if (tabStateService.activeTab === tab) return;

  // Handle transition UI
  applicationStateService.setTransitioning(true);

  await tabStateService.switchTab(tab);

  // Brief delay to allow transition to complete
  setTimeout(() => {
    applicationStateService.setTransitioning(false);
  }, 300);
}

export function isTabActive(tab: string): boolean {
  return tabStateService.isTabActive(tab);
}

export function setFullScreen(fullScreen: boolean): void {
  applicationStateService.setFullScreen(fullScreen);
}

// Settings management
export function showSettingsDialog(): void {
  applicationStateService.showSettingsDialog();
}

export function hideSettingsDialog(): void {
  applicationStateService.hideSettingsDialog();
}

export function toggleSettingsDialog(): void {
  applicationStateService.toggleSettingsDialog();
}

export function updateSettings(newSettings: Partial<AppSettings>): void {
  settingsService.updateSettings(newSettings);

  // Update theme in UI state if theme changed
  if (newSettings.theme) {
    applicationStateService.setTheme(newSettings.theme);
  }
}

export function setTheme(theme: Theme): void {
  applicationStateService.setTheme(theme);
  settingsService.updateSettings({ theme });
}

// Performance tracking
export function updateInitializationTime(time: number): void {
  performanceMetricsService.updateInitializationTime(time);
}

export function updateLastRenderTime(time: number): void {
  performanceMetricsService.updateLastRenderTime(time);
}

export function updateMemoryUsage(): void {
  performanceMetricsService.updateMemoryUsage();
}

// ============================================================================
// APPLICATION LIFECYCLE
// ============================================================================

export async function restoreApplicationState(): Promise<void> {
  await tabStateService.restoreApplicationState();
}

// ============================================================================
// UTILITIES & DEBUG
// ============================================================================

// Performance snapshot for debugging
export function createPerformanceSnapshot(): PerformanceSnapshot {
  return {
    timestamp: Date.now(),
    metrics: performanceMetricsService.performanceMetrics,
    appState: applicationStateService.getStateSnapshot(),
    memoryUsage: performanceMetricsService.performanceMetrics.memoryUsage,
  };
}

export function resetMetrics(): void {
  performanceMetricsService.resetMetrics();
}

export function clearStoredSettings(): void {
  settingsService.clearStoredSettings();
}

export function debugSettings(): void {
  settingsService.debugSettings();
}

// Reset all application state to defaults
export function resetAppState(): void {
  applicationStateService.resetState();
  initializationService.resetInitializationState();
  performanceMetricsService.resetMetrics();
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
