/**
 * Arrow Adjustment Lookup Service
 *
 * Focused service for handling special placement and default adjustment lookups.
 * Extracted from the god class ArrowAdjustmentCalculatorService.
 *
 * RESPONSIBILITIES:
 * - Special placement lookup (stored adjustments)
 * - Default placement calculation fallback
 * - Key generation for lookups
 * - Error handling with proper exceptions
 *
 * Direct TypeScript mirror of reference/modern/application/services/positioning/arrows/orchestration/arrow_adjustment_lookup.py
 */

import type {
  ArrowData,
  GridMode,
  MotionData,
  PictographData,
} from "$lib/domain";
import type {
  IAttributeKeyGenerator,
  IPlacementKeyGenerator,
  ISpecialPlacementOriKeyGenerator,
  ITurnsTupleKeyGenerator,
} from "../../data-services";
import type {
  IDefaultPlacementService,
  ISpecialPlacementService,
} from "../../placement-services";
import type { MotionType, Point } from "../../types";

export class ArrowAdjustmentLookup {
  /**
   * Focused service for arrow adjustment lookups.
   *
   * Handles the lookup phase of arrow positioning:
   * 1. Try special placement lookup (stored values)
   * 2. Fall back to default calculation
   * 3. Return proper Result types with error handling
   */

  private specialPlacementService: ISpecialPlacementService;
  private defaultPlacementService: IDefaultPlacementService;
  private orientationKeyService: ISpecialPlacementOriKeyGenerator;
  private placementKeyService: IPlacementKeyGenerator;
  private turnsTupleService: ITurnsTupleKeyGenerator;
  private attributeKeyService: IAttributeKeyGenerator;

  constructor(
    specialPlacementService: ISpecialPlacementService,
    defaultPlacementService: IDefaultPlacementService,
    orientationKeyService: ISpecialPlacementOriKeyGenerator,
    placementKeyService: IPlacementKeyGenerator,
    turnsTupleService: ITurnsTupleKeyGenerator,
    attributeKeyService: IAttributeKeyGenerator,
  ) {
    /**Initialize with required services for lookup operations.*/
    this.specialPlacementService = specialPlacementService;
    this.defaultPlacementService = defaultPlacementService;
    this.orientationKeyService = orientationKeyService;
    this.placementKeyService = placementKeyService;
    this.turnsTupleService = turnsTupleService;
    this.attributeKeyService = attributeKeyService;
  }

  async getBaseAdjustment(
    pictographData: PictographData,
    motionData: MotionData,
    letter: string,
    arrowColor?: string,
  ): Promise<Point> {
    /**
     * Get base adjustment using streamlined lookup logic.
     *
     * Args:
     *     pictographData: Pictograph data for context
     *     motionData: Motion data containing type, rotation, and location info
     *     letter: Letter for special placement lookup
     *     arrowColor: Color of the arrow ('red' or 'blue')
     *
     * Returns:
     *     Point adjustment
     *
     * Throws:
     *     Error: If input data is invalid or lookup fails
     */
    if (!motionData || !letter) {
      throw new Error("Missing motion or letter data for adjustment lookup");
    }

    try {
      // Generate required keys for special placement lookup
      const [oriKey, turnsTuple, attrKey] = this.generateLookupKeys(
        pictographData,
        motionData,
      );

      console.debug(
        `Generated keys - ori: ${oriKey}, turns: ${turnsTuple}, attr: ${attrKey}`,
      );

      try {
        const specialAdjustment = await this.lookupSpecialPlacement(
          motionData,
          pictographData,
          arrowColor,
        );
        return specialAdjustment;
      } catch {
        // No special placement found - fall back to default
        console.debug("No special placement found, falling back to default");
      }

      // STEP 2: Fall back to default calculation
      const defaultAdjustment = await this.calculateDefaultAdjustment(
        motionData,
        pictographData,
      );
      console.debug(
        `Using default adjustment: (${defaultAdjustment.x.toFixed(1)}, ${defaultAdjustment.y.toFixed(1)})`,
      );
      return defaultAdjustment;
    } catch (error) {
      console.error("Error in base adjustment lookup:", error);
      throw new Error(`Arrow adjustment lookup failed: ${error}`);
    }
  }

  private generateLookupKeys(
    pictographData: PictographData,
    motionData: MotionData,
  ): [string, string, string] {
    /**Generate all required keys for special placement lookup.*/
    try {
      const oriKey = this.orientationKeyService.generateOrientationKey(
        motionData,
        pictographData,
      );
      const turnsTuple =
        this.turnsTupleService.generateTurnsTuple(pictographData);

      // Create minimal arrow data for attribute key generation
      const color = "blue";
      const tempArrow: ArrowData = {
        id: "temp",
        arrow_type: "BLUE" as ArrowData["arrow_type"],
        color,
        motion_type: motionData.motion_type || "",
        location: "center",
        start_orientation: motionData.start_ori || "",
        end_orientation: motionData.end_ori || "",
        rotation_direction: motionData.prop_rot_dir || "",
        turns: typeof motionData.turns === "number" ? motionData.turns : 0,
        is_mirrored: false,
        position_x: 0,
        position_y: 0,
        rotation_angle: 0,
        is_visible: true,
        is_selected: false,
      };

      const attrKey = this.attributeKeyService.getKeyFromArrow(
        tempArrow,
        pictographData,
      );

      return [oriKey, turnsTuple.join(","), attrKey];
    } catch (error) {
      console.error("Failed to generate lookup keys:", error);
      throw new Error(`Key generation failed: ${error}`);
    }
  }

  private async lookupSpecialPlacement(
    motionData: MotionData,
    pictographData: PictographData,
    arrowColor?: string,
  ): Promise<Point> {
    /**
     * Look up special placement using exact legacy logic.
     *
     * Returns Point if found, throws Error if not found.
     */
    try {
      // This should return stored adjustment values if they exist
      const adjustment =
        await this.specialPlacementService.getSpecialAdjustment(
          motionData,
          pictographData,
          arrowColor,
        );

      if (adjustment) {
        return adjustment;
      }

      // No special placement found
      throw new Error("No special placement found");
    } catch (error) {
      if (
        error instanceof Error &&
        error.message === "No special placement found"
      ) {
        throw error; // Re-throw as-is
      }
      console.error("Error in special placement lookup:", error);
      throw new Error(`Special placement lookup failed: ${error}`);
    }
  }

  private async calculateDefaultAdjustment(
    motionData: MotionData,
    pictographData: PictographData,
    gridMode: string = "diamond",
  ): Promise<Point> {
    /**
     * Calculate default adjustment using placement key and motion type.
     *
     * Returns Point adjustment.
     */
    try {
      // Build a map of available placement keys for the motion/grid
      const keys = await this.defaultPlacementService.getAvailablePlacementKeys(
        motionData.motion_type as MotionType,
        pictographData.grid_mode as GridMode,
      );
      const defaultPlacements: Record<string, unknown> = Object.fromEntries(
        (keys || []).map((k) => [k, true]),
      );

      // Generate placement key for default lookup
      const placementKey = this.placementKeyService.generatePlacementKey(
        motionData,
        pictographData,
        defaultPlacements,
        gridMode,
      );

      // Get adjustment from default placement service
      const adjustmentPoint =
        await this.defaultPlacementService.getDefaultAdjustment(
          placementKey,
          motionData.turns || 0,
          motionData.motion_type as MotionType,
          gridMode as GridMode,
        );

      return adjustmentPoint;
    } catch (error) {
      console.error("Error calculating default adjustment:", error);
      throw new Error(`Default adjustment calculation failed: ${error}`);
    }
  }
}
