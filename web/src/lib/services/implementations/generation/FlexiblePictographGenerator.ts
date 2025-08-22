/**
 * Flexible Pattern Engine for TKA Pictograph Generation
 * Handles A-F with data-driven pattern definitions
 */

import type { PictographData } from "$lib/domain/PictographData";
import { createPictographData } from "$lib/domain/PictographData";
import { createMotionData } from "$lib/domain/MotionData";
import { Letter, getLetterType } from "$lib/domain";
import {
  GridPosition,
  Timing,
  Direction,
  MotionType,
  RotationDirection,
  Location,
  MotionColor,
  GridMode,
} from "$lib/domain/enums";

// Pattern Definition System
interface LetterPattern {
  letter: string;
  sequences: PositionSequence[];
  variations: VariationRule[];
  baseParams: BaseParameters;
}

interface PositionSequence {
  name: string;
  positions: GridPosition[];
  timingPattern: Timing[];
  direction: Direction;
}

interface VariationRule {
  name: string;
  blueMotion: MotionType;
  redMotion: MotionType;
  blueRotation: RotationDirection;
  redRotation: RotationDirection;
  sequenceModifier?: "forward" | "reverse";
}

interface BaseParameters {
  letter: string;
}

interface MovementParams {
  letter: string;
  startPosition: GridPosition;
  endPosition: GridPosition;
  timing: Timing;
  direction: Direction;
  blueMotion: MotionType;
  redMotion: MotionType;
  blueRotation: RotationDirection;
  redRotation: RotationDirection;
  blueStartLocation: Location;
  blueEndLocation: Location;
  redStartLocation: Location;
  redEndLocation: Location;
}

export class FlexiblePictographGenerator {
  // Universal position to hand location mapping
  private readonly positionMappings: Record<
    GridPosition,
    [Location, Location]
  > = {
    // Alpha positions (diamond grid)
    [GridPosition.ALPHA1]: [Location.SOUTH, Location.NORTH],
    [GridPosition.ALPHA2]: [Location.SOUTHWEST, Location.NORTHEAST],
    [GridPosition.ALPHA3]: [Location.WEST, Location.EAST],
    [GridPosition.ALPHA4]: [Location.NORTHWEST, Location.SOUTHEAST],
    [GridPosition.ALPHA5]: [Location.NORTH, Location.SOUTH],
    [GridPosition.ALPHA6]: [Location.NORTHEAST, Location.SOUTHWEST],
    [GridPosition.ALPHA7]: [Location.EAST, Location.WEST],
    [GridPosition.ALPHA8]: [Location.SOUTHEAST, Location.NORTHWEST],

    // Beta positions (box grid)
    [GridPosition.BETA1]: [Location.NORTH, Location.NORTH],
    [GridPosition.BETA2]: [Location.NORTHEAST, Location.NORTHEAST],
    [GridPosition.BETA3]: [Location.EAST, Location.EAST],
    [GridPosition.BETA4]: [Location.SOUTHEAST, Location.SOUTHEAST],
    [GridPosition.BETA5]: [Location.SOUTH, Location.SOUTH],
    [GridPosition.BETA6]: [Location.SOUTHWEST, Location.SOUTHWEST],
    [GridPosition.BETA7]: [Location.WEST, Location.WEST],
    [GridPosition.BETA8]: [Location.NORTHWEST, Location.NORTHWEST],

    // Gamma positions
    [GridPosition.GAMMA1]: [Location.WEST, Location.NORTH],
    [GridPosition.GAMMA2]: [Location.NORTHWEST, Location.NORTHEAST],
    [GridPosition.GAMMA3]: [Location.NORTH, Location.EAST],
    [GridPosition.GAMMA4]: [Location.NORTHEAST, Location.SOUTHEAST],
    [GridPosition.GAMMA5]: [Location.EAST, Location.SOUTH],
    [GridPosition.GAMMA6]: [Location.SOUTHEAST, Location.SOUTHWEST],
    [GridPosition.GAMMA7]: [Location.SOUTH, Location.WEST],
    [GridPosition.GAMMA8]: [Location.SOUTHWEST, Location.NORTHWEST],
    [GridPosition.GAMMA9]: [Location.EAST, Location.NORTH],
    [GridPosition.GAMMA10]: [Location.SOUTHEAST, Location.NORTHEAST],
    [GridPosition.GAMMA11]: [Location.SOUTH, Location.EAST],
    [GridPosition.GAMMA12]: [Location.SOUTHWEST, Location.SOUTHEAST],
    [GridPosition.GAMMA13]: [Location.WEST, Location.SOUTH],
    [GridPosition.GAMMA14]: [Location.NORTHWEST, Location.SOUTHWEST],
    [GridPosition.GAMMA15]: [Location.NORTH, Location.WEST],
    [GridPosition.GAMMA16]: [Location.NORTHEAST, Location.NORTHWEST],
  };

