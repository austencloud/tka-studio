/**
 * Circular Position Maps for CAP (Circular Arrangement Pattern) Generation
 *
 * These maps define the valid end positions for circular sequences based on rotation angles.
 * - Halved CAPs: 180° rotation (position +4 or -4)
 * - Quartered CAPs: 90° rotation (position +2 or -2 for clockwise/counter-clockwise)
 */

import { GridPosition } from "$shared/pictograph/grid/domain/enums/grid-enums";

/**
 * Half position map - 180° rotation
 * Maps each position to its opposite position (4 positions away)
 */
export const HALF_POSITION_MAP: Record<GridPosition, GridPosition> = {
  [GridPosition.ALPHA1]: GridPosition.ALPHA5,
  [GridPosition.ALPHA2]: GridPosition.ALPHA6,
  [GridPosition.ALPHA3]: GridPosition.ALPHA7,
  [GridPosition.ALPHA4]: GridPosition.ALPHA8,
  [GridPosition.ALPHA5]: GridPosition.ALPHA1,
  [GridPosition.ALPHA6]: GridPosition.ALPHA2,
  [GridPosition.ALPHA7]: GridPosition.ALPHA3,
  [GridPosition.ALPHA8]: GridPosition.ALPHA4,

  [GridPosition.BETA1]: GridPosition.BETA5,
  [GridPosition.BETA2]: GridPosition.BETA6,
  [GridPosition.BETA3]: GridPosition.BETA7,
  [GridPosition.BETA4]: GridPosition.BETA8,
  [GridPosition.BETA5]: GridPosition.BETA1,
  [GridPosition.BETA6]: GridPosition.BETA2,
  [GridPosition.BETA7]: GridPosition.BETA3,
  [GridPosition.BETA8]: GridPosition.BETA4,

  [GridPosition.GAMMA1]: GridPosition.GAMMA5,
  [GridPosition.GAMMA2]: GridPosition.GAMMA6,
  [GridPosition.GAMMA3]: GridPosition.GAMMA7,
  [GridPosition.GAMMA4]: GridPosition.GAMMA8,
  [GridPosition.GAMMA5]: GridPosition.GAMMA1,
  [GridPosition.GAMMA6]: GridPosition.GAMMA2,
  [GridPosition.GAMMA7]: GridPosition.GAMMA3,
  [GridPosition.GAMMA8]: GridPosition.GAMMA4,

  [GridPosition.GAMMA9]: GridPosition.GAMMA13,
  [GridPosition.GAMMA10]: GridPosition.GAMMA14,
  [GridPosition.GAMMA11]: GridPosition.GAMMA15,
  [GridPosition.GAMMA12]: GridPosition.GAMMA16,
  [GridPosition.GAMMA13]: GridPosition.GAMMA9,
  [GridPosition.GAMMA14]: GridPosition.GAMMA10,
  [GridPosition.GAMMA15]: GridPosition.GAMMA11,
  [GridPosition.GAMMA16]: GridPosition.GAMMA12,
};

/**
 * Quarter position map - Clockwise 90° rotation
 * Maps each position to 2 positions clockwise (for box grid)
 */
