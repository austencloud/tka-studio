/**
 * Domain Models Validation Tests
 *
 * These tests validate that the domain models work correctly
 * and maintain compatibility with the Python source.
 */

import { describe, it, expect } from "vitest";
import {
  // Enums
  MotionType,
  Orientation,
  Location,
  RotationDirection,
  LetterType,
  ArrowType,
  PropType,
  GridMode,

  // Utility functions
  createDefaultMotionData,
  createDefaultPictographData,
  createDefaultSequenceData,
  convertOrientation,

  // Letter utilities
  getLetterType,
  LetterTypeClassifier,
} from "../index.js";

describe("Core Enums", () => {
  it("should have correct MotionType values", () => {
    expect(MotionType.PRO).toBe("pro");
    expect(MotionType.ANTI).toBe("anti");
    expect(MotionType.STATIC).toBe("static");
  });

  it("should have correct Orientation values", () => {
    expect(Orientation.IN).toBe("in");
    expect(Orientation.OUT).toBe("out");
    expect(Orientation.CLOCK).toBe("clock");
    expect(Orientation.COUNTER).toBe("counter");
  });

  it("should have correct Location values", () => {
    expect(Location.NORTH).toBe("n");
    expect(Location.EAST).toBe("e");
    expect(Location.SOUTH).toBe("s");
    expect(Location.WEST).toBe("w");
  });
});

describe("Utility Functions", () => {
  it("should create default motion data", () => {
    const motion = createDefaultMotionData();
    expect(motion.motionType).toBe("pro");
    expect(motion.startLoc).toBe("n");
    expect(motion.endLoc).toBe("e");
    expect(motion.turns).toBe(0);
    expect(motion.propRotDir).toBe("cw");
    expect(motion.startOri).toBe("in");
    expect(motion.endOri).toBe("in");
  });

  it("should convert orientation values correctly", () => {
    expect(convertOrientation("in")).toBe(Orientation.IN);
    expect(convertOrientation("OUT")).toBe(Orientation.OUT);
    expect(convertOrientation(0)).toBe(Orientation.IN);
    expect(convertOrientation(180)).toBe(Orientation.OUT);
    expect(convertOrientation("invalid")).toBe(Orientation.IN);
  });

  it("should create default pictograph data", () => {
    const pictograph = createDefaultPictographData();
    expect(pictograph.id).toBeDefined();
    expect(pictograph.arrows.blue).toBeDefined();
    expect(pictograph.arrows.red).toBeDefined();
    expect(pictograph.props.blue).toBeDefined();
    expect(pictograph.props.red).toBeDefined();
    expect(pictograph.is_blank).toBe(false);
  });

  it("should create default sequence data", () => {
    const sequence = createDefaultSequenceData();
    expect(sequence.id).toBeDefined();
    expect(sequence.name).toBe("");
    expect(sequence.beats).toEqual([]);
    expect(sequence.metadata).toEqual({});
  });
});

describe("Letter Type Classifier", () => {
  it("should classify Type1 letters correctly", () => {
    expect(getLetterType("A")).toBe("Type1");
    expect(getLetterType("D")).toBe("Type1");
    expect(getLetterType("V")).toBe("Type1");
  });

  it("should classify Type2 letters correctly", () => {
    expect(getLetterType("W")).toBe("Type2");
    expect(getLetterType("X")).toBe("Type2");
    expect(getLetterType("Σ")).toBe("Type2");
  });

  it("should classify Type3 letters correctly", () => {
    expect(getLetterType("W-")).toBe("Type3");
    expect(getLetterType("X-")).toBe("Type3");
    expect(getLetterType("Σ-")).toBe("Type3");
  });

  it("should default to Type1 for unknown letters", () => {
    expect(getLetterType("Unknown")).toBe("Type1");
    expect(getLetterType("")).toBe("Type1");
  });

  it("should get letters for specific types", () => {
    const type1Letters = LetterTypeClassifier.getLettersForType("Type1");
    expect(type1Letters).toContain("A");
    expect(type1Letters).toContain("D");
    expect(type1Letters.length).toBeGreaterThan(0);
  });

  it("should provide classification statistics", () => {
    const stats = LetterTypeClassifier.getClassificationStats();
    expect(stats.Type1).toBeGreaterThan(0);
    expect(stats.Type2).toBeGreaterThan(0);
    expect(typeof stats.Type1).toBe("number");
  });
});

describe("Arrow and Prop Types", () => {
  it("should have correct ArrowType values", () => {
    expect(ArrowType.BLUE).toBe("blue");
    expect(ArrowType.RED).toBe("red");
  });

  it("should have correct PropType values", () => {
    expect(PropType.STAFF).toBe("staff");
    expect(PropType.HAND).toBe("hand");
    expect(PropType.CLUB).toBe("club");
  });
});

describe("Grid Mode", () => {
  it("should have correct GridMode values", () => {
    expect(GridMode.DIAMOND).toBe("diamond");
    expect(GridMode.BOX).toBe("box");
  });
});
