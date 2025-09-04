/**
 * Base Letter Generator
 *
 * Abstract base class providing common functionality for all letter generators.
 * Handles pattern creation, movement generation, and caching.
 */

import type { MotionData, PictographData } from "$domain";
import {
  Direction,
  Letter,
  MotionType,
  PositionSystem,
  RotationDirection,
  Timing,
  createPictographData,
} from "$domain";
import type {
  IDirectionCalculator,
  ILetterGenerator,
  IPictographValidatorService,
  IPositionPatternService
} from "$services";

export abstract class BaseLetterGenerator implements ILetterGenerator {
  private static readonly movementCache = new Map<string, PictographData>();

  constructor(
    protected readonly patternService: IPositionPatternService,
    protected readonly positionCalculator: IDirectionCalculator,
    protected readonly validator: IPictographValidatorService
  ) {}

  abstract readonly letter: Letter;

  /**
   * Generate movement set for this letter
   * Template method - subclasses implement createPatterns()
   */
  generate(): PictographData {
    const cacheKey = this.createCacheKey();

    if (BaseLetterGenerator.movementCache.has(cacheKey)) {
      const cached = BaseLetterGenerator.movementCache.get(cacheKey);
      if (cached) {
        return cached;
      }
    }

    const patterns = this.createPatterns();

    // For now, use the first pattern to generate the pictograph
    const pattern = patterns[0];
    const motions = this.generateMotionsFromPattern(pattern);

    const pictographData = createPictographData({
      letter: this.letter,
      motions,
      startPosition: pattern.startPosition,
      endPosition: pattern.endPosition,
    });

    if (!this.validator.validatePictograph(pictographData)) {
      throw new Error(`Generated invalid movement set for ${this.letter}`);
    }

    BaseLetterGenerator.movementCache.set(cacheKey, pictographData);
    return pictographData;
  }

  /**
   * Create patterns for this letter
   * Subclasses must implement this method
   */
  protected abstract createPatterns(): PictographData[];

  /**
   * Helper method to create a standard pattern
   */
  protected createPattern(_config: {
    timing: Timing;
    direction: Direction;
    positionSystem: PositionSystem;
    baseBlueMotion: MotionType;
    baseRedMotion: MotionType;
    baseBlueRotation: RotationDirection;
    baseRedRotation: RotationDirection;
  }): PictographData {
    // This is a placeholder - subclasses should implement specific pattern logic
    return createPictographData({
      letter: this.letter,
      motions: {},
    });
  }

  /**
   * Generate motions from a pattern
   * Subclasses should override this for specific letter logic
   */
  private generateMotionsFromPattern(
    pattern: PictographData
  ): Partial<Record<import("$domain").MotionColor, MotionData>> {
    // Default implementation - subclasses should override
    return pattern.motions;
  }

  /**
   * Create cache key for this letter
   */
  private createCacheKey(): string {
    return `movement-${this.letter}`;
  }
}
