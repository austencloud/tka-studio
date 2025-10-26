/**
 * Math Constants
 *
 * Centralized mathematical constants used throughout the animator.
 */

import { GridLocation } from "$shared/pictograph/grid/domain/enums/grid-enums";

// Core mathematical constants
export const PI = Math.PI;
export const TWO_PI = 2 * PI;
export const HALF_PI = PI / 2;

// GridLocation angles mapping using centralized enums
export const LOCATION_ANGLES = {
  [GridLocation.EAST]: 0,
  [GridLocation.SOUTH]: HALF_PI,
  [GridLocation.WEST]: PI,
  [GridLocation.NORTH]: -HALF_PI,
  [GridLocation.NORTHEAST]: -HALF_PI / 2,
  [GridLocation.SOUTHEAST]: HALF_PI / 2,
  [GridLocation.SOUTHWEST]: PI + HALF_PI / 2,
  [GridLocation.NORTHWEST]: PI - HALF_PI / 2,
} as const;
