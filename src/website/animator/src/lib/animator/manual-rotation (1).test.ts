import { describe, it, expect } from 'vitest';
import {
	setManualRotationDegrees,
	calculateManualStaffRotation,
	hasManualRotation,
	clearManualRotation,
	degreesToRadians
} from './utils/manual-rotation.js';
import type { PropAttributes } from './types/core.js';

describe('Manual Rotation System', () => {
	const baseAttributes: PropAttributes = {
		start_loc: 's',
		end_loc: 'w',
		start_ori: 'in',
		end_ori: 'in',
		prop_rot_dir: 'cw',
		turns: 0,
		motion_type: 'pro'
	};

	it('should set manual rotation in degrees', () => {
		const attrs = setManualRotationDegrees(baseAttributes, 0, 90, 'cw');

		expect(attrs.manual_start_rotation).toBeCloseTo(0);
		expect(attrs.manual_end_rotation).toBeCloseTo(degreesToRadians(90));
		expect(attrs.manual_rotation_direction).toBe('cw');
	});

	it('should detect manual rotation presence', () => {
		const attrsWithoutManual = baseAttributes;
		const attrsWithManual = setManualRotationDegrees(baseAttributes, 0, 90, 'cw');

		expect(hasManualRotation(attrsWithoutManual)).toBe(false);
		expect(hasManualRotation(attrsWithManual)).toBe(true);
	});

	it('should calculate manual staff rotation correctly', () => {
		const attrs = setManualRotationDegrees(baseAttributes, 0, 90, 'cw');

		// At t=0, should be at start angle (0 degrees = 0 radians)
		const rotationAtStart = calculateManualStaffRotation(attrs, 0);
		expect(rotationAtStart).toBeCloseTo(0);

		// At t=1, should be at end angle (90 degrees = π/2 radians)
		const rotationAtEnd = calculateManualStaffRotation(attrs, 1);
		expect(rotationAtEnd).toBeCloseTo(degreesToRadians(90));

		// At t=0.5, should be halfway (45 degrees = π/4 radians)
		const rotationAtMiddle = calculateManualStaffRotation(attrs, 0.5);
		expect(rotationAtMiddle).toBeCloseTo(degreesToRadians(45));
	});

	it('should return null for attributes without manual rotation', () => {
		const rotation = calculateManualStaffRotation(baseAttributes, 0.5);
		expect(rotation).toBeNull();
	});

	it('should handle counter-clockwise rotation', () => {
		const attrs = setManualRotationDegrees(baseAttributes, 0, -90, 'ccw');

		const rotationAtEnd = calculateManualStaffRotation(attrs, 1);
		expect(rotationAtEnd).toBeCloseTo(degreesToRadians(270)); // -90° normalized to 270°
	});

	it('should handle shortest path rotation', () => {
		const attrs = setManualRotationDegrees(baseAttributes, 10, 350, 'shortest');

		// Should take the shorter path: 10° to 350° = -20° rotation
		const rotationAtMiddle = calculateManualStaffRotation(attrs, 0.5);
		expect(rotationAtMiddle).toBeCloseTo(degreesToRadians(0)); // 10° + (-20° * 0.5) = 0°
	});

	it('should clear manual rotation', () => {
		const attrsWithManual = setManualRotationDegrees(baseAttributes, 0, 90, 'cw');
		const attrsCleared = clearManualRotation(attrsWithManual);

		expect(hasManualRotation(attrsCleared)).toBe(false);
		expect(attrsCleared.manual_start_rotation).toBeUndefined();
		expect(attrsCleared.manual_end_rotation).toBeUndefined();
		expect(attrsCleared.manual_rotation_direction).toBeUndefined();
	});
});