  // Pattern Definitions for A-F
  private readonly LETTER_PATTERNS: Record<string, LetterPattern> = {
    A: {
      letter: Letter.A,
      sequences: [
        {
          name: "alpha_cycle",
          positions: [
            GridPosition.ALPHA3,
            GridPosition.ALPHA5,
            GridPosition.ALPHA7,
            GridPosition.ALPHA1,
          ],
          timingPattern: [Timing.SPLIT],
          direction: Direction.SAME,
        },
      ],
      variations: [
        {
          name: "cw",
          blueMotion: MotionType.PRO,
          redMotion: MotionType.PRO,
          blueRotation: RotationDirection.CLOCKWISE,
          redRotation: RotationDirection.CLOCKWISE,
          sequenceModifier: "forward",
        },
        {
          name: "ccw",
          blueMotion: MotionType.PRO,
          redMotion: MotionType.PRO,
          blueRotation: RotationDirection.COUNTER_CLOCKWISE,
          redRotation: RotationDirection.COUNTER_CLOCKWISE,
          sequenceModifier: "reverse",
        },
      ],
      baseParams: { letter: Letter.A },
    },

    B: {
      letter: Letter.B,
      sequences: [
        {
          name: "alpha_cycle",
          positions: [
            GridPosition.ALPHA3,
            GridPosition.ALPHA5,
            GridPosition.ALPHA7,
            GridPosition.ALPHA1,
          ],
          timingPattern: [Timing.SPLIT],
          direction: Direction.SAME,
        },
      ],
      variations: [
        {
          name: "ccw",
          blueMotion: MotionType.ANTI,
          redMotion: MotionType.ANTI,
          blueRotation: RotationDirection.COUNTER_CLOCKWISE,
          redRotation: RotationDirection.COUNTER_CLOCKWISE,
          sequenceModifier: "forward",
        },
        {
          name: "cw",
          blueMotion: MotionType.ANTI,
          redMotion: MotionType.ANTI,
          blueRotation: RotationDirection.CLOCKWISE,
          redRotation: RotationDirection.CLOCKWISE,
          sequenceModifier: "reverse",
        },
      ],
      baseParams: { letter: Letter.B },
    },

    C: {
      letter: Letter.C,
      sequences: [
        {
          name: "alpha_cycle",
          positions: [
            GridPosition.ALPHA3,
            GridPosition.ALPHA5,
            GridPosition.ALPHA7,
            GridPosition.ALPHA1,
          ],
          timingPattern: [Timing.SPLIT],
          direction: Direction.SAME,
        },
      ],
      variations: [
        // First 8: anti/pro combinations
        {
          name: "anti_pro_ccw_cw",
          blueMotion: MotionType.ANTI,
          redMotion: MotionType.PRO,
          blueRotation: RotationDirection.COUNTER_CLOCKWISE,
          redRotation: RotationDirection.CLOCKWISE,
          sequenceModifier: "forward",
        },
        {
          name: "anti_pro_cw_ccw",
          blueMotion: MotionType.ANTI,
          redMotion: MotionType.PRO,
          blueRotation: RotationDirection.CLOCKWISE,
          redRotation: RotationDirection.COUNTER_CLOCKWISE,
          sequenceModifier: "reverse",
        },
        // Second 8: pro/anti combinations
        {
          name: "pro_anti_cw_ccw",
          blueMotion: MotionType.PRO,
          redMotion: MotionType.ANTI,
          blueRotation: RotationDirection.CLOCKWISE,
          redRotation: RotationDirection.COUNTER_CLOCKWISE,
          sequenceModifier: "forward",
        },
        {
          name: "pro_anti_ccw_cw",
          blueMotion: MotionType.PRO,
          redMotion: MotionType.ANTI,
          blueRotation: RotationDirection.COUNTER_CLOCKWISE,
          redRotation: RotationDirection.CLOCKWISE,
          sequenceModifier: "reverse",
        },
      ],
      baseParams: { letter: Letter.C },
    },

    D: {
      letter: Letter.D,
      sequences: [
        {
          name: "beta_alpha_cross",
          positions: [
            GridPosition.BETA3,
            GridPosition.ALPHA5,
            GridPosition.BETA5,
            GridPosition.ALPHA7,
            GridPosition.BETA7,
            GridPosition.ALPHA1,
            GridPosition.BETA1,
            GridPosition.ALPHA3,
          ],
          timingPattern: [Timing.SPLIT, Timing.TOG], // Alternating
          direction: Direction.OPP,
        },
      ],
      variations: [
        {
          name: "ccw_cw",
          blueMotion: MotionType.PRO,
          redMotion: MotionType.PRO,
          blueRotation: RotationDirection.COUNTER_CLOCKWISE,
          redRotation: RotationDirection.CLOCKWISE,
          sequenceModifier: "forward",
        },
        {
          name: "cw_ccw",
          blueMotion: MotionType.PRO,
          redMotion: MotionType.PRO,
          blueRotation: RotationDirection.CLOCKWISE,
          redRotation: RotationDirection.COUNTER_CLOCKWISE,
          sequenceModifier: "reverse",
        },
      ],
      baseParams: { letter: Letter.D },
    },

    E: {
      letter: Letter.E,
      sequences: [
        {
          name: "beta_alpha_cross",
          positions: [
            GridPosition.BETA3,
            GridPosition.ALPHA5,
            GridPosition.BETA5,
            GridPosition.ALPHA7,
            GridPosition.BETA7,
            GridPosition.ALPHA1,
            GridPosition.BETA1,
            GridPosition.ALPHA3,
          ],
          timingPattern: [Timing.SPLIT, Timing.TOG],
          direction: Direction.OPP,
        },
      ],
      variations: [
        {
          name: "cw_ccw",
          blueMotion: MotionType.ANTI,
          redMotion: MotionType.ANTI,
          blueRotation: RotationDirection.CLOCKWISE,
          redRotation: RotationDirection.COUNTER_CLOCKWISE,
          sequenceModifier: "forward",
        },
        {
          name: "ccw_cw",
          blueMotion: MotionType.ANTI,
          redMotion: MotionType.ANTI,
          blueRotation: RotationDirection.COUNTER_CLOCKWISE,
          redRotation: RotationDirection.CLOCKWISE,
          sequenceModifier: "reverse",
        },
      ],
      baseParams: { letter: Letter.E },
    },

    F: {
      letter: Letter.F,
      sequences: [
        {
          name: "beta_alpha_cross",
          positions: [
            GridPosition.BETA3,
            GridPosition.ALPHA5,
            GridPosition.BETA5,
            GridPosition.ALPHA7,
            GridPosition.BETA7,
            GridPosition.ALPHA1,
            GridPosition.BETA1,
            GridPosition.ALPHA3,
          ],
          timingPattern: [Timing.SPLIT, Timing.TOG],
          direction: Direction.OPP,
        },
      ],
      variations: [
        // First 8: anti/pro combinations
        {
          name: "anti_pro_cw_cw",
          blueMotion: MotionType.ANTI,
          redMotion: MotionType.PRO,
          blueRotation: RotationDirection.CLOCKWISE,
          redRotation: RotationDirection.CLOCKWISE,
          sequenceModifier: "forward",
        },
        // Second 8: pro/anti combinations
        {
          name: "pro_anti_ccw_ccw",
          blueMotion: MotionType.PRO,
          redMotion: MotionType.ANTI,
          blueRotation: RotationDirection.COUNTER_CLOCKWISE,
          redRotation: RotationDirection.COUNTER_CLOCKWISE,
          sequenceModifier: "forward",
        },
      ],
      baseParams: { letter: Letter.F },
    },
  };

