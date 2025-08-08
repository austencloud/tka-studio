// src/lib/components/Backgrounds/contexts/BackgroundContext.ts
/**
 * DEPRECATED: Background Context Module
 *
 * This file is deprecated as we've moved to 100% Svelte 5 runes.
 * NO STORES - RUNES ONLY!
 *
 * Use BackgroundContext.svelte.ts for the modern runes-based implementation.
 */

import { getRunesBackgroundContext } from './BackgroundContext.svelte';
import type {
	BackgroundType,
	Dimensions,
	PerformanceMetrics,
	QualityLevel,
	BackgroundSystem
} from '../types/types';

// DEPRECATED: All store-based interfaces and functions are deprecated

// Define the state interface for backward compatibility
export interface BackgroundState {
	dimensions: Dimensions;
	performanceMetrics: PerformanceMetrics;
	isActive: boolean;
	qualityLevel: QualityLevel;
	isLoading: boolean;
	backgroundType: BackgroundType;
	isInitialized: boolean;
}

// DEPRECATED: Use the runes-based context instead
export interface BackgroundContext {
	// All methods are deprecated
	initializeCanvas: (canvas: HTMLCanvasElement, onReady?: () => void) => void;
	startAnimation: (
		renderFn: (ctx: CanvasRenderingContext2D, dimensions: Dimensions) => void,
		reportFn?: (metrics: PerformanceMetrics) => void
	) => void;
	stopAnimation: () => void;
	setQuality: (quality: QualityLevel) => void;
	setLoading: (isLoading: boolean) => void;
	setBackgroundType: (type: BackgroundType) => void;
	cleanup: () => void;
}

// DEPRECATED: All functions are deprecated - use runes-based context instead
function createBackgroundContext(): BackgroundContext {
	throw new Error(
		'createBackgroundContext is deprecated. Use the runes-based BackgroundContext.svelte.ts instead.'
	);
}

// DEPRECATED: All functions are deprecated - use runes-based context instead
export function setBackgroundContext(): BackgroundContext {
	throw new Error(
		'setBackgroundContext is deprecated. Use the runes-based BackgroundContext.svelte.ts instead.'
	);
}

export function getBackgroundContext(): BackgroundContext {
	// Try to get the runes-based context and return a compatibility wrapper
	const runesContext = getRunesBackgroundContext();

	if (runesContext) {
		// Return a minimal compatibility wrapper
		return {
			initializeCanvas: runesContext.initializeCanvas,
			startAnimation: runesContext.startAnimation,
			stopAnimation: runesContext.stopAnimation,
			setQuality: runesContext.setQuality,
			setLoading: runesContext.setLoading,
			setBackgroundType: runesContext.setBackgroundType,
			cleanup: runesContext.cleanup
		};
	}

	throw new Error(
		'No background context found. Use the runes-based BackgroundContext.svelte.ts instead.'
	);
}

export function createBackgroundContextStore(): BackgroundContext {
	throw new Error(
		'createBackgroundContextStore is deprecated. Use the runes-based BackgroundContext.svelte.ts instead.'
	);
}
