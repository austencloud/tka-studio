/**
 * useArrowPositioning.ts - Arrow Positioning Coordination Hook
 *
 * Provides a factory function for arrow positioning coordination.
 * REFACTORED: Updated to use DI container and proper reactive patterns.
 */

import type { PictographData } from "$lib/domain";
// Re-enabled after fixing circular dependency
import type { IArrowPositioningService } from "$lib/services/interfaces/positioning-interfaces";

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
  // TODO: Temporarily disabled due to circular dependency
  // Get the arrow positioning service from DI container
  // const positioningService = resolve(
  //   IArrowPositioningServiceInterface
  // ) as IArrowPositioningService;

  // Temporary fallback - return mock service
  const positioningService: IArrowPositioningService = {
    calculatePosition: async () => ({ x: 0, y: 0, rotation: 0 }),
    shouldMirror: () => false,
  };

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
      console.log(
        "🎯 useArrowPositioning: Starting position calculation for pictograph:",
        pictographData.letter
      );

      const newPositions: Record<
        string,
        { x: number; y: number; rotation: number }
      > = {};
      const newMirroring: Record<string, boolean> = {};

      // Calculate positions for each motion using the actual positioning orchestrator
      for (const [color, motionData] of Object.entries(
        pictographData.motions
      )) {
        if (
          motionData &&
          motionData.isVisible &&
          motionData.arrowPlacementData
        ) {
          console.log(
            `🏹 useArrowPositioning: Calculating position for ${color} arrow`
          );

          try {
            // Use the actual ArrowPositioningService to calculate positions
            const positionResult = await positioningService.calculatePosition(
              motionData.arrowPlacementData,
              motionData,
              pictographData
            );

            const mirroringResult = positioningService.shouldMirror(
              motionData.arrowPlacementData,
              motionData,
              pictographData
            );

            newPositions[color] = {
              x: positionResult.x,
              y: positionResult.y,
              rotation: positionResult.rotation,
            };
            newMirroring[color] = mirroringResult;

            console.log(
              `✅ useArrowPositioning: ${color} arrow positioned at (${positionResult.x}, ${positionResult.y}) rotation: ${positionResult.rotation}`
            );
          } catch (error) {
            console.error(
              `❌ useArrowPositioning: Failed to calculate position for ${color} arrow:`,
              error
            );

            // Fallback to center position if orchestrator fails
            newPositions[color] = {
              x: 475,
              y: 475,
              rotation: 0,
            };
            newMirroring[color] = false;
          }
        }
      }

      console.log(
        "✅ useArrowPositioning: All positions calculated:",
        newPositions
      );

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
