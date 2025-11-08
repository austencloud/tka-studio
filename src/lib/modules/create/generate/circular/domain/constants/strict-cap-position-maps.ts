/**
 * Position and Location Maps for Strict CAP Variations
 *
 * These maps define transformations for:
 * - STRICT_MIRRORED: Vertical mirroring of positions and locations
 * - STRICT_SWAPPED: Color swapping position transformations
 * - STRICT_COMPLEMENTARY: Letter complementarity mappings
 *
 * Note: STRICT_ROTATED uses different maps defined in circular-position-maps.ts
 */

import {
  GridPosition,
  GridLocation,
} from "$shared/pictograph/grid/domain/enums/grid-enums";

/**
 * Vertical Mirror Position Map
 * Mirrors positions vertically across the center horizontal axis
 * Used by STRICT_MIRRORED CAP type
 *
 * Examples:
 * - ALPHA2 (SW-NE) ↔ ALPHA8 (SE-NW) - diagonals flip
 * - ALPHA3 (W-E) ↔ ALPHA7 (E-W) - horizontals swap
 * - ALPHA1 (S-N) → ALPHA1 - vertical stays same
 * - GAMMA1 (W-N) ↔ GAMMA9 (E-N) - gammas cross-mirror
 */
export const VERTICAL_MIRROR_POSITION_MAP: Record<GridPosition, GridPosition> =
  {
    // Alpha group - vertical axis symmetry
    [GridPosition.ALPHA1]: GridPosition.ALPHA1, // S-N → S-N (on axis)
    [GridPosition.ALPHA2]: GridPosition.ALPHA8, // SW-NE → SE-NW
    [GridPosition.ALPHA3]: GridPosition.ALPHA7, // W-E → E-W
    [GridPosition.ALPHA4]: GridPosition.ALPHA6, // NW-SE → NE-SW
    [GridPosition.ALPHA5]: GridPosition.ALPHA5, // N-S → N-S (on axis)
    [GridPosition.ALPHA6]: GridPosition.ALPHA4, // NE-SW → NW-SE
    [GridPosition.ALPHA7]: GridPosition.ALPHA3, // E-W → W-E
    [GridPosition.ALPHA8]: GridPosition.ALPHA2, // SE-NW → SW-NE

    // Beta group - same sides stay same
    [GridPosition.BETA1]: GridPosition.BETA1, // N-N → N-N (on axis)
    [GridPosition.BETA2]: GridPosition.BETA8, // NE-NE → NW-NW
    [GridPosition.BETA3]: GridPosition.BETA7, // E-E → W-W
    [GridPosition.BETA4]: GridPosition.BETA6, // SE-SE → SW-SW
    [GridPosition.BETA5]: GridPosition.BETA5, // S-S → S-S (on axis)
    [GridPosition.BETA6]: GridPosition.BETA4, // SW-SW → SE-SE
    [GridPosition.BETA7]: GridPosition.BETA3, // W-W → E-E
    [GridPosition.BETA8]: GridPosition.BETA2, // NW-NW → NE-NE

    // Gamma group - cross-mirror pattern
    [GridPosition.GAMMA1]: GridPosition.GAMMA9, // W-N ↔ E-N
    [GridPosition.GAMMA2]: GridPosition.GAMMA16, // NW-NE ↔ NE-NW
    [GridPosition.GAMMA3]: GridPosition.GAMMA15, // N-E ↔ N-W
    [GridPosition.GAMMA4]: GridPosition.GAMMA14, // NE-SE ↔ NW-SW
    [GridPosition.GAMMA5]: GridPosition.GAMMA13, // E-S ↔ W-S
    [GridPosition.GAMMA6]: GridPosition.GAMMA12, // SE-SW ↔ SW-SE
    [GridPosition.GAMMA7]: GridPosition.GAMMA11, // S-W ↔ S-E
    [GridPosition.GAMMA8]: GridPosition.GAMMA10, // SW-NW ↔ SE-NE
    [GridPosition.GAMMA9]: GridPosition.GAMMA1, // E-N ↔ W-N
    [GridPosition.GAMMA10]: GridPosition.GAMMA8, // SE-NE ↔ SW-NW
    [GridPosition.GAMMA11]: GridPosition.GAMMA7, // S-E ↔ S-W
    [GridPosition.GAMMA12]: GridPosition.GAMMA6, // SW-SE ↔ SE-SW
    [GridPosition.GAMMA13]: GridPosition.GAMMA5, // W-S ↔ E-S
    [GridPosition.GAMMA14]: GridPosition.GAMMA4, // NW-SW ↔ NE-SE
    [GridPosition.GAMMA15]: GridPosition.GAMMA3, // N-W ↔ N-E
    [GridPosition.GAMMA16]: GridPosition.GAMMA2, // NE-NW ↔ NW-NE
  };

