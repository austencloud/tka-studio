import { describe, it, expect, beforeEach, vi } from "vitest";
import { ArrowPositionCalculator } from "../lib/services/positioning/arrows/orchestration/ArrowPositionCalculator";
import { Location, MotionType } from "../lib/domain";
import type { MotionData } from "../lib/domain";

describe("Arrow Rotation Transformation", () => {
  let orchestrator: ArrowPositionCalculator;

  beforeEach(() => {
    // Create mock dependencies for the calculator
    const mockLocationCalculator = {
      calculateLocation: vi.fn().mockReturnValue(Location.NORTHEAST),
    };
    const mockRotationCalculator = {
      calculateRotation: vi.fn().mockReturnValue(225),
    };
    const mockAdjustmentCalculator = {
      calculateAdjustment: vi.fn().mockResolvedValue({ x: 40, y: 25 }),
    };
    const mockCoordinateSystem = {
      getSceneCenter: vi.fn().mockReturnValue({ x: 100, y: 100 }),
      getInitialPosition: vi.fn().mockResolvedValue({ x: 100, y: 100 }),
    };

    orchestrator = new ArrowPositionCalculator(
      mockLocationCalculator as any,
      mockRotationCalculator as any,
      mockAdjustmentCalculator as any,
      mockCoordinateSystem as any
    );
  });

  describe("transformAdjustmentByRotation", () => {
    it("should not transform adjustments for 0° rotation", () => {
      // Access private method for testing
      const transform = (orchestrator as any).transformAdjustmentByRotation;

      const [transformedX, transformedY] = transform(40, 25, 0);

      expect(transformedX).toBeCloseTo(40, 5);
      expect(transformedY).toBeCloseTo(25, 5);
    });

    it("should correctly transform adjustments for 90° rotation", () => {
      const transform = (orchestrator as any).transformAdjustmentByRotation;

      // For 90° rotation, (x,y) should become (y,-x) in inverse rotation
      const [transformedX, transformedY] = transform(40, 25, 90);

      expect(transformedX).toBeCloseTo(25, 5);
      expect(transformedY).toBeCloseTo(-40, 5);
    });

    it("should correctly transform adjustments for 180° rotation", () => {
      const transform = (orchestrator as any).transformAdjustmentByRotation;

      // For 180° rotation, (x,y) should become (-x,-y) in inverse rotation
      const [transformedX, transformedY] = transform(40, 25, 180);

      expect(transformedX).toBeCloseTo(-40, 5);
      expect(transformedY).toBeCloseTo(-25, 5);
    });

    it("should correctly transform adjustments for 270° rotation", () => {
      const transform = (orchestrator as any).transformAdjustmentByRotation;

      // For 270° rotation, (x,y) should become (-y,x) in inverse rotation
      const [transformedX, transformedY] = transform(40, 25, 270);

      expect(transformedX).toBeCloseTo(-25, 5);
      expect(transformedY).toBeCloseTo(40, 5);
    });

    it("should handle negative adjustment values correctly", () => {
      const transform = (orchestrator as any).transformAdjustmentByRotation;

      const [transformedX, transformedY] = transform(-40, -25, 90);

      expect(transformedX).toBeCloseTo(-25, 5);
      expect(transformedY).toBeCloseTo(40, 5);
    });
  });

  describe("Real-world arrow positioning scenarios", () => {
    it("should apply rotation transformation in positioning pipeline", () => {
      // Test the transformation method directly with real-world values
      const transform = (orchestrator as any).transformAdjustmentByRotation;

      // Your observed case: Northwest arrow with 225° rotation and (40, 25) adjustment
      const adjustmentX = 40;
      const adjustmentY = 25;
      const rotation = 225;

      // Apply the transformation
      const [transformedX, transformedY] = transform(
        adjustmentX,
        adjustmentY,
        rotation
      );

      // Calculate expected values manually
      const rotationRadians = (225 * Math.PI) / 180;
      const cos = Math.cos(-rotationRadians);
      const sin = Math.sin(-rotationRadians);
      const expectedX = 40 * cos - 25 * sin;
      const expectedY = 40 * sin + 25 * cos;

      // Verify the transformation matches expected calculation
      expect(transformedX).toBeCloseTo(expectedX, 5);
      expect(transformedY).toBeCloseTo(expectedY, 5);

      // Verify it's different from the original values (proving transformation occurred)
      expect(transformedX).not.toBeCloseTo(adjustmentX, 1);
      expect(transformedY).not.toBeCloseTo(adjustmentY, 1);
    });

    it("should demonstrate the difference between old and new positioning", () => {
      const transform = (orchestrator as any).transformAdjustmentByRotation;

      // Your observed case: Northwest arrow with 225° rotation and (40, 25) adjustment
      const adjustmentX = 40;
      const adjustmentY = 25;
      const rotation = 225;
      const initialX = 100;
      const initialY = 100;

      // Old method (simple addition - what was happening before)
      const oldFinalX = initialX + adjustmentX; // 140
      const oldFinalY = initialY + adjustmentY; // 125

      // New method (with rotation transformation)
      const [transformedX, transformedY] = transform(
        adjustmentX,
        adjustmentY,
        rotation
      );
      const newFinalX = initialX + transformedX;
      const newFinalY = initialY + transformedY;

      // The results should be different, proving the transformation is working
      expect(newFinalX).not.toBeCloseTo(oldFinalX, 1);
      expect(newFinalY).not.toBeCloseTo(oldFinalY, 1);

      // Log the difference for debugging
      console.log("Old positioning:", { x: oldFinalX, y: oldFinalY });
      console.log("New positioning:", { x: newFinalX, y: newFinalY });
      console.log("Transformation applied:", { transformedX, transformedY });
    });
  });
});
