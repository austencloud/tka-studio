/**
 * StrictComplementaryCAPExecutor Tests
 *
 * Comprehensive test suite to verify:
 * 1. Validation logic - only accepts sequences that return to start position
 * 2. Letter complementarity - correctly maps to complementary letters (A↔B, D↔E, etc.)
 * 3. Motion type flipping - flips PRO↔ANTI
 * 4. Prop rotation flipping - flips CW↔CCW
 * 5. Position preservation - end position equals start position
 * 6. Location preservation - keeps same locations
 * 7. Sequence completion - doubles the sequence correctly
 * 8. Index mapping - correctly maps second half to first half
 */

import type { BeatData } from "$shared";
import {
  GridLocation,
  GridPosition,
  MotionColor,
  MotionType,
  RotationDirection,
} from "$shared";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { SliceSize } from "../../../../src/lib/modules/create/generate/circular/domain";
import { StrictComplementaryCAPExecutor } from "../../../../src/lib/modules/create/generate/circular/services/implementations";

// Mock dependencies
const mockOrientationService = {
  updateStartOrientations: vi.fn((beat, prevBeat) => beat),
  updateEndOrientations: vi.fn((beat) => beat),
};

const mockGridPositionDeriver = {
  getGridPositionFromLocations: vi.fn((blue, red) => GridPosition.ALPHA1),
};

