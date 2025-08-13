/**
 * PictographService Svelte 5 Runes Tests
 *
 * Tests for the rune-based pictograph service
 */

import { createBeatData, createPictographData } from "$lib/domain";
import {
  ArrowType,
  GridMode,
  Location,
  MotionType,
  Orientation,
  PropType,
  RotationDirection,
} from "$lib/domain/enums";
import { beforeEach, describe, expect, it } from "vitest";
import {
  createBeatPictographService,
  createPictographService,
} from "../PictographService.svelte";

describe("PictographService (Runes)", () => {
  let service: ReturnType<typeof createPictographService>;

  beforeEach(() => {
    service = createPictographService({
      debugMode: false,
      loadingTimeout: 1000,
    });
  });

  describe("Initial State", () => {
    it("should start with clean initial state", () => {
      expect(service.currentData).toBeNull();
      expect(service.isLoading).toBe(false);
      expect(service.errorMessage).toBeNull();
      expect(service.loadingProgress).toBe(0);
      expect(service.hasValidData).toBe(false);
    });
  });

  describe("setPictographData", () => {
    it("should set pictograph data and start loading", () => {
      const pictographData = createPictographData({
        letter: "A",
        grid_data: {
          grid_mode: GridMode.DIAMOND,
          center_x: 0,
          center_y: 0,
          radius: 100,
          grid_points: {},
        },
        arrows: {
          blue: {
            id: "blue-arrow",
            arrow_type: ArrowType.BLUE,
            color: "blue",
            motion_type: MotionType.PRO,
            location: Location.NORTH,
            start_orientation: Orientation.IN,
            end_orientation: Orientation.OUT,
            rotation_direction: RotationDirection.CLOCKWISE,
            position_x: 0,
            position_y: 0,
            is_visible: true,
            is_selected: false,
            turns: 1,
            is_mirrored: false,
            coordinates: null,
            rotation_angle: 0,
            svg_center: null,
            svg_mirrored: false,
          },
          red: {
            id: "red-arrow",
            arrow_type: ArrowType.RED,
            color: "red",
            motion_type: MotionType.ANTI,
            location: Location.SOUTH,
            start_orientation: Orientation.IN,
            end_orientation: Orientation.OUT,
            rotation_direction: RotationDirection.COUNTER_CLOCKWISE,
            position_x: 0,
            position_y: 0,
            is_visible: true,
            is_selected: false,
            turns: 1,
            is_mirrored: false,
            coordinates: null,
            rotation_angle: 180,
            svg_center: null,
            svg_mirrored: false,
          },
        },
      });

      service.setPictographData(pictographData);

      expect(service.currentData).toEqual(pictographData);
      expect(service.hasValidData).toBe(true);
      expect(service.isLoading).toBe(true);
      expect(service.errorMessage).toBeNull();
    });

    it("should handle invalid data gracefully", () => {
      const invalidData = null;

      service.setPictographData(invalidData);

      expect(service.currentData).toBeNull();
      expect(service.hasValidData).toBe(false);
      expect(service.isLoading).toBe(false);
      expect(service.errorMessage).toBe("Invalid pictograph data provided");
    });

    it("should convert legacy data format", () => {
      const legacyData = {
        id: "legacy-test",
        gridMode: "box",
        letter: "B",
        redArrowData: {
          motionType: "pro",
          loc: "e",
          turns: 1.5,
        },
      };

      service.setPictographData(legacyData);

      expect(service.currentData).toBeDefined();
      expect(service.currentData?.letter).toBe("B");
      expect(service.currentData?.grid_data.grid_mode).toBe(GridMode.BOX);
      expect(service.currentData?.arrows.red?.motion_type).toBe("pro");
      expect(service.currentData?.arrows.red?.location).toBe("e");
      expect(service.hasValidData).toBe(true);
    });
  });

  describe("setBeatData", () => {
    it("should set data from beat with pictograph", () => {
      const pictographData = createPictographData({
        letter: "C",
        grid_data: {
          grid_mode: GridMode.DIAMOND,
          center_x: 0,
          center_y: 0,
          radius: 100,
          grid_points: {},
        },
      });

      const beatData = createBeatData({
        beat_number: 1,
        pictograph_data: pictographData,
      });

      service.setBeatData(beatData);

      expect(service.currentData).toEqual(pictographData);
      expect(service.hasValidData).toBe(true);
      expect(service.isLoading).toBe(true);
    });

    it("should clear data for beat without pictograph", () => {
      // First set some data
      const pictographData = createPictographData({ letter: "D" });
      service.setPictographData(pictographData);
      expect(service.hasValidData).toBe(true);

      // Then set blank beat
      const blankBeat = createBeatData({
        beat_number: 2,
        is_blank: true,
      });

      service.setBeatData(blankBeat);

      expect(service.currentData).toBeNull();
      expect(service.hasValidData).toBe(false);
      expect(service.isLoading).toBe(false);
    });
  });

  describe("Component Loading Tracking", () => {
    beforeEach(() => {
      const pictographData = createPictographData({
        letter: "E",
        arrows: {
          blue: {
            id: "blue",
            arrow_type: ArrowType.BLUE,
            color: "blue",
            motion_type: MotionType.PRO,
            location: Location.NORTH,
            start_orientation: Orientation.IN,
            end_orientation: Orientation.OUT,
            rotation_direction: RotationDirection.CLOCKWISE,
            position_x: 0,
            position_y: 0,
            is_visible: true,
            is_selected: false,
            turns: 1,
            is_mirrored: false,
            coordinates: null,
            rotation_angle: 0,
            svg_center: null,
            svg_mirrored: false,
          },
          red: {
            id: "red",
            arrow_type: ArrowType.RED,
            color: "red",
            motion_type: MotionType.ANTI,
            location: Location.SOUTH,
            start_orientation: Orientation.IN,
            end_orientation: Orientation.OUT,
            rotation_direction: RotationDirection.COUNTER_CLOCKWISE,
            position_x: 0,
            position_y: 0,
            is_visible: true,
            is_selected: false,
            turns: 1,
            is_mirrored: false,
            coordinates: null,
            rotation_angle: 180,
            svg_center: null,
            svg_mirrored: false,
          },
        },
        props: {
          blue: {
            id: "blue-prop",
            prop_type: PropType.STAFF,
            color: "blue",
            location: Location.NORTH,
            orientation: Orientation.IN,
            rotation_direction: RotationDirection.NO_ROTATION,
            position_x: 0,
            position_y: 0,
            is_visible: true,
            is_selected: false,
            coordinates: null,
            rotation_angle: 0,
            svg_center: null,
          },
          red: {
            id: "red-prop",
            prop_type: PropType.STAFF,
            color: "red",
            location: Location.SOUTH,
            orientation: Orientation.IN,
            rotation_direction: RotationDirection.NO_ROTATION,
            position_x: 0,
            position_y: 0,
            is_visible: true,
            is_selected: false,
            coordinates: null,
            rotation_angle: 180,
            svg_center: null,
          },
        },
      });

      service.setPictographData(pictographData);
    });

    it("should track component loading progress", () => {
      expect(service.isLoading).toBe(true);
      expect(service.loadingProgress).toBe(0); // 0 of 5 components loaded

      service.markComponentLoaded("grid");
      expect(service.loadingProgress).toBe(20); // 1 of 5 components loaded

      service.markComponentLoaded("blue-arrow");
      expect(service.loadingProgress).toBe(40); // 2 of 5 components loaded

      service.markComponentLoaded("red-arrow");
      expect(service.loadingProgress).toBe(60); // 3 of 5 components loaded

      service.markComponentLoaded("blue-prop");
      expect(service.loadingProgress).toBe(80); // 4 of 5 components loaded

      service.markComponentLoaded("red-prop");
      expect(service.loadingProgress).toBe(100); // 5 of 5 components loaded
      expect(service.isLoading).toBe(false); // Should auto-complete
    });

    it("should handle component errors gracefully", () => {
      service.markComponentError("grid", "Failed to load grid SVG");

      expect(service.errorMessage).toBe("grid: Failed to load grid SVG");
      expect(service.loadingProgress).toBe(20); // Still marks as loaded to prevent blocking
    });

    it("should complete loading even with errors", () => {
      service.markComponentLoaded("grid");
      service.markComponentError("blue-arrow", "Network error");
      service.markComponentLoaded("red-arrow");
      service.markComponentLoaded("blue-prop");
      service.markComponentLoaded("red-prop");

      expect(service.isLoading).toBe(false);
      expect(service.loadingProgress).toBe(100);
      expect(service.errorMessage).toBe("blue-arrow: Network error");
    });
  });

  describe("Service Configuration", () => {
    it("should create service with custom config", () => {
      const customService = createPictographService({
        debugMode: true,
        defaultGridMode: "box",
        loadingTimeout: 2000,
      });

      const config = customService.getConfig();
      expect(config.debugMode).toBe(true);
      expect(config.defaultGridMode).toBe("box");
      expect(config.loadingTimeout).toBe(2000);
    });

    it("should allow toggling debug mode", () => {
      const config = service.getConfig();
      expect(config.debugMode).toBe(false);

      service.setDebugMode(true);
      const updatedConfig = service.getConfig();
      expect(updatedConfig.debugMode).toBe(true);
    });
  });

  describe("reset", () => {
    it("should reset service to initial state", () => {
      // Set up some state
      const pictographData = createPictographData({ letter: "F" });
      service.setPictographData(pictographData);
      service.markComponentLoaded("grid");
      service.markComponentError("arrow", "Some error");

      // Reset
      service.reset();

      expect(service.currentData).toBeNull();
      expect(service.isLoading).toBe(false);
      expect(service.errorMessage).toBeNull();
      expect(service.loadingProgress).toBe(0);
      expect(service.hasValidData).toBe(false);
    });
  });
});

describe("createBeatPictographService", () => {
  it("should create service bound to specific beat", () => {
    const pictographData = createPictographData({
      letter: "G",
    });

    const beatData = createBeatData({
      beat_number: 3,
      pictograph_data: pictographData,
    });

    const beatService = createBeatPictographService(beatData, {
      debugMode: true,
    });

    expect(beatService.currentData).toEqual(pictographData);
    expect(beatService.hasValidData).toBe(true);
    expect(beatService.getConfig().debugMode).toBe(true);
  });

  it("should handle blank beat", () => {
    const blankBeat = createBeatData({
      beat_number: 4,
      is_blank: true,
    });

    const beatService = createBeatPictographService(blankBeat);

    expect(beatService.currentData).toBeNull();
    expect(beatService.hasValidData).toBe(false);
  });
});
