/**
 * Type 1 Shared Utilities
 *
 * Common utility functions used by all Type 1 letter generators.
 * Type 1 letters only use PRO/ANTI motion types with matching rotations.
 */

import { RotationDirection } from "$domain";
import type { Type1LetterConfig } from "./Type1Configurations";

/**
 * Generate matching rotation pairs (CW/CW and CCW/CCW) for Type 1 letters
 * Type 1 letters use synchronized rotations as shown in the diamond dataframe
 */
export function getType1MatchingRotationPairs(): [
  RotationDirection,
  RotationDirection,
][] {
  return [
    [RotationDirection.CLOCKWISE, RotationDirection.CLOCKWISE],
    [RotationDirection.COUNTER_CLOCKWISE, RotationDirection.COUNTER_CLOCKWISE],
  ];
}

/**
 * Generate all combinations of CW/CCW rotations
 * This is kept for potential future use, but Type 1 letters use matching rotations
 */
export function getAllRotationCombinations(): [
  RotationDirection,
  RotationDirection,
][] {
  const rotations = [
    RotationDirection.CLOCKWISE,
    RotationDirection.COUNTER_CLOCKWISE,
  ];
  const combinations: [RotationDirection, RotationDirection][] = [];

  for (const blue of rotations) {
    for (const red of rotations) {
      combinations.push([blue, red]);
    }
  }

  return combinations;
}

/**
 * Get supported letters for a Type 1 position system configuration
 */
export function getType1SupportedLetters(
  config: Record<string, Type1LetterConfig>
): string[] {
  return Object.keys(config);
}

/**
 * Check if a letter is supported by a Type 1 position system configuration
 */
export function isType1LetterSupported(
  letter: string,
  config: Record<string, Type1LetterConfig>
): boolean {
  return letter in config;
}

/**
 * Calculate expected variation count for Type 1 letters
 * Formula: motion pairs × 2 matching rotations × 4 position transitions
 */
export function calculateType1VariationCount(motionPairCount: number): number {
  const matchingRotations = 2; // CW/CW and CCW/CCW
  const positionTransitions = 4; // Each position system has 4 transitions in the cycle
  return motionPairCount * matchingRotations * positionTransitions;
}

/**
 * Type 1 Pattern Generation Summary
 *
 * All Type 1 letters follow this pattern:
 * 1. Motion Pattern determines motion pairs (PRO_PRO=1, ANTI_ANTI=1, PRO_ANTI=2)
 * 2. Always use matching rotations (CW/CW, CCW/CCW) - never mixed
 * 3. Position system determines the 4-step transition cycle
 * 4. Pattern service generates all position transitions automatically
 *
 * Results:
 * - PRO_PRO or ANTI_ANTI: 1 × 2 × 4 = 8 variations
 * - PRO_ANTI: 2 × 2 × 4 = 16 variations
 */
