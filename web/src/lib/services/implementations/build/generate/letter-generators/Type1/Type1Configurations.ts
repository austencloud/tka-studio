/**
 * Type 1 Letter Configurations
 *
 * Type 1 letters only use PRO and ANTI motion types.
 * They are organized by position system transitions.
 */

import { Direction, MotionType, Timing } from "$domain";

export enum Type1MotionPattern {
  // Type 1 only uses PRO and ANTI
  PRO_PRO = "pro_pro",
  ANTI_ANTI = "anti_anti",
  PRO_ANTI = "pro_anti", // PRO/ANTI + ANTI/PRO (doubles variations)

  // Special patterns for U and V
  U_PATTERN = "u_pattern", // PRO/ANTI with quarter timing (U leads with PRO)
  V_PATTERN = "v_pattern", // ANTI/PRO with quarter timing (V leads with ANTI)
}

export interface Type1LetterConfig {
  motionPattern: Type1MotionPattern;
  // timing and direction will be calculated based on position system
}

/**
 * Calculate timing based on position system using the logical rules
 */
export function calculateTimingForPositionSystem(
  positionSystem: string
): Timing {
  // Gamma systems always use QUARTER timing
  if (positionSystem.includes("gamma")) {
    return Timing.QUARTER;
  }

  // For alpha/beta systems, determine if hands reach south point simultaneously
  switch (positionSystem) {
    case "alpha_to_alpha":
      // Alpha-to-alpha: hands never reach south point simultaneously
      return Timing.SPLIT;
    case "beta_to_beta":
      // Beta-to-beta: hands DO reach south point simultaneously
      return Timing.TOG;
    case "beta_to_alpha":
    case "alpha_to_beta":
      // Mixed systems: some movements are split, some are tog
      // For now, we'll use SPLIT as the base (mixed handling comes later)
      // TODO: Add mixed timing handling
      return Timing.SPLIT;
    default:
      throw new Error(`Unknown position system: ${positionSystem}`);
  }
}

/**
 * Calculate direction based on position system using the logical rules
 */
export function calculateDirectionForPositionSystem(
  positionSystem: string
): Direction {
  switch (positionSystem) {
    case "alpha_to_alpha":
    case "beta_to_beta":
      // Same-to-same transitions are SAME direction
      return Direction.SAME;
    case "beta_to_alpha":
    case "alpha_to_beta":
      // Cross transitions are OPP direction
      return Direction.OPP;
    case "gamma_to_gamma":
      // Gamma-to-gamma can be either - need to check specific letters
      // M-R are OPP, S-V are SAME (this is the pattern from CSV)
      // For now, we'll default to OPP and handle exceptions
      return Direction.OPP;
    default:
      throw new Error(`Unknown position system: ${positionSystem}`);
  }
}

/**
 * Generate motion pairs from Type 1 motion pattern
 */
export function getType1MotionPairsFromPattern(
  pattern: Type1MotionPattern
): [MotionType, MotionType][] {
  switch (pattern) {
    case Type1MotionPattern.PRO_PRO:
      return [[MotionType.PRO, MotionType.PRO]];
    case Type1MotionPattern.ANTI_ANTI:
      return [[MotionType.ANTI, MotionType.ANTI]];
    case Type1MotionPattern.PRO_ANTI:
      return [
        [MotionType.PRO, MotionType.ANTI],
        [MotionType.ANTI, MotionType.PRO],
      ];
    case Type1MotionPattern.U_PATTERN:
      // U leads with PRO (isolation), follows with ANTI
      return [
        [MotionType.PRO, MotionType.ANTI],
        [MotionType.ANTI, MotionType.PRO],
      ];
    case Type1MotionPattern.V_PATTERN:
      // V leads with ANTI, follows with PRO (isolation)
      return [
        [MotionType.ANTI, MotionType.PRO],
        [MotionType.PRO, MotionType.ANTI],
      ];
    default:
      throw new Error(`Unknown Type 1 motion pattern: ${pattern}`);
  }
}

// ===== TYPE 1 LETTER CONFIGURATIONS BY POSITION SYSTEM =====

/**
 * Type 1 Letters - Alpha to Alpha (A, B, C)
 * Timing and direction calculated automatically based on position system
 */
