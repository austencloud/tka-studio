/**
 * Fade State Management - Svelte 5 Runes Implementation
 * Integrates with existing app state for seamless fade transitions
 */

import { getFadeOrchestrator, type FadeOrchestrator } from './fadeOrchestrator';
import type { MainTabId, ConstructSubTabId, TabTransitionState, FadeConfig } from './fadeTypes';

// ============================================================================
// FADE STATE
// ============================================================================

const fadeState = $state({
	orchestrator: null as FadeOrchestrator | null,
	isInitialized: false,
	mainTabTransition: {
		isTransitioning: false,
		fromTab: null as MainTabId | null,
		toTab: null as MainTabId | null,
		transitionId: null as string | null,
	},
	subTabTransition: {
		isTransitioning: false,
		fromTab: null as ConstructSubTabId | null,
		toTab: null as ConstructSubTabId | null,
		transitionId: null as string | null,
	},
	settings: {
		enabled: true,
		mainTabDuration: 350,
		subTabDuration: 250,
		globalDuration: 300,
	},
});

// ============================================================================
// GETTERS
// ============================================================================

export function getFadeState() {
	return fadeState;
}

export function isFadeEnabled(): boolean {
	return fadeState.settings.enabled;
}

export function isMainTabTransitioning(): boolean {
	return fadeState.mainTabTransition.isTransitioning;
}

export function isSubTabTransitioning(): boolean {
	return fadeState.subTabTransition.isTransitioning;
}

export function isAnyTabTransitioning(): boolean {
	return isMainTabTransitioning() || isSubTabTransitioning();
}

export function getMainTabTransition() {
	return fadeState.mainTabTransition;
}

export function getSubTabTransition() {
	return fadeState.subTabTransition;
}

export function getFadeSettings() {
	return fadeState.settings;
}

// ============================================================================
// INITIALIZATION
// ============================================================================

/**
 * Initialize the fade system
 */
export function initializeFadeSystem(config: Partial<FadeConfig> = {}): void {
	if (fadeState.isInitialized) {
		console.warn('Fade system already initialized');
		return;
	}

	// Create orchestrator
	fadeState.orchestrator = getFadeOrchestrator();

	// Apply configuration
	if (config.duration) {
		fadeState.settings.globalDuration = config.duration;
	}

	// Set up event listeners
	fadeState.orchestrator.addEventListener('transition_start', (event) => {
		const { type, fromTab, toTab } = event.details;

		if (type === 'main_tab') {
			fadeState.mainTabTransition = {
				isTransitioning: true,
				fromTab: fromTab as MainTabId,
				toTab: toTab as MainTabId,
				transitionId: event.operationId,
			};
		} else if (type === 'sub_tab') {
			fadeState.subTabTransition = {
				isTransitioning: true,
				fromTab: fromTab as ConstructSubTabId,
				toTab: toTab as ConstructSubTabId,
				transitionId: event.operationId,
			};
		}
	});

	fadeState.orchestrator.addEventListener('transition_complete', (event) => {
		const { type } = event.details;

		if (type === 'main_tab') {
			fadeState.mainTabTransition = {
				isTransitioning: false,
				fromTab: null,
				toTab: null,
				transitionId: null,
			};
		} else if (type === 'sub_tab') {
			fadeState.subTabTransition = {
				isTransitioning: false,
				fromTab: null,
				toTab: null,
				transitionId: null,
			};
		}
	});

	fadeState.isInitialized = true;
	console.log('🎭 Fade system initialized successfully');
}

// ============================================================================
// MAIN TAB TRANSITIONS
// ============================================================================

/**
 * Start a transition between main tabs
 */
export async function transitionToMainTab(
	fromTab: MainTabId,
	toTab: MainTabId
): Promise<string | null> {
	if (!fadeState.orchestrator) {
		console.warn('Fade orchestrator not initialized');
		return null;
	}

	if (fromTab === toTab) {
		console.warn(`Already on tab ${toTab}`);
		return null;
	}

	if (fadeState.mainTabTransition.isTransitioning) {
		console.warn(
			`Already transitioning from ${fadeState.mainTabTransition.fromTab} to ${fadeState.mainTabTransition.toTab}`
		);
		return fadeState.mainTabTransition.transitionId;
	}

	console.log(`🎭 Starting main tab transition: ${fromTab} → ${toTab}`);

	const transitionId = await fadeState.orchestrator.startMainTabTransition(fromTab, toTab, {
		duration: fadeState.settings.mainTabDuration,
	});

	return transitionId;
}

/**
 * Complete a main tab transition
 */
export function completeMainTabTransition(transitionId: string): void {
	if (!fadeState.orchestrator) {
		console.warn('Fade orchestrator not initialized');
		return;
	}

	fadeState.orchestrator.completeMainTabTransition(transitionId);
}

// ============================================================================
// SUB TAB TRANSITIONS
// ============================================================================

/**
 * Start a transition between construct sub-tabs
 */
