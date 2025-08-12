/**
 * Svelte 5 Runes Integration for Background Context
 *
 * This module provides utilities for integrating the background context
 * with Svelte 5 runes. This file has a .svelte.ts extension to enable runes support.
 */

import { browser } from '$app/environment';
import { getContext, setContext } from 'svelte';
import { detectAppropriateQuality } from '../config';
import { BackgroundFactory } from '../core/BackgroundFactory';
import { PerformanceTracker } from '../core/PerformanceTracker';
import type {
	BackgroundSystem,
	BackgroundType,
	Dimensions,
	PerformanceMetrics,
	QualityLevel,
} from '../types/types';

// The context key
const BACKGROUND_CONTEXT_KEY = 'background-context-runes';

/**
 * Interface for the runes-based background context
 */
export interface RunesBackgroundContext {
	// State
	dimensions: Dimensions;
	performanceMetrics: PerformanceMetrics;
	isActive: boolean;
	qualityLevel: QualityLevel;
	isLoading: boolean;
	backgroundType: BackgroundType;
	isInitialized: boolean;
	shouldRender: boolean;
	backgroundSystem: BackgroundSystem | null;

	// Methods
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

	// State persistence
	savePreferences: () => void;
	loadPreferences: () => void;
}

// Track created context instances to prevent duplicates
const contextInstances = new Set();

/**
 * Create a new background context using Svelte 5 runes
 *
 * This function creates a new background context using Svelte 5's runes system
 * for reactive state management. It provides the same API as the original context
 * but uses runes instead of stores.
 *
 * @returns A runes-based background context
 */
