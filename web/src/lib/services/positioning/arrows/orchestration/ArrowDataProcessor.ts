/**
 * Arrow Data Processor
 *
 * Handles data extraction, validation, and manipulation for arrow positioning.
 * Responsible for working with pictograph data and arrow data structures.
 */

import type { ArrowData, MotionData, PictographData } from "$lib/domain";
import type { IArrowCoordinateSystemService } from "../../core-services";
import type { Point } from "../../types";

export class ArrowDataProcessor {
  private coordinateSystem: IArrowCoordinateSystemService;

  constructor(coordinateSystem: IArrowCoordinateSystemService) {
    this.coordinateSystem = coordinateSystem;
  }

  getMotionFromPictograph(
    arrowData: ArrowData,
    pictographData: PictographData
  ): MotionData | undefined {
    /**
     * Extract motion data from pictograph data.
     */
    if (!pictographData?.motions) {
      return undefined;
    }
    return pictographData.motions[arrowData.color];
  }

  ensureValidPosition(initialPosition: Point): Point {
    /**
     * Ensure position object has valid x and y attributes.
     */
    if (
      initialPosition &&
      typeof initialPosition.x === "number" &&
      typeof initialPosition.y === "number"
    ) {
      return initialPosition;
    }

    console.warn("Invalid initial position, using scene center");
    return this.coordinateSystem.getSceneCenter();
  }

  extractAdjustmentValues(adjustment: Point | number): [number, number] {
    /**
     * Extract x and y values from adjustment object.
     */
    if (typeof adjustment === "number") {
      return [adjustment, adjustment];
    }

    if (adjustment && typeof adjustment === "object") {
      const x = typeof adjustment.x === "number" ? adjustment.x : 0;
      const y = typeof adjustment.y === "number" ? adjustment.y : 0;
      return [x, y];
    }

    return [0.0, 0.0];
  }

  updateArrowInPictograph(
    pictographData: PictographData,
    color: string,
    updates: Partial<ArrowData>
  ): PictographData {
    /**
     * Update arrow properties in pictograph data.
     */
    const updatedPictograph = { ...pictographData };

    if (updatedPictograph.arrows && updatedPictograph.arrows[color]) {
      updatedPictograph.arrows[color] = {
        ...updatedPictograph.arrows[color],
        ...updates,
      };
    }

    return updatedPictograph;
  }

  validateArrowData(arrowData: ArrowData): boolean {
    /**
     * Validate arrow data structure.
     */
    if (!arrowData) {
      return false;
    }

    // Check required properties
    const hasColor =
      typeof arrowData.color === "string" && arrowData.color.length > 0;
    const hasValidCoordinates =
      typeof arrowData.position_x === "number" &&
      typeof arrowData.position_y === "number";

    return hasColor && hasValidCoordinates;
  }

  validateMotionData(motionData: MotionData): boolean {
    /**
     * Validate motion data structure.
     */
    if (!motionData) {
      return false;
    }

    // Check required properties
    const hasMotionType = typeof motionData.motion_type === "string";
    const hasStartLocation = motionData.start_loc !== undefined;
    const hasEndLocation = motionData.end_loc !== undefined;

    return hasMotionType && hasStartLocation && hasEndLocation;
  }

  validatePictographData(pictographData: PictographData): boolean {
    /**
     * Validate pictograph data structure.
     */
    if (!pictographData) {
      return false;
    }

    // Check for arrows object
    if (!pictographData.arrows || typeof pictographData.arrows !== "object") {
      return false;
    }

    // Validate at least one arrow exists
    const arrowColors = Object.keys(pictographData.arrows);
    if (arrowColors.length === 0) {
      return false;
    }

    // Validate each arrow
    for (const color of arrowColors) {
      const arrow = pictographData.arrows[color];
      if (!this.validateArrowData(arrow)) {
        return false;
      }
    }

    return true;
  }

  extractArrowColors(pictographData: PictographData): string[] {
    /**
     * Extract all arrow colors from pictograph data.
     */
    if (!pictographData?.arrows) {
      return [];
    }

    return Object.keys(pictographData.arrows);
  }

  getArrowByColor(
    pictographData: PictographData,
    color: string
  ): ArrowData | undefined {
    /**
     * Get arrow data by color.
     */
    if (!pictographData?.arrows) {
      return undefined;
    }

    return pictographData.arrows[color];
  }

  hasMotionData(pictographData: PictographData, color: string): boolean {
    /**
     * Check if motion data exists for the given arrow color.
     */
    if (!pictographData?.motions) {
      return false;
    }

    return color in pictographData.motions;
  }

  clonePictographData(pictographData: PictographData): PictographData {
    /**
     * Create a deep clone of pictograph data.
     */
    return JSON.parse(JSON.stringify(pictographData));
  }
}
