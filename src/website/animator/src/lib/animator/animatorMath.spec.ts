import { describe, it, expect } from 'vitest';
import {
	PI,
	TWO_PI,
	HALF_PI,
	locationAngles,
	normalizeAnglePositive,
	normalizeAngleSigned,
	mapPositionToAngle,
	mapOrientationToAngle,
	lerp,
	lerpAngle,
	calculateProIsolationStaffAngle,
	calculateAntispinTargetAngle,
	calculateStaticStaffAngle,
	calculateDashTargetAngle,
	calculateFloatStaffAngle
} from './utils/math/index.js';

describe('animatorMath', () => {
	it('locationAngles are correct', () => {
		expect(locationAngles.e).toBe(0);
		expect(locationAngles.s).toBeCloseTo(HALF_PI);
		expect(locationAngles.w).toBeCloseTo(PI);
		expect(locationAngles.n).toBeCloseTo(-HALF_PI);
	});

	it('normalizeAnglePositive wraps correctly', () => {
		expect(normalizeAnglePositive(0)).toBe(0);
		expect(normalizeAnglePositive(TWO_PI)).toBe(0);
		expect(normalizeAnglePositive(-PI)).toBeCloseTo(PI);
		expect(normalizeAnglePositive(3 * PI)).toBeCloseTo(PI);
	});

	it('normalizeAngleSigned wraps correctly', () => {
		expect(normalizeAngleSigned(0)).toBe(0);
		expect(normalizeAngleSigned(TWO_PI)).toBe(0);
		expect(normalizeAngleSigned(-PI)).toBeCloseTo(PI); // -PI normalizes to PI in signed range
		expect(normalizeAngleSigned(3 * PI)).toBeCloseTo(PI); // 3*PI normalizes to PI in signed range
	});

	it('mapPositionToAngle returns correct angles', () => {
		expect(mapPositionToAngle('e')).toBe(0);
		expect(mapPositionToAngle('s')).toBeCloseTo(HALF_PI);
		expect(mapPositionToAngle('w')).toBeCloseTo(PI);
		expect(mapPositionToAngle('n')).toBeCloseTo(-HALF_PI);
		expect(mapPositionToAngle('X')).toBe(0);
		expect(mapPositionToAngle(undefined)).toBe(0);
	});

	it('mapOrientationToAngle returns correct angles', () => {
		expect(mapOrientationToAngle('in')).toBeCloseTo(PI);
		expect(mapOrientationToAngle('out')).toBeCloseTo(0);
		expect(mapOrientationToAngle('n')).toBeCloseTo(-HALF_PI);
		expect(mapOrientationToAngle('e')).toBeCloseTo(0);
		expect(mapOrientationToAngle('s')).toBeCloseTo(HALF_PI);
		expect(mapOrientationToAngle('w')).toBeCloseTo(PI);
	});

	it('lerp interpolates linearly', () => {
		expect(lerp(0, 10, 0)).toBe(0);
		expect(lerp(0, 10, 1)).toBe(10);
		expect(lerp(0, 10, 0.5)).toBe(5);
	});

	it('lerpAngle interpolates angles correctly', () => {
		expect(lerpAngle(0, PI, 0.5)).toBeCloseTo(PI / 2);
		expect(lerpAngle(PI, 0, 0.5)).toBeCloseTo((3 * PI) / 2); // Takes the shorter path around the circle
		expect(lerpAngle(0, TWO_PI, 0.5)).toBeCloseTo(0); // 0 and 2*PI are the same angle
	});

	it('calculateProIsolationStaffAngle returns correct angle', () => {
		// Test pro motion with 0 turns: should perform 90-degree isolation
		// Starting from 'in' (PI), clockwise 90 degrees at t=0.5 should be PI + (PI/2 * 0.5) = PI + PI/4
		expect(calculateProIsolationStaffAngle('in', 'out', 'cw', 0, 0.5)).toBeCloseTo(
			PI + HALF_PI * 0.5
		);
		// Starting from 'in' (PI), counter-clockwise 90 degrees at t=0.5 should be PI + (-PI/2 * 0.5) = PI - PI/4
		expect(calculateProIsolationStaffAngle('in', 'out', 'ccw', 0, 0.5)).toBeCloseTo(
			PI - HALF_PI * 0.5
		);

		// Test pro motion with non-zero turns: should use orientation interpolation
		// From 'in' (PI) to 'out' (0) with 1 turn clockwise at t=0.5
		expect(calculateProIsolationStaffAngle('in', 'out', 'cw', 1, 0.5)).toBeCloseTo(3 * HALF_PI);
	});

	it('calculateAntispinTargetAngle returns correct angle', () => {
		// Test antispin with 0 turns: should perform 90-degree rotation opposite to prop_rot_dir
		// Starting from 'in' (PI), clockwise prop_rot_dir means -90 degrees at t=0.5 should be PI + (-PI/2 * 0.5) = PI - PI/4
		expect(calculateAntispinTargetAngle(0, 'in', 'out', 'cw', 0, 0.5)).toBeCloseTo(
			PI - HALF_PI * 0.5
		);
		// Starting from 'in' (PI), counter-clockwise prop_rot_dir means +90 degrees at t=0.5 should be PI + (PI/2 * 0.5) = PI + PI/4
		expect(calculateAntispinTargetAngle(0, 'in', 'out', 'ccw', 0, 0.5)).toBeCloseTo(
			PI + HALF_PI * 0.5
		);

		// Test antispin with non-zero turns: should use orientation interpolation with additional turns
		// From 'in' (PI) to 'out' (0), orientation change = -PI (shortest path)
		// Antispin: opposite rotation = +PI, plus 1 turn clockwise = +PI
		// Total: PI + PI + PI = 3*PI, normalized to PI
		expect(calculateAntispinTargetAngle(0, 'in', 'out', 'cw', 1, 1.0)).toBeCloseTo(PI);
	});

	it('calculateStaticStaffAngle returns correct angle', () => {
		expect(calculateStaticStaffAngle(0, 'in')).toBeCloseTo(PI);
		expect(calculateStaticStaffAngle(0, 'out')).toBeCloseTo(0);
	});

	it('calculateDashTargetAngle returns correct angle', () => {
		expect(calculateDashTargetAngle(0, 'in', 'out', 0.5)).toBeCloseTo(HALF_PI);
	});

	it('calculateFloatStaffAngle returns correct angle', () => {
		// Test float motion: simple interpolation between orientations
		// From 'in' (PI) to 'out' (0) at t=0.5 should be PI/2 (taking shorter path)
		expect(calculateFloatStaffAngle('in', 'out', 0.5)).toBeCloseTo(HALF_PI);
		// From 'out' (0) to 'in' (PI) at t=0.5 should be PI/2
		expect(calculateFloatStaffAngle('out', 'in', 0.5)).toBeCloseTo(HALF_PI);
		// Same orientation should return the same angle
		expect(calculateFloatStaffAngle('in', 'in', 0.5)).toBeCloseTo(PI);
		// Test at t=0 and t=1
		expect(calculateFloatStaffAngle('in', 'out', 0)).toBeCloseTo(PI);
		expect(calculateFloatStaffAngle('in', 'out', 1)).toBeCloseTo(0);
	});
});
