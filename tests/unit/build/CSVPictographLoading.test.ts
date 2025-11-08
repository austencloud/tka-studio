/**
 * CSV Pictograph Loading and Data Validation Tests
 *
 * Tests the infrastructure for loading real pictograph data from CSV files.
 * Uses RealPictographLoader to verify CSV parsing and data structure.
 *
 * IMPORTANT: This does NOT test CAP execution logic - that will be added later.
 * This validates that:
 * 1. CSV data can be loaded successfully
 * 2. Parsed data has expected structure
 * 3. Real pictographs have valid motion data
 *
 * Key principle: If we don't know if a pictograph is valid,
 * we load it from the CSV which is the source of truth.
 */

import { describe, expect, it, beforeAll } from "vitest";
import { Letter } from "../../../src/lib/shared/foundation/domain/models/Letter";
import { GridMode } from "../../../src/lib/shared/pictograph/grid/domain/enums/grid-enums";
import { MotionColor } from "../../../src/lib/shared/pictograph/shared/domain/enums/pictograph-enums";
import type { PictographData } from "$shared";
import { initializeContainer } from "$shared/inversify/container";
import {
  getValidPictograph,
  getAllLetterVariants,
} from "../../helpers/real-pictograph-loader";

describe("CSV Pictograph Loading", () => {
  let samplePictographs: PictographData[];

  beforeAll(async () => {
    // Initialize DI container FIRST
    await initializeContainer();

    // Load REAL pictographs from CSV
    samplePictographs = await Promise.all([
      getValidPictograph(Letter.A, GridMode.DIAMOND),
      getValidPictograph(Letter.B, GridMode.DIAMOND),
      getValidPictograph(Letter.C, GridMode.DIAMOND),
    ]).then((pictos) => pictos.filter((p) => p !== null) as PictographData[]);
  });

  describe("CSV Data Loading", () => {
    it("should load valid pictographs from CSV files", () => {
      expect(samplePictographs.length).toBeGreaterThan(0);
      expect(samplePictographs[0]!.letter).toBeDefined();
      expect(samplePictographs[0]!.startPosition).toBeDefined();
      expect(samplePictographs[0]!.endPosition).toBeDefined();
    });

    it("should have valid motion data structure", () => {
      const picto = samplePictographs[0];
      expect(picto!.motions).toBeDefined();
      expect(picto!.motions[MotionColor.BLUE]).toBeDefined();
      expect(picto!.motions[MotionColor.RED]).toBeDefined();
      expect(picto!.motions[MotionColor.BLUE]?.startLocation).toBeDefined();
      expect(picto!.motions[MotionColor.BLUE]?.endLocation).toBeDefined();
    });
  });

  describe("Letter-Specific Data Loading", () => {
    it("should load Letter A with correct structure", async () => {
      const letterA = await getValidPictograph(Letter.A, GridMode.DIAMOND);
      expect(letterA).not.toBeNull();
      expect(letterA!.letter).toBe(Letter.A);
      expect(typeof letterA!.startPosition).toBe("string");
      expect(typeof letterA!.endPosition).toBe("string");
    });

    it("should load Letter B with valid motion types", async () => {
      const letterB = await getValidPictograph(Letter.B, GridMode.DIAMOND);
      expect(letterB).not.toBeNull();
      expect(letterB!.letter).toBe(Letter.B);
      expect(letterB!.motions[MotionColor.BLUE]?.motionType).toBeDefined();
      expect(letterB!.motions[MotionColor.RED]?.motionType).toBeDefined();
    });

    it("should load all Letter C variants from CSV", async () => {
      const letterCVariants = await getAllLetterVariants(
        Letter.C,
        GridMode.DIAMOND
      );
      expect(letterCVariants.length).toBeGreaterThanOrEqual(1);

      letterCVariants.forEach((variant) => {
        expect(variant.letter).toBe(Letter.C);
        expect(variant.motions[MotionColor.BLUE]).toBeDefined();
        expect(variant.motions[MotionColor.RED]).toBeDefined();
      });
    });
  });

  describe("Data Variants", () => {
    it("should load multiple variants for Letter A", async () => {
      const letterAVariants = await getAllLetterVariants(
        Letter.A,
        GridMode.DIAMOND
      );
      expect(letterAVariants.length).toBeGreaterThan(0);

      // All variants should have Letter A
      letterAVariants.forEach((variant) => {
        expect(variant.letter).toBe(Letter.A);
        expect(variant.startPosition).toBeTruthy();
        expect(variant.endPosition).toBeTruthy();
      });
    });
  });
});

/**
 * WHAT THIS TEST VALIDATES:
 *
 * ✅ CSV files can be loaded successfully
 * ✅ CSVPictographParser correctly parses data
 * ✅ RealPictographLoader provides valid data
 * ✅ Pictograph data has expected structure
 * ✅ Motion data is present for both colors
 * ✅ Letter variants can be retrieved
 *
 * WHAT THIS TEST DOES NOT COVER (Yet):
 *
 * ❌ CAP execution logic (will be added later)
 * ❌ Position rotation calculations
 * ❌ Beat sequence generation
 * ❌ StrictRotatedCAPExecutor functionality
 *
 * NOTE: This is intentionally focused on data loading infrastructure.
 * CAP execution tests will be written separately once the execution
 * logic is fully implemented and we understand the proper way to
 * convert PictographData → BeatData.
 */
