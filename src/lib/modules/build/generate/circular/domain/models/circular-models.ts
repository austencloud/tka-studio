/**
 * Circular Generation Models
 *
 * Type definitions for circular word (CAP - Circular Arrangement Pattern) generation.
 */

import type { GridPosition } from "$shared/pictograph/grid/domain/enums/grid-enums";

/**
 * CAP Type Enum
 * Defines the different types of circular arrangement patterns
 */
export enum CAPType {
  /** Strict rotated - rotates positions around the grid */
  STRICT_ROTATED = "strict_rotated",

  /** Strict mirrored - mirrors positions vertically */
  STRICT_MIRRORED = "strict_mirrored",

  /** Strict swapped - swaps blue and red attributes */
  STRICT_SWAPPED = "strict_swapped",

  /** Strict complementary - uses complementary letters (opposite motion types) */
  STRICT_COMPLEMENTARY = "strict_complementary",

  /** Swapped complementary - combines swapping with complementary motion */
  SWAPPED_COMPLEMENTARY = "swapped_complementary",

  /** Rotated complementary - combines rotation with complementary motion */
  ROTATED_COMPLEMENTARY = "rotated_complementary",

  /** Mirrored swapped - combines mirroring with color swapping */
  MIRRORED_SWAPPED = "mirrored_swapped",

  /** Mirrored complementary - combines mirroring with complementary motion */
  MIRRORED_COMPLEMENTARY = "mirrored_complementary",

  /** Rotated swapped - combines rotation with color swapping */
  ROTATED_SWAPPED = "rotated_swapped",

  /** Mirrored rotated - combines mirroring with rotation */
  MIRRORED_ROTATED = "mirrored_rotated",

  /** Mirrored complementary rotated - combines all three transformations */
  MIRRORED_COMPLEMENTARY_ROTATED = "mirrored_complementary_rotated",
}

/**
 * Slice Size
 * Determines how the circle is divided for rotation
 */
export enum SliceSize {
  /** Half rotation - 180° */
  HALVED = "halved",

  /** Quarter rotation - 90° */
  QUARTERED = "quartered",
}

/**
 * CAP Generation Options
 * Configuration for generating circular words
 */
export interface CAPGenerationOptions {
  /** Total sequence length (will be multiplied based on slice size) */
  length: number;

  /** CAP type to apply */
  capType: CAPType;

  /** Slice size for rotational CAPs */
  sliceSize: SliceSize;

  /** Turn intensity (1-3) */
  turnIntensity: number;

  /** Difficulty level (1-3) */
  level: number;

  /** Prop continuity setting */
  propContinuity: "continuous" | "non-continuous";

  /** Grid mode */
  gridMode: "box" | "diamond";
}

/**
 * CAP Validation Result
 * Result of validating whether a sequence can perform a given CAP
 */
export interface CAPValidationResult {
  /** Whether the sequence is valid for the CAP type */
  isValid: boolean;

  /** Reason for invalidity (if applicable) */
  reason?: string;

  /** Expected end position for the CAP (if applicable) */
  expectedEndPosition?: GridPosition;
}

/**
 * CAP User-friendly labels
 * Maps CAP types to display names for UI
 */
export const CAP_TYPE_LABELS: Record<CAPType, string> = {
  [CAPType.STRICT_ROTATED]: "Rotated",
  [CAPType.STRICT_MIRRORED]: "Mirrored",
  [CAPType.STRICT_SWAPPED]: "Swapped",
  [CAPType.STRICT_COMPLEMENTARY]: "Complementary",
  [CAPType.SWAPPED_COMPLEMENTARY]: "Swapped / Complementary",
  [CAPType.MIRRORED_SWAPPED]: "Mirrored / Swapped",
  [CAPType.ROTATED_COMPLEMENTARY]: "Rotated / Complementary",
  [CAPType.MIRRORED_COMPLEMENTARY]: "Mirrored / Complementary",
  [CAPType.ROTATED_SWAPPED]: "Rotated / Swapped",
  [CAPType.MIRRORED_ROTATED]: "Mirrored / Rotated",
  [CAPType.MIRRORED_COMPLEMENTARY_ROTATED]: "Mir / Comp / Rot",
};
