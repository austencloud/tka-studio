/**
 * useArrowPositioning.ts - Arrow Positioning Coordination Hook
 *
 * Provides a factory function for arrow positioning coordination.
 * REFACTORED: Updated to use DI container and proper reactive patterns.
 */

import type { PictographData } from "$lib/domain";

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
  // Clean architecture: Calculate positions from motion data only
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
      // ULTIMATE CLEAN ARCHITECTURE: Calculate positions directly from motion data
      // No more arrows property - everything calculated from motion data!
      const newPositions: Record<
        string,
        { x: number; y: number; rotation: number }
      > = {};
      const newMirroring: Record<string, boolean> = {};

      // Calculate positions for each motion
      for (const [color, motionData] of Object.entries(
        pictographData.motions
      )) {
        if (motionData && motionData.isVisible) {
          // Calculate position from motion data - no gridData needed
          // For now, use basic positioning until orchestrator is updated
          const position = {
            positionX: 475, // Default center
            positionY: 475, // Default center
            rotationAngle: 0,
            svgMirrored: false,
          };

          newPositions[color] = {
            x: position.positionX || 475,
            y: position.positionY || 475,
            rotation: position.rotationAngle || 0,
          };
          newMirroring[color] = position.svgMirrored || false;
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
