/**
 * Type definitions for Grid component events
 */

/**
 * Interface for the error event detail
 */
export interface GridErrorEventDetail {
	message: string;
}

/**
 * Type for the Grid component's custom events
 */
export interface GridEvents {
	error: { message: string };
}
