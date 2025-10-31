/**
 * SequenceValidationService Tests - Simplified
 *
 * HIGH-VALUE: Catches validation bugs that would corrupt data
 */

import { describe, expect, it } from "vitest";
import { SequenceValidationService } from "../../../src/lib/modules/build/shared/services/implementations/SequenceValidationService";
import type { BeatData, SequenceData } from "$shared";

describe("SequenceValidationService", () => {
  const service = new SequenceValidationService();

  const createBeat = (num: number, dur: number = 1.0): BeatData => ({
    id: "test-" + num,
    beatNumber: num,
    duration: dur,
    blueReversal: false,
    redReversal: false,
    isBlank: true,
    letter: null,
    startPosition: null,
    endPosition: null,
    motions: {},
  });

  const createSeq = (name: string, beats: BeatData[]): SequenceData => ({
    id: "seq-id",
    name,
    word: "",
    beats,
    thumbnails: [],
    isFavorite: false,
    isCircular: false,
    level: 2,
    difficultyLevel: "intermediate",
    tags: [],
    metadata: {},
  });

  describe("validateSequence", () => {
    it("should pass valid sequence", () => {
      const seq = createSeq("Valid", [createBeat(1), createBeat(2)]);
      const result = service.validateSequence(seq);

      expect(result.isValid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it("should fail for empty name", () => {
      const seq = createSeq("", [createBeat(1)]);
      const result = service.validateSequence(seq);

      expect(result.isValid).toBe(false);
      expect(result.errors.some((e) => e.message.includes("name"))).toBe(true);
    });

    it("should fail for wrong beat numbers", () => {
      const seq = createSeq("Test", [
        createBeat(1),
        createBeat(99),
        createBeat(3),
      ]);
      const result = service.validateSequence(seq);

      expect(result.isValid).toBe(false);
      expect(
        result.errors.some((e) => e.message.includes("incorrect beat number"))
      ).toBe(true);
    });

    it("should fail for negative duration", () => {
      const seq = createSeq("Test", [createBeat(1, -1.0)]);
      const result = service.validateSequence(seq);

      expect(result.isValid).toBe(false);
      expect(
        result.errors.some((e) => e.message.includes("invalid duration"))
      ).toBe(true);
    });

    it("should fail for too many beats", () => {
      const beats = Array.from({ length: 65 }, (_, i) => createBeat(i + 1));
      const seq = createSeq("Too Long", beats);
      const result = service.validateSequence(seq);

      expect(result.isValid).toBe(false);
      expect(
        result.errors.some((e) => e.message.includes("more than 64"))
      ).toBe(true);
    });
  });

  describe("isValidBeatIndex", () => {
    it("should validate beat indices", () => {
      const seq = createSeq("Test", [
        createBeat(1),
        createBeat(2),
        createBeat(3),
      ]);

      expect(service.isValidBeatIndex(seq, 0)).toBe(true);
      expect(service.isValidBeatIndex(seq, 2)).toBe(true);
      expect(service.isValidBeatIndex(seq, 3)).toBe(false);
      expect(service.isValidBeatIndex(seq, -1)).toBe(false);
    });

    it("should return false for null sequence", () => {
      expect(service.isValidBeatIndex(null, 0)).toBe(false);
    });
  });

  describe("validateSequenceName", () => {
    it("should pass valid name", () => {
      expect(service.validateSequenceName("My Sequence").isValid).toBe(true);
    });

    it("should fail for empty name", () => {
      expect(service.validateSequenceName("").isValid).toBe(false);
      expect(service.validateSequenceName("   ").isValid).toBe(false);
    });
  });

  describe("validateSequenceLength", () => {
    it("should pass valid lengths", () => {
      expect(service.validateSequenceLength(1).isValid).toBe(true);
      expect(service.validateSequenceLength(64).isValid).toBe(true);
    });

    it("should fail for invalid lengths", () => {
      expect(service.validateSequenceLength(0).isValid).toBe(false);
      expect(service.validateSequenceLength(65).isValid).toBe(false);
      expect(service.validateSequenceLength(-1).isValid).toBe(false);
    });
  });
});
