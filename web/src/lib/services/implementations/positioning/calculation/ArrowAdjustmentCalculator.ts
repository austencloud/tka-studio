/**
 * Arrow Adjustment Calculator - Consolidated Service
 *
 * Consolidated service that combines ArrowAdjustmentCalculator and ArrowAdjustmentLookup
 * to eliminate pure delegation layer. Maintains exact same interface and behavior.
 *
 * CONSOLIDATION BENEFITS:
 * - Removes unnecessary delegation layer
 * - Maintains identical logic and results
 * - Preserves all existing interfaces and test compatibility
 * - Better TypeScript organization
 */

import type { MotionData, PictographData } from "$domain";
import { GridMode, MotionColor } from "$domain";
import type {
  IArrowAdjustmentCalculator,
  IAttributeKeyGenerator,
  IDefaultPlacementService,
  IGridModeDeriver,
  ISpecialPlacementOriKeyGenerator,
  ISpecialPlacementService,
  ITurnsTupleKeyGenerator,
  Location,
  MotionType as MotionTypeType,
  Point,
} from "$lib/services/contracts/positioning-interfaces";
import { TYPES } from "$lib/services/inversify/types";
import { inject, injectable } from "inversify";
import { ArrowPlacementKeyService } from "../ArrowPlacementKeyService";
import { type IDirectionalTupleProcessor } from "../processors/DirectionalTupleProcessor";

@injectable()
export class ArrowAdjustmentCalculator implements IArrowAdjustmentCalculator {
  /**
   * Consolidated service combining lookup and calculation logic.
   * Eliminates the pure delegation layer while maintaining identical behavior.
   */

  // Lookup services (previously in ArrowAdjustmentLookup)
  private specialPlacementService: ISpecialPlacementService;
  private defaultPlacementService: IDefaultPlacementService;
  private orientationKeyService: ISpecialPlacementOriKeyGenerator;
  private placementKeyService: ArrowPlacementKeyService;
  private turnsTupleService: ITurnsTupleKeyGenerator;
  private attributeKeyService: IAttributeKeyGenerator;

  // Processing services
  private tupleProcessor: IDirectionalTupleProcessor;
  private gridModeService: IGridModeDeriver;

  constructor(
    @inject(TYPES.IGridModeDeriver) gridModeService: IGridModeDeriver,
    @inject(TYPES.ISpecialPlacementService)
    specialPlacementService: ISpecialPlacementService,
    @inject(TYPES.IDefaultPlacementService)
    defaultPlacementService: IDefaultPlacementService,
    @inject(TYPES.ISpecialPlacementOriKeyGenerator)
    orientationKeyService: ISpecialPlacementOriKeyGenerator,
    @inject(TYPES.IArrowPlacementKeyService)
    placementKeyService: ArrowPlacementKeyService,
    @inject(TYPES.ITurnsTupleKeyGenerator)
    turnsTupleService: ITurnsTupleKeyGenerator,
    @inject(TYPES.IAttributeKeyGenerator)
    attributeKeyService: IAttributeKeyGenerator,
    @inject(TYPES.IDirectionalTupleProcessor)
    tupleProcessor: IDirectionalTupleProcessor
  ) {
    // Store all injected services
    this.gridModeService = gridModeService;
    this.specialPlacementService = specialPlacementService;
    this.defaultPlacementService = defaultPlacementService;
    this.orientationKeyService = orientationKeyService;
    this.placementKeyService = placementKeyService;
    this.turnsTupleService = turnsTupleService;
    this.attributeKeyService = attributeKeyService;
    this.tupleProcessor = tupleProcessor;
  }

  async calculateAdjustment(
    pictographData: PictographData,
    motionData: MotionData,
    letter: string,
    location: Location,
    arrowColor?: string
  ): Promise<Point> {
    /**
     * Calculate arrow position adjustment - IDENTICAL logic to original.
     */
    try {
      return await this.calculateAdjustmentResult(
        pictographData,
        motionData,
        letter,
        location,
        arrowColor
      );
    } catch (error) {
      // Log error and return default for backward compatibility
      console.error(`Adjustment calculation failed: ${error}`);
      return { x: 0, y: 0 };
    }
  }

  async calculateAdjustmentResult(
    pictographData: PictographData,
    motionData: MotionData,
    letter: string,
    location: Location,
    arrowColor?: string
  ): Promise<Point> {
    /**
     * Calculate arrow position adjustment with proper error handling.
     * IDENTICAL logic to original ArrowAdjustmentCalculator.
     */
    try {
      // STEP 1: Look up base adjustment (special → default) - EXACTLY like legacy
      const baseAdjustment = await this.getBaseAdjustment(
        pictographData,
        motionData,
        letter,
        arrowColor
      );

      // STEP 2: Process directional tuples - EXACTLY like legacy
      const finalAdjustment = this.tupleProcessor.processDirectionalTuples(
        baseAdjustment,
        motionData,
        location
      );

      return finalAdjustment;
    } catch (error) {
      console.error(
        `Adjustment calculation failed for letter ${letter}: ${error}`
      );
      throw new Error(`Arrow adjustment calculation failed: ${error}`);
    }
  }

