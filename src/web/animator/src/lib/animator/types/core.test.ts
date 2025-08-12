/**
 * Unit tests for Phase 1 native compatibility refactoring
 * Tests motion data extraction, backward compatibility adapters, and type conversions
 */

import { describe, it, expect } from "vitest";
import type {
  UnifiedSequenceData,
  SequenceData,
  SequenceStep,
  PropAttributes,
  ExtractedMotionData,
  WebAppSequenceData,
  WebAppBeatData,
  WebAppMotionData,
} from "./core.js";
import {
  extractMotionData,
  convertMotionDataToPropAttributes,
  createDefaultPropAttributes,
  adaptSequenceData,
  isUnifiedSequenceData,
  isWebAppSequenceData,
  isLegacySequenceData,
  convertLegacyToUnified,
  convertWebAppToUnified,
  convertPropAttributesToMotionData,
  extractStepsFromUnified,
  extractMetaFromUnified,
} from "./core.js";

describe("Phase 1: Motion Data Extraction", () => {
  const mockWebAppMotionData: WebAppMotionData = {
    motion_type: "pro",
    prop_rot_dir: "cw",
    start_loc: "center",
    end_loc: "right",
    turns: 2,
    start_ori: "in",
    end_ori: "out",
    is_visible: true,
    metadata: {},
  };

  const mockWebAppBeatData: WebAppBeatData = {
    id: "beat-1",
    beat_number: 1,
    duration: 1,
    blue_reversal: false,
    red_reversal: false,
    is_blank: false,
    pictograph_data: {
      id: "pictograph-1",
      grid_data: null,
      arrows: [],
      props: [],
      motions: {
        blue: mockWebAppMotionData,
        red: { ...mockWebAppMotionData, motion_type: "anti" },
      },
      letter: "A",
      metadata: {},
    },
    metadata: {},
  };

  it("should extract motion data from web app beat structure", () => {
    const result = extractMotionData(mockWebAppBeatData);

    expect(result.hasMotionData).toBe(true);
    expect(result.source).toBe("pictograph_data");
    expect(result.blue.motion_type).toBe("pro");
    expect(result.red.motion_type).toBe("anti");
    expect(result.blue.start_loc).toBe("center");
    expect(result.blue.end_loc).toBe("right");
  });

  it("should handle missing motion data gracefully", () => {
    const beatWithoutMotions: WebAppBeatData = {
      ...mockWebAppBeatData,
      pictograph_data: undefined,
    };

    const result = extractMotionData(beatWithoutMotions);

    expect(result.hasMotionData).toBe(false);
    expect(result.source).toBe("default");
    expect(result.blue.motion_type).toBe("static");
    expect(result.red.motion_type).toBe("static");
  });

  it("should convert motion data to prop attributes correctly", () => {
    const propAttrs = convertMotionDataToPropAttributes(mockWebAppMotionData);

    expect(propAttrs.motion_type).toBe("pro");
    expect(propAttrs.prop_rot_dir).toBe("cw");
    expect(propAttrs.start_loc).toBe("center");
    expect(propAttrs.end_loc).toBe("right");
    expect(propAttrs.turns).toBe(2);
    expect(propAttrs.start_ori).toBe("in");
    expect(propAttrs.end_ori).toBe("out");
  });

  it("should create default prop attributes", () => {
    const defaults = createDefaultPropAttributes();

    expect(defaults.motion_type).toBe("static");
    expect(defaults.prop_rot_dir).toBe("no_rot");
    expect(defaults.start_loc).toBe("center");
    expect(defaults.end_loc).toBe("center");
    expect(defaults.turns).toBe(0);
  });
});

describe("Phase 1: Type Guards", () => {
  const mockUnifiedData: UnifiedSequenceData = {
    id: "test-sequence",
    name: "Test Sequence",
    word: "test",
    beats: [],
    metadata: {},
    legacy: undefined, // This makes it unified (has legacy field)
  };

  const mockWebAppData: WebAppSequenceData = {
    id: "test-sequence",
    name: "Test Sequence",
    word: "test",
    beats: [],
    metadata: {},
  };

  const mockLegacyData: SequenceData = [
    { id: "test", word: "test", author: "test", level: 1, grid_mode: "grid" },
    {
      beat: 1,
      blue_attributes: createDefaultPropAttributes(),
      red_attributes: createDefaultPropAttributes(),
    },
  ];

  it("should identify unified sequence data", () => {
    expect(isUnifiedSequenceData(mockUnifiedData)).toBe(true);
    expect(isUnifiedSequenceData(mockLegacyData)).toBe(false);
    expect(isUnifiedSequenceData(null)).toBe(false);
  });

  it("should identify web app sequence data", () => {
    expect(isWebAppSequenceData(mockWebAppData)).toBe(true);
    expect(isWebAppSequenceData(mockUnifiedData)).toBe(false); // has legacy field
    expect(isWebAppSequenceData(mockLegacyData)).toBe(false);
  });

  it("should identify legacy sequence data", () => {
    expect(isLegacySequenceData(mockLegacyData)).toBe(true);
    expect(isLegacySequenceData(mockWebAppData)).toBe(false);
    expect(isLegacySequenceData([])).toBe(false);
  });
});

describe("Phase 1: Data Conversion", () => {
  const mockLegacyData: SequenceData = [
    {
      id: "legacy-test",
      word: "legacy",
      author: "test-author",
      level: 2,
      grid_mode: "grid",
    },
    {
      beat: 1,
      letter: "A",
      blue_attributes: {
        motion_type: "pro",
        start_loc: "center",
        end_loc: "right",
        prop_rot_dir: "cw",
        turns: 1,
        start_ori: "in",
        end_ori: "out",
      },
      red_attributes: createDefaultPropAttributes(),
    },
  ];

  it("should convert legacy data to unified format", () => {
    const unified = convertLegacyToUnified(mockLegacyData);

    expect(unified.id).toBe("legacy-test");
    expect(unified.word).toBe("legacy");
    expect(unified.beats).toHaveLength(1);
    expect(unified.beats[0].beat_number).toBe(1);
    expect(unified.beats[0].pictograph_data?.letter).toBe("A");
    expect(unified.legacy).toBe(mockLegacyData);
  });

  it("should extract steps from unified data", () => {
    const unified = convertLegacyToUnified(mockLegacyData);
    const steps = extractStepsFromUnified(unified);

    expect(steps).toHaveLength(1);
    expect(steps[0].beat).toBe(1);
    expect(steps[0].letter).toBe("A");
    expect(steps[0].blue_attributes.motion_type).toBe("pro");
  });

  it("should extract metadata from unified data", () => {
    const unified = convertLegacyToUnified(mockLegacyData);
    const meta = extractMetaFromUnified(unified);

    expect(meta.id).toBe("legacy-test");
    expect(meta.word).toBe("legacy");
    expect(meta.author).toBe("test-author");
    expect(meta.level).toBe(2);
  });
});

describe("Phase 1: Adapter System", () => {
  it("should adapt any sequence data format", () => {
    const legacyData: SequenceData = [
      { id: "test", word: "test", author: "test", level: 1, grid_mode: "grid" },
      {
        beat: 1,
        blue_attributes: createDefaultPropAttributes(),
        red_attributes: createDefaultPropAttributes(),
      },
    ];

    const unified = adaptSequenceData(legacyData);

    expect(unified.id).toBe("test");
    expect(unified.word).toBe("test");
    expect(unified.beats).toHaveLength(1);
  });

  it("should handle unknown data format", () => {
    expect(() => adaptSequenceData({} as any)).toThrow(
      "Unknown sequence data format"
    );
  });
});
