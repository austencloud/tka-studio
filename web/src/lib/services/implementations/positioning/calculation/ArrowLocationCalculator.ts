/**
 * Arrow Location Calculator Service
 *
 * Pure algorithmic service for calculating arrow locations based on motion data.
 * Direct TypeScript port of the Python ArrowLocationCalculatorService.
 *
 * This service handles:
 * - Static motion location calculation (uses start location)
 * - Shift motion location calculation (PRO/ANTI/FLOAT using start/end pair mapping)
 * - Dash motion location calculation (with Type 3 detection support)
 *
 * No UI dependencies, completely testable in isolation.
 */

import type { MotionData, PictographData } from "$domain";
import { Location, MotionType } from "$domain/enums";
import type { IArrowLocationCalculator } from "$lib/services/contracts/positioning-interfaces";
import { inject, injectable } from "inversify";
import { TYPES } from "../../../inversify/types";
import { DashLocationCalculator } from "./DashLocationCalculator";

@injectable()
export class ArrowLocationCalculator implements IArrowLocationCalculator {
  /**
   * Pure algorithmic service for calculating arrow locations.
   *
   * Implements location calculation algorithms without any UI dependencies.
   * Each motion type has its own calculation strategy.
   */

  private dashLocationService: DashLocationCalculator;

  // Direction pairs mapping for shift arrows (PRO/ANTI/FLOAT)
  // Maps start/end location pairs to their calculated arrow location
  private readonly shiftDirectionPairs: Record<string, Location> = {
    // Cardinal + Diagonal combinations
    [this.createLocationPairKey([Location.NORTH, Location.EAST])]:
      Location.NORTHEAST,
    [this.createLocationPairKey([Location.EAST, Location.SOUTH])]:
      Location.SOUTHEAST,
    [this.createLocationPairKey([Location.SOUTH, Location.WEST])]:
      Location.SOUTHWEST,
    [this.createLocationPairKey([Location.WEST, Location.NORTH])]:
      Location.NORTHWEST,
    // Diagonal + Cardinal combinations
    [this.createLocationPairKey([Location.NORTHEAST, Location.NORTHWEST])]:
      Location.NORTH,
    [this.createLocationPairKey([Location.NORTHEAST, Location.SOUTHEAST])]:
      Location.EAST,
    [this.createLocationPairKey([Location.SOUTHWEST, Location.SOUTHEAST])]:
      Location.SOUTH,
    [this.createLocationPairKey([Location.NORTHWEST, Location.SOUTHWEST])]:
      Location.WEST,
  };

  constructor(
    @inject(TYPES.IDashLocationCalculator)
    dashLocationService: DashLocationCalculator
  ) {
    /**
     * Initialize the location calculator.
     *
     * Args:
     *     dashLocationService: Service for dash location calculations
     */
    this.dashLocationService = dashLocationService;
  }

  calculateLocation(
    motion: MotionData,
    pictographData: PictographData
  ): Location {
    /**
     * Calculate arrow location based on motion type and data.
     *
     * Args:
     *     motion: Motion data containing type, start/end locations, rotation direction
     *     pictographData: Optional pictograph data for DASH motion Type 3 detection
     *
     * Returns:
     *     Location enum value representing the calculated arrow location
     *
     * Throws:
     *     Error: If dash motion requires pictograph data but none provided
     */
    const motionType = motion.motionType?.toLowerCase();

    switch (motionType) {
      case "static":
        return this.calculateStaticLocation(motion);
      case "pro":
      case "anti":
      case "float":
        return this.calculateShiftLocation(motion);
      case "dash":
        return this.calculateDashLocation(motion, pictographData);
      default:
        console.warn(
          `Unknown motion type: ${motionType}, using start location`
        );
        return motion.startLocation || Location.NORTH;
    }
  }

  private calculateStaticLocation(motion: MotionData): Location {
    /**
     * Calculate location for static arrows.
     *
     * Static arrows use their start location directly.
     *
     * Args:
     *     motion: Motion data with STATIC type
     *
     * Returns:
     *     The start location of the motion
     */
    return motion.startLocation || Location.NORTH;
  }