export async function transitionToSubTab(
	fromTab: ConstructSubTabId,
	toTab: ConstructSubTabId
): Promise<string | null> {
	if (!fadeState.orchestrator) {
		console.warn('Fade orchestrator not initialized');
		return null;
	}

	if (fromTab === toTab) {
		console.warn(`Already on sub-tab ${toTab}`);
		return null;
	}

	if (fadeState.subTabTransition.isTransitioning) {
		console.warn(
			`Already transitioning from ${fadeState.subTabTransition.fromTab} to ${fadeState.subTabTransition.toTab}`
		);
		return fadeState.subTabTransition.transitionId;
	}

	console.log(`🎭 Starting sub-tab transition: ${fromTab} → ${toTab}`);

	const transitionId = await fadeState.orchestrator.startSubTabTransition(fromTab, toTab, {
		duration: fadeState.settings.subTabDuration,
	});

	return transitionId;
}

/**
 * Complete a sub-tab transition
 */
export function completeSubTabTransition(
	transitionId: string,
	fromTab: string,
	toTab: string
): void {
	if (!fadeState.orchestrator) {
		console.warn('Fade orchestrator not initialized');
		return;
	}

	fadeState.orchestrator.completeSubTabTransition(transitionId, fromTab, toTab);
}

// ============================================================================
// GENERAL FADE OPERATIONS
// ============================================================================

/**
 * Execute a fade-and-update operation
 */
export async function fadeAndUpdate(
	updateCallback: () => void | Promise<void>,
	config: Partial<FadeConfig> = {}
): Promise<string | null> {
	if (!fadeState.orchestrator) {
		console.warn('Fade orchestrator not initialized');
		await updateCallback();
		return null;
	}

	const operationId = await fadeState.orchestrator.fadeAndUpdate(updateCallback, {
		duration: config.duration || fadeState.settings.globalDuration,
		...config,
	});

	return operationId;
}

// ============================================================================
// SETTINGS MANAGEMENT
// ============================================================================

/**
 * Update fade settings
 */
export function updateFadeSettings(newSettings: Partial<typeof fadeState.settings>): void {
	Object.assign(fadeState.settings, newSettings);

	// Apply to orchestrator if available
	if (fadeState.orchestrator) {
		fadeState.orchestrator.setFadesEnabled(fadeState.settings.enabled);
	}
}

/**
 * Enable or disable fade animations globally
 */
export function setFadeEnabled(enabled: boolean): void {
	fadeState.settings.enabled = enabled;

	if (fadeState.orchestrator) {
		fadeState.orchestrator.setFadesEnabled(enabled);
	}
}

// ============================================================================
// UTILITIES
// ============================================================================

/**
 * Get the current transition key for a tab (useful for crossfade)
 */
export function getTabTransitionKey(tabType: 'main' | 'sub', tabId: string): string {
	const prefix = tabType === 'main' ? 'main_tab' : 'sub_tab';
	return `${prefix}_${tabId}`;
}

/**
 * Get fade configuration for a specific transition type
 */
export function getFadeConfigForTransition(type: 'main_tab' | 'sub_tab' | 'general'): FadeConfig {
	if (!fadeState.orchestrator) {
		// Return default config if orchestrator not available
		const defaults = {
			main_tab: { duration: 350, delay: 0 },
			sub_tab: { duration: 250, delay: 0 },
			general: { duration: 300, delay: 0 },
		};
		return defaults[type];
	}

	return fadeState.orchestrator.getFadeConfig(type);
}

/**
 * Check if a specific transition is currently running
 */
export function isSpecificTransitionRunning(
	type: 'main' | 'sub',
	fromTab: string,
	toTab: string
): boolean {
	if (type === 'main') {
		const transition = fadeState.mainTabTransition;
		return (
			transition.isTransitioning &&
			transition.fromTab === fromTab &&
			transition.toTab === toTab
		);
	} else {
		const transition = fadeState.subTabTransition;
		return (
			transition.isTransitioning &&
			transition.fromTab === fromTab &&
			transition.toTab === toTab
		);
	}
}

/**
 * Get debug information about the fade system
 */
export function getFadeDebugInfo() {
	return {
		isInitialized: fadeState.isInitialized,
		settings: fadeState.settings,
		mainTabTransition: fadeState.mainTabTransition,
		subTabTransition: fadeState.subTabTransition,
		orchestrator: fadeState.orchestrator?.getDebugInfo() || null,
	};
}

/**
 * Reset the fade system
 */
export function resetFadeSystem(): void {
	if (fadeState.orchestrator) {
		fadeState.orchestrator.cancelAllOperations();
	}

	fadeState.isInitialized = false;
	fadeState.orchestrator = null;
	fadeState.mainTabTransition = {
		isTransitioning: false,
		fromTab: null,
		toTab: null,
		transitionId: null,
	};
	fadeState.subTabTransition = {
		isTransitioning: false,
		fromTab: null,
		toTab: null,
		transitionId: null,
	};
}
