// src/lib/components/construct/option-picker/layoutContext.svelte.ts
import { getContext, setContext } from 'svelte';
import type { DeviceType, ContainerAspect, ResponsiveLayoutConfig } from './config';
import type { FoldableDetectionResult } from './utils/deviceDetection';

export const LAYOUT_CONTEXT_KEY = Symbol('layout-context');

export interface LayoutContextValue {
	deviceType: DeviceType;
	isMobile: boolean;
	isTablet: boolean;
	isPortrait: boolean;
	containerWidth: number;
	containerHeight: number; // Renamed from ht for clarity
	ht: number; // Keep for backward compatibility
	containerAspect: ContainerAspect;
	layoutConfig: ResponsiveLayoutConfig;
	foldableInfo?: FoldableDetectionResult;
}

/**
 * Creates a layout context using Svelte 5 runes
 */
export function createLayoutContext(
	windowWidth: number = 800,
	windowHeight: number = 600,
	containerWidth: number = 800,
	containerHeight: number = 600
) {
	// State using runes
	let _windowWidth = $state(windowWidth);
	let _windowHeight = $state(windowHeight);
	let _containerWidth = $state(containerWidth);
	let _containerHeight = $state(containerHeight);

	// Context value derived from state
	const contextValue = $derived<LayoutContextValue>({
		deviceType: 'desktop' as DeviceType, // Will be calculated in the component using this
		isMobile: false,
		isTablet: false,
		isPortrait: _containerHeight > _containerWidth,
		containerWidth: _containerWidth,
		containerHeight: _containerHeight,
		ht: _containerHeight,
		containerAspect: 'square' as ContainerAspect, // Will be calculated
		layoutConfig: {
			gridColumns: 'repeat(4, minmax(0, 1fr))',
			optionSize: '100px',
			gridGap: '8px',
			gridClass: '',
			aspectClass: '',
			scaleFactor: 1.0
		}
	});

	// Update functions
	function updateWindowDimensions(width: number, height: number) {
		_windowWidth = width;
		_windowHeight = height;
	}

	function updateContainerDimensions(width: number, height: number) {
		_containerWidth = width;
		_containerHeight = height;
	}

	return {
		// Reactive getters
		get windowWidth() { return _windowWidth; },
		get windowHeight() { return _windowHeight; },
		get containerWidth() { return _containerWidth; },
		get containerHeight() { return _containerHeight; },
		get contextValue() { return contextValue; },

		// Update functions
		updateWindowDimensions,
		updateContainerDimensions
	};
}

/**
 * Sets the layout context for child components
 */
export function setLayoutContext(context: ReturnType<typeof createLayoutContext>) {
	setContext(LAYOUT_CONTEXT_KEY, context);
	return context;
}

/**
 * Gets the layout context from a parent component
 */
export function getLayoutContext(): ReturnType<typeof createLayoutContext> | undefined {
	return getContext<ReturnType<typeof createLayoutContext>>(LAYOUT_CONTEXT_KEY);
}

// Type helper for consuming the context
export type LayoutContext = ReturnType<typeof createLayoutContext>;
