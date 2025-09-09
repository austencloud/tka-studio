/**
 * Special Placement Service for Modern Arrow Positioning
 *
 * This service implements special placement logic using the same JSON configuration data.
 * It provides pixel-perfect special placement adjustments for specific pictograph configurations.
 *
 * IMPLEMENTS SPECIAL PLACEMENT PIPELINE:
 * - Loads special placement JSON files from static/data/arrow_placement directory
 * - Generates orientation keys (ori_key) for motion classification
 * - Applies letter-specific, turn-specific, and motion-type-specific adjustments
 * - Handles complex placement rules for specific pictograph patterns
 *
 * Direct TypeScript mirror of reference/modern/application/services/positioning/arrows/placement/special_placement_service.py
 */

import type { IGridModeDeriver, ISpecialPlacementService } from "$shared";
import {
    type MotionData,
    type PictographData,
    GridMode,
    resolve,
    TYPES,
} from "$shared";
import { Point } from "fabric";
import { injectable } from "inversify";
import { jsonCache } from "../../../../../shared/services/implementations/SimpleJsonCache";
import { SpecialPlacementOriKeyGenerator } from "../../../key-generation/services/implementations/SpecialPlacementOriKeyGenerator";

@injectable()
export class SpecialPlacementService implements ISpecialPlacementService {
  // Structure: [gridMode][oriKey][letter] -> Record<string, unknown>
  private specialPlacements: Record<
    string,
    Record<string, Record<string, Record<string, unknown>>>
  > = {};
  private loadingCache: Set<string> = new Set();
  private oriKeyGenerator: SpecialPlacementOriKeyGenerator;
  private gridModeService: IGridModeDeriver | null = null;

  private getGridModeService(): IGridModeDeriver {
    if (!this.gridModeService) {
      this.gridModeService = resolve(
        TYPES.IGridModeDeriver
      ) as IGridModeDeriver;
    }
    return this.gridModeService;
  }

  constructor() {
    // Defer loading; we'll lazily load per-letter on demand
    this.specialPlacements = { diamond: {}, box: {} } as Record<
      string,
      Record<string, Record<string, Record<string, unknown>>>
    >;
    this.oriKeyGenerator = new SpecialPlacementOriKeyGenerator();
  }

  /**
   * Get special adjustment for arrow based on special placement logic.
   *
   * @param motionData Motion data containing motion information
   * @param pictographData Pictograph data containing letter and context
   * @param arrowColor Color of the arrow ('red' or 'blue') - if not provided, will try to determine from motion
   * @returns Point with special adjustment or null if no special placement found
   */
  async getSpecialAdjustment(
    motionData: MotionData,
    pictographData: PictographData,
    arrowColor?: string
  ): Promise<Point | null> {
    if (!motionData || !pictographData.letter) {
      return null;
    }

    const motion = motionData;
    const letter = pictographData.letter;

    // Generate orientation key using validated logic
    const oriKey = this.oriKeyGenerator.generateOrientationKey(
      motion,
      pictographData
    );

    // Get grid mode - compute from motion data
    const gridMode =
      pictographData.motions?.blue && pictographData.motions?.red
        ? this.getGridModeService().deriveGridMode(
            pictographData.motions.blue,
            pictographData.motions.red
          )
        : GridMode.DIAMOND;

    // Generate turns tuple for lookup
    const turnsTuple = this.generateTurnsTuple(pictographData);

    // Ensure the letter-specific special placement data is loaded lazily
    await this.ensureLetterPlacementsLoaded(gridMode, oriKey, letter);

    // Look up special placement data
    const letterData = this.specialPlacements[gridMode]?.[oriKey]?.[letter] as
      | Record<string, unknown>
      | undefined;

    if (!letterData) {
      return null;
    }

    // Get turn-specific data
    const turnData = letterData?.[turnsTuple] as
      | Record<string, unknown>
      | undefined;

    if (!turnData) {
      return null;
    }

    // First, try direct color-based coordinate lookup (most common case)
    let colorKey = "";
    if (arrowColor) {
      // Use provided arrow color directly
      colorKey = arrowColor;
    } else if (
      pictographData.motions?.blue &&
      pictographData.motions.blue === motion
    ) {
      colorKey = "blue";
    } else if (
      pictographData.motions?.red &&
      pictographData.motions.red === motion
    ) {
      colorKey = "red";
    } else {
      // Fallback: try to determine from motion data
      colorKey = "blue"; // Default fallback
    }

    if (colorKey in turnData) {
      const adjustmentValues = turnData[colorKey];
      if (Array.isArray(adjustmentValues) && adjustmentValues.length === 2) {
        return new Point(adjustmentValues[0], adjustmentValues[1]);
      }
    }

    // Second, try motion-type-specific adjustment (for letters like I)
    const motionTypeKey = motionData.motionType?.toLowerCase() || "";

    if (motionTypeKey in turnData) {
      const adjustmentValues = turnData[motionTypeKey];
      if (Array.isArray(adjustmentValues) && adjustmentValues.length === 2) {
        return new Point(adjustmentValues[0], adjustmentValues[1]);
      }
    }

    return null;
  }

