/**
 * Test Beta Detection System
 *
 * This test suite verifies the beta detection approach works correctly.
 */

import { describe, it, expect } from "vitest";
import { GridPosition } from "$lib/domain/enums";
import { Letter } from "$lib/domain/Letter";
import type { PictographData } from "$lib/domain/PictographData";
import { endsWithBeta, isBetaPosition } from "$lib/utils/betaDetection";

describe("Beta Detection System", () => {
  describe("isBetaPosition", () => {
    it("should correctly identify beta positions", () => {
      expect(isBetaPosition(GridPosition.BETA1)).toBe(true);
      expect(isBetaPosition(GridPosition.ALPHA1)).toBe(false);
      expect(isBetaPosition(GridPosition.GAMMA1)).toBe(false);
      expect(isBetaPosition("beta3")).toBe(true);
      expect(isBetaPosition("alpha5")).toBe(false);
    });
  });

  describe("endsWithBeta", () => {
    it("should handle pictographs with missing motion data gracefully", () => {
      // Test pictograph with no motion data
      const pictographWithoutMotions: Partial<PictographData> = {
        letter: Letter.A,
        startPosition: GridPosition.ALPHA1,
        endPosition: GridPosition.BETA3,
        // No motions property
      };

      // Should return false when motion data is missing
      expect(endsWithBeta(pictographWithoutMotions as PictographData)).toBe(
        false
      );
    });

    it("should handle pictographs with incomplete motion data", () => {
      // Test pictograph with incomplete motion data
      const pictographWithIncompleteMotions: Partial<PictographData> = {
        letter: Letter.A,
        startPosition: GridPosition.ALPHA1,
        endPosition: GridPosition.BETA3,
        motions: {
          blue: {
            motionType: "pro" as any,
            startLocation: "n" as any,
            endLocation: "e" as any,
            turns: 0,
            rotationDirection: "cw" as any,
            startOrientation: "in" as any,
            endOrientation: "out" as any,
            isVisible: true,
            color: "blue" as any,
            propType: "fan" as any,
            arrowLocation: "n" as any,
            arrowPlacementData: {} as any,
            propPlacementData: {} as any,
          },
          // Missing red motion
        },
      };

      // Should return false when motion data is incomplete
      expect(
        endsWithBeta(pictographWithIncompleteMotions as PictographData)
      ).toBe(false);
    });
  });
});