/**
 * Vertical Mirror Location Map
 * Mirrors hand locations vertically (flips east/west)
 * Used by STRICT_MIRRORED for transforming motion end locations
 *
 * Examples:
 * - E (east) ↔ W (west)
 * - NE (northeast) ↔ NW (northwest)
 * - N (north) → N (stays on vertical axis)
 * - S (south) → S (stays on vertical axis)
 */
export const VERTICAL_MIRROR_LOCATION_MAP: Record<GridLocation, GridLocation> =
  {
    [GridLocation.NORTH]: GridLocation.NORTH, // On axis - no change
    [GridLocation.SOUTH]: GridLocation.SOUTH, // On axis - no change
    [GridLocation.EAST]: GridLocation.WEST, // Flip east/west
    [GridLocation.WEST]: GridLocation.EAST, // Flip west/east
    [GridLocation.NORTHEAST]: GridLocation.NORTHWEST, // Flip NE/NW
    [GridLocation.NORTHWEST]: GridLocation.NORTHEAST, // Flip NW/NE
    [GridLocation.SOUTHEAST]: GridLocation.SOUTHWEST, // Flip SE/SW
    [GridLocation.SOUTHWEST]: GridLocation.SOUTHEAST, // Flip SW/SE
  };

/**
 * Swapped Position Map
 * Maps positions to their color-swapped equivalents
 * Used by STRICT_SWAPPED CAP type
 *
 * Pattern:
 * - Alpha: 180° rotation (cross-pattern)
 * - Beta: No change (same positions stay same)
 * - Gamma: Complex cross-swap pattern
 */
export const SWAPPED_POSITION_MAP: Record<GridPosition, GridPosition> = {
  // Alpha group - 180° swap pattern
  [GridPosition.ALPHA1]: GridPosition.ALPHA5, // S-N ↔ N-S
  [GridPosition.ALPHA2]: GridPosition.ALPHA6, // SW-NE ↔ NE-SW
  [GridPosition.ALPHA3]: GridPosition.ALPHA7, // W-E ↔ E-W
  [GridPosition.ALPHA4]: GridPosition.ALPHA8, // NW-SE ↔ SE-NW
  [GridPosition.ALPHA5]: GridPosition.ALPHA1, // N-S ↔ S-N
  [GridPosition.ALPHA6]: GridPosition.ALPHA2, // NE-SW ↔ SW-NE
  [GridPosition.ALPHA7]: GridPosition.ALPHA3, // E-W ↔ W-E
  [GridPosition.ALPHA8]: GridPosition.ALPHA4, // SE-NW ↔ NW-SE

  // Beta group - no change (both hands same location)
  [GridPosition.BETA1]: GridPosition.BETA1, // N-N → N-N
  [GridPosition.BETA2]: GridPosition.BETA2, // NE-NE → NE-NE
  [GridPosition.BETA3]: GridPosition.BETA3, // E-E → E-E
  [GridPosition.BETA4]: GridPosition.BETA4, // SE-SE → SE-SE
  [GridPosition.BETA5]: GridPosition.BETA5, // S-S → S-S
  [GridPosition.BETA6]: GridPosition.BETA6, // SW-SW → SW-SW
  [GridPosition.BETA7]: GridPosition.BETA7, // W-W → W-W
  [GridPosition.BETA8]: GridPosition.BETA8, // NW-NW → NW-NW

  // Gamma group - cross-swap pattern
  [GridPosition.GAMMA1]: GridPosition.GAMMA15, // W-N ↔ N-W
  [GridPosition.GAMMA2]: GridPosition.GAMMA16, // NW-NE ↔ NE-NW
  [GridPosition.GAMMA3]: GridPosition.GAMMA9, // N-E ↔ E-N
  [GridPosition.GAMMA4]: GridPosition.GAMMA10, // NE-SE ↔ SE-NE
  [GridPosition.GAMMA5]: GridPosition.GAMMA11, // E-S ↔ S-E
  [GridPosition.GAMMA6]: GridPosition.GAMMA12, // SE-SW ↔ SW-SE
  [GridPosition.GAMMA7]: GridPosition.GAMMA13, // S-W ↔ W-S
  [GridPosition.GAMMA8]: GridPosition.GAMMA14, // SW-NW ↔ NW-SW
  [GridPosition.GAMMA9]: GridPosition.GAMMA3, // E-N ↔ N-E
  [GridPosition.GAMMA10]: GridPosition.GAMMA4, // SE-NE ↔ NE-SE
  [GridPosition.GAMMA11]: GridPosition.GAMMA5, // S-E ↔ E-S
  [GridPosition.GAMMA12]: GridPosition.GAMMA6, // SW-SE ↔ SE-SW
  [GridPosition.GAMMA13]: GridPosition.GAMMA7, // W-S ↔ S-W
  [GridPosition.GAMMA14]: GridPosition.GAMMA8, // NW-SW ↔ SW-NW
  [GridPosition.GAMMA15]: GridPosition.GAMMA1, // N-W ↔ W-N
  [GridPosition.GAMMA16]: GridPosition.GAMMA2, // NE-NW ↔ NW-NE
};

