/**
 * Fade Animation System - Main Export
 *
 * Complete fade management system ported from TKA desktop app
 * Provides smooth transitions for tab switching and UI animations
 */

// Core Types
export type {
	FadeConfig,
	TransitionConfig,
	CrossfadeConfig,
	FadeTarget,
	FadeOperation,
	TabTransitionState,
	FadeOrchestratorState,
	FadeEvent,
	FadeEventType,
	MainTabId,
	ConstructSubTabId,
	TabFadeConfig,
} from './fadeTypes';

// Orchestrator
export {
	FadeOrchestrator,
	getFadeOrchestrator,
	initializeFadeOrchestrator,
	resetFadeOrchestrator,
} from './fadeOrchestrator';

// Custom Transitions
export {
	enhancedFade,
	createTabCrossfade,
	slideFade,
	scaleFade,
	fluidTransition,
	tabSend,
	tabReceive,
	quickFade,
	slowFade,
	slideLeft,
	slideRight,
	slideUp,
	slideDown,
} from './transitions';

// State Management (Svelte 5 Runes)
export {
	getFadeState,
	isFadeEnabled,
	isMainTabTransitioning,
	isSubTabTransitioning,
	isAnyTabTransitioning,
	getMainTabTransition,
	getSubTabTransition,
	getFadeSettings,
	initializeFadeSystem,
	transitionToMainTab,
	completeMainTabTransition,
	transitionToSubTab,
	completeSubTabTransition,
	fadeAndUpdate,
	updateFadeSettings,
	setFadeEnabled,
	getTabTransitionKey,
	getFadeConfigForTransition,
	isSpecificTransitionRunning,
	getFadeDebugInfo,
	resetFadeSystem,
} from './fadeState.svelte';

// Utility functions for common fade patterns
export const fadeUtils = {
	/**
	 * Create a simple fade in/out pair
	 */
	createFadePair: (duration = 300) => {
		return {
			in: (node: Element) =>
				enhancedFade(node, {
					duration,
					direction: 'in',
					opacity: { start: 0, end: 1 },
				}),
			out: (node: Element) =>
				enhancedFade(node, {
					duration,
					direction: 'out',
					opacity: { start: 1, end: 0 },
				}),
		};
	},

	/**
	 * Create a slide fade pair
	 */
	createSlideFadePair: (
		direction: 'left' | 'right' | 'up' | 'down' = 'right',
		duration = 300
	) => {
		return {
			in: (node: Element) =>
				slideFade(node, {
					duration,
					direction,
					opacity: { start: 0, end: 1 },
				}),
			out: (node: Element) =>
				slideFade(node, {
					duration,
					direction,
					opacity: { start: 1, end: 0 },
				}),
		};
	},

	/**
	 * Create a crossfade pair for specific keys
	 */
	createKeyedCrossfade: (duration = 300) => {
		const [send, receive] = createTabCrossfade({ duration });
		return { send, receive };
	},
};

// Import the transition functions for direct use
import { enhancedFade, slideFade, scaleFade, fluidTransition } from './transitions';
