/**
 * Pictograph Rendering Utilities
 *
 * This module provides helper functions for rendering the Pictograph component.
 */

import type { PictographData } from '$lib/types/PictographData';

/**
 * Determines if the pictograph should show a beat label
 *
 * @param beatNumber The beat number to display
 * @param isStartPosition Whether this is a start position
 * @returns True if a beat label should be shown
 */
export function shouldShowBeatLabel(beatNumber: number | null, isStartPosition: boolean): boolean {
    return beatNumber !== null || isStartPosition;
}

/**
 * Determines if the pictograph should show motion components
 *
 * @param state The current state of the pictograph
 * @returns True if motion components should be shown
 */
export function shouldShowMotionComponents(state: string): boolean {
    return state !== 'grid_only' && state !== 'initializing' && state !== 'error';
}

/**
 * Determines if the pictograph should show loading indicators
 *
 * @param state The current state of the pictograph
 * @param showLoadingIndicator Whether loading indicators are enabled
 * @returns True if loading indicators should be shown
 */
export function shouldShowLoadingIndicator(state: string, showLoadingIndicator: boolean): boolean {
    return (state === 'initializing' || state === 'loading') && showLoadingIndicator;
}

/**
 * Determines if the pictograph should show debug information
 *
 * @param debug Whether debug mode is enabled
 * @returns True if debug information should be shown
 */
export function shouldShowDebugInfo(debug: boolean): boolean {
    return debug;
}

/**
 * Gets the appropriate ARIA role for the pictograph
 *
 * @param onClick The click handler, if any
 * @returns The ARIA role ('button' or 'img')
 */
export function getPictographRole(onClick: (() => void) | undefined): string {
    return onClick ? 'button' : 'img';
}

/**
 * Gets the appropriate HTML element for the pictograph
 *
 * @param onClick The click handler, if any
 * @returns The HTML element name ('button' or 'div')
 */
export function getPictographElement(onClick: (() => void) | undefined): string {
    return onClick ? 'button' : 'div';
}
