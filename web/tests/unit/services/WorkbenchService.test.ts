/**
 * Tests for WorkbenchService
 *
 * Verifies that the pure business logic service works correctly
 * after extraction from the mixed reactive service.
 */

import {
  GridMode,
  Letter,
  createPictographData,
  type BeatData,
  type SequenceData,
  type WorkbenchMode,
} from "$domain";
import { WorkbenchService } from "$lib/services/implementations/workbench/WorkbenchService";
import { beforeEach, describe, expect, it } from "vitest";

describe("WorkbenchService", () => {
  let service: WorkbenchService;

  beforeEach(() => {
    service = new WorkbenchService();
  });

  describe("Initialization", () => {
    it("should initialize with correct default config", () => {
      const config = service.initialize();

      expect(config.mode).toBe("construct");
      expect(config.isInitialized).toBe(true);
    });

    it("should check initialization status correctly", () => {
      const config = service.initialize();
      expect(service.isInitialized(config)).toBe(true);

      const uninitializedConfig = {
        mode: "view" as WorkbenchMode,
        isInitialized: false,
      };
      expect(service.isInitialized(uninitializedConfig)).toBe(false);
    });
  });

  describe("Mode Management", () => {
    it("should set mode correctly", () => {
      const initialConfig = service.initialize();
      const updatedConfig = service.setMode(initialConfig, "edit");

      expect(updatedConfig.mode).toBe("edit");
      expect(updatedConfig.isInitialized).toBe(true);
    });

    it("should determine edit capability correctly", () => {
      expect(service.canEditInMode("construct")).toBe(true);
      expect(service.canEditInMode("edit")).toBe(true);
      expect(service.canEditInMode("view")).toBe(false);
    });
  });

  describe("Beat Interaction Logic", () => {
    it("should determine beat selection correctly", () => {
      expect(service.shouldSelectBeatOnClick("construct", 0)).toBe(true);
      expect(service.shouldSelectBeatOnClick("view", 2)).toBe(true);
      expect(service.shouldSelectBeatOnClick("construct", -1)).toBe(false);
    });

    it("should determine beat editing on double click correctly", () => {
      expect(service.shouldEditBeatOnDoubleClick("construct", 0)).toBe(true);
      expect(service.shouldEditBeatOnDoubleClick("edit", 1)).toBe(true);
      expect(service.shouldEditBeatOnDoubleClick("view", 0)).toBe(false);
      expect(service.shouldEditBeatOnDoubleClick("construct", -1)).toBe(false);
    });
  });

  describe("Beat Data Creation", () => {
    it("should create default pictograph data", () => {
      const pictographData = service.createDefaultPictographData();

      expect(pictographData.letter).toBe(Letter.A);
    });

    it("should create default pictograph data with custom letter", () => {
      const pictographData = service.createDefaultPictographData(Letter.B);

      expect(pictographData.letter).toBe(Letter.B);
    });

    it("should create edited beat data correctly", () => {
      const originalBeat: BeatData = {
        id: "test-beat",
        beatNumber: 1,
        duration: 1.0,
        blueReversal: false,
        redReversal: false,
        isBlank: true,
        pictographData: null,
      };

      const pictographData = service.createDefaultPictographData();
      const editedBeat = service.createEditedBeatData(
        originalBeat,
        pictographData
      );

      expect(editedBeat.isBlank).toBe(false);
      expect(editedBeat.pictographData).toBe(pictographData);
      expect(editedBeat.id).toBe(originalBeat.id);
      expect(editedBeat.beatNumber).toBe(originalBeat.beatNumber);
    });

    it("should create cleared beat data correctly", () => {
      const originalBeat: BeatData = {
        id: "test-beat",
        beatNumber: 1,
        duration: 1.0,
        blueReversal: false,
        redReversal: false,
        isBlank: false,
        pictographData: createPictographData({ letter: Letter.A }),
      };

      const clearedBeat = service.createClearedBeatData(originalBeat);

      expect(clearedBeat.isBlank).toBe(true);
      expect(clearedBeat.pictographData).toBeNull();
      expect(clearedBeat.id).toBe(originalBeat.id);
      expect(clearedBeat.beatNumber).toBe(originalBeat.beatNumber);
    });
  });

  describe("Sequence Operations", () => {
    it("should validate sequence creation correctly", () => {
      const validResult = service.validateSequenceCreation("Test Sequence", 16);
      expect(validResult.isValid).toBe(true);
      expect(validResult.errors).toHaveLength(0);
    });

    it("should detect sequence creation errors", () => {
      const invalidResult = service.validateSequenceCreation("", 0);
      expect(invalidResult.isValid).toBe(false);
      expect(invalidResult.errors).toContain("Sequence name is required");
      expect(invalidResult.errors).toContain(
        "Sequence length must be at least 1"
      );
    });

    it("should warn about large sequences", () => {
      const result = service.validateSequenceCreation("Large Sequence", 40);
      expect(result.isValid).toBe(true);
      expect(result.warnings).toContain(
        "Large sequences may impact performance"
      );
    });

    it("should create sequence creation parameters correctly", () => {
      const params = service.createSequenceCreationParams("Test", 8);
      expect(params.name).toBe("Test");
      expect(params.length).toBe(8);
    });

    it("should handle default sequence creation parameters", () => {
      const params = service.createSequenceCreationParams();
      expect(params.name).toBe("New Sequence");
      expect(params.length).toBe(16);
    });

    it("should sanitize sequence creation parameters", () => {
      const params = service.createSequenceCreationParams("   ", 100);
      expect(params.name).toBe("New Sequence");
      expect(params.length).toBe(64); // clamped to max
    });
  });

  describe("Configuration Operations", () => {
    it("should validate grid mode changes", () => {
      expect(
        service.validateGridModeChange(GridMode.DIAMOND, GridMode.BOX)
      ).toBe(true);
      expect(
        service.validateGridModeChange(GridMode.BOX, GridMode.DIAMOND)
      ).toBe(true);
    });

    it("should validate beat size changes", () => {
      expect(service.validateBeatSizeChange(160, 200)).toBe(true);
      expect(service.validateBeatSizeChange(160, 40)).toBe(false); // too small
      expect(service.validateBeatSizeChange(160, 400)).toBe(false); // too large
    });
  });

  describe("Validation Helpers", () => {
    const mockSequence: SequenceData = {
      id: "test-sequence",
      name: "Test",
      word: "AB",
      thumbnails: [],
      isFavorite: false,
      isCircular: false,
      tags: [],
      metadata: {},
      beats: [
        {
          id: "beat-0",
          beatNumber: 1,
          duration: 1.0,
          blueReversal: false,
          redReversal: false,
          isBlank: true,
          pictographData: null,
        },
        {
          id: "beat-1",
          beatNumber: 2,
          duration: 1.0,
          blueReversal: false,
          redReversal: false,
          isBlank: false,
          pictographData: null,
        },
      ],
    };

    it("should validate beat indices correctly", () => {
      expect(service.isValidBeatIndex(mockSequence, 0)).toBe(true);
      expect(service.isValidBeatIndex(mockSequence, 1)).toBe(true);
      expect(service.isValidBeatIndex(mockSequence, 2)).toBe(false);
      expect(service.isValidBeatIndex(mockSequence, -1)).toBe(false);
      expect(service.isValidBeatIndex(null, 0)).toBe(false);
    });

    it("should determine if beat can be edited", () => {
      expect(service.canEditBeat(mockSequence, 0, "construct")).toBe(true);
      expect(service.canEditBeat(mockSequence, 0, "edit")).toBe(true);
      expect(service.canEditBeat(mockSequence, 0, "view")).toBe(false);
      expect(service.canEditBeat(mockSequence, 5, "construct")).toBe(false);
    });

    it("should determine if beat can be cleared", () => {
      expect(service.canClearBeat(mockSequence, 0)).toBe(false); // blank beat
      expect(service.canClearBeat(mockSequence, 1)).toBe(true); // non-blank beat
      expect(service.canClearBeat(mockSequence, 5)).toBe(false); // invalid index
    });
  });

  describe("Beat Operation Helpers", () => {
    it("should determine correct edit action", () => {
      const blankBeat: BeatData = {
        id: "blank",
        beatNumber: 1,
        duration: 1.0,
        blueReversal: false,
        redReversal: false,
        isBlank: true,
        pictographData: null,
      };
      const filledBeat: BeatData = {
        id: "filled",
        beatNumber: 1,
        duration: 1.0,
        blueReversal: false,
        redReversal: false,
        isBlank: false,
        pictographData: null,
      };

      expect(service.getBeatEditAction(blankBeat)).toBe("edit");
      expect(service.getBeatEditAction(filledBeat)).toBe("clear");
    });

    it("should apply beat edit actions correctly", () => {
      const blankBeat: BeatData = {
        id: "blank",
        beatNumber: 1,
        duration: 1.0,
        blueReversal: false,
        redReversal: false,
        isBlank: true,
        pictographData: null,
      };

      const editedBeat = service.applyBeatEditAction(blankBeat, "edit");
      expect(editedBeat.isBlank).toBe(false);
      expect(editedBeat.pictographData).toBeTruthy();

      const clearedBeat = service.applyBeatEditAction(editedBeat, "clear");
      expect(clearedBeat.isBlank).toBe(true);
      expect(clearedBeat.pictographData).toBeNull();
    });
  });
});
