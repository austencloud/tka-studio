import type { GridPosition } from "$shared/pictograph/grid/domain/enums/grid-enums";
import type { BeatData } from "../../domain/models/BeatData";
import type { SequenceData } from "$shared/foundation/domain/models/SequenceData";

/**
 * Circular Sequence Type
 *
 * Defines the relationship between start and end positions:
 * - 'same': Ends at exact same position (e.g., beta1 to beta1)
 * - 'halved': Ends at opposite position (e.g., beta1 to beta5)
 * - 'quartered': Ends at adjacent 90° position (e.g., beta1 to beta3 or beta7)
 */
export type CircularType = "same" | "halved" | "quartered";

/**
 * CAP (Continuous Assembly Pattern) Type
 *
 * Strict variations based on rotation and mirroring:
 * - 'rotated': Pure rotation without mirroring
 * - 'mirrored': Pure mirroring without rotation
 * - 'rotated-mirrored': Combination of rotation and mirroring
 * - 'static': No rotation or mirroring (same position)
 */
export type StrictCapType =
  | "rotated"
  | "mirrored"
  | "rotated-mirrored"
  | "static";

/**
 * Circularity Analysis Result
 *
 * Complete analysis of a sequence's circular properties.
 */
export interface CircularityAnalysis {
  /** Whether the sequence forms a valid circular pattern */
  readonly isCircular: boolean;

  /** Type of circular relationship (same/halved/quartered) */
  readonly circularType: CircularType | null;

  /** Starting position of the sequence */
  readonly startPosition: GridPosition | null;

  /** Ending position of the sequence */
  readonly endPosition: GridPosition | null;

  /** Whether start position is a beta position */
  readonly startIsBeta: boolean;

  /** Whether end position is a beta position */
  readonly endIsBeta: boolean;

  /** Possible CAP types this sequence could become */
  readonly possibleCapTypes: readonly StrictCapType[];

  /** Human-readable description of the circular relationship */
  readonly description: string;
}

/**
 * Sequence Analysis Service Contract
 *
 * Service for analyzing sequences to detect circular patterns,
 * CAP (Continuous Assembly Pattern) potential, and autocomplete capability.
 *
 * This service is used to:
 * - Detect if a sequence can form a circular pattern
 * - Determine what type of CAP pattern is possible
 * - Enable autocomplete functionality for the user
 */
export interface ISequenceAnalysisService {
  /**
   * Analyze a sequence for circular properties
   *
   * Determines if a sequence has the potential to be completed as a
   * circular pattern (CAP - Continuous Assembly Pattern).
   *
   * A sequence is circular-capable if:
   * 1. It has at least one beat with pictograph data
   * 2. Both start and end positions are defined
   * 3. Both positions are in the same position group (alpha→alpha, beta→beta, or gamma→gamma)
   * 4. End position relates to start position in a valid way (same/halved/quartered)
   *
   * Valid circular relationships:
   * - Alpha to Alpha (any variation, e.g., alpha1→alpha3)
   * - Beta to Beta (any variation, e.g., beta1→beta5)
   * - Gamma to Gamma (any variation, e.g., gamma1→gamma8)
   *
   * @param sequence - The sequence to analyze
   * @returns Complete circularity analysis
   *
   * @example
   * const analysis = service.analyzeCircularity(sequence);
   * if (analysis.isCircular) {
   *   console.log(`Circular type: ${analysis.circularType}`);
   *   console.log(`Possible CAPs: ${analysis.possibleCapTypes.join(', ')}`);
   * }
   */
  analyzeCircularity(sequence: SequenceData): CircularityAnalysis;

  /**
   * Check if a sequence is circular-capable (simple boolean check)
   *
   * @param sequence - The sequence to check
   * @returns true if the sequence can be completed as a circular pattern
   *
   * @example
   * if (service.isCircularCapable(sequence)) {
   *   // Show sparkles indicator
   * }
   */
  isCircularCapable(sequence: SequenceData): boolean;