  // === PRIVATE METHODS - Consolidated from ArrowAdjustmentLookup ===

  private async getBaseAdjustment(
    pictographData: PictographData,
    motionData: MotionData,
    letter: string,
    arrowColor?: string
  ): Promise<Point> {
    /**
     * Get base adjustment using streamlined lookup logic.
     * IDENTICAL to ArrowAdjustmentLookup.getBaseAdjustment()
     */
    if (!motionData || !letter) {
      throw new Error("Missing motion or letter data for adjustment lookup");
    }

    try {
      // Generate required keys for special placement lookup
      const [oriKey, turnsTuple, attrKey] = this.generateLookupKeys(
        pictographData,
        motionData
      );

      console.debug(
        `Generated keys - ori: ${oriKey}, turns: ${turnsTuple}, attr: ${attrKey}`
      );

      try {
        const specialAdjustment = await this.lookupSpecialPlacement(
          motionData,
          pictographData,
          arrowColor
        );

        if (specialAdjustment) {
          return specialAdjustment;
        }

        // No special placement found - fall back to default
        console.debug("No special placement found, falling back to default");
      } catch {
        // Error in special placement lookup - fall back to default
        console.debug(
          "Error in special placement lookup, falling back to default"
        );
      }

      // STEP 2: Fall back to default calculation
      const defaultAdjustment = await this.calculateDefaultAdjustment(
        motionData,
        pictographData
      );
      console.debug(
        `Using default adjustment: (${defaultAdjustment.x.toFixed(1)}, ${defaultAdjustment.y.toFixed(1)})`
      );
      return defaultAdjustment;
    } catch (error) {
      console.error("Error in base adjustment lookup:", error);
      throw new Error(`Arrow adjustment lookup failed: ${error}`);
    }
  }

  private generateLookupKeys(
    pictographData: PictographData,
    motionData: MotionData
  ): [string, string, string] {
    /**Generate all required keys for special placement lookup.*/
    try {
      const oriKey = this.orientationKeyService.generateOrientationKey(
        motionData,
        pictographData
      );
      const turnsTuple =
        this.turnsTupleService.generateTurnsTuple(pictographData);

      // ✅ FIXED: Create proper ArrowPlacementData and pass color separately
      const color = MotionColor.BLUE;
      const tempArrow = {
        id: "temp",
        arrowLocation: null,
        positionX: 0,
        positionY: 0,
        rotationAngle: 0, // ✅ FIXED: Added missing rotationAngle property
        coordinates: { x: 0, y: 0 },
        svgCenter: { x: 0, y: 0 },
        svgMirrored: false,
        isVisible: true,
        isSelected: false,
      };

      const attrKey = this.attributeKeyService.getKeyFromArrow(
        tempArrow,
        pictographData,
        color
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
    arrowColor?: string
  ): Promise<Point | null> {
    /**
     * Look up special placement using exact legacy logic.
     * IDENTICAL to ArrowAdjustmentLookup.lookupSpecialPlacement()
     */
    try {
      const adjustment =
        await this.specialPlacementService.getSpecialAdjustment(
          motionData,
          pictographData,
          arrowColor
        );

      if (adjustment) {
        return adjustment;
      }

      // Return null instead of throwing when no special placement found
      return null;
    } catch (error) {
      console.error("Error in special placement lookup:", error);
      // Return null on error to allow fallback to default adjustment
      return null;
    }
  }

  private async calculateDefaultAdjustment(
    motionData: MotionData,
    pictographData: PictographData
  ): Promise<Point> {
    /**
     * Calculate default adjustment - IDENTICAL to ArrowAdjustmentLookup.
     */
    try {
      // Compute gridMode from motion data
      const derivedGridMode =
        pictographData.motions?.blue && pictographData.motions?.red
          ? this.gridModeService.deriveGridMode(
              pictographData.motions.blue,
              pictographData.motions.red
            )
          : GridMode.DIAMOND;

      const keys = await this.defaultPlacementService.getAvailablePlacementKeys(
        motionData.motionType as MotionTypeType,
        derivedGridMode as GridMode
      );
      const defaultPlacements: Record<string, unknown> = Object.fromEntries(
        (keys || []).map((k) => [k, true])
      );

      const availableKeys = Object.keys(defaultPlacements || []);

      const placementKey = this.placementKeyService.generatePlacementKey(
        motionData,
        pictographData,
        availableKeys
      );

      const adjustmentPoint =
        await this.defaultPlacementService.getDefaultAdjustment(
          placementKey,
          motionData.turns || 0,
          motionData.motionType as MotionTypeType,
          derivedGridMode as GridMode
        );

      return adjustmentPoint;
    } catch (error) {
      console.error("Error calculating default adjustment:", error);
      throw new Error(`Default adjustment calculation failed: ${error}`);
    }
  }
}
