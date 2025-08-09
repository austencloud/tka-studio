/**
 * Arrow Positioning Service
 *
 * Implements the arrow positioning pipeline from the desktop app:
 * 1. Initial position (from grid coordinates)
 * 2. Default adjustments
 * 3. Special placements (letter-specific)
 * 4. Directional adjustments
 * 5. Final positioning
 */

export interface ArrowPositioningInput {
	arrow_type: 'blue' | 'red';
	motion_type: string;
	location: string;
	grid_mode: string;
	turns: number;
	letter?: string;
	start_orientation?: string;
	end_orientation?: string;
}

export interface Position {
	x: number;
	y: number;
}

export class ArrowPositioningService {
	private readonly SCENE_SIZE = 950;
	private readonly CENTER_X = 475;
	private readonly CENTER_Y = 475;

	/**
	 * Calculate the final position for an arrow based on all factors
	 */
	calculatePosition(input: ArrowPositioningInput): Position {
		// Step 1: Get initial position from grid coordinates
		const initialPosition = this.getInitialPosition(input);

		// Step 2: Get default adjustments
		const defaultAdjustment = this.getDefaultAdjustment(input);

		// Step 3: Apply special placements (simplified for now)
		const specialAdjustment = this.getSpecialAdjustment(input);

		// Step 4: Get directional adjustments
		const directionalAdjustment = this.getDirectionalAdjustment(input);

		// Step 5: Combine all adjustments
		const finalX =
			initialPosition.x + defaultAdjustment.x + specialAdjustment.x + directionalAdjustment.x;
		const finalY =
			initialPosition.y + defaultAdjustment.y + specialAdjustment.y + directionalAdjustment.y;

		return { x: finalX, y: finalY };
	}

	/**
	 * Get initial position based on motion type and location
	 */
	private getInitialPosition(input: ArrowPositioningInput): Position {
		const { motion_type, location, grid_mode } = input;

		// For PRO/ANTI/FLOAT - use shift coordinates (layer2 points)
		if (['pro', 'anti', 'float'].includes(motion_type)) {
			return this.getShiftCoordinates(location, grid_mode);
		}

		// For STATIC/DASH - use hand points
		if (['static', 'dash'].includes(motion_type)) {
			return this.getHandCoordinates(location, grid_mode);
		}

		// Default to center
		return { x: this.CENTER_X, y: this.CENTER_Y };
	}

	/**
	 * Get shift coordinates for PRO/ANTI/FLOAT motions
	 * These are the layer2 points where arrows are positioned
	 */
	private getShiftCoordinates(location: string, grid_mode: string): Position {
		// Base coordinates for diamond grid layer2 points
		// These are estimated positions - ideally we'd load from data files
		const diamondLayer2Points: Record<string, Position> = {
			n: { x: 475, y: 200 },
			ne: { x: 625, y: 275 },
			e: { x: 700, y: 475 },
			se: { x: 625, y: 675 },
			s: { x: 475, y: 750 },
			sw: { x: 325, y: 675 },
			w: { x: 250, y: 475 },
			nw: { x: 325, y: 275 },
		};

		const boxLayer2Points: Record<string, Position> = {
			n: { x: 475, y: 225 },
			ne: { x: 600, y: 300 },
			e: { x: 675, y: 475 },
			se: { x: 600, y: 650 },
			s: { x: 475, y: 725 },
			sw: { x: 350, y: 650 },
			w: { x: 275, y: 475 },
			nw: { x: 350, y: 300 },
		};

		const points = grid_mode === 'box' ? boxLayer2Points : diamondLayer2Points;
		return points[location] || { x: this.CENTER_X, y: this.CENTER_Y };
	}