  /**
   * Get possible CAP types for a circular sequence
   *
   * Based on the circular type, returns which CAP patterns are possible:
   * - 'same' (distance 0): Returns to exact same position → mirrored/swapped/complementary
   * - 'halved' (distance 4 or 8): Opposite position → halved rotated
   * - 'quartered' (distance 2 or 4): Quarter-turn position → quartered rotated
   *
   * @param sequence - The sequence to analyze
   * @returns Array of possible strict CAP types
   *
   * @example
   * const capTypes = service.getPossibleCapTypes(sequence);
   * // ['rotated'] for quartered sequences (e.g., alpha1→alpha3)
   * // ['mirrored'] for halved sequences (e.g., beta1→beta5)
   * // ['static'] for same-position sequences (e.g., gamma1→gamma1)
   */
  getPossibleCapTypes(sequence: SequenceData): readonly StrictCapType[];

  /**
   * Determine the circular relationship between two positions
   *
   * Works for positions within the same group (alpha→alpha, beta→beta, gamma→gamma).
   *
   * @param startPosition - Starting position (any group)
   * @param endPosition - Ending position (must be same group as start)
   * @returns The circular type or null if not circular
   *
   * @example
   * service.getCircularType(GridPosition.BETA1, GridPosition.BETA3);
   * // Returns: 'quartered' (90° turn)
   *
   * service.getCircularType(GridPosition.ALPHA1, GridPosition.ALPHA5);
   * // Returns: 'halved' (180° turn)
   *
   * service.getCircularType(GridPosition.GAMMA1, GridPosition.GAMMA1);
   * // Returns: 'same' (returns to same position)
   */
  getCircularType(
    startPosition: GridPosition,
    endPosition: GridPosition
  ): CircularType | null;

  /**
   * Check if a position is a beta position
   *
   * @param position - Grid position to check
   * @returns true if the position is a beta position
   *
   * @example
   * service.isBetaPosition(GridPosition.BETA1); // true
   * service.isBetaPosition(GridPosition.ALPHA1); // false
   */
  isBetaPosition(position: GridPosition): boolean;

  /**
   * Get the first beat with valid pictograph data (start beat)
   *
   * @param sequence - The sequence to analyze
   * @returns The first beat with pictograph data, or null
   */
  getStartBeat(sequence: SequenceData): BeatData | null;

  /**
   * Get the last beat with valid pictograph data (end beat)
   *
   * @param sequence - The sequence to analyze
   * @returns The last beat with pictograph data, or null
   */
  getEndBeat(sequence: SequenceData): BeatData | null;

  /**
   * Get a human-readable description of the circular relationship
   *
   * @param analysis - The circularity analysis
   * @returns Descriptive string explaining the relationship
   *
   * @example
   * const desc = service.getCircularDescription(analysis);
   * // "Quartered sequence: beta1 → beta3 (adjacent 90°)"
   */
  getCircularDescription(analysis: CircularityAnalysis): string;

  /**
   * Detect the actual CAP type of a COMPLETED sequence
   *
   * Analyzes all consecutive beat transformations to determine what type
   * of completed CAP pattern the sequence represents.
   *
   * Logic:
   * 1. Static CAP: All beats at the same position
   * 2. Rotated CAP: Each consecutive pair shows 90° rotation
   * 3. Mirrored CAP: Each consecutive pair shows mirroring relationship
   *
   * @param sequence - The completed sequence to analyze
   * @returns Array of CAP types this sequence represents (can be multiple)
   *
   * @example
   * // For a rotated sequence: alpha1 → alpha3 → alpha5 → alpha7 → alpha1
   * service.detectCompletedCapTypes(sequence); // ['rotated']
   *
   * // For a mirrored sequence: gamma1 → gamma9 → gamma1 → gamma9 → gamma1
   * service.detectCompletedCapTypes(sequence); // ['mirrored']
   *
   * // For a static sequence: beta1 → beta1 → beta1 → beta1
   * service.detectCompletedCapTypes(sequence); // ['static']
   */
  detectCompletedCapTypes(sequence: SequenceData): readonly StrictCapType[];
}