/**
 * Complementary Letter Map
 * Maps letters to their complementary pairs (opposite motion types)
 * Used by STRICT_COMPLEMENTARY CAP type
 *
 * Pattern:
 * - Most letters pair with adjacent letter (A↔B, D↔E, etc.)
 * - Some letters are self-complementary (C, F, I, etc.)
 * - Greek letters follow similar pairing rules
 */
export const COMPLEMENTARY_LETTER_MAP: Record<string, string> = {
  // Basic alphabet pairs
  A: "B",
  B: "A",
  C: "C", // Self-complementary
  D: "E",
  E: "D",
  F: "F", // Self-complementary
  G: "H",
  H: "G",
  I: "I", // Self-complementary
  J: "K",
  K: "J",
  L: "L", // Self-complementary
  M: "N",
  N: "M",
  O: "O", // Self-complementary
  P: "Q",
  Q: "P",
  R: "R", // Self-complementary
  S: "T",
  T: "S",
  U: "V",
  V: "U",
  W: "X",
  X: "W",
  Y: "Z",
  Z: "Y",

  // Greek letters
  Σ: "Δ",
  Δ: "Σ",
  θ: "Ω",
  Ω: "θ",
  Φ: "Φ", // Self-complementary
  Ψ: "Ψ", // Self-complementary
  Λ: "Λ", // Self-complementary
  α: "α", // Self-complementary
  β: "β", // Self-complementary
  Γ: "Γ", // Self-complementary

  // Dash variations
  "W-": "X-",
  "X-": "W-",
  "Y-": "Z-",
  "Z-": "Y-",
  "Σ-": "Δ-",
  "Δ-": "Σ-",
  "θ-": "Ω-",
  "Ω-": "θ-",
  "Φ-": "Φ-", // Self-complementary
  "Ψ-": "Ψ-", // Self-complementary
  "Λ-": "Λ-", // Self-complementary
};

/**
 * Get complementary letter for a given letter
 * @throws Error if letter not found in map
 */
export function getComplementaryLetter(letter: string): string {
  const complementary = COMPLEMENTARY_LETTER_MAP[letter];

  if (!complementary) {
    throw new Error(
      `No complementary letter mapping found for letter: ${letter}`
    );
  }

  return complementary;
}

/**
 * Validation Sets for Strict CAP Types
 * These define which (start_position, end_position) pairs are valid for each CAP type
 */

/**
 * Mirrored CAP validation set
 * Valid when: vertical_mirror(start_pos) === end_pos
 */
export const MIRRORED_CAP_VALIDATION_SET = new Set<string>(
  Object.entries(VERTICAL_MIRROR_POSITION_MAP).map(
    ([start, end]) => `${start},${end}`
  )
);

/**
 * Swapped CAP validation set
 * Valid when: swapped(start_pos) === end_pos
 */
export const SWAPPED_CAP_VALIDATION_SET = new Set<string>(
  Object.entries(SWAPPED_POSITION_MAP).map(([start, end]) => `${start},${end}`)
);

/**
 * Mirrored-Swapped CAP validation set
 * Valid when: vertical_mirror(start_pos) === end_pos (same as mirrored)
 * The swapping happens with motion attributes, but position requirement is same as mirrored
 */
export const MIRRORED_SWAPPED_VALIDATION_SET = new Set<string>(
  Object.entries(VERTICAL_MIRROR_POSITION_MAP).map(
    ([start, end]) => `${start},${end}`
  )
);

/**
 * Complementary CAP validation set
 * Valid when: start_pos === end_pos (returns to starting position)
 */
export const COMPLEMENTARY_CAP_VALIDATION_SET = new Set<string>(
  Object.values(GridPosition).map((pos) => `${pos},${pos}`)
);

/**
 * Mirrored-Complementary CAP validation set
 * Valid when: vertical_mirror(start_pos) === end_pos (same as mirrored)
 * The complementary transformation happens with motion types and letters, but position requirement is same as mirrored
 */
export const MIRRORED_COMPLEMENTARY_VALIDATION_SET = new Set<string>(
  Object.entries(VERTICAL_MIRROR_POSITION_MAP).map(
    ([start, end]) => `${start},${end}`
  )
);