  private calculateShiftLocation(motion: MotionData): Location {
    /**
     * Calculate location for shift arrows (PRO/ANTI/FLOAT).
     *
     * Shift arrows use a mapping from start/end location pairs to determine
     * their arrow location. This implements the proven shift location algorithm.
     *
     * Args:
     *     motion: Motion data with PRO, ANTI, or FLOAT type
     *
     * Returns:
     *     Calculated location based on start/end pair mapping
     */
    if (!motion.startLocation || !motion.endLocation) {
      console.warn(
        "Shift motion missing startLocation or endLocation, using startLocation"
      );
      return motion.startLocation || Location.NORTH;
    }

    const locationPairKey = this.createLocationPairKey([
      motion.startLocation,
      motion.endLocation,
    ]);
    const calculatedLocation =
      this.shiftDirectionPairs[locationPairKey] || motion.startLocation;

    return calculatedLocation;
  }

  private calculateDashLocation(
    motion: MotionData,
    pictographData: PictographData
  ): Location {
    /**
     * Calculate location for dash arrows.
     *
     * Dash arrows use specialized logic that require pictograph data
     * for Type 3 detection and other special cases.
     *
     * Args:
     *     motion: Motion data with DASH type
     *     pictographData: Pictograph data for Type 3 detection
     *
     * Returns:
     *     Calculated dash location
     *
     * Throws:
     *     Error: If pictograph data is required but not provided
     */
    if (!pictographData) {
      console.warn(
        "No pictograph data provided for dash location calculation, using start location"
      );
      return motion.startLocation || Location.NORTH;
    }

    const isBlueArrow = this.isBlueArrowMotion(motion, pictographData);

    return this.dashLocationService.calculateDashLocationFromPictographData(
      pictographData,
      isBlueArrow
    );
  }

  getSupportedMotionTypes(): MotionType[] {
    /**
     * Get list of motion types supported by this calculator.
     *
     * Returns:
     *     List of supported MotionType enum values
     */
    return [
      MotionType.STATIC,
      MotionType.PRO,
      MotionType.ANTI,
      MotionType.FLOAT,
      MotionType.DASH,
    ];
  }

  validateMotionData(motion: MotionData): boolean {
    /**
     * Validate that motion data is suitable for location calculation.
     *
     * Args:
     *     motion: Motion data to validate
     *
     * Returns:
     *     True if motion data is valid for location calculation
     */
    if (!motion) {
      return false;
    }

    const motionType = motion.motionType?.toLowerCase();
    if (!this.getSupportedMotionTypes().includes(motionType as MotionType)) {
      return false;
    }

    // Validate required fields based on motion type
    if (["pro", "anti", "float"].includes(motionType || "")) {
      // Shift motions require both start and end locations
      return motion.startLocation != null && motion.endLocation != null;
    }
    if (["static", "dash"].includes(motionType || "")) {
      // Static and dash motions require at least start location
      return motion.startLocation != null;
    }

    return true;
  }

  isBlueArrowMotion(
    motion: MotionData,
    pictographData: PictographData
  ): boolean {
    /**Determine if the given motion belongs to the blue arrow.*/
    // Compare the motion with blue and red motions in pictograph data
    if (pictographData.motions?.blue === motion) {
      return true;
    }
    if (pictographData.motions?.red === motion) {
      return false;
    }
    // Fallback: if we can't determine, assume blue
    console.warn("Could not determine arrow color for motion, assuming blue");
    return true;
  }

  /**
   * Create a normalized key for location pairs to enable bidirectional lookup.
   * This ensures that [A, B] and [B, A] produce the same key.
   */
  private createLocationPairKey(locations: Location[]): string {
    // Sort locations to ensure consistent key regardless of order
    const sortedLocations = [...locations].sort();
    return sortedLocations.join(",");
  }
}