  /**
   * Load special placement data from JSON configuration files.
   */
  private async ensureLetterPlacementsLoaded(
    gridMode: string,
    oriKey: string,
    letter: string
  ): Promise<void> {
    try {
      if (!this.specialPlacements[gridMode]) {
        this.specialPlacements[gridMode] = {} as Record<
          string,
          Record<string, Record<string, unknown>>
        >;
      }
      if (!this.specialPlacements[gridMode][oriKey]) {
        this.specialPlacements[gridMode][oriKey] = {} as Record<
          string,
          Record<string, unknown>
        >;
      }
      if (this.specialPlacements[gridMode][oriKey][letter]) {
        return; // already loaded
      }

      const cacheKey = `${gridMode}:${oriKey}:${letter}`;
      if (this.loadingCache.has(cacheKey)) {
        return; // loading in progress or already attempted
      }
      this.loadingCache.add(cacheKey);

      // Files are served under /data/... in the web app
      // Example path: /data/arrow_placement/diamond/special/from_layer1/A_placements.json
      const encodedLetter = encodeURIComponent(letter);
      const basePath = `/data/arrow_placement/${gridMode}/special/${oriKey}/${encodedLetter}_placements.json`;
      try {
        const data = (await jsonCache.get(basePath)) as Record<string, unknown>;
        this.specialPlacements[gridMode][oriKey][letter] = data;
      } catch (error) {
        this.specialPlacements[gridMode][oriKey][letter] = {};
      }
    } catch (error) {
      console.error("Error ensuring special placement data:", error);
    }
  }

  /**
   * Generate turns tuple string matching the turns_tuple_generator logic.
   *
   * This creates a string representation of the turn values for lookup in JSON data.
   * Format: "(blue_turns, red_turns)" e.g., "(0, 1.5)", "(1, 0.5)"
   */
  private generateTurnsTuple(pictographData: PictographData): string {
    try {
      const blueMotion = pictographData.motions?.blue;
      const redMotion = pictographData.motions?.red;

      if (blueMotion && redMotion) {
        const blueTurns =
          typeof blueMotion.turns === "number" ? blueMotion.turns : 0;
        const redTurns =
          typeof redMotion.turns === "number" ? redMotion.turns : 0;

        const blueStr =
          blueTurns === Math.floor(blueTurns)
            ? Math.floor(blueTurns).toString()
            : blueTurns.toString();
        const redStr =
          redTurns === Math.floor(redTurns)
            ? Math.floor(redTurns).toString()
            : redTurns.toString();

        return `(${blueStr}, ${redStr})`;
      }

      return "(0, 0)";
    } catch (error) {
      return "(0, 0)";
    }
  }
}