  // ===== PUBLIC API =====

  generateA(): PictographData[] {
    return this.generateLetter("A");
  }
  generateB(): PictographData[] {
    return this.generateLetter("B");
  }
  generateC(): PictographData[] {
    return this.generateLetter("C");
  }
  generateD(): PictographData[] {
    return this.generateLetter("D");
  }
  generateE(): PictographData[] {
    return this.generateLetter("E");
  }
  generateF(): PictographData[] {
    return this.generateLetter("F");
  }

  /**
   * Get movement counts for validation
   */
  getMovementCounts(): Record<string, number> {
    const counts: Record<string, number> = {};
    ["A", "B", "C", "D", "E", "F"].forEach((letter) => {
      counts[letter] = this.generateLetter(letter).length;
    });
    return counts;
  }

  // ===== CORE ENGINE =====

  /**
   * Generate any letter from pattern definition
   */
  private generateLetter(letter: string): PictographData[] {
    const pattern = this.LETTER_PATTERNS[letter];
    if (!pattern) {
      throw new Error(`No pattern defined for letter: ${letter}`);
    }

    const allMovements: PictographData[] = [];

    // For each sequence in the pattern
    for (const sequence of pattern.sequences) {
      // For each variation rule
      for (const variation of pattern.variations) {
        // Generate movements for this sequence + variation combo
        const movements = this.generateSequenceVariation(
          sequence,
          variation,
          pattern.baseParams
        );
        allMovements.push(...movements);
      }
    }

    return allMovements;
  }

