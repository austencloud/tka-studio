/**
 * StrictSwappedCAPExecutor Tests
 *
 * Comprehensive test suite to verify:
 * 1. Validation logic - only accepts valid swapped position pairs
 * 2. Position swapping - correctly maps to swapped positions
 * 3. Color swapping - swaps blue and red motion attributes
 * 4. Motion type preservation - keeps PRO/ANTI the same (but swaps which color has which)
 * 5. Prop rotation preservation - keeps rotation direction the same (but swaps colors)
 * 6. Letter preservation - keeps same letters
 * 7. Sequence completion - doubles the sequence correctly
 * 8. Index mapping - correctly maps second half to first half
 */

import type { BeatData } from "$build/workbench";
import {
  GridLocation,
  GridPosition,
  Letter,
  MotionColor,
  MotionType,
  RotationDirection,
} from "$shared";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { SliceSize } from "../../../../src/lib/modules/build/generate/circular/domain/models/circular-models";
import { StrictSwappedCAPExecutor } from "../../../../src/lib/modules/build/generate/circular/services/implementations/StrictSwappedCAPExecutor";

// Mock dependencies
const mockOrientationService = {
  updateStartOrientations: vi.fn((beat, prevBeat) => beat),
  updateEndOrientations: vi.fn((beat) => beat),
};

const mockGridPositionDeriver = {
  getGridPositionFromLocations: vi.fn((blue, red) => GridPosition.ALPHA1),
};