export const QUARTER_POSITION_MAP_CW: Record<GridPosition, GridPosition> = {
  [GridPosition.ALPHA1]: GridPosition.ALPHA3,
  [GridPosition.ALPHA2]: GridPosition.ALPHA4,
  [GridPosition.ALPHA3]: GridPosition.ALPHA5,
  [GridPosition.ALPHA4]: GridPosition.ALPHA6,
  [GridPosition.ALPHA5]: GridPosition.ALPHA7,
  [GridPosition.ALPHA6]: GridPosition.ALPHA8,
  [GridPosition.ALPHA7]: GridPosition.ALPHA1,
  [GridPosition.ALPHA8]: GridPosition.ALPHA2,

  [GridPosition.BETA1]: GridPosition.BETA3,
  [GridPosition.BETA2]: GridPosition.BETA4,
  [GridPosition.BETA3]: GridPosition.BETA5,
  [GridPosition.BETA4]: GridPosition.BETA6,
  [GridPosition.BETA5]: GridPosition.BETA7,
  [GridPosition.BETA6]: GridPosition.BETA8,
  [GridPosition.BETA7]: GridPosition.BETA1,
  [GridPosition.BETA8]: GridPosition.BETA2,

  [GridPosition.GAMMA1]: GridPosition.GAMMA3,
  [GridPosition.GAMMA2]: GridPosition.GAMMA4,
  [GridPosition.GAMMA3]: GridPosition.GAMMA5,
  [GridPosition.GAMMA4]: GridPosition.GAMMA6,
  [GridPosition.GAMMA5]: GridPosition.GAMMA7,
  [GridPosition.GAMMA6]: GridPosition.GAMMA8,
  [GridPosition.GAMMA7]: GridPosition.GAMMA1,
  [GridPosition.GAMMA8]: GridPosition.GAMMA2,

  [GridPosition.GAMMA9]: GridPosition.GAMMA11,
  [GridPosition.GAMMA10]: GridPosition.GAMMA12,
  [GridPosition.GAMMA11]: GridPosition.GAMMA13,
  [GridPosition.GAMMA12]: GridPosition.GAMMA14,
  [GridPosition.GAMMA13]: GridPosition.GAMMA15,
  [GridPosition.GAMMA14]: GridPosition.GAMMA16,
  [GridPosition.GAMMA15]: GridPosition.GAMMA9,
  [GridPosition.GAMMA16]: GridPosition.GAMMA10,
};

/**
 * Quarter position map - Counter-clockwise 90° rotation
 * Maps each position to 2 positions counter-clockwise (for box grid)
 */
export const QUARTER_POSITION_MAP_CCW: Record<GridPosition, GridPosition> = {
  [GridPosition.ALPHA1]: GridPosition.ALPHA7,
  [GridPosition.ALPHA2]: GridPosition.ALPHA8,
  [GridPosition.ALPHA3]: GridPosition.ALPHA1,
  [GridPosition.ALPHA4]: GridPosition.ALPHA2,
  [GridPosition.ALPHA5]: GridPosition.ALPHA3,
  [GridPosition.ALPHA6]: GridPosition.ALPHA4,
  [GridPosition.ALPHA7]: GridPosition.ALPHA5,
  [GridPosition.ALPHA8]: GridPosition.ALPHA6,

  [GridPosition.BETA1]: GridPosition.BETA7,
  [GridPosition.BETA2]: GridPosition.BETA8,
  [GridPosition.BETA3]: GridPosition.BETA1,
  [GridPosition.BETA4]: GridPosition.BETA2,
  [GridPosition.BETA5]: GridPosition.BETA3,
  [GridPosition.BETA6]: GridPosition.BETA4,
  [GridPosition.BETA7]: GridPosition.BETA5,
  [GridPosition.BETA8]: GridPosition.BETA6,

  [GridPosition.GAMMA1]: GridPosition.GAMMA7,
  [GridPosition.GAMMA2]: GridPosition.GAMMA8,
  [GridPosition.GAMMA3]: GridPosition.GAMMA1,
  [GridPosition.GAMMA4]: GridPosition.GAMMA2,
  [GridPosition.GAMMA5]: GridPosition.GAMMA3,
  [GridPosition.GAMMA6]: GridPosition.GAMMA4,
  [GridPosition.GAMMA7]: GridPosition.GAMMA5,
  [GridPosition.GAMMA8]: GridPosition.GAMMA6,

  [GridPosition.GAMMA9]: GridPosition.GAMMA15,
  [GridPosition.GAMMA10]: GridPosition.GAMMA16,
  [GridPosition.GAMMA11]: GridPosition.GAMMA9,
  [GridPosition.GAMMA12]: GridPosition.GAMMA10,
  [GridPosition.GAMMA13]: GridPosition.GAMMA11,
  [GridPosition.GAMMA14]: GridPosition.GAMMA12,
  [GridPosition.GAMMA15]: GridPosition.GAMMA13,
  [GridPosition.GAMMA16]: GridPosition.GAMMA14,
};

/**
 * Halved CAP validation set
 * Set of (start_position, end_position) tuples that are valid for halved CAPs
 */
