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

import { Point } from "fabric";
import { injectable } from "inversify";
import { resolve, TYPES } from "../../../../../../inversify";
import { type IGridModeDeriver, GridMode } from "../../../../../grid";
import {
  type MotionData,
  type PictographData,
  jsonCache,
} from "../../../../../shared";
import { SpecialPlacementOriKeyGenerator } from "../../../key-generation";
import type { ISpecialPlacementService } from "../contracts";

@injectable()
export class SpecialPlacementService implements ISpecialPlacementService {
  // Structure: [gridMode][oriKey][letter] -> Record<string, unknown>
  private specialPlacements: Record<
    string,
    Record<string, Record<string, Record<string, unknown>>>
  > = {};
  private loadingPromises = new Map<string, Promise<void>>();
  private oriKeyGenerator: SpecialPlacementOriKeyGenerator;
  private gridModeService: IGridModeDeriver | null = null;

  private getGridModeService(): IGridModeDeriver {
    if (!this.gridModeService) {
      this.gridModeService = resolve<IGridModeDeriver>(TYPES.IGridModeDeriver);
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
   * @param attributeKey Optional attribute key from AttributeKeyGenerator for precise lookup
   * @returns Point with special adjustment or null if no special placement found
   */
  async getSpecialAdjustment(
    motionData: MotionData,
    pictographData: PictographData,
    arrowColor?: string,
    attributeKey?: string
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

    // Handle nested structure like legacy system does
    // For G letter: letterData = { G: { "(0, 0)": { "red": [0, -130] } } }
    // We need to check letterData[letter] first, then fall back to letterData
    const actualLetterData =
      (letterData?.[letter] as Record<string, unknown>) || letterData;

    // Get turn-specific data
    const turnData = (actualLetterData as Record<string, unknown>)?.[
      turnsTuple
    ] as Record<string, unknown> | undefined;

    if (!turnData) {
      return null;
    }

    // Use attribute key if provided (preferred method matching legacy logic)
    if (attributeKey && attributeKey in turnData) {
      const adjustmentValues = turnData[attributeKey];
      if (Array.isArray(adjustmentValues) && adjustmentValues.length === 2) {
        return new Point(adjustmentValues[0], adjustmentValues[1]);
      }
    }

    // FALLBACK LOGIC (when attributeKey not provided or not found)
    // Try multiple lookup strategies for backward compatibility

    // Determine key strategy based on letter type (HYBRID vs NON-HYBRID)
    const isHybridLetter = this.isHybridLetter(letter);
    const startsFromStandardOrientation =
      this.startsFromStandardOrientation(pictographData);

    // For HYBRID letters with standard orientation, use motion type as PRIMARY key
    if (isHybridLetter && startsFromStandardOrientation) {
      const motionTypeKey = motionData.motionType?.toLowerCase() || "";

      if (motionTypeKey in turnData) {
        const adjustmentValues = turnData[motionTypeKey];
        if (Array.isArray(adjustmentValues) && adjustmentValues.length === 2) {
          return new Point(adjustmentValues[0], adjustmentValues[1]);
        }
      }
    } else {
      // For NON-HYBRID letters, try color-based lookup first
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

      // Fallback: try motion-type-specific adjustment for NON-HYBRID letters
      const motionTypeKey = motionData.motionType?.toLowerCase() || "";

      if (motionTypeKey in turnData) {
        const adjustmentValues = turnData[motionTypeKey];
        if (Array.isArray(adjustmentValues) && adjustmentValues.length === 2) {
          return new Point(adjustmentValues[0], adjustmentValues[1]);
        }
      }
    }

    return null;
  }

  /**
   * Check if letter is HYBRID (uses motion type keys for special placement)
   */
  private isHybridLetter(letter: string): boolean {
    const hybridLetters = [
      "C",
      "F",
      "I",
      "L",
      "O",
      "R",
      "U",
      "V",
      "W",
      "X",
      "Y",
      "Z",
      "W-",
      "X-",
      "Y-",
      "Z-",
      "Σ",
      "Δ",
      "θ",
      "Ω",
      "Σ-",
      "Δ-",
      "θ-",
      "Ω-",
      "Φ",
      "Ψ",
      "Λ",
    ];
    return hybridLetters.includes(letter);
  }

  /**
   * Check if pictograph starts from standard orientation (both motions same layer)
   */
  private startsFromStandardOrientation(
    pictographData: PictographData
  ): boolean {
    try {
      const blueMotion = pictographData.motions?.blue;
      const redMotion = pictographData.motions?.red;

      if (!blueMotion || !redMotion) {
        return true; // Default to standard
      }

      const IN = "in";
      const OUT = "out";

      const blueStart = blueMotion.startOrientation || "";
      const redStart = redMotion.startOrientation || "";

      // Standard if both are layer1 (IN/OUT) or both are layer2 (CLOCK/COUNTER)
      const blueLayer1 = [IN, OUT].includes(blueStart);
      const redLayer1 = [IN, OUT].includes(redStart);

      return blueLayer1 === redLayer1; // Same layer = standard orientation
    } catch {
      return true; // Default to standard
    }
  }

  /**
   * Load special placement data from JSON configuration files.
   * Uses Promise-based caching to prevent race conditions.
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

      // Check if loading is already in progress
      if (this.loadingPromises.has(cacheKey)) {
        // Wait for the existing loading operation to complete
        await this.loadingPromises.get(cacheKey);
        return;
      }

      // Start new loading operation
      const loadingPromise = this.loadLetterData(gridMode, oriKey, letter);
      this.loadingPromises.set(cacheKey, loadingPromise);

      try {
        await loadingPromise;
      } finally {
        // Clean up the promise from cache when done
        this.loadingPromises.delete(cacheKey);
      }
    } catch (error) {
      console.error("Error ensuring special placement data:", error);
    }
  }

  private async loadLetterData(
    gridMode: string,
    oriKey: string,
    letter: string
  ): Promise<void> {
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

  /**
   * Check if rotation angle override exists for this motion.
   *
   * Used by ArrowRotationCalculator to determine if special rotation angles
   * should be used instead of default rotation maps.
   *
   * @param motionData Motion data containing motion information
   * @param pictographData Pictograph data containing letter and context
   * @param rotationOverrideKey Key generated by RotationAngleOverrideKeyGenerator
   * @returns true if rotation override flag is present in special placement data
   */
  async hasRotationAngleOverride(
    motionData: MotionData,
    pictographData: PictographData,
    rotationOverrideKey: string
  ): Promise<boolean> {
    if (!motionData || !pictographData.letter) {
      return false;
    }

    // Only DASH and STATIC motions can have rotation overrides
    const motionType = motionData.motionType?.toLowerCase();
    if (motionType !== "dash" && motionType !== "static") {
      return false;
    }

    const motion = motionData;
    const letter = pictographData.letter;

    // Generate orientation key
    const oriKey = this.oriKeyGenerator.generateOrientationKey(
      motion,
      pictographData
    );

    // Get grid mode
    const gridMode =
      pictographData.motions?.blue && pictographData.motions?.red
        ? this.getGridModeService().deriveGridMode(
            pictographData.motions.blue,
            pictographData.motions.red
          )
        : GridMode.DIAMOND;

    // Generate turns tuple
    const turnsTuple = this.generateTurnsTuple(pictographData);

    // Ensure letter data is loaded
    await this.ensureLetterPlacementsLoaded(gridMode, oriKey, letter);

    // Look up letter data
    const letterData = this.specialPlacements[gridMode]?.[oriKey]?.[letter] as
      | Record<string, unknown>
      | undefined;

    if (!letterData) {
      return false;
    }

    // Handle nested structure
    const actualLetterData =
      (letterData?.[letter] as Record<string, unknown>) || letterData;

    // Get turn-specific data
    const turnData = (actualLetterData as Record<string, unknown>)?.[
      turnsTuple
    ] as Record<string, unknown> | undefined;

    if (!turnData) {
      return false;
    }

    // Check if rotation override flag exists and is true
    const overrideFlag = turnData[rotationOverrideKey];
    return overrideFlag === true;
  }
}
