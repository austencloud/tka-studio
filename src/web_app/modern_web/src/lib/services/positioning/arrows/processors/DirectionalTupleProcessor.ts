/**
 * Directionexport interface IDirectionalTupleService {
	calculateDirectionalTuple(_motion: MotionData, location: Location): [number, number];
	generateDirectionalTuples(
		_motion: MotionData,
		baseX: number,
		baseY: number
	): Array<[number, number]>;
} Processor
 *
 * Handles complex directional tuple processing for arrow positioning adjustments.
 * Direct TypeScript port of the Python DirectionalTupleProcessor.
 *
 * This service handles:
 * - Directional tuple generation based on motion data
 * - Quadrant index calculation for proper tuple selection
 * - Complex adjustment processing for different motion types
 */

import type { MotionData } from '$lib/domain';
import { Location } from '$lib/domain';
import type { Point } from '../../interfaces';

export interface IDirectionalTupleCalculator {
	calculateDirectionalTuple(motion: MotionData, location: Location): [number, number];
	generateDirectionalTuples(
		motion: MotionData,
		baseX: number,
		baseY: number
	): Array<[number, number]>;
}

export interface IQuadrantIndexCalculator {
	calculateQuadrantIndex(location: Location): number;
}

export interface IDirectionalTupleProcessor {
	processDirectionalTuples(baseAdjustment: Point, _motion: MotionData, location: Location): Point;
}

export class DirectionalTupleCalculator implements IDirectionalTupleCalculator {
	/**
	 * Calculator for directional tuples used in arrow positioning.
	 */

	calculateDirectionalTuple(_motion: MotionData, location: Location): [number, number] {
		/**
		 * Calculate directional tuple for arrow positioning.
		 *
		 * Args:
		 *     motion: Motion data containing type and rotation direction
		 *     location: Arrow location
		 *
		 * Returns:
		 *     Tuple of [x_offset, y_offset] directional adjustments
		 */
		// This is a simplified implementation
		// In the full version, this would use complex directional calculations
		const motionType = _motion.motion_type?.toLowerCase();
		const rotationDir = _motion.prop_rot_dir?.toLowerCase();

		// Basic directional adjustments based on motion type and rotation
		let baseX = 0;
		let baseY = 0;

		if (motionType === 'pro') {
			if (rotationDir === 'clockwise' || rotationDir === 'cw') {
				baseX = 1;
				baseY = 0;
			} else {
				baseX = -1;
				baseY = 0;
			}
		} else if (motionType === 'anti') {
			if (rotationDir === 'clockwise' || rotationDir === 'cw') {
				baseX = -1;
				baseY = 0;
			} else {
				baseX = 1;
				baseY = 0;
			}
		}

		// Apply location-based adjustments
		const locationMultiplier = this.getLocationMultiplier(location);
		return [baseX * locationMultiplier.x, baseY * locationMultiplier.y];
	}

	generateDirectionalTuples(
		_motion: MotionData,
		baseX: number,
		baseY: number
	): Array<[number, number]> {
		/**
		 * Generate directional tuples for the given motion and base adjustment.
		 *
		 * Args:
		 *     motion: Motion data containing type, rotation, and location info
		 *     baseX: Base X adjustment value
		 *     baseY: Base Y adjustment value
		 *
		 * Returns:
		 *     Array of 4 directional tuples representing rotated adjustments
		 */
		const tuples: Array<[number, number]> = [];

		// Generate 4 rotational variants of the base adjustment
		// This implements the 4-tuple rotation logic from the reference
		for (let i = 0; i < 4; i++) {
			const angle = (i * 90 * Math.PI) / 180; // Convert to radians
			const cos = Math.cos(angle);
			const sin = Math.sin(angle);

			// Apply rotation matrix
			const rotatedX = baseX * cos - baseY * sin;
			const rotatedY = baseX * sin + baseY * cos;

			tuples.push([Math.round(rotatedX), Math.round(rotatedY)]);
		}

		return tuples;
	}

	private getLocationMultiplier(location: Location): { x: number; y: number } {
		/**Get location-based multiplier for directional adjustments.*/
		const multipliers: Record<Location, { x: number; y: number }> = {
			[Location.NORTH]: { x: 0, y: -1 },
			[Location.NORTHEAST]: { x: 1, y: -1 },
			[Location.EAST]: { x: 1, y: 0 },
			[Location.SOUTHEAST]: { x: 1, y: 1 },
			[Location.SOUTH]: { x: 0, y: 1 },
			[Location.SOUTHWEST]: { x: -1, y: 1 },
			[Location.WEST]: { x: -1, y: 0 },
			[Location.NORTHWEST]: { x: -1, y: -1 },
		};

		return multipliers[location] || { x: 0, y: 0 };
	}
}

export class QuadrantIndexCalculator implements IQuadrantIndexCalculator {
	/**
	 * Calculator for quadrant indices used in directional tuple selection.
	 */

	calculateQuadrantIndex(location: Location): number {
		/**
		 * Calculate quadrant index for the given location.
		 *
		 * Args:
		 *     location: Arrow location
		 *
		 * Returns:
		 *     Quadrant index (0-3)
		 */
		const quadrantMap: Record<Location, number> = {
			[Location.NORTHEAST]: 0,
			[Location.SOUTHEAST]: 1,
			[Location.SOUTHWEST]: 2,
			[Location.NORTHWEST]: 3,
			// Cardinal directions map to nearest quadrant
			[Location.NORTH]: 0, // Maps to NE quadrant
			[Location.EAST]: 1, // Maps to SE quadrant
			[Location.SOUTH]: 2, // Maps to SW quadrant
			[Location.WEST]: 3, // Maps to NW quadrant
		};

		return quadrantMap[location] || 0;
	}
}

export class DirectionalTupleProcessor implements IDirectionalTupleProcessor {
	/**
	 * Processor for applying directional tuple adjustments to arrow positioning.
	 */

	constructor(
		private directionalTupleService: IDirectionalTupleCalculator,
		private quadrantIndexService: IQuadrantIndexCalculator
	) {}

	processDirectionalTuples(
		baseAdjustment: Point,
		_motion: MotionData,
		location: Location
	): Point {
		/**
		 * Process directional tuples to calculate final adjustment.
		 *
		 * Args:
		 *     baseAdjustment: Base adjustment from placement services
		 *     motion: Motion data for directional calculations
		 *     location: Arrow location for quadrant selection
		 *
		 * Returns:
		 *     Final adjustment point after directional processing
		 */
		try {
			// Generate directional tuples from base adjustment
			const directionalTuples = this.directionalTupleService.generateDirectionalTuples(
				_motion,
				baseAdjustment.x,
				baseAdjustment.y
			);

			// Calculate quadrant index for tuple selection
			const quadrantIndex = this.quadrantIndexService.calculateQuadrantIndex(location);

			// Select the appropriate tuple based on quadrant
			const selectedTuple = directionalTuples[quadrantIndex] || [0, 0];

			// Calculate directional tuple for additional adjustments
			const directionalTuple = this.directionalTupleService.calculateDirectionalTuple(
				_motion,
				location
			);

			// Combine base adjustment, selected tuple, and directional tuple
			const finalX = baseAdjustment.x + selectedTuple[0] + directionalTuple[0];
			const finalY = baseAdjustment.y + selectedTuple[1] + directionalTuple[1];

			return { x: finalX, y: finalY };
		} catch (error) {
			console.warn('Directional tuple processing failed, using base adjustment:', error);
			return baseAdjustment;
		}
	}
}
