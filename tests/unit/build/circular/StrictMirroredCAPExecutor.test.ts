/**
 * StrictMirroredCAPExecutor Tests
 *
 * Comprehensive test suite to verify:
 * 1. Validation logic - only accepts valid mirrored position pairs
 * 2. Position mirroring - correctly mirrors positions vertically
 * 3. Location mirroring - correctly mirrors locations (E↔W, NE↔NW, etc.)
 * 4. Prop rotation flipping - correctly flips CW↔CCW
 * 5. Motion type preservation - keeps PRO/ANTI the same
 * 6. Letter preservation - keeps same letters
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
import { StrictMirroredCAPExecutor } from "../../../../src/lib/modules/create/generate/circular/services/implementations";

// Mock dependencies
const mockOrientationService = {
  updateStartOrientations: vi.fn((beat, prevBeat) => beat),
  updateEndOrientations: vi.fn((beat) => beat),
};

const mockGridPositionDeriver = {
  getGridPositionFromLocations: vi.fn((blue, red) => GridPosition.ALPHA1),
};

describe("StrictMirroredCAPExecutor", () => {
  let executor: StrictMirroredCAPExecutor;

  beforeEach(() => {
    executor = new StrictMirroredCAPExecutor(
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
        propRotationDirection: RotationDirection.CLOCKWISE,
        startOrientation: null,
        endOrientation: null,
        turns: 1,
        ...blueMotion,
      },
      [MotionColor.RED]: {
        motionType: MotionType.ANTI,
        startLocation: GridLocation.NORTH,
        endLocation: GridLocation.EAST,
        propRotationDirection: RotationDirection.COUNTER_CLOCKWISE,
        startOrientation: null,
        endOrientation: null,
        turns: 1,
        ...redMotion,
      },
    },
  });

  describe("Validation", () => {
    it("should accept valid mirrored position pairs - ALPHA2↔ALPHA8", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA8,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      expect(() =>
        executor.executeCAP(sequence, SliceSize.HALVED)
      ).not.toThrow();
    });

    it("should accept valid mirrored position pairs - ALPHA3↔ALPHA7", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA3,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA3,
        GridPosition.ALPHA7,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      expect(() =>
        executor.executeCAP(sequence, SliceSize.HALVED)
      ).not.toThrow();
    });

    it("should accept valid mirrored position pairs - GAMMA1↔GAMMA9", () => {
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
        "A",
        GridPosition.GAMMA1,
        GridPosition.GAMMA9,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      expect(() =>
        executor.executeCAP(sequence, SliceSize.HALVED)
      ).not.toThrow();
    });

    it("should reject invalid mirrored position pairs - ALPHA1→ALPHA2", () => {
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
        /Invalid position pair for mirrored CAP/
      );
    });

    it("should reject when end position doesn't match mirror of start", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA3,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      expect(() => executor.executeCAP(sequence, SliceSize.HALVED)).toThrow(
        /must end at alpha8/i
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

  describe("Position Mirroring", () => {
    it("should mirror ALPHA positions vertically", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA8,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      // Result should have 3 beats: startPos + beat1 + mirrored beat2
      expect(result).toHaveLength(3);
      expect(result[2]!.endPosition).toBe(GridPosition.ALPHA2); // Mirrored ALPHA8 → ALPHA2
    });

    it("should keep ALPHA1 and ALPHA5 on vertical axis", () => {
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

      expect(result[2]!.endPosition).toBe(GridPosition.ALPHA1); // Stays on axis
    });

    it("should cross-mirror GAMMA positions", () => {
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
        "A",
        GridPosition.GAMMA1,
        GridPosition.GAMMA9,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result[2]!.endPosition).toBe(GridPosition.GAMMA1); // Mirrored GAMMA9 → GAMMA1
    });
  });

  describe("Location Mirroring", () => {
    it("should mirror EAST to WEST", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA3,
        { endLocation: GridLocation.WEST },
        { endLocation: GridLocation.EAST }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA3,
        GridPosition.ALPHA7,
        { startLocation: GridLocation.WEST, endLocation: GridLocation.EAST },
        { startLocation: GridLocation.EAST, endLocation: GridLocation.WEST }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const mirroredBeat = result[2];
      // EAST should mirror to WEST
      expect(mirroredBeat!.motions[MotionColor.BLUE]!.endLocation).toBe(
        GridLocation.WEST
      );
    });

    it("should mirror NORTHEAST to NORTHWEST", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        { endLocation: GridLocation.SOUTHWEST },
        { endLocation: GridLocation.NORTHEAST }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA8,
        {
          startLocation: GridLocation.SOUTHWEST,
          endLocation: GridLocation.NORTHEAST,
        },
        {
          startLocation: GridLocation.NORTHEAST,
          endLocation: GridLocation.SOUTHWEST,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const mirroredBeat = result[2];
      // NORTHEAST should mirror to NORTHWEST
      expect(mirroredBeat!.motions[MotionColor.BLUE]!.endLocation).toBe(
        GridLocation.NORTHWEST
      );
    });

    it("should keep NORTH and SOUTH on vertical axis", () => {
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

      const mirroredBeat = result[2];
      // NORTH stays NORTH (on axis)
      expect(mirroredBeat!.motions[MotionColor.BLUE]!.endLocation).toBe(
        GridLocation.NORTH
      );
    });
  });

  describe("Prop Rotation Flipping", () => {
    it("should flip CLOCKWISE to COUNTER_CLOCKWISE", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        {
          endLocation: GridLocation.SOUTHWEST,
          propRotationDirection: RotationDirection.CLOCKWISE,
        },
        {
          endLocation: GridLocation.NORTHEAST,
          propRotationDirection: RotationDirection.CLOCKWISE,
        }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA8,
        {
          startLocation: GridLocation.SOUTHWEST,
          endLocation: GridLocation.NORTHEAST,
          propRotationDirection: RotationDirection.CLOCKWISE,
        },
        {
          startLocation: GridLocation.NORTHEAST,
          endLocation: GridLocation.SOUTHWEST,
          propRotationDirection: RotationDirection.CLOCKWISE,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const mirroredBeat = result[2];
      expect(mirroredBeat!.motions[MotionColor.BLUE]!.rotationDirection).toBe(
        RotationDirection.COUNTER_CLOCKWISE
      );
      expect(mirroredBeat!.motions[MotionColor.RED]!.rotationDirection).toBe(
        RotationDirection.COUNTER_CLOCKWISE
      );
    });

    it("should flip COUNTER_CLOCKWISE to CLOCKWISE", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        {
          endLocation: GridLocation.SOUTHWEST,
          propRotationDirection: RotationDirection.COUNTER_CLOCKWISE,
        },
        {
          endLocation: GridLocation.NORTHEAST,
          propRotationDirection: RotationDirection.COUNTER_CLOCKWISE,
        }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA8,
        {
          startLocation: GridLocation.SOUTHWEST,
          endLocation: GridLocation.NORTHEAST,
          propRotationDirection: RotationDirection.COUNTER_CLOCKWISE,
        },
        {
          startLocation: GridLocation.NORTHEAST,
          endLocation: GridLocation.SOUTHWEST,
          propRotationDirection: RotationDirection.COUNTER_CLOCKWISE,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const mirroredBeat = result[2];
      expect(mirroredBeat!.motions[MotionColor.BLUE]!.rotationDirection).toBe(
        RotationDirection.CLOCKWISE
      );
    });

    it("should keep NO_ROTATION unchanged", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        {
          endLocation: GridLocation.SOUTHWEST,
          propRotationDirection: RotationDirection.NO_ROTATION,
        },
        {
          endLocation: GridLocation.NORTHEAST,
          propRotationDirection: RotationDirection.NO_ROTATION,
        }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA8,
        {
          startLocation: GridLocation.SOUTHWEST,
          endLocation: GridLocation.NORTHEAST,
          propRotationDirection: RotationDirection.NO_ROTATION,
        },
        {
          startLocation: GridLocation.NORTHEAST,
          endLocation: GridLocation.SOUTHWEST,
          propRotationDirection: RotationDirection.NO_ROTATION,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const mirroredBeat = result[2];
      expect(mirroredBeat!.motions[MotionColor.BLUE]!.rotationDirection).toBe(
        RotationDirection.NO_ROTATION
      );
    });
  });

  describe("Motion Type Preservation", () => {
    it("should keep PRO as PRO", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        { endLocation: GridLocation.SOUTHWEST, motionType: MotionType.PRO },
        { endLocation: GridLocation.NORTHEAST, motionType: MotionType.PRO }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA8,
        {
          startLocation: GridLocation.SOUTHWEST,
          endLocation: GridLocation.NORTHEAST,
          motionType: MotionType.PRO,
        },
        {
          startLocation: GridLocation.NORTHEAST,
          endLocation: GridLocation.SOUTHWEST,
          motionType: MotionType.PRO,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const mirroredBeat = result[2];
      expect(mirroredBeat!.motions[MotionColor.BLUE]!.motionType).toBe(
        MotionType.PRO
      );
      expect(mirroredBeat!.motions[MotionColor.RED]!.motionType).toBe(
        MotionType.PRO
      );
    });

    it("should keep ANTI as ANTI", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        { endLocation: GridLocation.SOUTHWEST, motionType: MotionType.ANTI },
        { endLocation: GridLocation.NORTHEAST, motionType: MotionType.ANTI }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA8,
        {
          startLocation: GridLocation.SOUTHWEST,
          endLocation: GridLocation.NORTHEAST,
          motionType: MotionType.ANTI,
        },
        {
          startLocation: GridLocation.NORTHEAST,
          endLocation: GridLocation.SOUTHWEST,
          motionType: MotionType.ANTI,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      const mirroredBeat = result[2];
      expect(mirroredBeat!.motions[MotionColor.BLUE]!.motionType).toBe(
        MotionType.ANTI
      );
    });
  });

  describe("Letter Preservation", () => {
    it("should keep the same letter", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA8,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result[2]!.letter).toBe("A"); // Same letter
    });
  });

  describe("Sequence Completion", () => {
    it("should double a 1-beat sequence to 2 beats + start", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA8,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result).toHaveLength(3); // startPos + beat1 + mirrored beat2
      expect(result[0]!.beatNumber).toBe(0);
      expect(result[1]!.beatNumber).toBe(1);
      expect(result[2]!.beatNumber).toBe(2);
    });

    it("should double a 2-beat sequence to 4 beats + start", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA4,
        {},
        {}
      );
      const beat2 = createBeat(
        2,
        "B",
        GridPosition.ALPHA4,
        GridPosition.ALPHA8,
        {},
        {}
      );
      const sequence = [startPos, beat1, beat2];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      expect(result).toHaveLength(5); // startPos + 2 original + 2 mirrored
    });

    it("should chain positions correctly", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        { endLocation: GridLocation.SOUTHWEST },
        { endLocation: GridLocation.NORTHEAST }
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA8,
        {
          startLocation: GridLocation.SOUTHWEST,
          endLocation: GridLocation.NORTHEAST,
        },
        {
          startLocation: GridLocation.NORTHEAST,
          endLocation: GridLocation.SOUTHWEST,
        }
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      // Beat 2 should start where beat 1 ended
      expect(result[2]!.startPosition).toBe(GridPosition.ALPHA8);
    });
  });

  describe("Index Mapping (Halved)", () => {
    it("should map beat 2 to beat 1 in a 2-beat sequence", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA8,
        {},
        {}
      );
      const sequence = [startPos, beat1];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      // Beat 2 should be mirrored from beat 1
      expect(result[2]!.letter).toBe(result[1]!.letter);
    });

    it("should map beat 3 to beat 1 and beat 4 to beat 2 in a 4-beat sequence", () => {
      const startPos = createBeat(
        0,
        "START",
        null,
        GridPosition.ALPHA2,
        {},
        {}
      );
      const beat1 = createBeat(
        1,
        "A",
        GridPosition.ALPHA2,
        GridPosition.ALPHA4,
        {},
        {}
      );
      const beat2 = createBeat(
        2,
        "B",
        GridPosition.ALPHA4,
        GridPosition.ALPHA8,
        {},
        {}
      );
      const sequence = [startPos, beat1, beat2];

      const result = executor.executeCAP(sequence, SliceSize.HALVED);

      // Beat 3 should mirror beat 1
      expect(result[3]!.letter).toBe("A");
      // Beat 4 should mirror beat 2
      expect(result[4]!.letter).toBe("B");
    });
  });
});
