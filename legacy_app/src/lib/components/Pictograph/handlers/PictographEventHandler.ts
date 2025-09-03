/**
 * Pictograph Event Handler
 *
 * This module provides event handling functionality for the Pictograph component.
 */

import type { EventDispatcher } from 'svelte';
import { browser } from '$app/environment';
import hapticFeedbackService from '$lib/services/HapticFeedbackService';

/**
 * Dispatches an error event
 *
 * @param dispatch The event dispatcher
 * @param source The source of the error
 * @param message The error message
 * @param componentsLoaded The number of components loaded
 * @param totalComponentsToLoad The total number of components to load
 */
export function dispatchErrorEvent(
	dispatch: EventDispatcher<any>,
	source: string,
	message: string,
	componentsLoaded: number,
	totalComponentsToLoad: number
): void {
	dispatch('error', {
		source,
		message,
		componentsLoaded,
		totalComponentsToLoad
	});
}

/**
 * Dispatches a component error event
 *
 * @param dispatch The event dispatcher
 * @param component The component that experienced the error
 * @param message The error message
 */
export function dispatchComponentErrorEvent(
	dispatch: EventDispatcher<any>,
	component: string,
	message: string
): void {
	dispatch('componentError', {
		component,
		message
	});
}

/**
 * Dispatches a load progress event
 *
 * @param dispatch The event dispatcher
 * @param progress The loading progress (0-100)
 */
export function dispatchLoadProgressEvent(dispatch: EventDispatcher<any>, progress: number): void {
	dispatch('loadProgress', { progress });
}

/**
 * Dispatches a complete event
 *
 * @param dispatch The event dispatcher
 */
export function dispatchCompleteEvent(dispatch: EventDispatcher<any>): void {
	dispatch('complete');
}

/**
 * Dispatches a data updated event
 *
 * @param dispatch The event dispatcher
 * @param type The type of update
 */
export function dispatchDataUpdatedEvent(dispatch: EventDispatcher<any>, type: string): void {
	dispatch('dataUpdated', { type });
}

/**
 * Handles a click event
 *
 * @param onClick The click handler function
 * @returns A function to handle the click event
 */
export function handleClick(onClick: (() => void) | undefined): (() => void) | undefined {
	if (!onClick) return undefined;
	return () => {
		// Provide haptic feedback when clicking on a pictograph
		if (browser) {
			hapticFeedbackService.trigger('selection');
		}

		// Call the original click handler
		onClick();
	};
}