describe("StrictSwappedCAPExecutor", () => {
  let executor: StrictSwappedCAPExecutor;

  beforeEach(() => {
    executor = new StrictSwappedCAPExecutor(
      mockOrientationService as any,
      mockGridPositionDeriver as any
    );
    vi.clearAllMocks();
  });

  // Helper to create test beats
  const createBeat = (
    beatNumber: number,
    letter: Letter | null,
    startPos: GridPosition | null,
    endPos: GridPosition | null,
    blueMotion: any = {},
    redMotion: any = {}
  ): BeatData => ({
    id: `beat-${beatNumber}`,
    beatNumber,
    letter,
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
    it("should accept valid swapped position pairs - ALPHA1↔ALPHA5", () => {
      const startPos = createBeat(0, null, null, GridPosition.ALPHA1, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.ALPHA1, GridPosition.ALPHA5, {}, {});
      const sequence = [startPos, beat1];

      expect(() => executor.executeCAP(sequence, SliceSize.HALVED)).not.toThrow();
    });

    it("should accept valid swapped position pairs - ALPHA3↔ALPHA7", () => {
      const startPos = createBeat(0, null, null, GridPosition.ALPHA3, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.ALPHA3, GridPosition.ALPHA7, {}, {});
      const sequence = [startPos, beat1];

      expect(() => executor.executeCAP(sequence, SliceSize.HALVED)).not.toThrow();
    });

    it("should accept BETA positions (no change - same side)", () => {
      const startPos = createBeat(0, null, null, GridPosition.BETA1, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.BETA1, GridPosition.BETA1, {}, {});
      const sequence = [startPos, beat1];

      expect(() => executor.executeCAP(sequence, SliceSize.HALVED)).not.toThrow();
    });

    it("should accept GAMMA swapped pairs - GAMMA1↔GAMMA15", () => {
      const startPos = createBeat(0, null, null, GridPosition.GAMMA1, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.GAMMA1, GridPosition.GAMMA15, {}, {});
      const sequence = [startPos, beat1];

      expect(() => executor.executeCAP(sequence, SliceSize.HALVED)).not.toThrow();
    });

    it("should reject invalid swapped position pairs - ALPHA1→ALPHA2", () => {
      const startPos = createBeat(0, null, null, GridPosition.ALPHA1, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.ALPHA1, GridPosition.ALPHA2, {}, {});
      const sequence = [startPos, beat1];

      expect(() => executor.executeCAP(sequence, SliceSize.HALVED)).toThrow(/Invalid position pair for swapped CAP/);
    });

    it("should reject when end position doesn't match swapped version of start", () => {
      const startPos = createBeat(0, null, null, GridPosition.ALPHA1, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.ALPHA1, GridPosition.ALPHA3, {}, {});
      const sequence = [startPos, beat1];

      expect(() => executor.executeCAP(sequence, SliceSize.HALVED)).toThrow(/must end at alpha5/i);
    });

    it("should require at least 2 beats", () => {
      const startPos = createBeat(0, null, null, GridPosition.ALPHA1, {}, {});
      const sequence = [startPos];

      expect(() => executor.executeCAP(sequence, SliceSize.HALVED)).toThrow(/at least 2 beats/);
    });
  });

  describe("Position Swapping", () => {
    it("should swap ALPHA1↔ALPHA5", () => {
      const startPos = createBeat(0, null, null, GridPosition.ALPHA1, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.ALPHA1, GridPosition.ALPHA5, {}, {});
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result).toHaveLength(3);
      expect(result[2].endPosition).toBe(GridPosition.ALPHA1); // Swapped ALPHA5 → ALPHA1
    });

    it("should keep BETA positions unchanged (same-side)", () => {
      const startPos = createBeat(0, null, null, GridPosition.BETA1, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.BETA1, GridPosition.BETA1, {}, {});
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result[2].endPosition).toBe(GridPosition.BETA1); // BETA1 stays BETA1
    });

    it("should cross-swap GAMMA positions - GAMMA1↔GAMMA15", () => {
      const startPos = createBeat(0, null, null, GridPosition.GAMMA1, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.GAMMA1, GridPosition.GAMMA15, {}, {});
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result[2].endPosition).toBe(GridPosition.GAMMA1); // Swapped GAMMA15 → GAMMA1
    });
  });

  describe("Color Swapping (Blue ↔ Red)", () => {
    it("should swap blue and red motion types", () => {
      const startPos = createBeat(
        0,
        null,
        null,
        GridPosition.ALPHA1,
        { endLocation: GridLocation.SOUTH, motionType: MotionType.PRO },
        { endLocation: GridLocation.NORTH, motionType: MotionType.ANTI }
      );
      const beat1 = createBeat(
        1,
        Letter.A,
        GridPosition.ALPHA1,
        GridPosition.ALPHA5,
        {
          startLocation: GridLocation.SOUTH,
          endLocation: GridLocation.NORTH,
          motionType: MotionType.PRO,
        },
        {
          startLocation: GridLocation.NORTH,
          endLocation: GridLocation.SOUTH,
          motionType: MotionType.ANTI,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const swappedBeat = result[2];
      // Blue should now have what red had (ANTI)
      expect(swappedBeat.motions[MotionColor.BLUE]?.motionType).toBe(MotionType.ANTI);
      // Red should now have what blue had (PRO)
      expect(swappedBeat.motions[MotionColor.RED]?.motionType).toBe(MotionType.PRO);
    });

    it("should swap blue and red prop rotation directions", () => {
      const startPos = createBeat(
        0,
        null,
        null,
        GridPosition.ALPHA1,
        { endLocation: GridLocation.SOUTH, rotationDirection: RotationDirection.CLOCKWISE },
        { endLocation: GridLocation.NORTH, rotationDirection: RotationDirection.COUNTER_CLOCKWISE }
      );
      const beat1 = createBeat(
        1,
        Letter.A,
        GridPosition.ALPHA1,
        GridPosition.ALPHA5,
        {
          startLocation: GridLocation.SOUTH,
          endLocation: GridLocation.NORTH,
          rotationDirection: RotationDirection.CLOCKWISE,
        },
        {
          startLocation: GridLocation.NORTH,
          endLocation: GridLocation.SOUTH,
          rotationDirection: RotationDirection.COUNTER_CLOCKWISE,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const swappedBeat = result[2];
      // Blue should now have CCW (from red)
      expect(swappedBeat.motions[MotionColor.BLUE]?.rotationDirection).toBe(
        RotationDirection.COUNTER_CLOCKWISE
      );
      // Red should now have CW (from blue)
      expect(swappedBeat.motions[MotionColor.RED]?.rotationDirection).toBe(
        RotationDirection.CLOCKWISE
      );
    });

    it("should swap blue and red end locations", () => {
      const startPos = createBeat(
        0,
        null,
        null,
        GridPosition.ALPHA1,
        { endLocation: GridLocation.SOUTH },
        { endLocation: GridLocation.NORTH }
      );
      const beat1 = createBeat(
        1,
        Letter.A,
        GridPosition.ALPHA1,
        GridPosition.ALPHA5,
        { startLocation: GridLocation.SOUTH, endLocation: GridLocation.NORTH },
        { startLocation: GridLocation.NORTH, endLocation: GridLocation.SOUTH }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const swappedBeat = result[2];
      // Blue should now have SOUTH (from red)
      expect(swappedBeat.motions[MotionColor.BLUE]?.endLocation).toBe(GridLocation.SOUTH);
      // Red should now have NORTH (from blue)
      expect(swappedBeat.motions[MotionColor.RED]?.endLocation).toBe(GridLocation.NORTH);
    });

    it("should swap blue and red turns", () => {
      const startPos = createBeat(
        0,
        null,
        null,
        GridPosition.ALPHA1,
        { endLocation: GridLocation.SOUTH, turns: 2 },
        { endLocation: GridLocation.NORTH, turns: 1 }
      );
      const beat1 = createBeat(
        1,
        Letter.A,
        GridPosition.ALPHA1,
        GridPosition.ALPHA5,
        { startLocation: GridLocation.SOUTH, endLocation: GridLocation.NORTH, turns: 2 },
        { startLocation: GridLocation.NORTH, endLocation: GridLocation.SOUTH, turns: 1 }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const swappedBeat = result[2];
      // Blue should now have 1 turn (from red)
      expect(swappedBeat.motions[MotionColor.BLUE]?.turns).toBe(1);
      // Red should now have 2 turns (from blue)
      expect(swappedBeat.motions[MotionColor.RED]?.turns).toBe(2);
    });
  });

  describe("Letter Preservation", () => {
    it("should keep the same letter", () => {
      const startPos = createBeat(0, null, null, GridPosition.ALPHA1, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.ALPHA1, GridPosition.ALPHA5, {}, {});
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result[2].letter).toBe(Letter.A); // Same letter
    });
  });

  describe("Sequence Completion", () => {
    it("should double a 1-beat sequence to 2 beats + start", () => {
      const startPos = createBeat(0, null, null, GridPosition.ALPHA1, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.ALPHA1, GridPosition.ALPHA5, {}, {});
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result).toHaveLength(3); // startPos + beat1 + swapped beat2
      expect(result[0].beatNumber).toBe(0);
      expect(result[1].beatNumber).toBe(1);
      expect(result[2].beatNumber).toBe(2);
    });

    it("should double a 2-beat sequence to 4 beats + start", () => {
      const startPos = createBeat(0, null, null, GridPosition.ALPHA1, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.ALPHA1, GridPosition.ALPHA3, {}, {});
      const beat2 = createBeat(2, Letter.B, GridPosition.ALPHA3, GridPosition.ALPHA5, {}, {});
      const sequence = [startPos, beat1, beat2];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result).toHaveLength(5); // startPos + 2 original + 2 swapped
    });

    it("should chain positions correctly", () => {
      const startPos = createBeat(
        0,
        null,
        null,
        GridPosition.ALPHA1,
        { endLocation: GridLocation.SOUTH },
        { endLocation: GridLocation.NORTH }
      );
      const beat1 = createBeat(
        1,
        Letter.A,
        GridPosition.ALPHA1,
        GridPosition.ALPHA5,
        { startLocation: GridLocation.SOUTH, endLocation: GridLocation.NORTH },
        { startLocation: GridLocation.NORTH, endLocation: GridLocation.SOUTH }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      // Beat 2 should start where beat 1 ended
      expect(result[2].startPosition).toBe(GridPosition.ALPHA5);
    });
  });

  describe("Index Mapping (Halved)", () => {
    it("should map beat 2 to beat 1 in a 2-beat sequence", () => {
      const startPos = createBeat(0, null, null, GridPosition.ALPHA1, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.ALPHA1, GridPosition.ALPHA5, {}, {});
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      // Beat 2 should be swapped from beat 1
      expect(result[2].letter).toBe(result[1].letter);
    });

    it("should map beat 3 to beat 1 and beat 4 to beat 2 in a 4-beat sequence", () => {
      const startPos = createBeat(0, null, null, GridPosition.ALPHA1, {}, {});
      const beat1 = createBeat(1, Letter.A, GridPosition.ALPHA1, GridPosition.ALPHA3, {}, {});
      const beat2 = createBeat(2, Letter.B, GridPosition.ALPHA3, GridPosition.ALPHA5, {}, {});
      const sequence = [startPos, beat1, beat2];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      // Beat 3 should swap beat 1
      expect(result[3].letter).toBe(Letter.A);
      // Beat 4 should swap beat 2
      expect(result[4].letter).toBe(Letter.B);
    });
  });
});
