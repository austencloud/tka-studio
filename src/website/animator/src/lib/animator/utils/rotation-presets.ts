/**
 * Preset rotation values and helper functions for common rotation patterns
 */

import type { PropAttributes } from '../types/core.js';
import { setManualRotationDegrees } from './manual-rotation.js';

/**
 * Common rotation presets in degrees
 */
export const ROTATION_PRESETS = {
	// No rotation
	STATIC: { start: 0, end: 0 },

	// Quarter turns (90 degrees)
	QUARTER_CW: { start: 0, end: 90 },
	QUARTER_CCW: { start: 0, end: -90 },

	// Half turns (180 degrees)
	HALF_CW: { start: 0, end: 180 },
	HALF_CCW: { start: 0, end: -180 },

	// Full turns (360 degrees)
	FULL_CW: { start: 0, end: 360 },
	FULL_CCW: { start: 0, end: -360 },

	// Pro isolation (90 degrees matching hand direction)
	PRO_ISOLATION_CW: { start: 0, end: 90 },
	PRO_ISOLATION_CCW: { start: 0, end: -90 },

	// Float (no rotation behavior)
	FLOAT: { start: 0, end: 0 },

	// Common orientations
	HORIZONTAL: { start: 0, end: 0 },
	VERTICAL: { start: 90, end: 90 },
	DIAGONAL_UP: { start: 45, end: 45 },
	DIAGONAL_DOWN: { start: -45, end: -45 }
} as const;

/**
 * Apply a rotation preset to prop attributes
 */
export function applyRotationPreset(
	attributes: PropAttributes,
	preset: keyof typeof ROTATION_PRESETS,
	direction: 'cw' | 'ccw' | 'shortest' = 'shortest'
): PropAttributes {
	const rotation = ROTATION_PRESETS[preset];
	return setManualRotationDegrees(attributes, rotation.start, rotation.end, direction);
}

/**
 * Create manual rotation for specific motion types with common patterns
 */
export const MOTION_TYPE_PRESETS = {
	/**
	 * Pro motion with 0 turns - 90 degree isolation
	 */
	pro_isolation_cw: (attributes: PropAttributes) =>
		setManualRotationDegrees(attributes, 0, 90, 'cw'),

	pro_isolation_ccw: (attributes: PropAttributes) =>
		setManualRotationDegrees(attributes, 0, -90, 'ccw'),

	/**
	 * Float motion - no rotation
	 */
	float_no_rotation: (attributes: PropAttributes) =>
		setManualRotationDegrees(attributes, 0, 0, 'shortest'),

	/**
	 * Static motion - maintain orientation
	 */
	static_horizontal: (attributes: PropAttributes) =>
		setManualRotationDegrees(attributes, 0, 0, 'shortest'),

	static_vertical: (attributes: PropAttributes) =>
		setManualRotationDegrees(attributes, 90, 90, 'shortest'),

	/**
	 * Custom turn amounts
	 */
	one_turn_cw: (attributes: PropAttributes) => setManualRotationDegrees(attributes, 0, 360, 'cw'),

	one_turn_ccw: (attributes: PropAttributes) =>
		setManualRotationDegrees(attributes, 0, -360, 'ccw'),

	two_turns_cw: (attributes: PropAttributes) => setManualRotationDegrees(attributes, 0, 720, 'cw'),

	two_turns_ccw: (attributes: PropAttributes) =>
		setManualRotationDegrees(attributes, 0, -720, 'ccw')
} as const;

/**
 * Quick helper to set custom rotation in degrees
 */
export function setCustomRotation(
	attributes: PropAttributes,
	startDegrees: number,
	endDegrees: number,
	direction: 'cw' | 'ccw' | 'shortest' = 'shortest'
): PropAttributes {
	return setManualRotationDegrees(attributes, startDegrees, endDegrees, direction);
}

/**
 * Helper to create a sequence step with manual rotation
 */
export function createStepWithManualRotation(
	beat: number,
	blueRotation: { start: number; end: number; direction?: 'cw' | 'ccw' | 'shortest' },
	redRotation: { start: number; end: number; direction?: 'cw' | 'ccw' | 'shortest' },
	baseBlueAttrs: Partial<PropAttributes> = {},
	baseRedAttrs: Partial<PropAttributes> = {}
) {
	const defaultAttrs: PropAttributes = {
		start_loc: 's',
		end_loc: 's',
		start_ori: 'in',
		end_ori: 'in',
		prop_rot_dir: 'no_rot',
		turns: 0,
		motion_type: 'static'
	};

	return {
		beat,
		blue_attributes: setManualRotationDegrees(
			{ ...defaultAttrs, ...baseBlueAttrs },
			blueRotation.start,
			blueRotation.end,
			blueRotation.direction || 'shortest'
		),
		red_attributes: setManualRotationDegrees(
			{ ...defaultAttrs, ...baseRedAttrs },
			redRotation.start,
			redRotation.end,
			redRotation.direction || 'shortest'
		)
	};
}

/**
 * Batch apply manual rotations to multiple steps
 */
export function applyManualRotationsToSteps(
	steps: any[],
	rotationMap: {
		[beat: number]: {
			blue?: { start: number; end: number; direction?: 'cw' | 'ccw' | 'shortest' };
			red?: { start: number; end: number; direction?: 'cw' | 'ccw' | 'shortest' };
		};
	}
): any[] {
	return steps.map((step) => {
		const rotation = rotationMap[step.beat];
		if (!rotation) {return step;}

		const updatedStep = { ...step };

		if (rotation.blue) {
			updatedStep.blue_attributes = setManualRotationDegrees(
				step.blue_attributes,
				rotation.blue.start,
				rotation.blue.end,
				rotation.blue.direction || 'shortest'
			);
		}

		if (rotation.red) {
			updatedStep.red_attributes = setManualRotationDegrees(
				step.red_attributes,
				rotation.red.start,
				rotation.red.end,
				rotation.red.direction || 'shortest'
			);
		}

		return updatedStep;
	});
}
