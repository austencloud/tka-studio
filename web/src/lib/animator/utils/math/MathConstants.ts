/**
 * Math Constants
 *
 * Centralized mathematical constants used throughout the animator.
 */

import { Location } from "$domain";

// Core mathematical constants
export const PI = Math.PI;
export const TWO_PI = 2 * PI;
export const HALF_PI = PI / 2;

// Location angles mapping using centralized enums
export const LOCATION_ANGLES = {
  [Location.EAST]: 0,
  [Location.SOUTH]: HALF_PI,
  [Location.WEST]: PI,
  [Location.NORTH]: -HALF_PI,
  [Location.NORTHEAST]: -HALF_PI / 2,
  [Location.SOUTHEAST]: HALF_PI / 2,
  [Location.SOUTHWEST]: PI + HALF_PI / 2,
  [Location.NORTHWEST]: PI - HALF_PI / 2,
} as const;