export function createRunesBackgroundContext(): RunesBackgroundContext {
	// Skip browser-specific initialization during SSR
	if (!browser) {
		return createMockRunesBackgroundContext();
	}

	// Debug counter to track context creation
	const contextId = Math.floor(Math.random() * 10000);

	// Ensure we don't create duplicate contexts
	if (contextInstances.size > 0) {
		// Try to get existing context, but don't throw during HMR
		try {
			const existingContext = getRunesBackgroundContext();
			if (existingContext) {
				return existingContext;
			}
		} catch {
			// Context not found (likely due to HMR), continue with creating new one
			contextInstances.clear(); // Clear stale instances
		}
	}

	// Initialize state with runes - use explicit initial values to avoid undefined
	let dimensions = $state<Dimensions>({ width: 0, height: 0 });
	let performanceMetrics = $state<PerformanceMetrics>({ fps: 60, warnings: [] });
	let isActive = $state(true);
	let qualityLevel = $state<QualityLevel>(detectAppropriateQuality());
	let isLoading = $state(false);
	let backgroundType = $state<BackgroundType>('snowfall');
	let isInitialized = $state(false);

	// Derived values
	const shouldRender = $derived(isActive && performanceMetrics.fps > 30);

	// Create background system based on type and quality
	let backgroundSystem = $state<BackgroundSystem | null>(null);

	// Canvas and context references
	let canvas: HTMLCanvasElement | null = null;
	let ctx: CanvasRenderingContext2D | null = null;

	// Initialize background system
	function initializeBackgroundSystem() {
		if (browser && !backgroundSystem) {
			try {
				backgroundSystem = BackgroundFactory.createBackgroundSystem({
					type: backgroundType,
					initialQuality: qualityLevel,
				});
			} catch (error) {
				console.error('[SYSTEM] Error creating initial background system:', error);
				// Try fallback
				try {
					backgroundSystem = BackgroundFactory.createBackgroundSystem({
						type: 'snowfall',
						initialQuality: qualityLevel,
					});
				} catch (fallbackError) {
					console.error(
						'[SYSTEM] Error creating fallback background system:',
						fallbackError
					);
				}
			}
		}
	}

	// Initialize on first load
	initializeBackgroundSystem();
	let animationFrameId: number | null = null;
	let reportCallback: ((metrics: PerformanceMetrics) => void) | null = null;

	// Load preferences from localStorage
	function loadPreferences() {
		if (!browser) return;

		try {
			const savedPrefs = localStorage.getItem('background-preferences');
			if (savedPrefs) {
				const prefs = JSON.parse(savedPrefs);

				// Only update if values are different to prevent triggering effects
				const currentBackgroundType = backgroundType;
				const currentQualityLevel = qualityLevel;

				if (prefs.backgroundType && prefs.backgroundType !== currentBackgroundType) {
					backgroundType = prefs.backgroundType;
				}

				if (prefs.qualityLevel && prefs.qualityLevel !== currentQualityLevel) {
					qualityLevel = prefs.qualityLevel;
				}
			}
		} catch (error) {
			console.error('Failed to load background preferences:', error);
		}
	}

	// Save preferences to localStorage
	function savePreferences() {
		if (!browser) return;

		try {
			const prefs = {
				backgroundType,
				qualityLevel,
			};
			localStorage.setItem('background-preferences', JSON.stringify(prefs));
		} catch (error) {
			console.error('Failed to save background preferences:', error);
		}
	}

	// Function to create and initialize the background system
	function createAndInitializeBackgroundSystem(
		type: BackgroundType,
		quality: QualityLevel
	): void {
		if (backgroundSystem) {
			backgroundSystem.cleanup();
		}

		try {
			const newSystem = BackgroundFactory.createBackgroundSystem({
				type,
				initialQuality: quality,
			});

			// Initialize if canvas is already set up
			if (isInitialized && canvas && ctx) {
				newSystem.initialize(dimensions, quality);
			}

			// Set the background system
			backgroundSystem = newSystem;
		} catch (error) {
			console.error('[SYSTEM] Error creating background system:', error);

			// Fallback to snowfall if there's an error with the requested background
			if (type !== 'snowfall') {
				try {
					const fallbackSystem = BackgroundFactory.createBackgroundSystem({
						type: 'snowfall',
						initialQuality: quality,
					});

					if (isInitialized && canvas && ctx) {
						fallbackSystem.initialize(dimensions, quality);
					}

					backgroundSystem = fallbackSystem;
				} catch (fallbackError) {
					console.error(
						'[SYSTEM] Error creating fallback background system:',
						fallbackError
					);
				}
			}
		}
	}

	// Remove problematic effects that cause circular dependencies
	// Instead, we'll handle updates through the setter methods

	// Initialize performance tracker
	const performanceTracker = PerformanceTracker.getInstance();

	// Actions
	function initializeCanvas(canvasElement: HTMLCanvasElement, onReady?: () => void): void {
		canvas = canvasElement;
		ctx = canvas.getContext('2d');

		if (!ctx) {
			return;
		}

		const initialWidth = browser ? window.innerWidth : 1280;
		const initialHeight = browser ? window.innerHeight : 720;

		dimensions = { width: initialWidth, height: initialHeight };

		canvas.width = initialWidth;
		canvas.height = initialHeight;

		if (browser) {
			window.addEventListener('resize', handleResize);
			document.addEventListener('visibilitychange', handleVisibilityChange);
		}

		isInitialized = true;

		// Initialize the background system if it exists
		if (backgroundSystem) {
			backgroundSystem.initialize(dimensions, qualityLevel);
		}

		if (onReady) {
			onReady();
		}
	}

	function startAnimation(
		renderFn: (ctx: CanvasRenderingContext2D, dimensions: Dimensions) => void,
		reportFn?: (metrics: PerformanceMetrics) => void
	): void {
		if (!ctx || !canvas) {
			return;
		}

		if (reportFn) {
			reportCallback = reportFn;
		}

		performanceTracker.reset();

		const animate = () => {
			if (!ctx || !canvas) return;

			performanceTracker.update();

			const perfStatus = performanceTracker.getPerformanceStatus();
			performanceMetrics = {
				fps: perfStatus.fps,
				warnings: perfStatus.warnings,
			};

			if (reportCallback) {
				reportCallback(performanceMetrics);
			}

			const shouldRenderNow = isActive && perfStatus.fps > 30;

			if (shouldRenderNow) {
				ctx.clearRect(0, 0, dimensions.width, dimensions.height);
				renderFn(ctx, dimensions);
			}

			animationFrameId = requestAnimationFrame(animate);
		};

		if (browser) {
			animationFrameId = requestAnimationFrame(animate);
		}
	}

	function stopAnimation(): void {
		if (animationFrameId && browser) {
			cancelAnimationFrame(animationFrameId);
			animationFrameId = null;
		}
	}

	function cleanup(): void {
		stopAnimation();

		if (browser) {
			window.removeEventListener('resize', handleResize);
			document.removeEventListener('visibilitychange', handleVisibilityChange);
		}

		if (backgroundSystem) {
			backgroundSystem.cleanup();
		}

		canvas = null;
		ctx = null;
	}

	function setQuality(quality: QualityLevel): void {
		qualityLevel = quality;
		if (backgroundSystem) {
			backgroundSystem.setQuality(quality);
		}
		savePreferences();
	}

	function setLoading(loading: boolean): void {
		isLoading = loading;
	}

	function setBackgroundType(type: BackgroundType): void {
		backgroundType = type;
		// Create new background system with the new type
		createAndInitializeBackgroundSystem(type, qualityLevel);
		savePreferences();
	}

	// Internal handlers
	function handleResize(): void {
		if (!canvas) return;
		if (!browser) return;

		const newWidth = window.innerWidth;
		const newHeight = window.innerHeight;

		canvas.width = newWidth;
		canvas.height = newHeight;

		dimensions = { width: newWidth, height: newHeight };

		// Temporarily reduce quality during resize for better performance
		const currentQuality = qualityLevel;
		qualityLevel = 'low';

		setTimeout(() => {
			setQuality(currentQuality);
		}, 500);
	}

	function handleVisibilityChange(): void {
		if (!browser) return;
		const isVisible = document.visibilityState === 'visible';
		isActive = isVisible;
	}

	// Load preferences on initialization
	if (browser) {
		loadPreferences();
	}

	// Mark context as created
	contextInstances.add(contextId);

	return {
		// State getters (reactive)
		get dimensions() {
			return dimensions;
		},
		get performanceMetrics() {
			return performanceMetrics;
		},
		get isActive() {
			return isActive;
		},
		get qualityLevel() {
			return qualityLevel;
		},
		get isLoading() {
			return isLoading;
		},
		get backgroundType() {
			return backgroundType;
		},
		get isInitialized() {
			return isInitialized;
		},
		get shouldRender() {
			return shouldRender;
		},
		get backgroundSystem() {
			return backgroundSystem;
		},

		// Actions
		initializeCanvas,
		startAnimation,
		stopAnimation,
		setQuality,
		setLoading,
		setBackgroundType,
		cleanup,
		savePreferences,
		loadPreferences,
	};
}

