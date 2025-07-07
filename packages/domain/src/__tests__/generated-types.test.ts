/**
 * Tests for Generated Types from JSON Schema
 *
 * These tests validate that our schema-generated types work correctly
 * and maintain compatibility with existing code.
 */

import { describe, it, expect } from "vitest";
import type { MotionData } from "../../generated/typescript/motion-data.js";
import type { PictographData } from "../../generated/typescript/pictograph-data.js";
import type { BeatDataSimple } from "../../generated/typescript/beat-data-simple.js";

describe("Generated MotionData Type", () => {
  it("should accept valid motion data", () => {
    const validMotion: MotionData = {
      motionType: "pro",
      propRotDir: "cw",
      startLoc: "n",
      endLoc: "e",
      turns: 1,
      startOri: "in",
      endOri: "out",
    };

    // TypeScript compilation success means the type is correct
    expect(validMotion.motionType).toBe("pro");
    expect(validMotion.turns).toBe(1);
  });

  it("should have correct enum values for motionType", () => {
    const motionTypes: MotionData["motionType"][] = [
      "pro",
      "anti",
      "float",
      "dash",
      "static",
    ];

    motionTypes.forEach((type) => {
      const motion: MotionData = {
        motionType: type,
        propRotDir: "cw",
        startLoc: "n",
        endLoc: "e",
        turns: 0,
        startOri: "in",
        endOri: "in",
      };
      expect(motion.motionType).toBe(type);
    });
  });

  it("should have correct enum values for locations", () => {
    const locations: MotionData["startLoc"][] = [
      "n",
      "e",
      "s",
      "w",
      "ne",
      "nw",
      "se",
      "sw",
    ];

    locations.forEach((loc) => {
      const motion: MotionData = {
        motionType: "pro",
        propRotDir: "cw",
        startLoc: loc,
        endLoc: loc,
        turns: 0,
        startOri: "in",
        endOri: "in",
      };
      expect(motion.startLoc).toBe(loc);
      expect(motion.endLoc).toBe(loc);
    });
  });

  it("should have correct enum values for orientations", () => {
    const orientations: MotionData["startOri"][] = [
      "in",
      "out",
      "clock",
      "counter",
    ];

    orientations.forEach((ori) => {
      const motion: MotionData = {
        motionType: "pro",
        propRotDir: "cw",
        startLoc: "n",
        endLoc: "e",
        turns: 0,
        startOri: ori,
        endOri: ori,
      };
      expect(motion.startOri).toBe(ori);
      expect(motion.endOri).toBe(ori);
    });
  });

  it("should have correct enum values for prop rotation direction", () => {
    const rotDirs: MotionData["propRotDir"][] = ["cw", "ccw", "no_rot"];

    rotDirs.forEach((dir) => {
      const motion: MotionData = {
        motionType: "pro",
        propRotDir: dir,
        startLoc: "n",
        endLoc: "e",
        turns: 0,
        startOri: "in",
        endOri: "in",
      };
      expect(motion.propRotDir).toBe(dir);
    });
  });

  it("should handle numeric turns correctly", () => {
    const motion: MotionData = {
      motionType: "pro",
      propRotDir: "cw",
      startLoc: "n",
      endLoc: "e",
      turns: 3.5,
      startOri: "in",
      endOri: "out",
    };

    expect(typeof motion.turns).toBe("number");
    expect(motion.turns).toBe(3.5);
  });
});

describe("Generated PictographData Type", () => {
  it("should accept valid pictograph data", () => {
    const validPictograph: PictographData = {
      gridMode: "diamond",
      grid: "test-grid",
    };

    expect(validPictograph.gridMode).toBe("diamond");
    expect(validPictograph.grid).toBe("test-grid");
  });

  it("should handle optional fields correctly", () => {
    const pictograph: PictographData = {
      gridMode: "box",
      grid: "test",
      letter: "A",
      startPos: "alpha1",
      endPos: "beta2",
      timing: "split",
      direction: "same",
      isStartPosition: true,
    };

    expect(pictograph.letter).toBe("A");
    expect(pictograph.startPos).toBe("alpha1");
    expect(pictograph.timing).toBe("split");
    expect(pictograph.isStartPosition).toBe(true);
  });
});

describe("Generated BeatDataSimple Type", () => {
  it("should accept valid beat data", () => {
    const validBeat: BeatDataSimple = {
      id: "beat-1",
      beat_number: 1,
      filled: true,
    };

    expect(validBeat.id).toBe("beat-1");
    expect(validBeat.beat_number).toBe(1);
    expect(validBeat.filled).toBe(true);
  });

  it("should handle optional fields correctly", () => {
    const beat: BeatDataSimple = {
      id: "beat-2",
      beat_number: 2,
      filled: false,
      letter: "B",
      duration: 2.5,
    };

    expect(beat.letter).toBe("B");
    expect(beat.duration).toBe(2.5);
  });
});