export const HALVED_CAPS = new Set<string>([
  `${GridPosition.ALPHA1},${GridPosition.ALPHA5}`,
  `${GridPosition.ALPHA2},${GridPosition.ALPHA6}`,
  `${GridPosition.ALPHA3},${GridPosition.ALPHA7}`,
  `${GridPosition.ALPHA4},${GridPosition.ALPHA8}`,
  `${GridPosition.ALPHA5},${GridPosition.ALPHA1}`,
  `${GridPosition.ALPHA6},${GridPosition.ALPHA2}`,
  `${GridPosition.ALPHA7},${GridPosition.ALPHA3}`,
  `${GridPosition.ALPHA8},${GridPosition.ALPHA4}`,

  `${GridPosition.BETA1},${GridPosition.BETA5}`,
  `${GridPosition.BETA2},${GridPosition.BETA6}`,
  `${GridPosition.BETA3},${GridPosition.BETA7}`,
  `${GridPosition.BETA4},${GridPosition.BETA8}`,
  `${GridPosition.BETA5},${GridPosition.BETA1}`,
  `${GridPosition.BETA6},${GridPosition.BETA2}`,
  `${GridPosition.BETA7},${GridPosition.BETA3}`,
  `${GridPosition.BETA8},${GridPosition.BETA4}`,

  `${GridPosition.GAMMA1},${GridPosition.GAMMA5}`,
  `${GridPosition.GAMMA2},${GridPosition.GAMMA6}`,
  `${GridPosition.GAMMA3},${GridPosition.GAMMA7}`,
  `${GridPosition.GAMMA4},${GridPosition.GAMMA8}`,
  `${GridPosition.GAMMA5},${GridPosition.GAMMA1}`,
  `${GridPosition.GAMMA6},${GridPosition.GAMMA2}`,
  `${GridPosition.GAMMA7},${GridPosition.GAMMA3}`,
  `${GridPosition.GAMMA8},${GridPosition.GAMMA4}`,

  `${GridPosition.GAMMA9},${GridPosition.GAMMA13}`,
  `${GridPosition.GAMMA10},${GridPosition.GAMMA14}`,
  `${GridPosition.GAMMA11},${GridPosition.GAMMA15}`,
  `${GridPosition.GAMMA12},${GridPosition.GAMMA16}`,
  `${GridPosition.GAMMA13},${GridPosition.GAMMA9}`,
  `${GridPosition.GAMMA14},${GridPosition.GAMMA10}`,
  `${GridPosition.GAMMA15},${GridPosition.GAMMA11}`,
  `${GridPosition.GAMMA16},${GridPosition.GAMMA12}`,
]);

/**
 * Quartered CAP validation set
 * Set of (start_position, end_position) tuples that are valid for quartered CAPs
 */
