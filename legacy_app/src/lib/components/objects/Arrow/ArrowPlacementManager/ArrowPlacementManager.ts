// src/lib/components/PlacementManagers/ArrowPlacementManager/ArrowPlacementManager.ts
import type { ArrowData } from '$lib/components/objects/Arrow/ArrowData';
import type { ArrowPlacementConfig, Coordinates } from './types';
import { getInitialPosition } from './utils/positionCalculator';
import { calculateAdjustment } from './utils/adjustmentCalculator';

/**
 * Main manager class that handles arrow placement calculations.
 * This class coordinates the initial position and adjustment calculations
 * for arrows in a pictograph, including handling mirrored arrows correctly.
 */
export class ArrowPlacementManager {
	private config: ArrowPlacementConfig;

	constructor(config: ArrowPlacementConfig) {
		const { gridData } = config;

		if (!gridData) {
			throw new Error('Grid data is required to initialize ArrowPlacementManager');
		}

		this.config = config;
	}

	/**
	 * Updates the position of all arrows based on their current properties
	 * and the pictograph configuration.
	 */
	public updateArrowPlacements(arrows: ArrowData[]): void {
		arrows.forEach(this.updateArrowPlacement.bind(this));
	}

	private updateArrowPlacement(arrow: ArrowData): void {
		// Get the initial position and adjustment
		const initialPos = getInitialPosition(arrow, this.config);
		const adjustment = calculateAdjustment(arrow, this.config);

		// Get SVG center coordinates
		const svgCenterX = arrow.svgData?.center?.x || arrow.svgCenter?.x || 0;
		const svgCenterY = arrow.svgData?.center?.y || arrow.svgCenter?.y || 0;

		// Log values for debugging
		if (arrow.loc == 'ne' && arrow.propRotDir == 'ccw' && arrow.motionType == 'pro') {

		}
		// Calculate final position accounting for mirroring
		if (arrow.svgMirrored) {
			// For mirrored arrows, apply the mirroring effect to the adjustment
			arrow.coords = {
				x: initialPos.x + adjustment.x - svgCenterX,
				y: initialPos.y + adjustment.y - svgCenterY
			};
		} else {
			// Standard positioning for normal arrows
			arrow.coords = {
				x: initialPos.x + adjustment.x - svgCenterX,
				y: initialPos.y + adjustment.y - svgCenterY
			};
		}

	}
}
