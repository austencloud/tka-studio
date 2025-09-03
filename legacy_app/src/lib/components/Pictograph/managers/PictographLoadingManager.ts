/**
 * Pictograph Loading Manager
 *
 * This module provides loading management functionality for the Pictograph component.
 */

import type { PictographData } from '$lib/types/PictographData';
import type { GridData } from '../../objects/Grid/GridData';
import { logger } from '$lib/core/logging';

/**
 * Context for loading management
 */
export interface LoadingManagerContext {
	state: {
		set: (value: string) => void;
		value?: string;
	};
	loadedComponents: Set<string>;
	requiredComponents: string[];
	componentsLoaded: number;
	totalComponentsToLoad: number;
	dispatch: (event: string, detail?: any) => void;
	pictographData: PictographData | undefined;
}

/**
 * Context for component creation
 */
export interface ComponentCreationContext {
	createAndPositionComponents: () => void;
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

	// Check if we have motion data
	const hasMotionData = hasRequiredMotionData(pictographData);

	// Set the appropriate state
	if (hasMotionData) {
		return 'loading';
	} else {
		return 'grid_only';
	}
}

/**
 * Checks if the pictograph data has the required motion data
 *
 * @param data The pictograph data to check
 * @returns True if the data has the required motion data
 */
export function hasRequiredMotionData(data: PictographData | undefined): boolean {
	if (!data) return false;
	return !!(data.redMotionData || data.blueMotionData);
}

/**
 * Handles the grid loaded event
 *
 * @param data The grid data
 * @param context The loading manager context
 * @param componentContext The component creation context
 */
export function handleGridLoaded(
	data: GridData,
	context: LoadingManagerContext,
	componentContext: ComponentCreationContext
): void {
	try {
		// Mark the grid as loaded
		if (!context.loadedComponents.has('grid')) {
			context.loadedComponents.add('grid');
			context.componentsLoaded++;
		}

		// Log the grid loading
		logger.debug('Pictograph: Grid loaded', {
			data: {
				gridMode: context.pictographData?.gridMode,
				hasPoints: !!data.allHandPointsNormal
			}
		});

		// Create and position components now that the grid is loaded
		componentContext.createAndPositionComponents();

		// Update progress
		const progress = Math.floor((context.componentsLoaded / context.totalComponentsToLoad) * 100);
		context.dispatch('loadProgress', { progress });

		// If we're in grid-only mode, mark as complete
		if (
			typeof context.state === 'object' &&
			context.state.set &&
			context.state.value === 'grid_only'
		) {
			context.state.set('complete');
			context.dispatch('complete');
		}
	} catch (error) {
		logger.error('Error handling grid loaded event', {
			error: error instanceof Error ? error : new Error(String(error))
		});
	}
}

/**
 * Handles a component loaded event
 *
 * @param component The component that was loaded
 * @param context The loading manager context
 */
export function handleComponentLoaded(component: string, context: LoadingManagerContext): void {
	try {
		// Mark the component as loaded
		if (!context.loadedComponents.has(component)) {
			context.loadedComponents.add(component);
			context.componentsLoaded++;

			// Log the component loading
			logger.debug(`Pictograph: Component loaded - ${component}`, {
				data: {
					componentsLoaded: context.componentsLoaded,
					totalComponentsToLoad: context.totalComponentsToLoad
				}
			});

			// Update progress
			const progress = Math.floor((context.componentsLoaded / context.totalComponentsToLoad) * 100);
			context.dispatch('loadProgress', { progress });
		}
	} catch (error) {
		logger.error('Error handling component loaded event', {
			error: error instanceof Error ? error : new Error(String(error))
		});
	}
}

/**
 * Checks if all required components are loaded
 *
 * @param context The loading manager context
 */
export function checkLoadingComplete(context: LoadingManagerContext): void {
	try {
		// Check if all required components are loaded
		const allLoaded = context.requiredComponents.every((comp) =>
			context.loadedComponents.has(comp)
		);

		// If all components are loaded, mark as complete
		if (
			allLoaded &&
			typeof context.state === 'object' &&
			context.state.set &&
			context.state.value !== 'complete' &&
			context.state.value !== 'error'
		) {
			context.state.set('complete');

			// Log the completion
			logger.info('Pictograph: Loading complete', {
				data: {
					componentsLoaded: context.componentsLoaded,
					totalComponentsToLoad: context.totalComponentsToLoad
				}
			});

			// Dispatch complete event
			context.dispatch('complete');
		}
	} catch (error) {
		logger.error('Error checking if loading is complete', {
			error: error instanceof Error ? error : new Error(String(error))
		});
	}
}
