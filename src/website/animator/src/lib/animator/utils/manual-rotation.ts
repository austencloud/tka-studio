/**
 * Utilities for manual rotation input and conversion
 */

import type { PropAttributes } from '../types/core.js';
import { PI, TWO_PI } from './math/constants.js';
import { normalizeAnglePositive, normalizeAngleSigned } from './math/angles.js';

/**
 * Convert degrees to radians
 */
export function degreesToRadians(degrees: number): number {
	return (degrees * PI) / 180;
}

/**
 * Convert radians to degrees
 */
export function radiansToDegrees(radians: number): number {
	return (radians * 180) / PI;
}

/**
 * Helper function to set manual rotation values in degrees
 */
export function setManualRotationDegrees(
	attributes: PropAttributes,
	startDegrees: number,
	endDegrees: number,
	direction: 'cw' | 'ccw' | 'shortest' = 'shortest'
): PropAttributes {
	return {
		...attributes,
		manual_start_rotation: degreesToRadians(startDegrees),
		manual_end_rotation: degreesToRadians(endDegrees),
		manual_rotation_direction: direction
	};
}

/**
 * Helper function to set manual rotation values in radians
 */
export function setManualRotationRadians(
	attributes: PropAttributes,
	startRadians: number,
	endRadians: number,
	direction: 'cw' | 'ccw' | 'shortest' = 'shortest'
): PropAttributes {
	return {
		...attributes,
		manual_start_rotation: startRadians,
		manual_end_rotation: endRadians,
		manual_rotation_direction: direction
	};
}

/**
 * Calculate manual staff rotation based on manual rotation fields
 */
export function calculateManualStaffRotation(attributes: PropAttributes, t: number): number | null {
	// Return null if manual rotation is not specified
	if (
		attributes.manual_start_rotation === undefined ||
		attributes.manual_end_rotation === undefined
	) {
		return null;
	}

	const startAngle = attributes.manual_start_rotation;
	const endAngle = attributes.manual_end_rotation;
	const direction = attributes.manual_rotation_direction || 'shortest';

	// Calculate the rotation based on direction
	let totalRotation: number;

	switch (direction) {
		case 'cw':
			// Force clockwise rotation
			totalRotation = endAngle - startAngle;
			if (totalRotation <= 0) {
				totalRotation += TWO_PI;
			}
			break;

		case 'ccw':
			// Force counter-clockwise rotation
			totalRotation = endAngle - startAngle;
			if (totalRotation >= 0) {
				totalRotation -= TWO_PI;
			}
			break;

		case 'shortest':
		default:
			// Take the shortest path
			totalRotation = normalizeAngleSigned(endAngle - startAngle);
			break;
	}

	const currentAngle = startAngle + totalRotation * t;
	return normalizeAnglePositive(currentAngle);
}

/**
 * Clear manual rotation values from attributes
 */
export function clearManualRotation(attributes: PropAttributes): PropAttributes {
	const {
		manual_start_rotation: _manual_start_rotation,
		manual_end_rotation: _manual_end_rotation,
		manual_rotation_direction: _manual_rotation_direction,
		...rest
	} = attributes;
	return rest;
}

/**
 * Check if attributes have manual rotation values
 */
export function hasManualRotation(attributes: PropAttributes): boolean {
	return (
		attributes.manual_start_rotation !== undefined && attributes.manual_end_rotation !== undefined
	);
}

/**
 * Get manual rotation values in degrees for display/editing
 */
export function getManualRotationDegrees(attributes: PropAttributes): {
	startDegrees: number | undefined;
	endDegrees: number | undefined;
	direction: 'cw' | 'ccw' | 'shortest' | undefined;
} {
	return {
		startDegrees:
			attributes.manual_start_rotation !== undefined
				? radiansToDegrees(attributes.manual_start_rotation)
				: undefined,
		endDegrees:
			attributes.manual_end_rotation !== undefined
				? radiansToDegrees(attributes.manual_end_rotation)
				: undefined,
		direction: attributes.manual_rotation_direction
	};
}

/**
 * Validate manual rotation values
 */
export function validateManualRotation(attributes: PropAttributes): {
	isValid: boolean;
	errors: string[];
} {
	const errors: string[] = [];

	if (attributes.manual_start_rotation !== undefined) {
		if (isNaN(attributes.manual_start_rotation)) {
			errors.push('Manual start rotation must be a valid number');
		}
	}

	if (attributes.manual_end_rotation !== undefined) {
		if (isNaN(attributes.manual_end_rotation)) {
			errors.push('Manual end rotation must be a valid number');
		}
	}

	if (attributes.manual_rotation_direction !== undefined) {
		const validDirections = ['cw', 'ccw', 'shortest'];
		if (!validDirections.includes(attributes.manual_rotation_direction)) {
			errors.push('Manual rotation direction must be "cw", "ccw", or "shortest"');
		}
	}

	// Check for partial manual rotation (both start and end should be specified)
	const hasStart = attributes.manual_start_rotation !== undefined;
	const hasEnd = attributes.manual_end_rotation !== undefined;
	if (hasStart !== hasEnd) {
		errors.push('Both manual_start_rotation and manual_end_rotation must be specified together');
	}

	return {
		isValid: errors.length === 0,
		errors
	};
}
