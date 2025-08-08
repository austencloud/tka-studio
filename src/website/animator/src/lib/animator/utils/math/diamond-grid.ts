/**
 * Diamond Grid Coordinate System
 * Maps position names to exact coordinates from the SVG specification
 */

import { ANIMATION_CONSTANTS } from '../../constants/animation.js';

export interface GridPoint {
	x: number;
	y: number;
	radius: number;
	id: string;
}

/**
 * Diamond grid points as defined in the SVG specification
 * All coordinates are from the 950x950 viewBox
 */
export const DIAMOND_GRID_POINTS: Record<string, GridPoint> = {
	// Outer diamond points (r=25)
	n: { x: 475, y: 175, radius: 25, id: 'n_diamond_outer_point' },
	e: { x: 775, y: 475, radius: 25, id: 'e_diamond_outer_point' },
	s: { x: 475, y: 775, radius: 25, id: 's_diamond_outer_point' },
	w: { x: 175, y: 475, radius: 25, id: 'w_diamond_outer_point' },

	// Hand points (r=8)
	n_hand: { x: 475, y: 331.9, radius: 8, id: 'n_diamond_hand_point' },
	e_hand: { x: 618.1, y: 475, radius: 8, id: 'e_diamond_hand_point' },
	s_hand: { x: 475, y: 618.1, radius: 8, id: 's_diamond_hand_point' },
	w_hand: { x: 331.9, y: 475, radius: 8, id: 'w_diamond_hand_point' },

	// Layer2 points (r=8.8)
	ne: { x: 618.1, y: 331.9, radius: 8.8, id: 'ne_diamond_layer2_point' },
	se: { x: 618.1, y: 618.1, radius: 8.8, id: 'se_diamond_layer2_point' },
	sw: { x: 331.9, y: 618.1, radius: 8.8, id: 'sw_diamond_layer2_point' },
	nw: { x: 331.9, y: 331.9, radius: 8.8, id: 'nw_diamond_layer2_point' },

	// Layer2 strict points (r=8.8)
	ne_strict: { x: 625, y: 325, radius: 8.8, id: 'ne_diamond_layer2_point_strict' },
	se_strict: { x: 625, y: 625, radius: 8.8, id: 'se_diamond_layer2_point_strict' },
	sw_strict: { x: 325, y: 625, radius: 8.8, id: 'sw_diamond_layer2_point_strict' },
	nw_strict: { x: 325, y: 325, radius: 8.8, id: 'nw_diamond_layer2_point_strict' },

	// Hand strict points (r=4.7)
	n_hand_strict: { x: 475, y: 325, radius: 4.7, id: 'n_diamond_hand_point_strict' },
	e_hand_strict: { x: 625, y: 475, radius: 4.7, id: 'e_diamond_hand_point_strict' },
	s_hand_strict: { x: 475, y: 625, radius: 4.7, id: 's_diamond_hand_point_strict' },
	w_hand_strict: { x: 325, y: 475, radius: 4.7, id: 'w_diamond_hand_point_strict' },

	// Center point (r=12)
	center: { x: 475, y: 475, radius: 12, id: 'center_point' }
};

/**
 * Convert diamond grid coordinates to canvas coordinates
 */
export function gridToCanvas(
	gridPoint: GridPoint,
	canvasWidth: number,
	canvasHeight: number
): { x: number; y: number } {
	const scaleX = canvasWidth / ANIMATION_CONSTANTS.GRID_VIEWBOX_SIZE;
	const scaleY = canvasHeight / ANIMATION_CONSTANTS.GRID_VIEWBOX_SIZE;

	return {
		x: gridPoint.x * scaleX,
		y: gridPoint.y * scaleY
	};
}

/**
 * Get grid point by position name
 */
export function getGridPoint(position: string): GridPoint | null {
	const normalizedPosition = position?.toLowerCase();
	return DIAMOND_GRID_POINTS[normalizedPosition] || null;
}

/**
 * Calculate angle from center to a grid point (for compatibility with existing angle-based system)
 */
export function gridPointToAngle(gridPoint: GridPoint): number {
	const centerX = ANIMATION_CONSTANTS.GRID_CENTER;
	const centerY = ANIMATION_CONSTANTS.GRID_CENTER;

	const deltaX = gridPoint.x - centerX;
	const deltaY = gridPoint.y - centerY;

	return Math.atan2(deltaY, deltaX);
}

/**
 * Map position name to coordinates (replaces angle-based system)
 */
export function mapPositionToCoordinates(position: string | undefined): { x: number; y: number } {
	if (!position) {return { x: ANIMATION_CONSTANTS.GRID_CENTER, y: ANIMATION_CONSTANTS.GRID_CENTER };}

	// Map cardinal directions to hand points for staff positioning
	const positionMapping: Record<string, string> = {
		n: 'n_hand',
		e: 'e_hand',
		s: 's_hand',
		w: 'w_hand'
	};

	const mappedPosition = positionMapping[position.toLowerCase()] || position.toLowerCase();
	const gridPoint = getGridPoint(mappedPosition);

	if (gridPoint) {
		return { x: gridPoint.x, y: gridPoint.y };
	}

	// Fallback to center if position not found
	return { x: ANIMATION_CONSTANTS.GRID_CENTER, y: ANIMATION_CONSTANTS.GRID_CENTER };
}

/**
 * Map position name to angle (updated for diamond grid) - kept for backward compatibility
 */
export function mapPositionToAngle(position: string | undefined): number {
	if (!position) {return 0;}

	// For cardinal directions, use hand points
	const positionMapping: Record<string, string> = {
		n: 'n_hand',
		e: 'e_hand',
		s: 's_hand',
		w: 'w_hand'
	};

	const mappedPosition = positionMapping[position.toLowerCase()] || position.toLowerCase();
	const gridPoint = getGridPoint(mappedPosition);

	if (gridPoint) {
		return gridPointToAngle(gridPoint);
	}

	// Fallback to legacy mapping for backward compatibility
	const legacyAngles: Record<string, number> = {
		e: 0,
		s: Math.PI / 2,
		w: Math.PI,
		n: -Math.PI / 2
	};

	return legacyAngles[position.toLowerCase()] || 0;
}

/**
 * Interpolate between two coordinate points
 */
export function lerpCoordinates(
	start: { x: number; y: number },
	end: { x: number; y: number },
	t: number
): { x: number; y: number } {
	return {
		x: start.x + (end.x - start.x) * t,
		y: start.y + (end.y - start.y) * t
	};
}

/**
 * Get all available position names
 */
export function getAvailablePositions(): string[] {
	return Object.keys(DIAMOND_GRID_POINTS);
}
