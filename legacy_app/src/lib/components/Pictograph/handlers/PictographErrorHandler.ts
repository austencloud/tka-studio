/**
 * Pictograph Error Handler
 *
 * This module provides error handling functionality for the Pictograph component.
 */

import type { Writable } from 'svelte/store';
import type { PictographData } from '$lib/types/PictographData';
import { errorService, ErrorSeverity } from '../../../services/ErrorHandlingService';
import { logger } from '$lib/core/logging';
import type { PropData } from '../../objects/Prop/PropData';
import type { ArrowData } from '../../objects/Arrow/ArrowData';

/**
 * Context for error handling
 */
export interface ErrorHandlerContext {
	pictographDataStore: Writable<PictographData>;
	dispatch: (event: string, detail?: any) => void;
	state: {
		set: (value: string) => void;
	};
	errorMessage: {
		set: (value: string | null) => void;
	};
	componentsLoaded: number;
	totalComponentsToLoad: number;
}

/**
 * Context for component error handling
 */
export interface ComponentErrorContext {
	loadedComponents: Set<string>;
	componentsLoaded: number;
	totalComponentsToLoad: number;
	dispatch: (event: string, detail?: any) => void;
	checkLoadingComplete: () => void;
}

/**
 * Context for fallback data
 */
export interface FallbackDataContext {
	redPropData: PropData | null;
	bluePropData: PropData | null;
	redArrowData: ArrowData | null;
	blueArrowData: ArrowData | null;
}

/**
 * Handles errors that occur during pictograph component operations
 * Logs the error, updates component state, and dispatches events
 *
 * @param source The source of the error (e.g., 'initialization', 'grid loading')
 * @param error The error object or message
 * @param context The error handler context containing necessary data and functions
 */
export function handlePictographError(
	source: string,
	error: any,
	context: ErrorHandlerContext
): void {
	try {
		// Create a safe error message that won't have circular references
		const errorMsg =
			error instanceof Error ? error.message : typeof error === 'string' ? error : 'Unknown error';

		// Log the error
		logger.error(`Pictograph error in ${source}: ${errorMsg}`, {
			error: error instanceof Error ? error : new Error(String(error))
		});

		// Update component state
		context.state.set('error');
		context.errorMessage.set(errorMsg);

		// Dispatch error event
		context.dispatch('error', {
			source,
			message: errorMsg,
			componentsLoaded: context.componentsLoaded,
			totalComponentsToLoad: context.totalComponentsToLoad
		});

		// Report to error service
		errorService.reportError({
			message: `Pictograph error in ${source}: ${errorMsg}`,
			severity: ErrorSeverity.ERROR,
			source: 'Pictograph'
		});
	} catch (secondaryError) {
		// If error handling itself fails, log to console as a last resort
		console.error('Error in pictograph error handler:', secondaryError);
		console.error('Original error:', error);
	}
}

/**
 * Handles errors that occur in specific pictograph components (Prop, Arrow, etc.)
 * Applies fallback positioning and continues loading
 *
 * @param component The component that experienced the error (e.g., 'redProp', 'blueArrow')
 * @param error The error object or message
 * @param context Additional context for error handling
 * @param fallbackData Object containing the data that needs fallback positioning
 */
export function handlePictographComponentError(
	component: string,
	error: any,
	context: ComponentErrorContext,
	fallbackData: FallbackDataContext
): void {
	try {
		// Create a safe error message
		const errorMsg =
			error instanceof Error ? error.message : typeof error === 'string' ? error : 'Unknown error';

		// Log the error
		logger.warn(`Pictograph component error in ${component}: ${errorMsg}`, {
			error: error instanceof Error ? error : new Error(String(error))
		});

		// Apply fallback positioning
		applyFallbackPositioning(component, fallbackData);

		// Mark the component as loaded despite the error
		if (!context.loadedComponents.has(component)) {
			context.loadedComponents.add(component);
			context.componentsLoaded++;
		}

		// Dispatch error event
		context.dispatch('componentError', {
			component,
			message: errorMsg
		});

		// Check if loading is complete
		context.checkLoadingComplete();

		// Report to error service
		errorService.reportError({
			message: `Pictograph component error in ${component}: ${errorMsg}`,
			severity: ErrorSeverity.WARNING,
			source: `Pictograph.${component}`
		});
	} catch (secondaryError) {
		// If error handling itself fails, log to console as a last resort
		console.error('Error in pictograph component error handler:', secondaryError);
		console.error('Original error:', error);
	}
}

/**
 * Applies fallback positioning to components when errors occur
 *
 * @param component The component that needs fallback positioning
 * @param data Object containing the data that needs fallback positioning
 */
export function applyFallbackPositioning(component: string, data: FallbackDataContext): void {
	const centerX = 475;
	const centerY = 475;
	const offset = 50;

	switch (component) {
		case 'redProp':
			if (data.redPropData) {
				data.redPropData.coords = { x: centerX - offset, y: centerY };
				data.redPropData.rotAngle = 0;
			}
			break;
		case 'blueProp':
			if (data.bluePropData) {
				data.bluePropData.coords = { x: centerX + offset, y: centerY };
				data.bluePropData.rotAngle = 0;
			}
			break;
		case 'redArrow':
			if (data.redArrowData) {
				data.redArrowData.coords = { x: centerX, y: centerY - offset };
				data.redArrowData.rotAngle = -90;
			}
			break;
		case 'blueArrow':
			if (data.blueArrowData) {
				data.blueArrowData.coords = { x: centerX, y: centerY + offset };
				data.blueArrowData.rotAngle = 90;
			}
			break;
		default:
			logger.warn(`Unknown component: ${component}, using center position`);
	}
}
