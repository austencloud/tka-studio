/**
 * Base Type 1 Pictograph Generator
 *
 * Abstract base class for all Type 1 pictograph generators.
 * Provides common functionality for PRO/ANTI motion patterns with matching rotations.
 * Generates pictograph data, not just letters.
 */


import { Direction, Letter, PositionSystem, Timing, type PictographData } from "$shared/domain";
import type { IDirectionCalculator, IPictographValidatorService, IPositionPatternService } from "../../../contracts/generate-contracts";
import { BaseLetterGenerator } from "../BaseLetterGenerator";
import {
  calculateDirectionForPositionSystem,
  calculateTimingForPositionSystem,
  getType1MotionPairsFromPattern,
  type Type1LetterConfig
} from "./Type1Configurations";
import {
  getType1MatchingRotationPairs,
  getType1SupportedLetters,
  isType1LetterSupported,
} from "./Type1Utils";

export abstract class BaseType1Generator extends BaseLetterGenerator {
  readonly letter: Letter;

  constructor(
    letter: Letter,
    patternService: IPositionPatternService,
    positionCalculator: IDirectionCalculator,
    validator: IPictographValidatorService
  ) {
    super(patternService, positionCalculator, validator);
    this.letter = letter;
  }

  /**
   * Get the letter configuration for this generator's position system
   * Subclasses must implement this to return their specific configuration
   */
  protected abstract getLetterConfig(): Record<
    string,
    Type1LetterConfig
  >;

  /**
   * Get the position system for this generator
   * Subclasses must implement this to return their specific position system
   */
  protected abstract getPositionSystem(): PositionSystem;

  /**
   * Get the timing for this letter (calculated from position system)
   */
  protected getTiming(): Timing {
    const positionSystemName = this.getPositionSystemName();
    const timing = calculateTimingForPositionSystem(positionSystemName);

    // Gamma system uses QUARTER timing and has 16 positions instead of 8
    // This naturally creates double the variations compared to alpha/beta systems

    return timing;
  }

  /**
   * Get the direction for this letter (calculated from position system)
   */
  protected getDirection(): Direction {
    const positionSystemName = this.getPositionSystemName();
    let direction = calculateDirectionForPositionSystem(positionSystemName);

    // Special handling for gamma-to-gamma letters S-V (they use SAME direction)
    if (
      positionSystemName === "gamma_to_gamma" &&
      ["S", "T", "U", "V"].includes(this.letter)
    ) {
      direction = Direction.SAME;
    }

    return direction;
  }

  /**
   * Get the position system name as a string for calculations
   */
  protected abstract getPositionSystemName(): string;

  /**
   * Create patterns using the Type 1 standard approach
   */
  protected createPatterns(): PictographData[] {
    const config = this.getLetterConfig()[this.letter];
    if (!config) {
      throw new Error(
        `Letter ${this.letter} is not supported by this generator`
      );
    }

    const patterns: PictographData[] = [];

    // Get motion pairs from Type 1 configuration
    const motionPairs = getType1MotionPairsFromPattern(config.motionPattern);

    // Type 1 letters always use matching rotations (CW/CW and CCW/CCW)
    const rotationPairs = getType1MatchingRotationPairs();

    // Generate patterns for each motion pair and each matching rotation pair
    for (const [blueMotion, redMotion] of motionPairs) {
      for (const [blueRotation, redRotation] of rotationPairs) {
        patterns.push(
          this.createPattern({
            timing: this.getTiming(),
            direction: this.getDirection(),
            positionSystem: this.getPositionSystem(),
            baseBlueMotion: blueMotion,
            baseRedMotion: redMotion,
            baseBlueRotation: blueRotation,
            baseRedRotation: redRotation,
          })
        );
      }
    }

    return patterns;
  }

  /**
   * Get all supported letters for this generator
   */
  getSupportedLetters(): string[] {
    return getType1SupportedLetters(this.getLetterConfig());
  }

  /**
   * Check if a letter is supported by this generator
   */
  supportsLetter(letter: string): boolean {
    return isType1LetterSupported(letter, this.getLetterConfig());
  }

  /**
   * Static method to get supported letters (for factory registration)
   * Subclasses should override this to return their specific letters
   */
  static getSupportedLetters(): string[] {
    throw new Error("Subclasses must implement getSupportedLetters()");
  }

  /**
   * Static method to check if a letter is supported (for factory registration)
   * Subclasses should override this to check their specific configuration
   */
  static supportsLetter(_letter: string): boolean {
    throw new Error("Subclasses must implement supportsLetter()");
  }
}
