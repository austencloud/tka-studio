// src/lib/components/Pictograph/utils/loadingManager.ts
import type { GridData } from '../../objects/Grid/GridData';
import { logger } from '$lib/core/logging';
import type { PictographData } from '$lib/types/PictographData';
import { hasRequiredMotionData } from './dataComparison';

/**
 * Interface for the loading manager context
 * Contains all the necessary data and functions for managing component loading
 */
export interface LoadingManagerContext {
	state: {
		set: (value: string) => void;
		subscribe?: (callback: (value: string) => void) => () => void;
	};
	loadedComponents: Set<string>;
	requiredComponents: string[];
	componentsLoaded: number;
	totalComponentsToLoad: number;
	dispatch: (event: string, detail?: any) => void;
	pictographData?: PictographData;
}

/**
 * Handles the grid loaded event
 * Updates state and continues with component creation if needed
 *
 * @param data The grid data that was loaded
 * @param context The loading manager context
 * @param callbacks Object containing callback functions
 * @returns The grid data that was loaded
 */
export function handleGridLoaded(
	data: GridData,
	context: LoadingManagerContext,
	callbacks: {
		createAndPositionComponents: () => void;
	}
): GridData {
	try {
		// Update state
		context.loadedComponents.add('grid');
		context.componentsLoaded++;

		// Get the current state value
		let currentState = '';
		if (typeof context.state === 'object' && context.state.subscribe) {
			// It's a store, get its value
			context.state.subscribe((value) => {
				currentState = value;
			})();
		} else if (typeof context.state === 'string') {
			// It's already a string
			currentState = context.state;
		}

		// Exit if grid-only mode
		if (currentState === 'grid_only') {
			context.dispatch('loaded', { complete: false });
			return data;
		}

		// Continue loading
		callbacks.createAndPositionComponents();

		return data;
	} catch (error) {
		logger.error('Error in handleGridLoaded', {
			error: error instanceof Error ? error : new Error(String(error))
		});
		throw error; // Re-throw to be handled by the main error handler
	}
}

/**
 * Handles a component being loaded
 * Updates state and checks if all components are loaded
 *
 * @param component The name of the component that was loaded
 * @param context The loading manager context
 */
export function handleComponentLoaded(component: string, context: LoadingManagerContext): void {
	context.loadedComponents.add(component);
	context.componentsLoaded++;
	context.dispatch('componentLoaded', { componentName: component });
	checkLoadingComplete(context);
}

/**
 * Checks if all required components have been loaded
 * Updates state and dispatches events accordingly
 *
 * @param context The loading manager context
 */
export function checkLoadingComplete(context: LoadingManagerContext): void {
	const startCheck = performance.now();
	const allLoaded = context.requiredComponents.every((component) =>
		context.loadedComponents.has(component)
	);

	if (allLoaded) {
		// Set state to complete
		if (context.state && typeof context.state.set === 'function') {
			context.state.set('complete');
		}

		const loadTime = performance.now() - startCheck;
		logger.info(`Pictograph fully loaded`, {
			duration: loadTime,
			data: {
				componentsLoaded: context.componentsLoaded,
				totalComponentsToLoad: context.totalComponentsToLoad,
				letter: context.pictographData?.letter,
				gridMode: context.pictographData?.gridMode,
				loadedComponents: Array.from(context.loadedComponents)
			}
		});

		context.dispatch('loaded', { complete: true });
	}
}

/**
 * Initializes the pictograph component state based on the data
 *
 * @param pictographData The current pictograph data
 * @param currentState The current state of the component
 * @returns The new state based on the data
 */
export function initializeComponentState(
	pictographData: PictographData | undefined,
	currentState: string
): string {
	// If we're already in an error state, don't change it
	if (currentState === 'error') {
		return currentState;
	}

	// If no data is available, use grid-only mode
	if (!pictographData) {
		return 'grid_only';
	}

	// Update state based on available motion data
	if (hasRequiredMotionData(pictographData)) {
		if (currentState === 'grid_only') {
			return 'loading';
		}
		return currentState; // Keep current state if it's already 'loading' or 'complete'
	} else {
		return 'grid_only';
	}
}
