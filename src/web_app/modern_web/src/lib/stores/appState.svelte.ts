/**
 * Application State - Pure Svelte 5 Runes
 * 
 * Global application state using only runes - no stores anywhere!
 */

import type { AppSettings } from '$services/interfaces';

// ============================================================================
// INITIALIZATION STATE
// ============================================================================

// Create state object to avoid export issues
const initState = $state({
	isInitialized: false,
	isInitializing: false,
	initializationError: null as string | null,
	initializationProgress: 0
});

// Export getter functions for the state
export function getIsInitialized() { return initState.isInitialized; }
export function getIsInitializing() { return initState.isInitializing; }
export function getInitializationError() { return initState.initializationError; }
export function getInitializationProgress() { return initState.initializationProgress; }

// ============================================================================
// UI STATE
// ============================================================================

const uiState = $state({
	activeTab: 'construct' as 'construct' | 'generate' | 'browse' | 'learn',
	isFullScreen: false,
	showSettings: false,
	theme: 'dark' as 'light' | 'dark'
});

export function getActiveTab() { return uiState.activeTab; }
export function getIsFullScreen() { return uiState.isFullScreen; }
export function getShowSettings() { return uiState.showSettings; }
export function getTheme() { return uiState.theme; }

// ============================================================================
// PERFORMANCE STATE
// ============================================================================

const perfState = $state({
	initializationTime: 0,
	lastRenderTime: 0,
	memoryUsage: 0
});

export function getPerformanceMetrics() { return perfState; }

// ============================================================================
// SETTINGS STATE
// ============================================================================

const settingsState = $state<AppSettings>({
	theme: 'dark',
	gridMode: 'diamond',
	showBeatNumbers: true,
	autoSave: true,
	exportQuality: 'high'
});

export function getSettings() { return settingsState; }

// ============================================================================
// DERIVED STATE
// ============================================================================

export function getIsReady(): boolean {
	return initState.isInitialized && !initState.isInitializing && !initState.initializationError;
}

export function getCanUseApp(): boolean {
	return getIsReady() && !uiState.showSettings;
}

export function getInitializationComplete(): boolean {
	return initState.initializationProgress >= 100;
}

// ============================================================================
// ACTIONS
// ============================================================================

/**
 * Set initialization state
 */
export function setInitializationState(
	initialized: boolean,
	initializing: boolean,
	error: string | null = null,
	progress: number = 0
): void {
	initState.isInitialized = initialized;
	initState.isInitializing = initializing;
	initState.initializationError = error;
	initState.initializationProgress = progress;
}

/**
 * Set initialization progress
 */
export function setInitializationProgress(progress: number): void {
	initState.initializationProgress = Math.max(0, Math.min(100, progress));
}

/**
 * Set initialization error
 */
export function setInitializationError(error: string | null): void {
	initState.initializationError = error;
	if (error) {
		initState.isInitializing = false;
	}
}

/**
 * Clear initialization error
 */
export function clearInitializationError(): void {
	initState.initializationError = null;
}

/**
 * Switch to a different tab
 */
export function switchTab(tab: 'construct' | 'generate' | 'browse' | 'learn'): void {
	uiState.activeTab = tab;
}

/**
 * Check if tab is active
 */
export function isTabActive(tab: string): boolean {
	return uiState.activeTab === tab;
}

/**
 * Toggle fullscreen
 */
export function toggleFullScreen(): void {
	uiState.isFullScreen = !uiState.isFullScreen;
}

/**
 * Set fullscreen state
 */
export function setFullScreen(fullscreen: boolean): void {
	uiState.isFullScreen = fullscreen;
}

/**
 * Show settings dialog
 */
export function showSettingsDialog(): void {
	uiState.showSettings = true;
}

/**
 * Hide settings dialog
 */
export function hideSettingsDialog(): void {
	uiState.showSettings = false;
}

/**
 * Toggle settings dialog
 */
export function toggleSettingsDialog(): void {
	uiState.showSettings = !uiState.showSettings;
}

/**
 * Set theme
 */
export function setTheme(newTheme: 'light' | 'dark'): void {
	uiState.theme = newTheme;
	settingsState.theme = newTheme;
}

/**
 * Update settings
 */
export function updateSettings(newSettings: Partial<AppSettings>): void {
	Object.assign(settingsState, newSettings);

	// Apply theme if changed
	if (newSettings.theme) {
		uiState.theme = newSettings.theme;
	}
}

/**
 * Set performance metrics
 */
export function setPerformanceMetrics(metrics: Partial<typeof perfState>): void {
	Object.assign(perfState, metrics);
}

/**
 * Track render time
 */
export function trackRenderTime(componentName: string, renderTime: number): void {
	perfState.lastRenderTime = renderTime;

	if (renderTime > 100) {
		console.warn(`Slow render detected for ${componentName}: ${renderTime}ms`);
	}
}

/**
 * Update memory usage
 */
export function updateMemoryUsage(): void {
	if (typeof performance !== 'undefined' && 'memory' in performance) {
		const memory = (performance as any).memory;
		perfState.memoryUsage = Math.round(memory.usedJSHeapSize / 1048576);
	}
}

// ============================================================================
// UTILITIES
// ============================================================================

/**
 * Get complete application state snapshot
 */
export function getAppStateSnapshot() {
	return {
		isInitialized: initState.isInitialized,
		isInitializing: initState.isInitializing,
		initializationError: initState.initializationError,
		initializationProgress: initState.initializationProgress,
		activeTab: uiState.activeTab,
		isFullScreen: uiState.isFullScreen,
		showSettings: uiState.showSettings,
		theme: uiState.theme,
		performanceMetrics: { ...perfState },
		settings: { ...settingsState }
	};
}

/**
 * Reset application state
 */
export function resetAppState(): void {
	initState.isInitialized = false;
	initState.isInitializing = false;
	initState.initializationError = null;
	initState.initializationProgress = 0;
	uiState.activeTab = 'construct';
	uiState.isFullScreen = false;
	uiState.showSettings = false;
	uiState.theme = 'dark';
	Object.assign(perfState, {
		initializationTime: 0,
		lastRenderTime: 0,
		memoryUsage: 0
	});
}
