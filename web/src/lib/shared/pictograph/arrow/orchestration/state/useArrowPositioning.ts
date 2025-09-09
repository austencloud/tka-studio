/**
 * useArrowPositioning.ts - Arrow Positioning Coordination Hook
 *
 * Provides a factory function for arrow positioning coordination.
 * REFACTORED: Updated to use DI container and proper reactive patterns.
 */

import type {
  IArrowPositioningOrchestrator,
  MotionData,
  PictographData,
} from "$shared";
import { resolve, TYPES } from "$shared";

export interface ArrowPositioningProps {
  /** Current pictograph data containing arrows */
  pictographData: PictographData | null;
}

export interface ArrowPositioningState {
  /** Calculate arrow positions for all arrows */
  calculateArrowPositions(data: PictographData | null): Promise<{
    positions: Record<string, { x: number; y: number; rotation: number }>;
    mirroring: Record<string, boolean>;
    showArrows: boolean;
  }>;
}

/**
 * Factory function for arrow positioning coordination.
 * Returns the orchestrator and calculation function using DI container.
 */
export function useArrowPositioning(
  _props: ArrowPositioningProps
): ArrowPositioningState {
  // 🚨 CRITICAL FIX: Re-enable the arrow positioning orchestrator
  // Get the arrow positioning orchestrator from DI container
  const arrowOrchestrator = resolve<IArrowPositioningOrchestrator>(
    TYPES.IArrowPositioningOrchestrator
  );

  // Clean architecture: Calculate positions from motion data using the orchestrator
  async function calculateArrowPositions(
    pictographData: PictographData | null
  ) {
    if (!pictographData?.motions) {
      return {
        positions: {},
        mirroring: {},
        showArrows: true,
      };
    }

    try {
      const newPositions: Record<
        string,
        { x: number; y: number; rotation: number }
      > = {};
      const newMirroring: Record<string, boolean> = {};

      // 🚨 CRITICAL FIX: Use the actual ArrowPositioningOrchestrator
      console.log(
        "🎯 useArrowPositioning: Starting calculation for pictograph"
      );

      // First, calculate all arrow positions using the orchestrator
      const updatedPictographData =
        await arrowOrchestrator.calculateAllArrowPoints(pictographData);

      // Extract positions and mirroring from the updated data
      for (const [color, motionData] of Object.entries(
        updatedPictographData.motions || {}
      )) {
        const typedMotionData = motionData as MotionData;
        if (
          typedMotionData &&
          typedMotionData.isVisible &&
          typedMotionData.arrowPlacementData
        ) {
          try {
            const arrowPlacement = typedMotionData.arrowPlacementData;

            newPositions[color] = {
              x: arrowPlacement.positionX,
              y: arrowPlacement.positionY,
              rotation: arrowPlacement.rotationAngle || 0,
            };

            newMirroring[color] = arrowPlacement.svgMirrored || false;
          } catch (error) {
            console.error(
              `❌ useArrowPositioning: Failed to extract position for ${color} arrow:`,
              error
            );

            // Fallback to center position if extraction fails
            newPositions[color] = {
              x: 475,
              y: 475,
              rotation: 0,
            };
            newMirroring[color] = false;
          }
        }
      }

      return {
        positions: newPositions,
        mirroring: newMirroring,
        showArrows: true,
      };
    } catch (error) {
      console.error("Orchestrator positioning failed:", error);
      // Fallback: show arrows without coordination
      return {
        positions: {},
        mirroring: {},
        showArrows: true,
      };
    }
  }

  return {
    calculateArrowPositions,
  };
}
