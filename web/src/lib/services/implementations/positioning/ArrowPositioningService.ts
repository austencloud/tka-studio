/**
 * Arrow Positioning Service for Svelte Components
 *
 * SINGLE SOURCE OF TRUTH: Thin wrapper around ArrowPositioningOrchestrator.
 * All positioning logic handled by the sophisticated positioning pipeline.
 * NO duplicate positioning logic allowed!
 *
 * REFACTORED: Removed singleton pattern, now uses DI container.
 */

import type { ArrowPlacementData, MotionData, PictographData } from "$domain";
import { GridMode, Orientation,  } from "$domain";
import { Location, MotionColor, MotionType } from "$domain/enums";
import type { Letter } from "$domain/core/Letter";
import type { IArrowPositioningOrchestrator } from "$lib/services/contracts/positioning-interfaces";
import { TYPES } from "$lib/services/inversify/types";
import { inject, injectable } from "inversify";

export interface ArrowPositionResult {
  x: number;
  y: number;
  rotation: number;
}

export interface ArrowPositioningInput {
  color: MotionColor;
  motionType: MotionType;
  location: Location;
  gridMode: GridMode;
  turns: number;
  letter: Letter;
  startOrientation: Orientation;
  endOrientatio?: Orientation;
}

export interface IArrowPositioningService {
  calculatePosition(
    arrowData: ArrowPlacementData,
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<ArrowPositionResult>;
  shouldMirror(
    arrowData: ArrowPlacementData,
    motionData: MotionData,
    pictographData: PictographData
  ): boolean;
}

@injectable()
export class ArrowPositioningService implements IArrowPositioningService {
  constructor(
    @inject(TYPES.IArrowPositioningOrchestrator)
    private orchestrator: IArrowPositioningOrchestrator
  ) {}

  /**
   * Calculate arrow position using the sophisticated positioning pipeline
   */
  async calculatePosition(
    arrowPlacementData: ArrowPlacementData,
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<ArrowPositionResult> {
    // Debug logging removed for performance

    try {
      // Use the sophisticated positioning pipeline
      const [x, y, rotation] = await this.orchestrator.calculateArrowPosition(
        pictographData,
        motionData
      );

      return { x, y, rotation };
    } catch (error) {
      console.error("Orchestrator positioning failed:", error);
      throw error; // Don't hide orchestrator failures
    }
  }

  /**
   * Determine if arrow should be mirrored based on motion data
   */
  shouldMirror(
    arrowData: ArrowPlacementData,
    _motionData: MotionData,
    pictographData: PictographData
  ): boolean {
    try {
      return this.orchestrator.shouldMirrorArrow(arrowData, pictographData);
    } catch (error) {
      console.error("Mirror determination failed:", error);
      throw error; // Don't hide orchestrator failures
    }
  }

  /**
   * Legacy interface for backward compatibility
   */
}
