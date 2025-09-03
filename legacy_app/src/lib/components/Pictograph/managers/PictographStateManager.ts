/**
 * Pictograph State Manager
 *
 * This module provides state management functionality for the Pictograph component.
 */

import { writable, get, type Writable } from 'svelte/store';
import type { PictographData } from '$lib/types/PictographData';
import { defaultPictographData } from '../utils/defaultPictographData';
import { createDataSnapshot, hasDataChanged, type PictographDataSnapshot } from '../utils/dataComparison';
import { logger } from '$lib/core/logging';
import { PictographService } from '../PictographService';

/**
 * Creates a pictograph data store with the provided initial data
 *
 * @param initialData The initial pictograph data
 * @returns A writable store containing the pictograph data
 */
export function createPictographDataStore(initialData?: PictographData): Writable<PictographData> {
    return writable(initialData || defaultPictographData);
}

/**
 * Initializes the pictograph service with the current data
 *
 * @param pictographDataStore The pictograph data store
 * @returns The initialized pictograph service
 */
export function initializePictographService(pictographDataStore: Writable<PictographData>): PictographService {
    return new PictographService(get(pictographDataStore));
}

/**
 * Checks if the pictograph data has changed
 *
 * @param newData The new pictograph data
 * @param lastDataSnapshot The last data snapshot for comparison
 * @returns True if the data has changed, along with the updated snapshot
 */
export function checkForDataChanges(
    newData: PictographData,
    lastDataSnapshot: PictographDataSnapshot | null
): { hasChanged: boolean; updatedSnapshot: PictographDataSnapshot } {
    // If this is the first time, always return true
    if (!lastDataSnapshot) {
        // Update last known values for safe comparison next time
        const updatedSnapshot = createDataSnapshot(newData);
        return { hasChanged: true, updatedSnapshot };
    }

    try {
        // Use the utility function to check for changes
        const fieldsChanged = hasDataChanged(newData, lastDataSnapshot);

        // Create updated snapshot if changed
        const updatedSnapshot = fieldsChanged
            ? createDataSnapshot(newData)
            : lastDataSnapshot;

        return { hasChanged: fieldsChanged, updatedSnapshot };
    } catch (error) {
        logger.warn('Error comparing pictograph data:', {
            error: error instanceof Error ? error : new Error(String(error))
        });
        // Assume changed on error to be safe
        return { hasChanged: true, updatedSnapshot: createDataSnapshot(newData) };
    }
}

/**
 * Updates the pictograph components based on the current data
 *
 * @param pictographDataStore The pictograph data store
 * @param service The pictograph service
 * @param state The current state
 * @param errorMessage The current error message
 * @param gridData The current grid data
 * @param createAndPositionComponents Function to create and position components
 * @param requiredComponents Array of required component names
 * @param hasRequiredMotionData Function to check if the data has required motion data
 * @returns Updated state information
 */
export function updateComponentsFromData(
    pictographDataStore: Writable<PictographData>,
    service: PictographService | null,
    state: string,
    errorMessage: string | null,
    gridData: any,
    createAndPositionComponents: () => void,
    requiredComponents: string[],
    loadedComponents: Set<string>,
    hasRequiredMotionData: (data: PictographData | undefined) => boolean
): { state: string; errorMessage: string | null; renderCount: number } {
    try {
        // Reset state if needed
        let newState = state;
        let newErrorMessage = errorMessage;
        let renderCount = 0;

        if (state === 'error') {
            newState = 'loading';
            newErrorMessage = null;
        }

        // Make sure we have data to work with
        if (!get(pictographDataStore)) {
            newState = 'grid_only';
            return { state: newState, errorMessage: newErrorMessage, renderCount };
        }

        // Update state based on available motion data
        if (hasRequiredMotionData(get(pictographDataStore))) {
            if (state === 'grid_only') newState = 'loading';
        } else {
            newState = 'grid_only';
        }

        // Only recreate components if grid data is available
        if (gridData) {
            // Create and position components
            createAndPositionComponents();

            // Update rendering count
            renderCount++;

            // If all required components were already loaded previously,
            // mark as complete immediately
            if (requiredComponents.every((comp) => loadedComponents.has(comp))) {
                newState = 'complete';
            }
        }

        return { state: newState, errorMessage: newErrorMessage, renderCount };
    } catch (error) {
        logger.error('Error updating components from data:', {
            error: error instanceof Error ? error : new Error(String(error))
        });
        return { state: 'error', errorMessage: String(error), renderCount: 0 };
    }
}

/**
 * Sets up a subscription to the pictograph data store
 *
 * @param pictographDataStore The pictograph data store
 * @param service The pictograph service
 * @param lastDataSnapshot The last data snapshot for comparison
 * @param updateComponentsFromData Function to update components from data
 * @param dispatch Function to dispatch events
 * @param debug Whether debug mode is enabled
 * @returns A function to unsubscribe from the store
 */
export function setupPictographDataSubscription(
    pictographDataStore: Writable<PictographData>,
    service: PictographService | null,
    lastDataSnapshot: PictographDataSnapshot | null,
    updateComponentsFn: () => void,
    dispatch: (event: string, detail?: any) => void,
    debug: boolean,
    checkForChanges: (data: PictographData, snapshot: PictographDataSnapshot | null) => { hasChanged: boolean; updatedSnapshot: PictographDataSnapshot }
): { unsubscribe: () => void; getSnapshot: () => PictographDataSnapshot | null } {
    let currentSnapshot = lastDataSnapshot;

    const unsubscribe = pictographDataStore.subscribe((data) => {
        if (data && service) {
            // Use a safe comparison method that avoids circular references
            const { hasChanged, updatedSnapshot } = checkForChanges(data, currentSnapshot);
            currentSnapshot = updatedSnapshot;

            // Only process if there's a real change and service is initialized
            if (hasChanged) {
                if (debug) console.debug('Pictograph data changed, updating components');

                // Update the service with new data
                service.updateData(data);

                // Update local state
                updateComponentsFn();

                // Notify parent about the update
                dispatch('dataUpdated', { type: 'all' });
            }
        }
    });

    return {
        unsubscribe,
        getSnapshot: () => currentSnapshot
    };
}
