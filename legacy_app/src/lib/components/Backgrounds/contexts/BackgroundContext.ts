// src/lib/components/Backgrounds/contexts/BackgroundContext.ts
/**
 * Background Context Module
 *
 * This module provides a context-based API for managing background animations.
 * It uses Svelte stores for state management and provides methods for
 * initializing, animating, and cleaning up background animations.
 *
 * For Svelte 5 runes-based state management, see BackgroundContext.svelte.ts
 */

import { getContext, setContext } from 'svelte';
import { writable, derived, type Readable, type Writable, get } from 'svelte/store';
import type {
	BackgroundType,
	Dimensions,
	PerformanceMetrics,
	QualityLevel,
	BackgroundSystem
} from '../types/types';
import { BackgroundFactory } from '../core/BackgroundFactory';
import { PerformanceTracker } from '../core/PerformanceTracker';
import { detectAppropriateQuality } from '../config';
import { browser } from '$app/environment';
import { getRunesBackgroundContext } from './BackgroundContext.svelte';

// The context key
const BACKGROUND_CONTEXT_KEY = 'background-context';

// Define the state interface
export interface BackgroundState {
	dimensions: Dimensions;
	performanceMetrics: PerformanceMetrics;
	isActive: boolean;
	qualityLevel: QualityLevel;
	isLoading: boolean;
	backgroundType: BackgroundType;
	isInitialized: boolean;
}

// Define the context interface
export interface BackgroundContext {
	// State stores (keeping for backward compatibility)
	dimensions: Writable<Dimensions>;
	performanceMetrics: Writable<PerformanceMetrics>;
	isActive: Writable<boolean>;
	qualityLevel: Writable<QualityLevel>;
	isLoading: Writable<boolean>;
	backgroundType: Writable<BackgroundType>;
	isInitialized: Writable<boolean>;

	// Derived stores (keeping for backward compatibility)
	shouldRender: Readable<boolean>;
	backgroundSystem: Readable<BackgroundSystem>;

