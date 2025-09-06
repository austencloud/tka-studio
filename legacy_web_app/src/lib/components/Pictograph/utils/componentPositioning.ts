// src/lib/components/Pictograph/utils/componentPositioning.ts
import type { PictographData } from '$lib/types/PictographData';
import type { PropData } from '../../objects/Prop/PropData';
import type { ArrowData } from '../../objects/Arrow/ArrowData';
import type { GridData } from '../../objects/Grid/GridData';
import type { MotionData } from '../../objects/Motion/MotionData';
import { logger } from '$lib/core/logging';
import type { PictographService } from '../PictographService';

/**
 * Creates and positions all components based on the pictograph data
 *
 * @param pictographData The current pictograph data
 * @param service The PictographService instance
 * @param gridData The grid data for positioning
 * @param state Current component state information
 * @returns Object containing created component data
 */
export function createAndPositionComponents(
	pictographData: PictographData,
	service: PictographService,
	gridData: GridData | null,
	state: {
		requiredComponents: string[];
		totalComponentsToLoad: number;
	}
): {
	redPropData: PropData | null;
	bluePropData: PropData | null;
	redArrowData: ArrowData | null;
	blueArrowData: ArrowData | null;
} {
	try {
		// Initialize required components
		state.requiredComponents = ['grid'];

		// Don't reset total components to load since we may already have loaded some
		if (state.totalComponentsToLoad === 0) state.totalComponentsToLoad = 1;

		// Initialize component data
		let redPropData: PropData | null = null;
		let bluePropData: PropData | null = null;
		let redArrowData: ArrowData | null = null;
		let blueArrowData: ArrowData | null = null;

		// Create red components if needed
		if (pictographData.redMotionData) {
			try {
				const redMotionData = pictographData.redMotionData as MotionData;
				redPropData = service.createPropData(redMotionData, 'red');
				redArrowData = service.createArrowData(redMotionData, 'red');

				if (!state.requiredComponents.includes('redProp')) {
					state.requiredComponents.push('redProp', 'redArrow');
					state.totalComponentsToLoad += 2;
				}

				logger.debug('Created red components', {
					redPropData,
					redArrowData,
					redMotionData: {
						id: redMotionData.id,
						motionType: redMotionData.motionType,
						startLoc: redMotionData.startLoc,
						endLoc: redMotionData.endLoc
					}
				});
			} catch (redError) {
				logger.error('Error creating red components', {
					error: redError instanceof Error ? redError : new Error(String(redError))
				});
			}
		}

		// Create blue components if needed
		if (pictographData.blueMotionData) {
			try {
				const blueMotionData = pictographData.blueMotionData as MotionData;
				bluePropData = service.createPropData(blueMotionData, 'blue');
				blueArrowData = service.createArrowData(blueMotionData, 'blue');

				if (!state.requiredComponents.includes('blueProp')) {
					state.requiredComponents.push('blueProp', 'blueArrow');
					state.totalComponentsToLoad += 2;
				}

				logger.debug('Created blue components', {
					bluePropData,
					blueArrowData,
					blueMotionData: {
						id: blueMotionData.id,
						motionType: blueMotionData.motionType,
						startLoc: blueMotionData.startLoc,
						endLoc: blueMotionData.endLoc
					}
				});
			} catch (blueError) {
				logger.error('Error creating blue components', {
					error: blueError instanceof Error ? blueError : new Error(String(blueError))
				});
			}
		}

		// Position components if grid data is available
		if (gridData) {
			try {
				service.positionComponents(
					redPropData,
					bluePropData,
					redArrowData,
					blueArrowData,
					gridData
				);

				logger.debug('Positioned components', {
					redPropCoords: redPropData?.coords,
					bluePropCoords: bluePropData?.coords,
					redArrowCoords: redArrowData?.coords,
					blueArrowCoords: blueArrowData?.coords
				});
			} catch (positionError) {
				logger.error('Error positioning components', {
					error: positionError instanceof Error ? positionError : new Error(String(positionError))
				});
			}
		}

		return {
			redPropData,
			bluePropData,
			redArrowData,
			blueArrowData
		};
	} catch (error) {
		logger.error('Error in createAndPositionComponents', {
			error: error instanceof Error ? error : new Error(String(error)),
			data: {
				letter: pictographData?.letter,
				gridMode: pictographData?.gridMode
			}
		});

		// Return empty components on error
		return {
			redPropData: null,
			bluePropData: null,
			redArrowData: null,
			blueArrowData: null
		};
	}
}

/**
 * Generates an ARIA label for the pictograph based on its current state
 *
 * @param state The current state of the pictograph ('error', 'complete', etc.)
 * @param errorMessage The current error message, if any
 * @param pictographData The current pictograph data
 * @returns An appropriate ARIA label string
 */
export function getPictographAriaLabel(
	state: string,
	errorMessage: string | null,
	pictographData?: PictographData
): string {
	if (state === 'error') return `Pictograph error: ${errorMessage}`;

	const letterPart = pictographData?.letter ? `for letter ${pictographData.letter}` : '';

	const statePart = state === 'complete' ? 'complete' : 'loading';

	return `Pictograph visualization ${letterPart} - ${statePart}`;
}
