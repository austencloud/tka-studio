/**
 * Motion Generation Service - Generate individual motions
 *
 * This service will eventually port the motion generation algorithms
 * from the desktop application. For now, it provides basic motion generation.
 */

import type { BeatData, MotionData } from "$lib/domain";
import {
  Location,
  MotionType,
  Orientation,
  RotationDirection,
} from "$lib/domain/enums";
import type {
  GenerationOptions,
  IMotionGenerationService,
} from "../interfaces";

export class MotionGenerationService implements IMotionGenerationService {
  /**
   * Generate a motion for a specific color
   */
  async generateMotion(
    color: "blue" | "red",
    _options: GenerationOptions,
    _previousBeats: BeatData[],
  ): Promise<MotionData> {
    try {
      console.log(`Generating ${color} motion`);

      // Basic motion generation (placeholder)
      const motionTypes = [
        MotionType.PRO,
        MotionType.ANTI,
        MotionType.FLOAT,
        MotionType.DASH,
        MotionType.STATIC,
      ];
      const locations = [
        Location.NORTH,
        Location.EAST,
        Location.SOUTH,
        Location.WEST,
        Location.NORTHEAST,
        Location.SOUTHEAST,
        Location.SOUTHWEST,
        Location.NORTHWEST,
      ];
      const orientations = [
        Orientation.IN,
        Orientation.OUT,
        Orientation.CLOCK,
        Orientation.COUNTER,
      ];
      const rotationDirections = [
        RotationDirection.CLOCKWISE,
        RotationDirection.COUNTER_CLOCKWISE,
        RotationDirection.NO_ROTATION,
      ];

      // Simple random selection (will be replaced with proper algorithms)
      const motionType = this.randomChoice(motionTypes);
      const startLoc = this.randomChoice(locations);
      const endLoc = this.randomChoice(locations);
      const startOri = this.randomChoice(orientations);
      const endOri = this.randomChoice(orientations);
      const propRotDir = this.randomChoice(rotationDirections);

      // Calculate turns based on motion type and locations
      const turns = this.calculateTurns(motionType, startLoc, endLoc);

      const motion: MotionData = {
        motion_type: motionType,
        prop_rot_dir: propRotDir,
        start_loc: startLoc,
        end_loc: endLoc,
        turns,
        start_ori: startOri,
        end_ori: endOri,
        is_visible: true,
      };

      console.log(`Generated ${color} motion:`, motion);
      return motion;
    } catch (error) {
      console.error(`Failed to generate ${color} motion:`, error);
      throw new Error(
        `Motion generation failed: ${error instanceof Error ? error.message : "Unknown error"}`,
      );
    }
  }

  /**
   * Calculate turns for a motion
   */
  private calculateTurns(
    motionType: string,
    startLoc: string,
    endLoc: string,
  ): number {
    // Simple turn calculation (placeholder)
    if (motionType === "static") return 0;
    if (motionType === "dash") return 0;

    // For pro/anti/float, calculate based on location change
    const locationOrder = ["n", "ne", "e", "se", "s", "sw", "w", "nw"];
    const startIndex = locationOrder.indexOf(startLoc);
    const endIndex = locationOrder.indexOf(endLoc);

    if (startIndex === -1 || endIndex === -1) return 1;

    const distance = Math.abs(endIndex - startIndex);
    return Math.min(distance, 8 - distance);
  }

  /**
   * Random choice helper
   */
  private randomChoice<T>(array: readonly T[]): T {
    if (array.length === 0) {
      throw new Error("randomChoice called with empty array");
    }
    // At this point array has at least one element; assertion is safe
    return array[Math.floor(Math.random() * array.length)] as T;
  }

  /**
   * Generate motion with constraints
   */
  async generateConstrainedMotion(
    color: "blue" | "red",
    options: GenerationOptions,
    previousBeats: BeatData[],
    _constraints: {
      allowedMotionTypes?: string[];
      allowedStartLocations?: string[];
      allowedEndLocations?: string[];
    },
  ): Promise<MotionData> {
    // TODO: Implement constrained generation
    // For now, use basic generation
    return this.generateMotion(color, options, previousBeats);
  }

  /**
   * Validate if a motion is valid given the context
   */
  validateMotion(
    motion: MotionData,
    _color: "blue" | "red",
    _previousBeats: BeatData[],
  ): { isValid: boolean; reasons: string[] } {
    const reasons: string[] = [];

    // Basic validation
    if (!motion.motion_type) {
      reasons.push("Motion type is required");
    }

    if (!motion.start_loc) {
      reasons.push("Start location is required");
    }

    if (!motion.end_loc) {
      reasons.push("End location is required");
    }

    // TODO: Add more sophisticated validation rules from desktop app

    return {
      isValid: reasons.length === 0,
      reasons,
    };
  }
}
