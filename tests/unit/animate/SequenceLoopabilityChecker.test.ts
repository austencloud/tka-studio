/**
 * Sequence Loopability Checker Tests
 *
 * Tests for detecting if a sequence can loop seamlessly
 * (ends in the same position/orientation as it starts).
 */

import { describe, it, expect } from "vitest";
import { SequenceLoopabilityChecker } from "$lib/modules/create/animate/services/implementations/SequenceLoopabilityChecker";
import { createBeatData } from "$lib/modules/create/shared/domain/factories/createBeatData";
import { GridPosition } from "$lib/shared/pictograph/grid/domain/enums/grid-enums";
import {
  Orientation,
  MotionColor,
} from "$lib/shared/pictograph/shared/domain/enums/pictograph-enums";
import { createSequenceData } from "$lib/shared/foundation/domain/models/SequenceData";

describe("SequenceLoopabilityChecker", () => {
  const checker = new SequenceLoopabilityChecker();

  describe("isSeamlesslyLoopable", () => {
    it("should return false for empty sequence", () => {
      const sequence = createSequenceData({
        id: "test",
        word: "TEST",
        author: "Test",
        beats: [],
      });

      expect(checker.isSeamlesslyLoopable(sequence)).toBe(false);
    });

    it("should return true when sequence ends in same position and orientation", () => {
      const sequence = createSequenceData({
        id: "test",
        word: "TEST",
        author: "Test",
        beats: [
          createBeatData({
            beatNumber: 1,
            startPosition: GridPosition.ALPHA1,
            endPosition: GridPosition.ALPHA2,
            motions: {
              [MotionColor.BLUE]: {
                startOrientation: Orientation.IN,
                endOrientation: Orientation.OUT,
              } as any,
              [MotionColor.RED]: {
                startOrientation: Orientation.OUT,
                endOrientation: Orientation.IN,
              } as any,
            },
          }),
          createBeatData({
            beatNumber: 2,
            startPosition: GridPosition.ALPHA2,
            endPosition: GridPosition.ALPHA1,
            motions: {
              [MotionColor.BLUE]: {
                startOrientation: Orientation.OUT,
                endOrientation: Orientation.IN, // Matches first beat's start
              } as any,
              [MotionColor.RED]: {
                startOrientation: Orientation.IN,
                endOrientation: Orientation.OUT, // Matches first beat's start
              } as any,
            },
          }),
        ],
      });

      expect(checker.isSeamlesslyLoopable(sequence)).toBe(true);
    });

    it("should return false when positions don't match", () => {
      const sequence = createSequenceData({
        id: "test",
        word: "TEST",
        author: "Test",
        beats: [
          createBeatData({
            beatNumber: 1,
            startPosition: GridPosition.ALPHA1,
            endPosition: GridPosition.ALPHA2,
            motions: {
              [MotionColor.BLUE]: {
                startOrientation: Orientation.IN,
                endOrientation: Orientation.OUT,
              } as any,
            },
          }),
          createBeatData({
            beatNumber: 2,
            startPosition: GridPosition.ALPHA2,
            endPosition: GridPosition.ALPHA3, // Different from first beat's start
            motions: {
              [MotionColor.BLUE]: {
                startOrientation: Orientation.OUT,
                endOrientation: Orientation.IN,
              } as any,
            },
          }),
        ],
      });

      expect(checker.isSeamlesslyLoopable(sequence)).toBe(false);
    });

    it("should return false when blue orientations don't match", () => {
      const sequence = createSequenceData({
        id: "test",
        word: "TEST",
        author: "Test",
        beats: [
          createBeatData({
            beatNumber: 1,
            startPosition: GridPosition.ALPHA1,
            endPosition: GridPosition.ALPHA2,
            motions: {
              [MotionColor.BLUE]: {
                startOrientation: Orientation.IN,
                endOrientation: Orientation.OUT,
              } as any,
            },
          }),
          createBeatData({
            beatNumber: 2,
            startPosition: GridPosition.ALPHA2,
            endPosition: GridPosition.ALPHA1,
            motions: {
              [MotionColor.BLUE]: {
                startOrientation: Orientation.OUT,
                endOrientation: Orientation.OUT, // Should be IN to match
              } as any,
            },
          }),
        ],
      });

      expect(checker.isSeamlesslyLoopable(sequence)).toBe(false);
    });

    it("should return false when red orientations don't match", () => {
      const sequence = createSequenceData({
        id: "test",
        word: "TEST",
        author: "Test",
        beats: [
          createBeatData({
            beatNumber: 1,
            startPosition: GridPosition.ALPHA1,
            endPosition: GridPosition.ALPHA2,
            motions: {
              [MotionColor.BLUE]: {
                startOrientation: Orientation.IN,
                endOrientation: Orientation.OUT,
              } as any,
              [MotionColor.RED]: {
                startOrientation: Orientation.OUT,
                endOrientation: Orientation.IN,
              } as any,
            },
          }),
          createBeatData({
            beatNumber: 2,
            startPosition: GridPosition.ALPHA2,
            endPosition: GridPosition.ALPHA1,
            motions: {
              [MotionColor.BLUE]: {
                startOrientation: Orientation.OUT,
                endOrientation: Orientation.IN,
              } as any,
              [MotionColor.RED]: {
                startOrientation: Orientation.IN,
                endOrientation: Orientation.IN, // Should be OUT to match
              } as any,
            },
          }),
        ],
      });

      expect(checker.isSeamlesslyLoopable(sequence)).toBe(false);
    });

    it("should return false when first beat has motion but last beat doesn't", () => {
      const sequence = createSequenceData({
        id: "test",
        word: "TEST",
        author: "Test",
        beats: [
          createBeatData({
            beatNumber: 1,
            startPosition: GridPosition.ALPHA1,
            endPosition: GridPosition.ALPHA2,
            motions: {
              [MotionColor.BLUE]: {
                startOrientation: Orientation.IN,
                endOrientation: Orientation.OUT,
              } as any,
            },
          }),
          createBeatData({
            beatNumber: 2,
            startPosition: GridPosition.ALPHA2,
            endPosition: GridPosition.ALPHA1,
            motions: {}, // No blue motion
          }),
        ],
      });

      expect(checker.isSeamlesslyLoopable(sequence)).toBe(false);
    });

    it("should handle single beat sequence", () => {
      const sequence = createSequenceData({
        id: "test",
        word: "TEST",
        author: "Test",
        beats: [
          createBeatData({
            beatNumber: 1,
            startPosition: GridPosition.ALPHA1,
            endPosition: GridPosition.ALPHA1, // Same position
            motions: {
              [MotionColor.BLUE]: {
                startOrientation: Orientation.IN,
                endOrientation: Orientation.IN, // Same orientation
              } as any,
            },
          }),
        ],
      });

      expect(checker.isSeamlesslyLoopable(sequence)).toBe(true);
    });
  });
});
