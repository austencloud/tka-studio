/**
 * Pictograph Lifecycle Manager
 *
 * This module provides lifecycle management functionality for the Pictograph component.
 */

import type { Writable } from 'svelte/store';
import { get } from 'svelte/store';
import type { PictographData } from '$lib/types/PictographData';
import type { PictographDataSnapshot } from '../utils/dataComparison';
import { createDataSnapshot } from '../utils/dataComparison';
import { logger } from '$lib/core/logging';
import type { PictographService } from '../PictographService';
import { hasRequiredMotionData } from './PictographLoadingManager';

/**
 * Context for component initialization
 */
export interface InitializationContext {
    pictographDataStore: Writable<PictographData>;
    service: Writable<PictographService | null>;
    state: Writable<string>;
    lastDataSnapshot: Writable<PictographDataSnapshot | null>;
    initializePictographService: (pictographDataStore: Writable<PictographData>) => PictographService;
    handleError: (source: string, error: any) => void;
}

/**
 * Initializes the pictograph component
 *
 * @param context The initialization context
 * @param debug Whether debug mode is enabled
 * @returns Performance metrics for the initialization
 */
export function initializePictograph(
    context: InitializationContext,
    debug: boolean
): { initTime: number } {
    const startTime = performance.now();

    try {
        // Make sure we have data to work with
        if (!get(context.pictographDataStore)) {
            logger.warn('Pictograph: No data available for initialization');
            return { initTime: 0 };
        }

        // Log component initialization
        logger.info('Pictograph component initializing', {
            data: {
                debug,
                hasMotionData: hasRequiredMotionData(get(context.pictographDataStore)),
                letter: get(context.pictographDataStore)?.letter,
                gridMode: get(context.pictographDataStore)?.gridMode
            }
        });

        // Initialize the service
        const service = context.initializePictographService(context.pictographDataStore);
        context.service.set(service);

        // Initialize data snapshot
        context.lastDataSnapshot.set(createDataSnapshot(get(context.pictographDataStore)));

        // Set initial state based on available motion data
        if (hasRequiredMotionData(get(context.pictographDataStore))) {
            context.state.set('loading');
            logger.debug('Pictograph: Motion data available, entering loading state', {
                data: {
                    redMotionData: get(context.pictographDataStore)?.redMotionData ? true : false,
                    blueMotionData: get(context.pictographDataStore)?.blueMotionData ? true : false
                }
            });
        } else {
            context.state.set('grid_only');
            logger.debug('Pictograph: No motion data, entering grid-only state');
        }

        const initTime = performance.now() - startTime;
        logger.info(`Pictograph initialized in ${initTime.toFixed(2)}ms`, {
            duration: initTime,
            data: {
                state: get(context.state),
                letter: get(context.pictographDataStore)?.letter,
                gridMode: get(context.pictographDataStore)?.gridMode
            }
        });

        return { initTime };
    } catch (error) {
        context.handleError('initialization', error);
        return { initTime: performance.now() - startTime };
    }
}

/**
 * Creates a cleanup function for the pictograph component
 *
 * @param loadedComponents The set of loaded components to clear
 * @param unsubscribe The function to unsubscribe from the data store
 * @returns A cleanup function
 */
export function createCleanupFunction(
    loadedComponents: Set<string>,
    unsubscribe: () => void
): () => void {
    return () => {
        loadedComponents.clear();
        unsubscribe();
        logger.debug('Pictograph component unmounting');
    };
}

/**
 * Creates a context for pictograph initialization
 *
 * @param pictographDataStore The pictograph data store
 * @param service The pictograph service
 * @param state The current state
 * @param lastDataSnapshot The last data snapshot
 * @param initializePictographService Function to initialize the pictograph service
 * @param handleError Function to handle errors
 * @returns An initialization context
 */
export function createInitializationContext(
    pictographDataStore: Writable<PictographData>,
    service: Writable<PictographService | null>,
    state: Writable<string>,
    lastDataSnapshot: Writable<PictographDataSnapshot | null>,
    initializePictographService: (pictographDataStore: Writable<PictographData>) => PictographService,
    handleError: (source: string, error: any) => void
): InitializationContext {
    return {
        pictographDataStore,
        service,
        state,
        lastDataSnapshot,
        initializePictographService,
        handleError
    };
}
