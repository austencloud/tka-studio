/**
 * Mathematical constants for the Pictograph Animator
 */

export const PI = Math.PI;
export const TWO_PI = 2 * PI;
export const HALF_PI = PI / 2;

export const locationAngles: Record<string, number> = {
	e: 0,
	s: HALF_PI,
	w: PI,
	n: -HALF_PI
};