export const QUARTERED_CAPS = new Set<string>([
  // Clockwise quarter rotations
  `${GridPosition.ALPHA1},${GridPosition.ALPHA3}`,
  `${GridPosition.ALPHA2},${GridPosition.ALPHA4}`,
  `${GridPosition.ALPHA3},${GridPosition.ALPHA5}`,
  `${GridPosition.ALPHA4},${GridPosition.ALPHA6}`,
  `${GridPosition.ALPHA5},${GridPosition.ALPHA7}`,
  `${GridPosition.ALPHA6},${GridPosition.ALPHA8}`,
  `${GridPosition.ALPHA7},${GridPosition.ALPHA1}`,
  `${GridPosition.ALPHA8},${GridPosition.ALPHA2}`,

  // Counter-clockwise quarter rotations
  `${GridPosition.ALPHA1},${GridPosition.ALPHA7}`,
  `${GridPosition.ALPHA2},${GridPosition.ALPHA8}`,
  `${GridPosition.ALPHA3},${GridPosition.ALPHA1}`,
  `${GridPosition.ALPHA4},${GridPosition.ALPHA2}`,
  `${GridPosition.ALPHA5},${GridPosition.ALPHA3}`,
  `${GridPosition.ALPHA6},${GridPosition.ALPHA4}`,
  `${GridPosition.ALPHA7},${GridPosition.ALPHA5}`,
  `${GridPosition.ALPHA8},${GridPosition.ALPHA6}`,

  // Beta clockwise
  `${GridPosition.BETA1},${GridPosition.BETA3}`,
  `${GridPosition.BETA2},${GridPosition.BETA4}`,
  `${GridPosition.BETA3},${GridPosition.BETA5}`,
  `${GridPosition.BETA4},${GridPosition.BETA6}`,
  `${GridPosition.BETA5},${GridPosition.BETA7}`,
  `${GridPosition.BETA6},${GridPosition.BETA8}`,
  `${GridPosition.BETA7},${GridPosition.BETA1}`,
  `${GridPosition.BETA8},${GridPosition.BETA2}`,

  // Beta counter-clockwise
  `${GridPosition.BETA1},${GridPosition.BETA7}`,
  `${GridPosition.BETA2},${GridPosition.BETA8}`,
  `${GridPosition.BETA3},${GridPosition.BETA1}`,
  `${GridPosition.BETA4},${GridPosition.BETA2}`,
  `${GridPosition.BETA5},${GridPosition.BETA3}`,
  `${GridPosition.BETA6},${GridPosition.BETA4}`,
  `${GridPosition.BETA7},${GridPosition.BETA5}`,
  `${GridPosition.BETA8},${GridPosition.BETA6}`,

  // Gamma 1-8 clockwise
  `${GridPosition.GAMMA1},${GridPosition.GAMMA3}`,
  `${GridPosition.GAMMA2},${GridPosition.GAMMA4}`,
  `${GridPosition.GAMMA3},${GridPosition.GAMMA5}`,
  `${GridPosition.GAMMA4},${GridPosition.GAMMA6}`,
  `${GridPosition.GAMMA5},${GridPosition.GAMMA7}`,
  `${GridPosition.GAMMA6},${GridPosition.GAMMA8}`,
  `${GridPosition.GAMMA7},${GridPosition.GAMMA1}`,
  `${GridPosition.GAMMA8},${GridPosition.GAMMA2}`,

  // Gamma 1-8 counter-clockwise
  `${GridPosition.GAMMA1},${GridPosition.GAMMA7}`,
  `${GridPosition.GAMMA2},${GridPosition.GAMMA8}`,
  `${GridPosition.GAMMA3},${GridPosition.GAMMA1}`,
  `${GridPosition.GAMMA4},${GridPosition.GAMMA2}`,
  `${GridPosition.GAMMA5},${GridPosition.GAMMA3}`,
  `${GridPosition.GAMMA6},${GridPosition.GAMMA4}`,
  `${GridPosition.GAMMA7},${GridPosition.GAMMA5}`,
  `${GridPosition.GAMMA8},${GridPosition.GAMMA6}`,

  // Gamma 9-16 clockwise
  `${GridPosition.GAMMA9},${GridPosition.GAMMA11}`,
  `${GridPosition.GAMMA10},${GridPosition.GAMMA12}`,
  `${GridPosition.GAMMA11},${GridPosition.GAMMA13}`,
  `${GridPosition.GAMMA12},${GridPosition.GAMMA14}`,
  `${GridPosition.GAMMA13},${GridPosition.GAMMA15}`,
  `${GridPosition.GAMMA14},${GridPosition.GAMMA16}`,
  `${GridPosition.GAMMA15},${GridPosition.GAMMA9}`,
  `${GridPosition.GAMMA16},${GridPosition.GAMMA10}`,

  // Gamma 9-16 counter-clockwise
  `${GridPosition.GAMMA9},${GridPosition.GAMMA15}`,
  `${GridPosition.GAMMA10},${GridPosition.GAMMA16}`,
  `${GridPosition.GAMMA11},${GridPosition.GAMMA9}`,
  `${GridPosition.GAMMA12},${GridPosition.GAMMA10}`,
  `${GridPosition.GAMMA13},${GridPosition.GAMMA11}`,
  `${GridPosition.GAMMA14},${GridPosition.GAMMA12}`,
  `${GridPosition.GAMMA15},${GridPosition.GAMMA13}`,
  `${GridPosition.GAMMA16},${GridPosition.GAMMA14}`,
]);

/**
 * Location Rotation Maps
 */

import { GridLocation } from "$shared/pictograph/grid/domain/enums/grid-enums";
import { RotationDirection } from "$shared/pictograph/shared/domain/enums/pictograph-enums";

/**
 * Clockwise location rotation map
 * Rotates locations 90° clockwise: S → W → N → E → S
 */