export const TYPE1_ALPHA_TO_ALPHA_LETTERS: Record<string, Type1LetterConfig> = {
  A: { motionPattern: Type1MotionPattern.PRO_PRO },
  B: { motionPattern: Type1MotionPattern.ANTI_ANTI },
  C: { motionPattern: Type1MotionPattern.PRO_ANTI },
};

/**
 * Type 1 Letters - Beta to Alpha (D, E, F)
 * Timing and direction calculated automatically based on position system
 */
export const TYPE1_BETA_TO_ALPHA_LETTERS: Record<string, Type1LetterConfig> = {
  D: { motionPattern: Type1MotionPattern.PRO_PRO },
  E: { motionPattern: Type1MotionPattern.ANTI_ANTI },
  F: { motionPattern: Type1MotionPattern.PRO_ANTI },
};

/**
 * Type 1 Letters - Beta to Beta (G, H, I)
 * Timing and direction calculated automatically based on position system
 */
export const TYPE1_BETA_TO_BETA_LETTERS: Record<string, Type1LetterConfig> = {
  G: { motionPattern: Type1MotionPattern.PRO_PRO },
  H: { motionPattern: Type1MotionPattern.ANTI_ANTI },
  I: { motionPattern: Type1MotionPattern.PRO_ANTI },
};

/**
 * Type 1 Letters - Alpha to Beta (J, K, L)
 * Timing and direction calculated automatically based on position system
 */
export const TYPE1_ALPHA_TO_BETA_LETTERS: Record<string, Type1LetterConfig> = {
  J: { motionPattern: Type1MotionPattern.PRO_PRO },
  K: { motionPattern: Type1MotionPattern.ANTI_ANTI },
  L: { motionPattern: Type1MotionPattern.PRO_ANTI },
};

/**
 * Type 1 Letters - Gamma to Gamma (M, N, O, P, Q, R, S, T, U, V)
 * Timing and direction calculated automatically, with special handling for S-V
 */
export const TYPE1_GAMMA_TO_GAMMA_LETTERS: Record<string, Type1LetterConfig> = {
  M: { motionPattern: Type1MotionPattern.PRO_PRO },
  N: { motionPattern: Type1MotionPattern.ANTI_ANTI },
  O: { motionPattern: Type1MotionPattern.PRO_ANTI },
  P: { motionPattern: Type1MotionPattern.PRO_PRO },
  Q: { motionPattern: Type1MotionPattern.ANTI_ANTI },
  R: { motionPattern: Type1MotionPattern.PRO_ANTI },
  S: { motionPattern: Type1MotionPattern.PRO_PRO },
  T: { motionPattern: Type1MotionPattern.ANTI_ANTI },
  U: { motionPattern: Type1MotionPattern.U_PATTERN },
  V: { motionPattern: Type1MotionPattern.V_PATTERN },
};

/**
 * Get Type 1 letter configuration by letter
 */
export function getType1LetterConfig(letter: string): Type1LetterConfig | null {
  const configs = [
    TYPE1_ALPHA_TO_ALPHA_LETTERS,
    TYPE1_BETA_TO_ALPHA_LETTERS,
    TYPE1_BETA_TO_BETA_LETTERS,
    TYPE1_ALPHA_TO_BETA_LETTERS,
    TYPE1_GAMMA_TO_GAMMA_LETTERS,
  ];

  for (const config of configs) {
    if (letter in config) {
      return config[letter];
    }
  }

  return null;
}

/**
 * Get all Type 1 letters for a specific position system
 */
export function getType1LettersForPositionSystem(
  positionSystem: string
): string[] {
  switch (positionSystem) {
    case "alpha_to_alpha":
      return Object.keys(TYPE1_ALPHA_TO_ALPHA_LETTERS);
    case "beta_to_alpha":
      return Object.keys(TYPE1_BETA_TO_ALPHA_LETTERS);
    case "beta_to_beta":
      return Object.keys(TYPE1_BETA_TO_BETA_LETTERS);
    case "alpha_to_beta":
      return Object.keys(TYPE1_ALPHA_TO_BETA_LETTERS);
    case "gamma_to_gamma":
      return Object.keys(TYPE1_GAMMA_TO_GAMMA_LETTERS);
    default:
      return [];
  }
}

/**
 * Check if a letter is a Type 1 letter
 */
export function isType1Letter(letter: string): boolean {
  return getType1LetterConfig(letter) !== null;
}
