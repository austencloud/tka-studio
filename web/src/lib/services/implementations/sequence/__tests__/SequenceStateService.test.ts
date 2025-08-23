/**
 * Tests for SequenceStateService
 *
 * Verifies that the pure business logic service works correctly
 * after extraction from the mixed reactive service.
 */

import type { SequenceData } from "$lib/domain";
import { beforeEach, describe, expect, it } from "vitest";
import { SequenceStateService } from "../SequenceStateService";

describe("SequenceStateService", () => {
  let service: SequenceStateService;

  beforeEach(() => {
    service = new SequenceStateService();
  });

  describe("Sequence Management", () => {
    it("should create a new sequence with default length", () => {
      const sequence = service.createNewSequence("Test Sequence");

      expect(sequence.name).toBe("Test Sequence");
      expect(sequence.beats).toHaveLength(16); // default length
      expect(sequence.beats[0].beatNumber).toBe(1);
      expect(sequence.beats[15].beatNumber).toBe(16);
    });

    it("should create a new sequence with custom length", () => {
      const sequence = service.createNewSequence("Custom Length", 8);

      expect(sequence.name).toBe("Custom Length");
      expect(sequence.beats).toHaveLength(8);
      expect(sequence.beats[0].beatNumber).toBe(1);
      expect(sequence.beats[7].beatNumber).toBe(8);
    });

    it("should throw error for invalid sequence name", () => {
      expect(() => service.createNewSequence("")).toThrow(
        "Sequence name is required"
      );
      expect(() => service.createNewSequence("   ")).toThrow(
        "Sequence name is required"
      );
    });

    it("should throw error for invalid sequence length", () => {
      expect(() => service.createNewSequence("Test", 0)).toThrow(
        "Sequence length must be between 1 and 64 beats"
      );
      expect(() => service.createNewSequence("Test", 65)).toThrow(
        "Sequence length must be between 1 and 64 beats"
      );
    });

    it("should validate sequence correctly", () => {
      const validSequence = service.createNewSequence("Valid", 4);
      const validation = service.validateSequence(validSequence);

      expect(validation.isValid).toBe(true);
      expect(validation.errors).toHaveLength(0);
    });

    it("should detect validation errors", () => {
      const invalidSequence = service.createNewSequence("Test", 4);
      // Corrupt the sequence (using type assertion for testing)
      (invalidSequence as { name: string }).name = "";
      (invalidSequence.beats[0] as { beatNumber: number }).beatNumber = 999;
      (invalidSequence.beats[1] as { duration: number }).duration = -1;

      const validation = service.validateSequence(invalidSequence);

      expect(validation.isValid).toBe(false);
      expect(validation.errors).toContain("Sequence name is required");
      expect(validation.errors).toContain(
        "Beat 1 has incorrect beat number: 999"
      );
      expect(validation.errors).toContain("Beat 2 has invalid duration: -1");
    });
  });

  describe("Beat Operations", () => {
    let testSequence: SequenceData;

    beforeEach(() => {
      testSequence = service.createNewSequence("Test", 4);
    });

    it("should add a beat to sequence", () => {
      const updatedSequence = service.addBeat(testSequence, { duration: 2.0 });

      expect(updatedSequence.beats).toHaveLength(5);
      expect(updatedSequence.beats[4].beatNumber).toBe(5);
      expect(updatedSequence.beats[4].duration).toBe(2.0);
    });

    it("should remove a beat from sequence", () => {
      const updatedSequence = service.removeBeat(testSequence, 1); // Remove second beat

      expect(updatedSequence.beats).toHaveLength(3);
      // Check that beat numbers are renumbered correctly
      expect(updatedSequence.beats[0].beatNumber).toBe(1);
      expect(updatedSequence.beats[1].beatNumber).toBe(2);
      expect(updatedSequence.beats[2].beatNumber).toBe(3);
    });

    it("should not remove beat with invalid index", () => {
      const updatedSequence = service.removeBeat(testSequence, -1);
      expect(updatedSequence).toBe(testSequence); // Should return unchanged

      const updatedSequence2 = service.removeBeat(testSequence, 10);
      expect(updatedSequence2).toBe(testSequence); // Should return unchanged
    });

    it("should update a beat in sequence", () => {
      const updatedSequence = service.updateBeat(testSequence, 1, {
        duration: 3.0,
        blueReversal: true,
      });

      expect(updatedSequence.beats[1].duration).toBe(3.0);
      expect(updatedSequence.beats[1].blueReversal).toBe(true);
      expect(updatedSequence.beats[1].beatNumber).toBe(2); // Should preserve beat number
    });

    it("should insert a beat at specific position", () => {
      const updatedSequence = service.insertBeat(testSequence, 2, {
        duration: 1.5,
      });

      expect(updatedSequence.beats).toHaveLength(5);
      expect(updatedSequence.beats[2].duration).toBe(1.5);
      expect(updatedSequence.beats[2].beatNumber).toBe(3);

      // Check that subsequent beats are renumbered
      expect(updatedSequence.beats[3].beatNumber).toBe(4);
      expect(updatedSequence.beats[4].beatNumber).toBe(5);
    });
  });

  describe("Beat Selection Helpers", () => {
    let testSequence: SequenceData;

    beforeEach(() => {
      testSequence = service.createNewSequence("Test", 4);
    });

    it("should validate beat indices correctly", () => {
      expect(service.isValidBeatIndex(testSequence, 0)).toBe(true);
      expect(service.isValidBeatIndex(testSequence, 3)).toBe(true);
      expect(service.isValidBeatIndex(testSequence, -1)).toBe(false);
      expect(service.isValidBeatIndex(testSequence, 4)).toBe(false);
      expect(service.isValidBeatIndex(null, 0)).toBe(false);
    });

    it("should get selected beat correctly", () => {
      const beat = service.getSelectedBeat(testSequence, 1);
      expect(beat).toBeTruthy();
      expect(beat?.beatNumber).toBe(2);

      const invalidBeat = service.getSelectedBeat(testSequence, 10);
      expect(invalidBeat).toBeNull();
    });
  });

  describe("Sequence Transformations", () => {
    let testSequence: SequenceData;

    beforeEach(() => {
      testSequence = service.createNewSequence("Test", 4);
      // Add some data to make clearing meaningful
      (testSequence.beats[0] as any).isBlank = false;
      (testSequence.beats[0] as any).blueReversal = true;
      (testSequence.beats[1] as any).redReversal = true;
    });

    it("should clear sequence", () => {
      const clearedSequence = service.clearSequence(testSequence);

      expect(clearedSequence.beats).toHaveLength(4);
      expect(clearedSequence.beats[0].isBlank).toBe(true);
      expect(clearedSequence.beats[0].blueReversal).toBe(false);
      expect(clearedSequence.beats[1].redReversal).toBe(false);
      expect(clearedSequence.startingPositionBeat).toBeUndefined();
    });

    it("should duplicate sequence", () => {
      const duplicated = service.duplicateSequence(
        testSequence,
        "Duplicated Test"
      );

      expect(duplicated.name).toBe("Duplicated Test");
      expect(duplicated.id).not.toBe(testSequence.id);
      expect(duplicated.beats).toHaveLength(4);
      expect(duplicated.beats[0].id).not.toBe(testSequence.beats[0].id);
      expect(duplicated.beats[0].beatNumber).toBe(1);
    });

    it("should duplicate sequence with default name", () => {
      const duplicated = service.duplicateSequence(testSequence);

      expect(duplicated.name).toBe("Test (Copy)");
    });

    it("should swap colors", () => {
      const swapped = service.swapColors(testSequence);

      expect(swapped.beats[0].blueReversal).toBe(false); // was true
      expect(swapped.beats[0].redReversal).toBe(true); // was false
      expect(swapped.beats[1].blueReversal).toBe(true); // was false
      expect(swapped.beats[1].redReversal).toBe(false); // was true
    });
  });

  describe("Utilities", () => {
    let testSequence: SequenceData;

    beforeEach(() => {
      testSequence = service.createNewSequence("Test", 4);
      (testSequence.beats[0] as any).duration = 2.0;
      (testSequence.beats[1] as any).duration = 1.5;
      (testSequence.beats[2] as any).duration = 1.0;
      (testSequence.beats[3] as any).duration = 0.5;
    });

    it("should calculate sequence duration", () => {
      const duration = service.calculateSequenceDuration(testSequence);
      expect(duration).toBe(5.0); // 2.0 + 1.5 + 1.0 + 0.5
    });

    it("should generate sequence statistics", () => {
      (testSequence.beats[0] as any).isBlank = false;
      (testSequence.beats[0] as any).blueReversal = true;
      (testSequence.beats[1] as any).redReversal = true;

      const stats = service.getSequenceStatistics(testSequence);

      expect(stats.totalBeats).toBe(4);
      expect(stats.blankBeats).toBe(3);
      expect(stats.filledBeats).toBe(1);
      expect(stats.totalDuration).toBe(5.0);
      expect(stats.averageBeatDuration).toBe(1.25);
      expect(stats.hasStartPosition).toBe(false);
      expect(stats.reversalCount.blue).toBe(1);
      expect(stats.reversalCount.red).toBe(1);
    });

    it("should generate sequence word from pictograph letters", () => {
      // Mock pictograph data
      (testSequence.beats[0] as any).pictographData = { letter: "A" } as any;
      (testSequence.beats[1] as any).pictographData = { letter: "B" } as any;
      (testSequence.beats[2] as any).pictographData = { letter: "C" } as any;

      const word = service.generateSequenceWord(testSequence);
      expect(word).toBe("ABC");
    });

    it("should fallback to sequence name when no letters", () => {
      const word = service.generateSequenceWord(testSequence);
      expect(word).toBe("Test");
    });
  });
});
