/**
 * Arrow Positioning Service for Svelte Components
 *
 * SINGLE SOURCE OF TRUTH: Thin wrapper around ArrowPositioningOrchestrator.
 * All positioning logic handled by the sophisticated positioning pipeline.
 * NO duplicate positioning logic allowed!
 */

import type { ArrowData, MotionData, PictographData } from "$lib/domain";
import { ArrowType } from "$lib/domain";
import type { IArrowPositioningOrchestrator } from "$lib/services/positioning";
import { getPositioningServiceFactory } from "$lib/services/positioning/PositioningServiceFactory";

export interface ArrowPositionResult {
  x: number;
  y: number;
  rotation: number;
}

export interface ArrowPositioningInput {
  arrow_type: "blue" | "red";
  motion_type: string;
  location: string;
  grid_mode: string;
  turns: number;
  letter?: string;
  start_orientation?: string;
  end_orientation?: string;
}

export interface Position {
  x: number;
  y: number;
}

export class ArrowPositioningService {
  private orchestrator: IArrowPositioningOrchestrator;

  constructor() {
    // Use the singleton factory to get a properly configured orchestrator
    // This prevents recreating placement services and reloading data on hot reload
    const factory = getPositioningServiceFactory();
    this.orchestrator = factory.createPositioningOrchestrator();
  }

  /**
   * Calculate arrow position using the sophisticated positioning pipeline
   */
  async calculatePosition(
    arrowData: ArrowData,
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<ArrowPositionResult> {
    console.log(
      `🎯 ArrowPositioningService.calculatePosition called for ${arrowData.color} arrow`
    );
    console.log(`Arrow data:`, {
      motion_type: arrowData.motion_type,
      start_orientation: arrowData.start_orientation,
      end_orientation: arrowData.end_orientation,
      turns: arrowData.turns,
      position_x: arrowData.position_x,
      position_y: arrowData.position_y,
    });
    console.log(`Motion data:`, {
      motion_type: motionData.motion_type,
      start_loc: motionData.start_loc,
      end_loc: motionData.end_loc,
      turns: motionData.turns,
    });

    try {
      // Use the sophisticated positioning pipeline
      console.log(`🔧 Calling orchestrator.calculateArrowPosition...`);
      const [x, y, rotation] = this.orchestrator.calculateArrowPosition(
        arrowData,
        pictographData,
        motionData
      );

      console.log(
        `✅ Orchestrator returned: (${x}, ${y}) rotation: ${rotation}°`
      );
      return { x, y, rotation };
    } catch (error) {
      console.error("🚨 CRITICAL: Orchestrator positioning failed:", error);
      console.error("This should never happen in production!");
      throw error; // Don't hide orchestrator failures
    }
  }

  /**
   * Synchronous position calculation (may not include full adjustments)
   */
  calculatePositionSync(
    arrowData: ArrowData,
    motionData: MotionData,
    pictographData: PictographData
  ): ArrowPositionResult {
    try {
      console.log(`🎯 Calculating sync position for ${arrowData.color} arrow`);
      console.log(
        `Motion: ${motionData.motion_type}, Start: ${motionData.start_loc}, End: ${motionData.end_loc}`
      );

      // Use the synchronous positioning method
      const [x, y, rotation] = this.orchestrator.calculateArrowPosition(
        arrowData,
        pictographData,
        motionData
      );

      console.log(
        `✅ Calculated sync position: (${x}, ${y}) rotation: ${rotation}°`
      );

      return { x, y, rotation };
    } catch (error) {
      console.error("🚨 CRITICAL: Sync positioning failed:", error);
      console.error("This should never happen in production!");
      throw error; // Don't hide orchestrator failures
    }
  }

  /**
   * Determine if arrow should be mirrored based on motion data
   */
  shouldMirror(
    arrowData: ArrowData,
    _motionData: MotionData,
    pictographData: PictographData
  ): boolean {
    try {
      return this.orchestrator.shouldMirrorArrow(arrowData, pictographData);
    } catch (error) {
      console.error("🚨 CRITICAL: Mirror determination failed:", error);
      throw error; // Don't hide orchestrator failures
    }
  }

  /**
   * Legacy interface for backward compatibility
   */
  async calculatePosition_legacy(
    input: ArrowPositioningInput
  ): Promise<Position> {
    const arrowData: ArrowData = {
      color: input.arrow_type,
      arrow_type: input.arrow_type === "blue" ? ArrowType.BLUE : ArrowType.RED,
      location: input.location,
      motion_type: input.motion_type,
    } as ArrowData;

    const motionData: MotionData = {
      motion_type: input.motion_type,
      start_loc: input.location,
      start_ori: input.start_orientation || "in",
      end_ori: input.end_orientation || "in",
      prop_rot_dir: "cw",
      turns: input.turns,
    } as MotionData;

    const pictographData: PictographData = {
      letter: input.letter || "A",
      grid_mode: input.grid_mode,
      motions: {
        [input.arrow_type]: motionData,
      },
    } as PictographData;

    const result = await this.calculatePosition(
      arrowData,
      motionData,
      pictographData
    );
    return { x: result.x, y: result.y };
  }

  /**
   * Emergency fallback - should never be used in normal operation
   */
  private getFallbackPosition(motionData: MotionData): ArrowPositionResult {
    console.error(
      "🚨 CRITICAL: Using emergency fallback positioning! This indicates orchestrator failure!"
    );
    console.error("Motion data:", motionData);

    // Use center position as emergency fallback
    return {
      x: 475.0,
      y: 475.0,
      rotation: 0,
    };
  }
}

// Create singleton instance
export const arrowPositioningService = new ArrowPositioningService();
