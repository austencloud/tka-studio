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

import type { MotionData, PictographData, GridMode } from "$lib/domain";
import { MotionType, ArrowType } from "$lib/domain";
import type { IArrowAdjustmentCalculator } from "../../core-services";
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
import type { Location, MotionType as MotionTypeType, Point } from "../../types";
import { AttributeKeyGenerator } from "../key_generators/AttributeKeyGenerator";
import { PlacementKeyGenerator } from "../key_generators/PlacementKeyGenerator";
import { SpecialPlacementOriKeyGenerator } from "../key_generators/SpecialPlacementOriKeyGenerator";
import { TurnsTupleKeyGenerator } from "../key_generators/TurnsTupleKeyGenerator";
import { DefaultPlacementService } from "../placement/DefaultPlacementService";
import { SpecialPlacementService } from "../placement/SpecialPlacementService";
import {
  DirectionalTupleCalculator,
  DirectionalTupleProcessor,
  QuadrantIndexCalculator,
  type IDirectionalTupleProcessor,
} from "../processors/DirectionalTupleProcessor";

export class ArrowAdjustmentCalculator implements IArrowAdjustmentCalculator {
  /**
   * Consolidated service combining lookup and calculation logic.
   * Eliminates the pure delegation layer while maintaining identical behavior.
   */

  // Lookup services (previously in ArrowAdjustmentLookup)
  private specialPlacementService: ISpecialPlacementService;
  private defaultPlacementService: IDefaultPlacementService;
  private orientationKeyService: ISpecialPlacementOriKeyGenerator;
  private placementKeyService: IPlacementKeyGenerator;
  private turnsTupleService: ITurnsTupleKeyGenerator;
  private attributeKeyService: IAttributeKeyGenerator;

  // Processing services
  private tupleProcessor: IDirectionalTupleProcessor;

  constructor(options?: {
    specialPlacementService?: ISpecialPlacementService;
    defaultPlacementService?: IDefaultPlacementService;
    orientationKeyService?: ISpecialPlacementOriKeyGenerator;
    placementKeyService?: IPlacementKeyGenerator;
    turnsTupleService?: ITurnsTupleKeyGenerator;
    attributeKeyService?: IAttributeKeyGenerator;
    tupleProcessor?: IDirectionalTupleProcessor;
  }) {
    // Initialize services with defaults if not provided
    this.specialPlacementService = options?.specialPlacementService || new SpecialPlacementService();
    this.defaultPlacementService = options?.defaultPlacementService || new DefaultPlacementService();
    this.orientationKeyService = options?.orientationKeyService || new SpecialPlacementOriKeyGenerator();
    this.placementKeyService = options?.placementKeyService || new PlacementKeyGenerator();
    this.turnsTupleService = options?.turnsTupleService || new TurnsTupleKeyGenerator();
    this.attributeKeyService = options?.attributeKeyService || new AttributeKeyGenerator();
    this.tupleProcessor = options?.tupleProcessor || this.createDefaultTupleProcessor();
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

  calculateAdjustmentSync(
    pictographData: PictographData,
    motionData: MotionData,
    letter: string,
    location: Location,
    _arrowColor?: string
  ): Point {
    /**
     * Synchronous version - IDENTICAL logic to original.
     * Uses simplified approach that bypasses async lookup services.
     */
    try {
      // Use the directional tuple processor directly with basic adjustments
      const baseAdjustment = this.getBasicAdjustmentSync(motionData);
      const finalAdjustment = this.tupleProcessor.processDirectionalTuples(
        baseAdjustment,
        motionData,
        location
      );

      console.debug(
        `Sync adjustment for ${motionData.motion_type} ${motionData.turns} turns at ${location}: (${finalAdjustment.x}, ${finalAdjustment.y})`
      );

      return finalAdjustment;
    } catch (error) {
      console.warn(
        `Sync adjustment calculation failed for letter ${letter}: ${error}`
      );
      return { x: 0, y: 0 };
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
        return specialAdjustment;
      } catch {
        // No special placement found - fall back to default
        console.debug("No special placement found, falling back to default");
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

      // Create minimal arrow data for attribute key generation
      const color = "blue";
      const tempArrow = {
        id: "temp",
        arrow_type: ArrowType.BLUE,
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
        pictographData
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
  ): Promise<Point> {
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

      throw new Error("No special placement found");
    } catch (error) {
      if (
        error instanceof Error &&
        error.message === "No special placement found"
      ) {
        throw error;
      }
      console.error("Error in special placement lookup:", error);
      throw new Error(`Special placement lookup failed: ${error}`);
    }
  }

  private async calculateDefaultAdjustment(
    motionData: MotionData,
    pictographData: PictographData,
    gridMode: string = "diamond"
  ): Promise<Point> {
    /**
     * Calculate default adjustment - IDENTICAL to ArrowAdjustmentLookup.
     */
    try {
      const keys = await this.defaultPlacementService.getAvailablePlacementKeys(
        motionData.motion_type as MotionTypeType,
        pictographData.grid_mode as GridMode
      );
      const defaultPlacements: Record<string, unknown> = Object.fromEntries(
        (keys || []).map((k) => [k, true])
      );

      const placementKey = this.placementKeyService.generatePlacementKey(
        motionData,
        pictographData,
        defaultPlacements,
        gridMode
      );

      const adjustmentPoint =
        await this.defaultPlacementService.getDefaultAdjustment(
          placementKey,
          motionData.turns || 0,
          motionData.motion_type as MotionTypeType,
          gridMode as GridMode
        );

      return adjustmentPoint;
    } catch (error) {
      console.error("Error calculating default adjustment:", error);
      throw new Error(`Default adjustment calculation failed: ${error}`);
    }
  }

  private getBasicAdjustmentSync(motionData: MotionData): Point {
    /**Get basic adjustment values for synchronous operation - IDENTICAL to original.*/
    const motionType = motionData.motion_type;
    const turns = typeof motionData.turns === "number" ? motionData.turns : 0;
    const turnsStr =
      turns === Math.floor(turns) ? turns.toString() : turns.toString();

    // Use actual placement data structure (simplified for sync operation)
    const placementData: Record<string, Record<string, [number, number]>> = {
      [MotionType.PRO]: {
        "0": [-10, -40],
        "0.5": [30, 105],
        "1": [30, 25],
        "1.5": [-35, 145],
        "2": [-10, -35],
        "2.5": [20, 100],
        "3": [30, 25],
      },
      [MotionType.ANTI]: {
        "0": [0, -40],
        "0.5": [-15, 110],
        "1": [0, -40],
        "1.5": [20, 155],
        "2": [0, -40],
        "2.5": [0, 100],
        "3": [0, -50],
      },
      [MotionType.STATIC]: {
        "0": [0, 0],
        "0.5": [0, -140],
        "1": [50, 50],
        "1.5": [0, 0],
        "2": [0, 0],
        "2.5": [0, 0],
        "3": [0, 0],
      },
      [MotionType.DASH]: {
        "0": [0, 0],
      },
      [MotionType.FLOAT]: {
        fl: [30, -30],
      },
    };

    const motionAdjustments = placementData[motionType];
    if (motionAdjustments && motionAdjustments[turnsStr]) {
      const [x, y] = motionAdjustments[turnsStr];
      return { x, y };
    }

    return { x: 0, y: 0 };
  }

  private createDefaultTupleProcessor(): IDirectionalTupleProcessor {
    /**Create tuple processor with default dependencies.*/
    return new DirectionalTupleProcessor(
      new DirectionalTupleCalculator(),
      new QuadrantIndexCalculator()
    );
  }
}