	/**
	 * Get hand coordinates for STATIC/DASH motions
	 * These are where props are positioned
	 */
	private getHandCoordinates(location: string, grid_mode: string): Position {
		// Base coordinates for diamond grid hand points
		const diamondHandPoints: Record<string, Position> = {
			n: { x: 475, y: 175 },
			ne: { x: 650, y: 250 },
			e: { x: 725, y: 475 },
			se: { x: 650, y: 700 },
			s: { x: 475, y: 775 },
			sw: { x: 300, y: 700 },
			w: { x: 225, y: 475 },
			nw: { x: 300, y: 250 },
		};

		const boxHandPoints: Record<string, Position> = {
			n: { x: 475, y: 200 },
			ne: { x: 625, y: 275 },
			e: { x: 700, y: 475 },
			se: { x: 625, y: 675 },
			s: { x: 475, y: 750 },
			sw: { x: 325, y: 675 },
			w: { x: 250, y: 475 },
			nw: { x: 325, y: 275 },
		};

		const points = grid_mode === 'box' ? boxHandPoints : diamondHandPoints;
		return points[location] || { x: this.CENTER_X, y: this.CENTER_Y };
	}

	/**
	 * Get default adjustment based on motion type and turns
	 */
	private getDefaultAdjustment(input: ArrowPositioningInput): Position {
		const { motion_type, turns, location } = input;

		// Basic default adjustments based on motion type and turns
		// This is a simplified version - the real system has complex lookup tables
		const adjustmentMap: Record<string, Record<string, Position>> = {
			pro: {
				'0': { x: 0, y: 25 },
				'0.5': { x: 15, y: 55 },
				'1': { x: -85, y: 80 },
				'1.5': { x: 10, y: 15 },
				'2': { x: -70, y: 15 },
				'2.5': { x: 20, y: 30 },
				'3': { x: -70, y: 50 },
			},
			anti: {
				'0': { x: 0, y: -25 },
				'0.5': { x: -15, y: -55 },
				'1': { x: 85, y: -80 },
				'1.5': { x: -10, y: -15 },
				'2': { x: 70, y: -15 },
				'2.5': { x: -20, y: -30 },
				'3': { x: 70, y: -50 },
			},
			float: {
				'0': { x: 5, y: 5 },
				'0.5': { x: 5, y: 5 },
				'1': { x: 5, y: 5 },
				'1.5': { x: 5, y: 5 },
				'2': { x: 5, y: 5 },
				'2.5': { x: 5, y: 5 },
				'3': { x: 5, y: 5 },
			},
		};

		const turnsKey = turns.toString();
		const motionAdjustments = adjustmentMap[motion_type] || {};
		return motionAdjustments[turnsKey] || { x: 0, y: 0 };
	}

	/**
	 * Get special adjustment for specific letters (simplified)
	 */
	private getSpecialAdjustment(input: ArrowPositioningInput): Position {
		// This would normally load from special placement JSON files
		// For now, return zero adjustment
		return { x: 0, y: 0 };
	}

	/**
	 * Get directional adjustment based on quadrant and motion type
	 */
	private getDirectionalAdjustment(input: ArrowPositioningInput): Position {
		const { motion_type, location } = input;

		// Simplified directional adjustments
		// The real system uses complex directional tuple generators
		const directionalAdjustments: Record<string, Record<string, Position>> = {
			pro: {
				n: { x: 0, y: -10 },
				ne: { x: 10, y: -10 },
				e: { x: 10, y: 0 },
				se: { x: 10, y: 10 },
				s: { x: 0, y: 10 },
				sw: { x: -10, y: 10 },
				w: { x: -10, y: 0 },
				nw: { x: -10, y: -10 },
			},
			anti: {
				n: { x: 0, y: 10 },
				ne: { x: -10, y: 10 },
				e: { x: -10, y: 0 },
				se: { x: -10, y: -10 },
				s: { x: 0, y: -10 },
				sw: { x: 10, y: -10 },
				w: { x: 10, y: 0 },
				nw: { x: 10, y: 10 },
			},
		};

		const motionAdjustments = directionalAdjustments[motion_type] || {};
		return motionAdjustments[location] || { x: 0, y: 0 };
	}
}

// Create singleton instance
export const arrowPositioningService = new ArrowPositioningService();
