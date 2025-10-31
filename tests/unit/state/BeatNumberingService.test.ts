/**
 * BeatNumberingService Tests
 *
 * Pure utility testing - these functions have no side effects,
 * so tests are simple and deterministic.
 *
 * HIGH-VALUE: Beat numbering is critical - if it breaks, the entire
 * sequence UI shows wrong numbers and operations fail silently.
 */

import { describe, expect, it } from "vitest";
import { BeatNumberingService } from "../../../src/lib/modules/build/shared/services/implementations/BeatNumberingService";
import type { BeatData } from "$shared";

describe("BeatNumberingService - Pure Utility", () => {
  const service = new BeatNumberingService();

  // Helper to create test beats
  const createBeat = (beatNumber: number): BeatData => ({
    id: crypto.randomUUID(),
    beatNumber,
    duration: 1.0,
    blueReversal: false,
    redReversal: false,
    isBlank: true,
    letter: null,
    startPosition: null,
    endPosition: null,
    motions: {},
  });

  describe("renumberBeats", () => {
    it("should renumber beats sequentially from 1", () => {
      const beats = [createBeat(5), createBeat(99), createBeat(1)];

      const result = service.renumberBeats(beats);

      expect(result[0].beatNumber).toBe(1);
      expect(result[1].beatNumber).toBe(2);
      expect(result[2].beatNumber).toBe(3);
    });

    it("should handle empty array", () => {
      const result = service.renumberBeats([]);
      expect(result).toHaveLength(0);
    });

    it("should handle single beat", () => {
      const beats = [createBeat(99)];
      const result = service.renumberBeats(beats);

      expect(result).toHaveLength(1);
      expect(result[0].beatNumber).toBe(1);
    });

    it("should preserve other beat properties", () => {
      const beat: BeatData = {
        ...createBeat(5),
        duration: 2.5,
        blueReversal: true,
      };

      const [result] = service.renumberBeats([beat]);

      expect(result.duration).toBe(2.5);
      expect(result.blueReversal).toBe(true);
      expect(result.id).toBe(beat.id); // Same beat, just renumbered
    });
  });

  describe("getNextBeatNumber", () => {
    it("should return 1 for empty array", () => {
      expect(service.getNextBeatNumber([])).toBe(1);
    });

    it("should return length + 1", () => {
      const beats = [createBeat(1), createBeat(2), createBeat(3)];
      expect(service.getNextBeatNumber(beats)).toBe(4);
    });

    it("should work regardless of current beat numbers", () => {
      // Even if beats are misnumbered, next number is based on count
      const beats = [createBeat(99), createBeat(42)];
      expect(service.getNextBeatNumber(beats)).toBe(3); // 2 beats + 1
    });
  });

  describe("validateBeatNumbering", () => {
    it("should return true for correctly numbered beats", () => {
      const beats = [createBeat(1), createBeat(2), createBeat(3)];
      expect(service.validateBeatNumbering(beats)).toBe(true);
    });

    it("should return false for incorrect numbering", () => {
      const beats = [createBeat(1), createBeat(3), createBeat(4)]; // Missing 2
      expect(service.validateBeatNumbering(beats)).toBe(false);
    });

    it("should return false for out-of-order numbers", () => {
      const beats = [createBeat(2), createBeat(1), createBeat(3)];
      expect(service.validateBeatNumbering(beats)).toBe(false);
    });

    it("should return true for empty array", () => {
      expect(service.validateBeatNumbering([])).toBe(true);
    });
  });

  describe("findNumberingGaps", () => {
    it("should return empty array for correct numbering", () => {
      const beats = [createBeat(1), createBeat(2), createBeat(3)];
      expect(service.findNumberingGaps(beats)).toEqual([]);
    });

    it("should find all incorrectly numbered beats", () => {
      const beats = [
        createBeat(1), // Correct (index 0)
        createBeat(5), // Wrong (index 1, should be 2)
        createBeat(3), // Correct (index 2)
        createBeat(99), // Wrong (index 3, should be 4)
      ];

      const gaps = service.findNumberingGaps(beats);
      expect(gaps).toEqual([1, 3]); // Indices of wrong beats
    });

    it("should handle all beats being wrong", () => {
      const beats = [createBeat(5), createBeat(10), createBeat(15)];
      expect(service.findNumberingGaps(beats)).toEqual([0, 1, 2]);
    });

    it("should return empty for empty array", () => {
      expect(service.findNumberingGaps([])).toEqual([]);
    });
  });
});

/**
 * WHY THESE TESTS ARE VALUABLE:
 *
 * Beat numbering is used everywhere:
 * - UI displays beat numbers to users
 * - Add/remove/insert operations depend on correct numbering
 * - Validation checks beat numbers
 * - Export/import relies on beat order
 *
 * If these functions break:
 * ❌ UI shows wrong beat numbers (confusing for users)
 * ❌ Operations silently fail (beats inserted at wrong position)
 * ❌ Validation fails incorrectly (blocks valid sequences)
 * ❌ Data corruption (wrong beats exported/imported)
 *
 * These tests catch:
 * ✅ Off-by-one errors
 * ✅ Empty array edge cases
 * ✅ Property preservation during renumbering
 * ✅ Incorrect validation logic
 */
