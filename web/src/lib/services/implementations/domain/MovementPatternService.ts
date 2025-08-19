/**
 * Movement Pattern Service - Movement pattern templates and variations
 *
 * Creates movement patterns from templates and generates variations.
 * Manages position sequences and pattern combinations for movement generation.
 */

import type { IMovementPatternService } from "../../interfaces/generation-interfaces";
import type { MovementPattern } from "$lib/domain/MovementData";
import { createMovementPattern } from "$lib/domain/MovementData";
import {
  GridPosition,
  Timing,
  Direction,
  MotionType,
  RotationDirection,
} from "$lib/domain/enums";

export class MovementPatternService implements IMovementPatternService {
  createPattern(
    letter: string,
    config: Partial<MovementPattern>
  ): MovementPattern {
    return createMovementPattern({
      letter,
      ...config,
    });
  }

  getAlphaSequence(): GridPosition[] {
    return [
      GridPosition.ALPHA3,
      GridPosition.ALPHA5,
      GridPosition.ALPHA7,
      GridPosition.ALPHA1,
    ];
  }

  getBetaSequence(): GridPosition[] {
    return [
      GridPosition.BETA3,
      GridPosition.BETA5,
      GridPosition.BETA7,
      GridPosition.BETA1,
    ];
  }

  getGammaSequence(): GridPosition[] {
    return [
      GridPosition.GAMMA3,
      GridPosition.GAMMA5,
      GridPosition.GAMMA7,
      GridPosition.GAMMA1,
      GridPosition.GAMMA11,
      GridPosition.GAMMA13,
      GridPosition.GAMMA15,
      GridPosition.GAMMA9,
    ];
  }

  getCustomSequence(positions: GridPosition[]): GridPosition[] {
    return [...positions];
  }

  createVariations(
    basePattern: MovementPattern,
    variations: Array<{
      motionCombination: [string, string];
      rotationCombination: [string, string];
    }>
  ): MovementPattern[] {
    return variations.map((variation, index) => {
      const [blueMotion, redMotion] = variation.motionCombination;
      const [blueRotation, redRotation] = variation.rotationCombination;

      return createMovementPattern({
        ...basePattern,
        letter: `${basePattern.letter}_${index + 1}`,
        baseBlueMotion: blueMotion as MotionType,
        baseRedMotion: redMotion as MotionType,
        baseBlueRotation: blueRotation as RotationDirection,
        baseRedRotation: redRotation as RotationDirection,
      });
    });
  }

  /**
   * Get predefined pattern templates for standard letters
   */
  getPatternA(): MovementPattern {
    return this.createPattern("A", {
      timing: Timing.SPLIT,
      direction: Direction.SAME,
      positionSystem: "alpha",
      baseBlueMotion: MotionType.PRO,
      baseRedMotion: MotionType.PRO,
      baseBlueRotation: RotationDirection.CLOCKWISE,
      baseRedRotation: RotationDirection.CLOCKWISE,
    });
  }

  getPatternB(): MovementPattern {
    return this.createPattern("B", {
      timing: Timing.SPLIT,
      direction: Direction.SAME,
      positionSystem: "alpha",
      baseBlueMotion: MotionType.ANTI,
      baseRedMotion: MotionType.ANTI,
      baseBlueRotation: RotationDirection.COUNTER_CLOCKWISE,
      baseRedRotation: RotationDirection.COUNTER_CLOCKWISE,
    });
  }

  getPatternC(): MovementPattern {
    return this.createPattern("C", {
      timing: Timing.SPLIT,
      direction: Direction.SAME,
      positionSystem: "alpha",
      baseBlueMotion: MotionType.ANTI,
      baseRedMotion: MotionType.PRO,
      baseBlueRotation: RotationDirection.COUNTER_CLOCKWISE,
      baseRedRotation: RotationDirection.CLOCKWISE,
      variations: [
        {
          name: "reversed",
          blueMotionType: MotionType.PRO,
          redMotionType: MotionType.ANTI,
          blueRotation: RotationDirection.CLOCKWISE,
          redRotation: RotationDirection.COUNTER_CLOCKWISE,
        },
      ],
    });
  }

  getPatternG(): MovementPattern {
    return this.createPattern("G", {
      timing: Timing.TOG,
      direction: Direction.SAME,
      positionSystem: "beta",
      baseBlueMotion: MotionType.PRO,
      baseRedMotion: MotionType.PRO,
      baseBlueRotation: RotationDirection.CLOCKWISE,
      baseRedRotation: RotationDirection.CLOCKWISE,
    });
  }

  getPatternM(): MovementPattern {
    return this.createPattern("M", {
      timing: Timing.QUARTER,
      direction: Direction.OPP,
      positionSystem: "gamma",
      baseBlueMotion: MotionType.PRO,
      baseRedMotion: MotionType.PRO,
      baseBlueRotation: RotationDirection.COUNTER_CLOCKWISE,
      baseRedRotation: RotationDirection.CLOCKWISE,
    });
  }

  getPatternW(): MovementPattern {
    return this.createPattern("W", {
      timing: Timing.NONE,
      direction: Direction.NONE,
      positionSystem: "gamma",
      baseBlueMotion: MotionType.STATIC,
      baseRedMotion: MotionType.PRO,
      baseBlueRotation: RotationDirection.NO_ROTATION,
      baseRedRotation: RotationDirection.CLOCKWISE,
      variations: [
        {
          name: "reversed",
          blueMotionType: MotionType.PRO,
          redMotionType: MotionType.STATIC,
          blueRotation: RotationDirection.CLOCKWISE,
          redRotation: RotationDirection.NO_ROTATION,
        },
      ],
    });
  }

  getPatternWDash(): MovementPattern {
    return this.createPattern("W-", {
      timing: Timing.NONE,
      direction: Direction.NONE,
      positionSystem: "gamma",
      baseBlueMotion: MotionType.DASH,
      baseRedMotion: MotionType.PRO,
      baseBlueRotation: RotationDirection.NO_ROTATION,
      baseRedRotation: RotationDirection.CLOCKWISE,
      variations: [
        {
          name: "reversed",
          blueMotionType: MotionType.PRO,
          redMotionType: MotionType.DASH,
          blueRotation: RotationDirection.CLOCKWISE,
          redRotation: RotationDirection.NO_ROTATION,
        },
      ],
    });
  }

  getPatternAlpha(): MovementPattern {
    return this.createPattern("α", {
      timing: Timing.NONE,
      direction: Direction.NONE,
      positionSystem: "alpha",
      baseBlueMotion: MotionType.STATIC,
      baseRedMotion: MotionType.STATIC,
      baseBlueRotation: RotationDirection.NO_ROTATION,
      baseRedRotation: RotationDirection.NO_ROTATION,
    });
  }

  /**
   * Generate position sequence based on pattern system
   */
  generatePositionSequence(
    pattern: MovementPattern,
    length: number = 8
  ): GridPosition[] {
    const baseSequence = this.getSequenceBySystem(pattern.positionSystem);
    const result: GridPosition[] = [];

    for (let i = 0; i < length; i++) {
      result.push(baseSequence[i % baseSequence.length]);
    }

    return result;
  }

  private getSequenceBySystem(
    system: "alpha" | "beta" | "gamma"
  ): GridPosition[] {
    switch (system) {
      case "alpha":
        return this.getAlphaSequence();
      case "beta":
        return this.getBetaSequence();
      case "gamma":
        return this.getGammaSequence();
      default:
        throw new Error(`Unknown position system: ${system}`);
    }
  }
}