export const LOCATION_MAP_CLOCKWISE: Record<GridLocation, GridLocation> = {
  [GridLocation.SOUTH]: GridLocation.WEST,
  [GridLocation.WEST]: GridLocation.NORTH,
  [GridLocation.NORTH]: GridLocation.EAST,
  [GridLocation.EAST]: GridLocation.SOUTH,

  [GridLocation.NORTHEAST]: GridLocation.SOUTHEAST,
  [GridLocation.SOUTHEAST]: GridLocation.SOUTHWEST,
  [GridLocation.SOUTHWEST]: GridLocation.NORTHWEST,
  [GridLocation.NORTHWEST]: GridLocation.NORTHEAST,
};

/**
 * Counter-clockwise location rotation map
 * Rotates locations 90° counter-clockwise: S → E → N → W → S
 */
export const LOCATION_MAP_COUNTER_CLOCKWISE: Record<GridLocation, GridLocation> = {
  [GridLocation.SOUTH]: GridLocation.EAST,
  [GridLocation.EAST]: GridLocation.NORTH,
  [GridLocation.NORTH]: GridLocation.WEST,
  [GridLocation.WEST]: GridLocation.SOUTH,

  [GridLocation.NORTHEAST]: GridLocation.NORTHWEST,
  [GridLocation.NORTHWEST]: GridLocation.SOUTHWEST,
  [GridLocation.SOUTHWEST]: GridLocation.SOUTHEAST,
  [GridLocation.SOUTHEAST]: GridLocation.NORTHEAST,
};

/**
 * Dash location rotation map
 * Flips locations to opposite: S ↔ N, E ↔ W
 */
export const LOCATION_MAP_DASH: Record<GridLocation, GridLocation> = {
  [GridLocation.SOUTH]: GridLocation.NORTH,
  [GridLocation.NORTH]: GridLocation.SOUTH,
  [GridLocation.WEST]: GridLocation.EAST,
  [GridLocation.EAST]: GridLocation.WEST,

  [GridLocation.NORTHEAST]: GridLocation.SOUTHWEST,
  [GridLocation.SOUTHEAST]: GridLocation.NORTHWEST,
  [GridLocation.SOUTHWEST]: GridLocation.NORTHEAST,
  [GridLocation.NORTHWEST]: GridLocation.SOUTHEAST,
};

/**
 * Static location rotation map
 * Locations stay in place (no rotation)
 */
export const LOCATION_MAP_STATIC: Record<GridLocation, GridLocation> = {
  [GridLocation.SOUTH]: GridLocation.SOUTH,
  [GridLocation.NORTH]: GridLocation.NORTH,
  [GridLocation.WEST]: GridLocation.WEST,
  [GridLocation.EAST]: GridLocation.EAST,

  [GridLocation.NORTHEAST]: GridLocation.NORTHEAST,
  [GridLocation.SOUTHEAST]: GridLocation.SOUTHEAST,
  [GridLocation.SOUTHWEST]: GridLocation.SOUTHWEST,
  [GridLocation.NORTHWEST]: GridLocation.NORTHWEST,
};

/**
 * Hand rotation direction map
 * Maps (startLocation, endLocation) tuples to rotation direction
 */
export const HAND_ROTATION_DIRECTION_MAP = new Map<
  string,
  RotationDirection | "dash" | "static"
