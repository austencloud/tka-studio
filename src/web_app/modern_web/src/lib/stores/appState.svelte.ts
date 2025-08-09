/**
 * Application State - Pure Svelte 5 Runes
 *
 * Global application state using only runes - no stores anywhere!
 * Now includes fade system integration for smooth transitions
 */

import type { AppSettings } from '$services/interfaces';
import { 
	initializeFadeSystem, 
	transitionToMainTab, 
	completeMainTabTransition,
	isFadeEnabled,
	isMainTabTransitioning,
	getMainTabTransition,
	type MainTabId
} from '$services/ui/animation';

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

// UPDATED: Tab types to match desktop app exactly - including sequence_card tab
type TabId = 'construct' | 'browse' | 'sequence_card' | 'write' | 'learn';

const uiState = $state({
	activeTab: 'construct' as TabId,
	isFullScreen: false,
	showSettings: false,
	theme: 'dark' as 'light' | 'dark'
});

export function getActiveTab() { return uiState.activeTab; }
export function getIsFullScreen() { return uiState.isFullScreen; }
export function getShowSettings() { return uiState.showSettings; }
export function getTheme() { return uiState.theme; }

// Fade transition state getters
export function getIsMainTabTransitioning() {
	try {
		return isMainTabTransitioning();
	} catch {
		return false;
	}
}

export function getMainTabTransitionState() {
	try {
		return getMainTabTransition();
	} catch {
		return { isTransitioning: false, fromTab: null, toTab: null, transitionId: null };
	}
}

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
	exportQuality: 'high',
	workbenchColumns: 5,
	// Background settings
	backgroundType: 'aurora',
	backgroundQuality: 'medium',
	backgroundEnabled: true
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
 * Set initialization state and initialize fade system when app is ready
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
	
	// Initialize fade system when app is fully initialized
	if (initialized && !initializing && !error) {
		try {
			initializeFadeSystem({
				duration: 300, // Default duration for transitions
				delay: 0
			});
			console.log('🎭 Fade system initialized with app state');
		} catch (fadeError) {
			console.warn('Failed to initialize fade system:', fadeError);
		}
	}
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
 * Switch to a different tab with fade transition - UPDATED to include sequence_card tab
 */
export async function switchTab(tab: TabId): Promise<void> {
	const currentTab = uiState.activeTab;
	
	// Don't transition if already on the same tab
	if (currentTab === tab) {
		return;
	}
	
	// Check if fade system is available and enabled
	if (initState.isInitialized && isFadeEnabled()) {
		try {
			// Start the fade transition
			const transitionId = await transitionToMainTab(currentTab as MainTabId, tab as MainTabId);
			
			if (transitionId) {
				// Update the active tab immediately for reactive state
				uiState.activeTab = tab;
				
				// Complete the transition after a brief delay to allow UI to update
				setTimeout(() => {
					completeMainTabTransition(transitionId);
				}, 50);
				
				console.log(`🎭 Tab transition started: ${currentTab} → ${tab}`);
			} else {
				// Fallback to immediate switch
				uiState.activeTab = tab;
			}
		} catch (error) {
			console.warn('Failed to start tab transition, falling back to immediate switch:', error);
			uiState.activeTab = tab;
		}
	} else {
		// Immediate switch if fade system not available or disabled
		uiState.activeTab = tab;
	}
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