/**
 * Create a mock background context for SSR
 */
function createMockRunesBackgroundContext(): RunesBackgroundContext {
	return {
		dimensions: { width: 0, height: 0 },
		performanceMetrics: { fps: 60, warnings: [] },
		isActive: true,
		qualityLevel: 'medium',
		isLoading: false,
		backgroundType: 'snowfall',
		isInitialized: false,
		shouldRender: true,
		backgroundSystem: null,
		initializeCanvas: () => {},
		startAnimation: () => {},
		stopAnimation: () => {},
		setQuality: () => {},
		setLoading: () => {},
		setBackgroundType: () => {},
		cleanup: () => {},
		savePreferences: () => {},
		loadPreferences: () => {},
	};
}

/**
 * Set the runes-based background context
 */
export function setRunesBackgroundContext(): RunesBackgroundContext {
	const context = createRunesBackgroundContext();
	setContext(BACKGROUND_CONTEXT_KEY, context);
	return context;
}

/**
 * Get the runes-based background context
 */
export function getRunesBackgroundContext(): RunesBackgroundContext {
	const context = getContext<RunesBackgroundContext>(BACKGROUND_CONTEXT_KEY);

	if (!context) {
		throw new Error(
			'No runes background context found. Make sure to use BackgroundProvider. This can happen during HMR - try refreshing the page.'
		);
	}

	return context;
}
