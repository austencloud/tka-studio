/**
 * Tests for BeatFrameService
 *
 * Verifies that the pure business logic service works correctly
 * after extraction from the mixed reactive service.
 */

import { GridMode } from "$domain";
import type { BeatFrameConfig } from "$domain";
import { BeatFrameService } from "$lib/services/implementations/layout/BeatFrameService";
import { beforeEach, describe, expect, it } from "vitest";

describe("BeatFrameService", () => {
  let service: BeatFrameService;

  beforeEach(() => {
    service = new BeatFrameService();
  });

  describe("Configuration", () => {
    it("should provide default configuration", () => {
      const config = service.getDefaultConfig();

      expect(config).toEqual({
        columns: 4,
        beatSize: 160,
        gap: 0,
        gridMode: GridMode.DIAMOND,
        hasStartTile: true,
      });
    });

    it("should validate configuration with defaults", () => {
      const partialConfig = { columns: 6, beatSize: 200 };
      const validatedConfig = service.validateConfig(partialConfig);

      expect(validatedConfig.columns).toBe(6);
      expect(validatedConfig.beatSize).toBe(200);
      expect(validatedConfig.gap).toBe(0); // default
      expect(validatedConfig.gridMode).toBe(GridMode.DIAMOND); // default
      expect(validatedConfig.hasStartTile).toBe(true); // default
    });

    it("should enforce minimum values", () => {
      const invalidConfig = { columns: -1, beatSize: 10 };
      const validatedConfig = service.validateConfig(invalidConfig);

      expect(validatedConfig.columns).toBe(1); // minimum
      expect(validatedConfig.beatSize).toBe(50); // minimum
    });
  });

  describe("Layout Calculations", () => {
    it("should calculate beat positions correctly", () => {
      const config: BeatFrameConfig = {
        columns: 4,
        beatSize: 160,
        cellSize: 160,
        gap: 0,
        gridMode: GridMode.DIAMOND,
        hasStartTile: true,
        showBeatNumbers: false,
        enableHover: true,
        enableDrag: true,
      };

      // First beat should be at column 1 (after start tile)
      const position0 = service.calculateBeatPosition(0, 1, config);
      expect(position0).toEqual({ x: 160, y: 0 });

      // Fourth beat should be at column 4 (end of first row)
      const position3 = service.calculateBeatPosition(3, 4, config);
      expect(position3).toEqual({ x: 640, y: 0 });

      // Fifth beat should be at column 1, row 1
      const position4 = service.calculateBeatPosition(4, 5, config);
      expect(position4).toEqual({ x: 160, y: 160 });
    });

    it("should calculate start position correctly", () => {
      const config: BeatFrameConfig = {
        columns: 4,
        beatSize: 160,
        cellSize: 160,
        gap: 0,
        gridMode: GridMode.DIAMOND,
        hasStartTile: true,
        showBeatNumbers: false,
        enableHover: true,
        enableDrag: true,
      };

      const startPosition = service.calculateStartPosition(5, config);
      expect(startPosition).toEqual({ x: 0, y: 0 });
    });

    it("should calculate frame dimensions correctly", () => {
      const config: BeatFrameConfig = {
        columns: 4,
        beatSize: 160,
        cellSize: 160,
        gap: 0,
        gridMode: GridMode.DIAMOND,
        hasStartTile: true,
        showBeatNumbers: false,
        enableHover: true,
        enableDrag: true,
      };

      // 4 beats should fit in 1 row + start tile = 5 columns total
      const dimensions = service.calculateFrameDimensions(4, config);
      expect(dimensions).toEqual({
        width: 800, // 5 columns * 160px
        height: 160, // 1 row * 160px
      });
    });

    it("should handle empty beat count", () => {
      const config: BeatFrameConfig = {
        columns: 4,
        beatSize: 160,
        cellSize: 160,
        gap: 0,
        gridMode: GridMode.DIAMOND,
        hasStartTile: true,
        showBeatNumbers: false,
        enableHover: true,
        enableDrag: true,
      };

      const dimensions = service.calculateFrameDimensions(0, config);
      expect(dimensions).toEqual({
        width: 160, // Just the start tile
        height: 160,
      });
    });
  });

  describe("Layout Optimization", () => {
    it("should auto-adjust layout for different beat counts", () => {
      expect(service.autoAdjustLayout(0)).toEqual([1, 1]);
      expect(service.autoAdjustLayout(4)).toEqual([1, 4]);
      expect(service.autoAdjustLayout(8)).toEqual([2, 4]);
      expect(service.autoAdjustLayout(12)).toEqual([3, 4]);
      expect(service.autoAdjustLayout(16)).toEqual([4, 4]);
    });

    it("should calculate cell size within constraints", () => {
      const cellSize = service.calculateCellSize(
        4, // beatCount
        800, // containerWidth
        400, // containerHeight
        1, // rows
        5, // totalCols (4 beats + 1 start tile)
        0 // gap
      );

      // Should fit within container: min(800/5, 400/1) = min(160, 400) = 160
      expect(cellSize).toBe(160);
    });

    it("should enforce minimum cell size", () => {
      const cellSize = service.calculateCellSize(
        4, // beatCount
        200, // small containerWidth
        100, // small containerHeight
        1, // rows
        5, // totalCols
        0 // gap
      );

      // Should enforce minimum size of 50
      expect(cellSize).toBe(50);
    });
  });

  describe("Beat Interaction", () => {
    it("should find beat at position correctly", () => {
      const config: BeatFrameConfig = {
        columns: 4,
        beatSize: 160,
        cellSize: 160,
        gap: 0,
        gridMode: GridMode.DIAMOND,
        hasStartTile: true,
        showBeatNumbers: false,
        enableHover: true,
        enableDrag: true,
      };

      // Click at beat 0 position (column 1)
      const beatIndex = service.getBeatAtPosition(160, 0, 4, config);
      expect(beatIndex).toBe(0);

      // Click in start tile area should return -1
      const startClick = service.getBeatAtPosition(80, 0, 4, config);
      expect(startClick).toBe(-1);

      // Click outside beat area should return -1
      const outsideClick = service.getBeatAtPosition(1000, 0, 4, config);
      expect(outsideClick).toBe(-1);
    });
  });
});