  /**
   * Generate movements for a specific sequence + variation combination
   */
  private generateSequenceVariation(
    sequence: PositionSequence,
    variation: VariationRule,
    baseParams: BaseParameters
  ): PictographData[] {
    const movements: PictographData[] = [];
    let positions = [...sequence.positions];

    // Apply sequence modifier
    if (variation.sequenceModifier === "reverse") {
      // For reverse, we need the reverse traversal order
      // Alpha: [7,5,3,1] or Beta-Alpha cross: reverse pairs
      if (sequence.name === "alpha_cycle") {
        // For counter-clockwise, we want: 7→5, 5→3, 3→1, 1→7
        // So the starting positions should be: [7,5,3,1]
        positions = [
          GridPosition.ALPHA7,
          GridPosition.ALPHA5,
          GridPosition.ALPHA3,
          GridPosition.ALPHA1,
        ];
      } else if (sequence.name === "beta_alpha_cross") {
        positions = [
          GridPosition.BETA7,
          GridPosition.ALPHA5,
          GridPosition.BETA1,
          GridPosition.ALPHA7,
          GridPosition.BETA5,
          GridPosition.ALPHA3,
          GridPosition.BETA3,
          GridPosition.ALPHA1,
        ];
      }
    }

    // Generate movement pairs - for cycles, we need to complete the loop back to start
    for (let i = 0; i < positions.length; i++) {
      const startPosition = positions[i];
      const endPosition = positions[(i + 1) % positions.length]; // Use modulo to wrap back to start
      const timing = sequence.timingPattern[i % sequence.timingPattern.length];

      const movementParams = this.createMovementParams(
        baseParams.letter,
        startPosition,
        endPosition,
        timing,
        sequence.direction,
        variation
      );

      movements.push(this.createPictographFromMovement(movementParams));
    }

    return movements;
  }

  /**
   * Create movement parameters with calculated locations
   */
  private createMovementParams(
    letter: string,
    startPosition: GridPosition,
    endPosition: GridPosition,
    timing: Timing,
    direction: Direction,
    variation: VariationRule
  ): MovementParams {
    const startMapping = this.positionMappings[startPosition];
    const endMapping = this.positionMappings[endPosition];

    if (!startMapping || !endMapping) {
      throw new Error(
        `Position mapping not found for ${startPosition} or ${endPosition}`
      );
    }

    const [blueStart, redStart] = startMapping;
    const [blueEnd, redEnd] = endMapping;

    return {
      letter,
      startPosition: startPosition,
      endPosition: endPosition,
      timing,
      direction,
      blueMotion: variation.blueMotion,
      redMotion: variation.redMotion,
      blueRotation: variation.blueRotation,
      redRotation: variation.redRotation,
      blueStartLocation: blueStart,
      blueEndLocation: blueEnd,
      redStartLocation: redStart,
      redEndLocation: redEnd,
    };
  }

  /**
   * Create complete PictographData from movement parameters
   */
  private createPictographFromMovement(params: MovementParams): PictographData {
    return createPictographData({
      id: crypto.randomUUID(),
      letter: params.letter as Letter, // Use letter string directly - TODO: fix Letter type
      startPosition: params.startPosition,
      endPosition: params.endPosition,
      timing: params.timing,
      direction: params.direction,
      letterType: getLetterType(params.letter as Letter), // Get type from letter string
      gridMode: GridMode.DIAMOND,
      // Arrows and props are now embedded in motions
      motions: {
        blue: createMotionData({
          motionType: params.blueMotion,
          rotationDirection: params.blueRotation,
          startLocation: params.blueStartLocation,
          endLocation: params.blueEndLocation,
          color: MotionColor.BLUE,
        }),
        red: createMotionData({
          motionType: params.redMotion,
          rotationDirection: params.redRotation,
          startLocation: params.redStartLocation,
          endLocation: params.redEndLocation,
          color: MotionColor.RED,
        }),
      },
      isBlank: false,
      metadata: {},
    });
  }
}
