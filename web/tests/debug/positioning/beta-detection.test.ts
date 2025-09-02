/**
 * Test Beta Detection System
 *
 * This test suite verifies the beta detection approach works correctly.
 */

import {
  GridPosition,
  Location,
  MotionColor,
  MotionType,
  Orientation,
  PropType,
  RotationDirection,
  Letter,
  createArrowPlacementData,
  createPropPlacementData,
} from "$domain";
import type { PictographData } from "$domain";
import { endsWithBeta, isBetaPosition } from "$lib/utils/betaDetection";
import { describe, expect, it } from "vitest";

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
            motionType: MotionType.PRO,
            startLocation: Location.NORTH,
            endLocation: Location.EAST,
            turns: 0,
            rotationDirection: RotationDirection.CLOCKWISE,
            startOrientation: Orientation.IN,
            endOrientation: Orientation.OUT,
            isVisible: true,
            color: MotionColor.BLUE,
            propType: PropType.FAN,
            arrowLocation: Location.NORTH,
            arrowPlacementData: createArrowPlacementData(),
            propPlacementData: createPropPlacementData(),
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