	// Actions
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

// Create the context with default values
function createBackgroundContext(): BackgroundContext {
	// Make sure we're in a browser environment
	if (!browser) {
		// Return a mock context for SSR
		return createMockBackgroundContext();
	}

	// Initialize state stores
	const dimensions = writable<Dimensions>({ width: 0, height: 0 });
	const performanceMetrics = writable<PerformanceMetrics>({ fps: 60, warnings: [] });
	const isActive = writable<boolean>(true);
	const qualityLevel = writable<QualityLevel>(detectAppropriateQuality());
	const isLoading = writable<boolean>(false);
	const backgroundType = writable<BackgroundType>('snowfall');
	const isInitialized = writable<boolean>(false);

	// Create derived stores
	const shouldRender = derived(
		[performanceMetrics, isActive],
		([$metrics, $isActive]) => $isActive && $metrics.fps > 30
	);

	const backgroundSystem = derived([backgroundType, qualityLevel], ([$type, $quality]) => {
		const system = BackgroundFactory.createBackgroundSystem({
			type: $type,
			initialQuality: $quality
		});
		return system;
	});

	// Initialize performance tracker
	const performanceTracker = PerformanceTracker.getInstance();

	// Canvas references
	let canvas: HTMLCanvasElement | null = null;
	let ctx: CanvasRenderingContext2D | null = null;
	let animationFrameId: number | null = null;
	let reportCallback: ((metrics: PerformanceMetrics) => void) | null = null;

	// Actions
	function initializeCanvas(canvasElement: HTMLCanvasElement, onReady?: () => void): void {
		canvas = canvasElement;
		ctx = canvas.getContext('2d');

		if (!ctx) {
			return;
		}

		const initialWidth = browser ? window.innerWidth : 1280;
		const initialHeight = browser ? window.innerHeight : 720;

		// Use direct assignment instead of .set() for better Svelte 5 compatibility
		dimensions.update(() => ({ width: initialWidth, height: initialHeight }));

		canvas.width = initialWidth;
		canvas.height = initialHeight;

		if (browser) {
			window.addEventListener('resize', handleResize);
			document.addEventListener('visibilitychange', handleVisibilityChange);
		}

		// Use direct assignment instead of .set()
		isInitialized.update(() => true);

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
			// Use update instead of set for better Svelte 5 compatibility
			performanceMetrics.update(() => ({
				fps: perfStatus.fps,
				warnings: perfStatus.warnings
			}));

			if (reportCallback) {
				reportCallback(get(performanceMetrics));
			}

			const currentDimensions = get(dimensions);
			const shouldRenderNow = get(isActive) && perfStatus.fps > 30;

			if (shouldRenderNow) {
				ctx.clearRect(0, 0, currentDimensions.width, currentDimensions.height);
				renderFn(ctx, currentDimensions);
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

		canvas = null;
		ctx = null;
	}

	function setQuality(quality: QualityLevel): void {
		// Use update instead of set for better Svelte 5 compatibility
		qualityLevel.update(() => quality);
	}

	function setLoading(loading: boolean): void {
		// Use update instead of set for better Svelte 5 compatibility
		isLoading.update(() => loading);
	}

	function setBackgroundType(type: BackgroundType): void {
		// Use update instead of set for better Svelte 5 compatibility
		backgroundType.update(() => type);
	}

	// Internal handlers
	function handleResize(): void {
		if (!canvas) return;
		if (!browser) return;

		const newWidth = window.innerWidth;
		const newHeight = window.innerHeight;

		canvas.width = newWidth;
		canvas.height = newHeight;

		// Use update instead of set for better Svelte 5 compatibility
		dimensions.update(() => ({ width: newWidth, height: newHeight }));

		// Temporarily reduce quality during resize for better performance
		const currentQuality = get(qualityLevel);
		qualityLevel.update(() => 'low');

		setTimeout(() => {
			qualityLevel.update(() => currentQuality);
		}, 500);
	}

	function handleVisibilityChange(): void {
		if (!browser) return;
		const isVisible = document.visibilityState === 'visible';
		// Use update instead of set for better Svelte 5 compatibility
		isActive.update(() => isVisible);
	}

	return {
		// Expose stores
		dimensions,
		performanceMetrics,
		isActive,
		qualityLevel,
		isLoading,
		backgroundType,
		isInitialized,

		// Expose derived stores
		shouldRender,
		backgroundSystem,

		// Expose actions
		initializeCanvas,
		startAnimation,
		stopAnimation,
		setQuality,
		setLoading,
		setBackgroundType,
		cleanup
	};
}

// Create a mock background context for SSR
function createMockBackgroundContext(): BackgroundContext {
	// Create empty writable stores
	const dimensions = writable<Dimensions>({ width: 0, height: 0 });
	const performanceMetrics = writable<PerformanceMetrics>({ fps: 60, warnings: [] });
	const isActive = writable<boolean>(true);
	const qualityLevel = writable<QualityLevel>('medium');
	const isLoading = writable<boolean>(false);
	const backgroundType = writable<BackgroundType>('snowfall');
	const isInitialized = writable<boolean>(false);

	// Create derived stores with mock values
	const shouldRender = derived([isActive], ([$isActive]) => $isActive);

	// Create a mock background system
	const mockSystem = {
		initialize: () => {},
		update: () => {},
		draw: () => {},
		setQuality: () => {},
		cleanup: () => {}
	} as BackgroundSystem;

	const backgroundSystem = writable<BackgroundSystem>(mockSystem);

	// Return a mock context with no-op functions
	return {
		dimensions,
		performanceMetrics,
		isActive,
		qualityLevel,
		isLoading,
		backgroundType,
		isInitialized,
		shouldRender,
		backgroundSystem,
		initializeCanvas: () => {},
		startAnimation: () => {},
		stopAnimation: () => {},
		setQuality: () => {},
		setLoading: () => {},
		setBackgroundType: () => {},
		cleanup: () => {}
	};
}

// Set the context
export function setBackgroundContext(): BackgroundContext {
	const context = createBackgroundContext();
	setContext(BACKGROUND_CONTEXT_KEY, context);
	return context;
}

// Get the context
export function getBackgroundContext(): BackgroundContext {
	// First try to get the store-based context
	const storeContext = getContext<BackgroundContext>(BACKGROUND_CONTEXT_KEY);

	if (storeContext) {
		return storeContext;
	}

	// If no store-based context is found, try to get the runes-based context
	// and create a store-based wrapper around it
	const runesContext = getRunesBackgroundContext();

	if (runesContext) {
		// Create store wrappers around the runes-based context
		const dimensions = writable<Dimensions>(runesContext.dimensions);
		const performanceMetrics = writable<PerformanceMetrics>(runesContext.performanceMetrics);
		const isActive = writable<boolean>(runesContext.isActive);
		const qualityLevel = writable<QualityLevel>(runesContext.qualityLevel);
		const isLoading = writable<boolean>(runesContext.isLoading);
		const backgroundType = writable<BackgroundType>(runesContext.backgroundType);
		const isInitialized = writable<boolean>(runesContext.isInitialized);

		// Create derived stores
		const shouldRender = derived(
			[performanceMetrics, isActive],
			([$metrics, $isActive]) => $isActive && $metrics.fps > 30
		);

		const backgroundSystem = writable<BackgroundSystem>(
			runesContext.backgroundSystem ||
				({
					initialize: () => {},
					update: () => {},
					draw: () => {},
					setQuality: () => {},
					cleanup: () => {}
				} as BackgroundSystem)
		);

		// Return a store-based context that delegates to the runes-based context
		return {
			// Expose stores
			dimensions,
			performanceMetrics,
			isActive,
			qualityLevel,
			isLoading,
			backgroundType,
			isInitialized,

			// Expose derived stores
			shouldRender,
			backgroundSystem,

			// Delegate actions to the runes-based context
			initializeCanvas: runesContext.initializeCanvas,
			startAnimation: runesContext.startAnimation,
			stopAnimation: runesContext.stopAnimation,
			setQuality: (quality: QualityLevel) => {
				runesContext.setQuality(quality);
				qualityLevel.update(() => quality);
			},
			setLoading: (loading: boolean) => {
				runesContext.setLoading(loading);
				isLoading.update(() => loading);
			},
			setBackgroundType: (type: BackgroundType) => {
				runesContext.setBackgroundType(type);
				backgroundType.update(() => type);
			},
			cleanup: runesContext.cleanup
		};
	}

	// If no context is found, throw an error
	throw new Error('No background context found. Make sure to use BackgroundProvider.');
}

// Create a background context without setting it
export function createBackgroundContextStore(): BackgroundContext {
	return createBackgroundContext();
}