describe("StrictComplementaryCAPExecutor", () => {
  let executor: StrictComplementaryCAPExecutor;

  beforeEach(() => {
    executor = new StrictComplementaryCAPExecutor(
      mockOrientationService as any,
      mockGridPositionDeriver as any
    );
    vi.clearAllMocks();
  });

  // Helper to create test beats
  const createBeat = (
    beatNumber: number,
    letter: string,
    startPos: GridPosition | null,
    endPos: GridPosition | null,
    blueMotion: any = {},
    redMotion: any = {}
  ): BeatData => ({
    id: `beat-${beatNumber}`,
    beatNumber,
    letter: letter as any,
    // For beat 0 (start position), both startPosition and endPosition should be the same
    startPosition: beatNumber === 0 ? endPos : startPos,
    endPosition: endPos,
    duration: 1.0,
    blueReversal: false,
    redReversal: false,
    isBlank: false,
    motions: {
      [MotionColor.BLUE]: {
        motionType: MotionType.PRO,
        startLocation: GridLocation.SOUTH,
        endLocation: GridLocation.WEST,
        rotationDirection: RotationDirection.CLOCKWISE,
        startOrientation: null,
        endOrientation: null,
        turns: 1,
        ...blueMotion,
      },
      [MotionColor.RED]: {
        motionType: MotionType.ANTI,
        startLocation: GridLocation.NORTH,
        endLocation: GridLocation.EAST,
        rotationDirection: RotationDirection.COUNTER_CLOCKWISE,
        startOrientation: null,
        endOrientation: null,
        turns: 1,
        ...redMotion,
      },
    },
  });

  describe("Validation", () => {
    it("should accept when end position equals start position - ALPHA1", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      expect(() =>
        executor.executeCAP(sequence, SliceSize.HALVED)
      ).not.toThrow();
    });

    it("should accept when end position equals start position - BETA5", () => {
      const startPos = createBeat(0, "START", null, GridPosition.BETA5, {}, {});
      const beat1 = createBeat(
        1,
        "D",
        GridPosition.BETA5,
        GridPosition.BETA5,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      expect(() =>
        executor.executeCAP(sequence, SliceSize.HALVED)
      ).not.toThrow();
    });

    it("should accept when end position equals start position - GAMMA9", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.GAMMA9,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "J",
        GridPosition.GAMMA9,
        GridPosition.GAMMA9,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      expect(() =>
        executor.executeCAP(sequence, SliceSize.HALVED)
      ).not.toThrow();
    });

    it("should reject when end position doesn't equal start position", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA2,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      expect(() => executor.executeCAP(sequence, SliceSize.HALVED)).toThrow(
        /must end at the same position it started/
      );
    });

    it("should require at least 2 beats", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const sequence = [startPos];

      expect(() => executor.executeCAP(sequence, SliceSize.HALVED)).toThrow(
        /at least 2 beats/
      );
    });
  });

  describe("Complementary Letters", () => {
    it("should map A to B", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result[2]!.letter).toBe("B");
    });

    it("should map B to A", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "B",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result[2]!.letter).toBe("A");
    });

    it("should map D to E", () => {
      const startPos = createBeat(0, "START", null, GridPosition.BETA1, {}, {});
      const beat1 = createBeat(
        1,
        "D",
        GridPosition.BETA1,
        GridPosition.BETA1,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result[2]!.letter).toBe("E");
    });

    it("should map E to D", () => {
      const startPos = createBeat(0, "START", null, GridPosition.BETA1, {}, {});
      const beat1 = createBeat(
        1,
        "E",
        GridPosition.BETA1,
        GridPosition.BETA1,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result[2]!.letter).toBe("D");
    });

    it("should keep self-complementary letter C unchanged", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "C",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result[2]!.letter).toBe("C"); // C → C
    });

    it("should keep self-complementary letter F unchanged", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "F",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result[2]!.letter).toBe("F"); // F → F
    });

    it("should map Greek letters Σ↔Δ", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.GAMMA1,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "Σ",
        GridPosition.GAMMA1,
        GridPosition.GAMMA1,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result[2]!.letter).toBe("Δ");
    });
  });

  describe("Motion Type Flipping", () => {
    it("should flip PRO to ANTI", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        { endLocation: GridLocation.SOUTH, motionType: MotionType.PRO },
        { endLocation: GridLocation.NORTH, motionType: MotionType.PRO }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {
          startLocation: GridLocation.SOUTH,
          endLocation: GridLocation.NORTH,
          motionType: MotionType.PRO,
        },
        {
          startLocation: GridLocation.NORTH,
          endLocation: GridLocation.SOUTH,
          motionType: MotionType.PRO,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const complementaryBeat = result[2];
      expect(complementaryBeat!.motions[MotionColor.BLUE]!.motionType).toBe(
        MotionType.ANTI
      );
      expect(complementaryBeat!.motions[MotionColor.RED]!.motionType).toBe(
        MotionType.ANTI
      );
    });

    it("should flip ANTI to PRO", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        { endLocation: GridLocation.SOUTH, motionType: MotionType.ANTI },
        { endLocation: GridLocation.NORTH, motionType: MotionType.ANTI }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {
          startLocation: GridLocation.SOUTH,
          endLocation: GridLocation.NORTH,
          motionType: MotionType.ANTI,
        },
        {
          startLocation: GridLocation.NORTH,
          endLocation: GridLocation.SOUTH,
          motionType: MotionType.ANTI,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const complementaryBeat = result[2];
      expect(complementaryBeat!.motions[MotionColor.BLUE]!.motionType).toBe(
        MotionType.PRO
      );
      expect(complementaryBeat!.motions[MotionColor.RED]!.motionType).toBe(
        MotionType.PRO
      );
    });

    it("should keep FLOAT unchanged", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        { endLocation: GridLocation.SOUTH, motionType: MotionType.FLOAT },
        { endLocation: GridLocation.NORTH, motionType: MotionType.FLOAT }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {
          startLocation: GridLocation.SOUTH,
          endLocation: GridLocation.NORTH,
          motionType: MotionType.FLOAT,
        },
        {
          startLocation: GridLocation.NORTH,
          endLocation: GridLocation.SOUTH,
          motionType: MotionType.FLOAT,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const complementaryBeat = result[2];
      expect(complementaryBeat!.motions[MotionColor.BLUE]!.motionType).toBe(
        MotionType.FLOAT
      );
    });

    it("should keep DASH unchanged", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        { endLocation: GridLocation.SOUTH, motionType: MotionType.DASH },
        { endLocation: GridLocation.NORTH, motionType: MotionType.DASH }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {
          startLocation: GridLocation.SOUTH,
          endLocation: GridLocation.NORTH,
          motionType: MotionType.DASH,
        },
        {
          startLocation: GridLocation.NORTH,
          endLocation: GridLocation.SOUTH,
          motionType: MotionType.DASH,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const complementaryBeat = result[2];
      expect(complementaryBeat!.motions[MotionColor.BLUE]!.motionType).toBe(
        MotionType.DASH
      );
    });

    it("should keep STATIC unchanged", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.BETA1,
        { endLocation: GridLocation.NORTH, motionType: MotionType.STATIC },
        { endLocation: GridLocation.NORTH, motionType: MotionType.STATIC }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.BETA1,
        GridPosition.BETA1,
        {
          startLocation: GridLocation.NORTH,
          endLocation: GridLocation.NORTH,
          motionType: MotionType.STATIC,
        },
        {
          startLocation: GridLocation.NORTH,
          endLocation: GridLocation.NORTH,
          motionType: MotionType.STATIC,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const complementaryBeat = result[2];
      expect(complementaryBeat!.motions[MotionColor.BLUE]!.motionType).toBe(
        MotionType.STATIC
      );
    });
  });

  describe("Prop Rotation Flipping", () => {
    it("should flip CLOCKWISE to COUNTER_CLOCKWISE", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {
          endLocation: GridLocation.SOUTH,
          rotationDirection: RotationDirection.CLOCKWISE,
        },
        {
          endLocation: GridLocation.NORTH,
          rotationDirection: RotationDirection.CLOCKWISE,
        }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {
          startLocation: GridLocation.SOUTH,
          endLocation: GridLocation.NORTH,
          rotationDirection: RotationDirection.CLOCKWISE,
        },
        {
          startLocation: GridLocation.NORTH,
          endLocation: GridLocation.SOUTH,
          rotationDirection: RotationDirection.CLOCKWISE,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const complementaryBeat = result[2];
      expect(
        complementaryBeat!.motions[MotionColor.BLUE]!.rotationDirection
      ).toBe(RotationDirection.COUNTER_CLOCKWISE);
      expect(
        complementaryBeat!.motions[MotionColor.RED]!.rotationDirection
      ).toBe(RotationDirection.COUNTER_CLOCKWISE);
    });

    it("should flip COUNTER_CLOCKWISE to CLOCKWISE", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {
          endLocation: GridLocation.SOUTH,
          rotationDirection: RotationDirection.COUNTER_CLOCKWISE,
        },
        {
          endLocation: GridLocation.NORTH,
          rotationDirection: RotationDirection.COUNTER_CLOCKWISE,
        }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {
          startLocation: GridLocation.SOUTH,
          endLocation: GridLocation.NORTH,
          rotationDirection: RotationDirection.COUNTER_CLOCKWISE,
        },
        {
          startLocation: GridLocation.NORTH,
          endLocation: GridLocation.SOUTH,
          rotationDirection: RotationDirection.COUNTER_CLOCKWISE,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const complementaryBeat = result[2];
      expect(
        complementaryBeat!.motions[MotionColor.BLUE]!.rotationDirection
      ).toBe(RotationDirection.CLOCKWISE);
    });

    it("should keep NO_ROTATION unchanged", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {
          endLocation: GridLocation.SOUTH,
          rotationDirection: RotationDirection.NO_ROTATION,
        },
        {
          endLocation: GridLocation.NORTH,
          rotationDirection: RotationDirection.NO_ROTATION,
        }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {
          startLocation: GridLocation.SOUTH,
          endLocation: GridLocation.NORTH,
          rotationDirection: RotationDirection.NO_ROTATION,
        },
        {
          startLocation: GridLocation.NORTH,
          endLocation: GridLocation.SOUTH,
          rotationDirection: RotationDirection.NO_ROTATION,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const complementaryBeat = result[2];
      expect(
        complementaryBeat!.motions[MotionColor.BLUE]!.rotationDirection
      ).toBe(RotationDirection.NO_ROTATION);
    });
  });

  describe("Position and Location Preservation", () => {
    it("should keep end position the same as matching beat", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result[2]!.endPosition).toBe(GridPosition.ALPHA1); // Same as beat 1
    });

    it("should keep end locations the same as matching beat", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        { endLocation: GridLocation.SOUTH },
        { endLocation: GridLocation.NORTH }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        { startLocation: GridLocation.SOUTH, endLocation: GridLocation.NORTH },
        { startLocation: GridLocation.NORTH, endLocation: GridLocation.SOUTH }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const complementaryBeat = result[2];
      expect(complementaryBeat!.motions[MotionColor.BLUE]!.endLocation).toBe(
        GridLocation.NORTH
      );
      expect(complementaryBeat!.motions[MotionColor.RED]!.endLocation).toBe(
        GridLocation.SOUTH
      );
    });
  });

  describe("Sequence Completion", () => {
    it("should double a 1-beat sequence to 2 beats + start", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result).toHaveLength(3); // startPos + beat1 + complementary beat2
      expect(result[0]!.beatNumber).toBe(0);
      expect(result[1]!.beatNumber).toBe(1);
      expect(result[2]!.beatNumber).toBe(2);
    });

    it("should double a 2-beat sequence to 4 beats + start", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA3,
        {},
        {}
      );
      const beat2 = createBeat(
        2,
        "D",
        GridPosition.ALPHA3,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const sequence = [startPos, beat1, beat2];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result).toHaveLength(5); // startPos + 2 original + 2 complementary
    });

    it("should chain positions correctly", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        { endLocation: GridLocation.SOUTH },
        { endLocation: GridLocation.NORTH }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        { startLocation: GridLocation.SOUTH, endLocation: GridLocation.NORTH },
        { startLocation: GridLocation.NORTH, endLocation: GridLocation.SOUTH }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      // Beat 2 should start where beat 1 ended
      expect(result[2]!.startPosition).toBe(GridPosition.ALPHA1);
    });
  });

  describe("Index Mapping (Halved)", () => {
    it("should map beat 2 to beat 1 in a 2-beat sequence", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      // Beat 2 should be complementary of beat 1
      expect(result[2]!.letter).toBe("B"); // A → B
    });

    it("should map beat 3 to beat 1 and beat 4 to beat 2 in a 4-beat sequence", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA1,
        GridPosition.ALPHA3,
        {},
        {}
      );
      const beat2 = createBeat(
        2,
        "D",
        GridPosition.ALPHA3,
        GridPosition.ALPHA1,
        {},
        {}
      );
      const sequence = [startPos, beat1, beat2];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      // Beat 3 should complement beat 1 (A → B)
      expect(result[3]!.letter).toBe("B");
      // Beat 4 should complement beat 2 (D → E)
      expect(result[4]!.letter).toBe("E");
    });
  });
});