>([
  // Clockwise cardinal rotations
  [`${GridLocation.SOUTH},${GridLocation.WEST}`, RotationDirection.CLOCKWISE],
  [`${GridLocation.WEST},${GridLocation.NORTH}`, RotationDirection.CLOCKWISE],
  [`${GridLocation.NORTH},${GridLocation.EAST}`, RotationDirection.CLOCKWISE],
  [`${GridLocation.EAST},${GridLocation.SOUTH}`, RotationDirection.CLOCKWISE],

  // Counter-clockwise cardinal rotations
  [`${GridLocation.WEST},${GridLocation.SOUTH}`, RotationDirection.COUNTER_CLOCKWISE],
  [`${GridLocation.NORTH},${GridLocation.WEST}`, RotationDirection.COUNTER_CLOCKWISE],
  [`${GridLocation.EAST},${GridLocation.NORTH}`, RotationDirection.COUNTER_CLOCKWISE],
  [`${GridLocation.SOUTH},${GridLocation.EAST}`, RotationDirection.COUNTER_CLOCKWISE],

  // Dash (opposite) movements
  [`${GridLocation.SOUTH},${GridLocation.NORTH}`, "dash"],
  [`${GridLocation.WEST},${GridLocation.EAST}`, "dash"],
  [`${GridLocation.NORTH},${GridLocation.SOUTH}`, "dash"],
  [`${GridLocation.EAST},${GridLocation.WEST}`, "dash"],

  // Static (no movement)
  [`${GridLocation.NORTH},${GridLocation.NORTH}`, "static"],
  [`${GridLocation.EAST},${GridLocation.EAST}`, "static"],
  [`${GridLocation.SOUTH},${GridLocation.SOUTH}`, "static"],
  [`${GridLocation.WEST},${GridLocation.WEST}`, "static"],

  // Clockwise diagonal rotations
  [`${GridLocation.NORTHEAST},${GridLocation.SOUTHEAST}`, RotationDirection.CLOCKWISE],
  [`${GridLocation.SOUTHEAST},${GridLocation.SOUTHWEST}`, RotationDirection.CLOCKWISE],
  [`${GridLocation.SOUTHWEST},${GridLocation.NORTHWEST}`, RotationDirection.CLOCKWISE],
  [`${GridLocation.NORTHWEST},${GridLocation.NORTHEAST}`, RotationDirection.CLOCKWISE],

  // Counter-clockwise diagonal rotations
  [`${GridLocation.NORTHEAST},${GridLocation.NORTHWEST}`, RotationDirection.COUNTER_CLOCKWISE],
  [`${GridLocation.NORTHWEST},${GridLocation.SOUTHWEST}`, RotationDirection.COUNTER_CLOCKWISE],
  [`${GridLocation.SOUTHWEST},${GridLocation.SOUTHEAST}`, RotationDirection.COUNTER_CLOCKWISE],
  [`${GridLocation.SOUTHEAST},${GridLocation.NORTHEAST}`, RotationDirection.COUNTER_CLOCKWISE],

  // Dash diagonal movements
  [`${GridLocation.NORTHEAST},${GridLocation.SOUTHWEST}`, "dash"],
  [`${GridLocation.SOUTHEAST},${GridLocation.NORTHWEST}`, "dash"],
  [`${GridLocation.SOUTHWEST},${GridLocation.NORTHEAST}`, "dash"],
  [`${GridLocation.NORTHWEST},${GridLocation.SOUTHEAST}`, "dash"],

  // Static diagonal (no movement)
  [`${GridLocation.NORTHEAST},${GridLocation.NORTHEAST}`, "static"],
  [`${GridLocation.SOUTHEAST},${GridLocation.SOUTHEAST}`, "static"],
  [`${GridLocation.SOUTHWEST},${GridLocation.SOUTHWEST}`, "static"],
  [`${GridLocation.NORTHWEST},${GridLocation.NORTHWEST}`, "static"],
]);

/**
 * Determine hand rotation direction based on start and end locations
 */
export function getHandRotationDirection(
  startLocation: GridLocation,
  endLocation: GridLocation
): RotationDirection | "dash" | "static" {
  const key = `${startLocation},${endLocation}`;
  const direction = HAND_ROTATION_DIRECTION_MAP.get(key);

  if (!direction) {
    throw new Error(
      `No hand rotation direction found for movement from ${startLocation} to ${endLocation}`
    );
  }

  return direction;
}

/**
 * Get location map for hand rotation
 */
export function getLocationMapForHandRotation(
  handRotationDir: RotationDirection | "dash" | "static"
): Record<GridLocation, GridLocation> {
  switch (handRotationDir) {
    case RotationDirection.CLOCKWISE:
      return LOCATION_MAP_CLOCKWISE;
    case RotationDirection.COUNTER_CLOCKWISE:
      return LOCATION_MAP_COUNTER_CLOCKWISE;
    case "dash":
      return LOCATION_MAP_DASH;
    case "static":
      return LOCATION_MAP_STATIC;
    default:
      throw new Error(`Unknown hand rotation direction: ${handRotationDir}`);
  }
}
