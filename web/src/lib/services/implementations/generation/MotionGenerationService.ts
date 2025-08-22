/**
 * Motion Generation Service - Generate individual motions
 *
 * This service will eventually port the motion generation algorithms
 * from the desktop application. For now, it provides basic motion generation.
 */

import type { BeatData, MotionData } from "$lib/domain";
import { createMotionData } from "$lib/domain";
import {
  Location,
  MotionType,
  Orientation,
  PropType,
  RotationDirection,
  MotionColor,
} from "$lib/domain/enums";
import type {
  GenerationOptions,
  IMotionGenerationService,
} from "../../interfaces/generation-interfaces";

export class MotionGenerationService implements IMotionGenerationService {
  /**
   * Generate a motion for a specific color
   */
  async generateMotion(
    color: MotionColor,
    _options: GenerationOptions,
    _previousBeats: BeatData[]
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
      const startLocation = this.randomChoice(locations);
      const endLocation = this.randomChoice(locations);
      const startOrientation = this.randomChoice(orientations);
      const endOrientation = this.randomChoice(orientations);
      const rotationDirection = this.randomChoice(rotationDirections);

      // Calculate turns based on motion type and locations
      const turns = this.calculateTurns(motionType, startLocation, endLocation);

      const motion: MotionData = createMotionData({
        motionType: motionType,
        rotationDirection: rotationDirection,
        startLocation: startLocation,
        endLocation: endLocation,
        turns,
        startOrientation: startOrientation,
        endOrientation: endOrientation,
        color: color,
        isVisible: true,
        propType: PropType.STAFF, // Default prop type
        arrowLocation: startLocation, // Will be calculated by ArrowLocationCalculator
      });

      console.log(`Generated ${color} motion:`, motion);
      return motion;
    } catch (error) {
      console.error(`Failed to generate ${color} motion:`, error);
      throw new Error(
        `Motion generation failed: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Calculate turns for a motion
   */
  private calculateTurns(
    motionType: string,
    startLocation: string,
    endLocation: string
  ): number {
    // Simple turn calculation (placeholder)
    if (motionType === "static") return 0;
    if (motionType === "dash") return 0;

    // For pro/anti/float, calculate based on location change
    const locationOrder = ["n", "ne", "e", "se", "s", "sw", "w", "nw"];
    const startIndex = locationOrder.indexOf(startLocation);
    const endIndex = locationOrder.indexOf(endLocation);

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
    color: MotionColor,
    options: GenerationOptions,
    previousBeats: BeatData[],
    _constraints: {
      allowedMotionTypes?: string[];
      allowedStartLocations?: string[];
      allowedEndLocations?: string[];
    }
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
    _color: MotionColor,
    _previousBeats: BeatData[]
  ): { isValid: boolean; reasons: string[] } {
    const reasons: string[] = [];

    // Basic validation
    if (!motion.motionType) {
      reasons.push("Motion type is required");
    }

    if (!motion.startLocation) {
      reasons.push("Start location is required");
    }

    if (!motion.endLocation) {
      reasons.push("End location is required");
    }

    // TODO: Add more sophisticated validation rules from desktop app

    return {
      isValid: reasons.length === 0,
      reasons,
    };
  }
}
