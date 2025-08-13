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

import type { MotionData, PictographData } from "$lib/domain";
import type { ISpecialPlacementService } from "../../placement-services";

// Define Point interface locally since it might not be in domain
interface Point {
  x: number;
  y: number;
}

export class SpecialPlacementService implements ISpecialPlacementService {
  // Structure: [gridMode][oriKey][letter] -> Record<string, unknown>
  private specialPlacements: Record<
    string,
    Record<string, Record<string, Record<string, unknown>>>
  > = {};
  private loadingCache: Set<string> = new Set();

  constructor() {
    // Defer loading; we'll lazily load per-letter on demand
    this.specialPlacements = { diamond: {}, box: {} } as Record<
      string,
      Record<string, Record<string, Record<string, unknown>>>
    >;
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
    arrowColor?: string,
  ): Promise<Point | null> {
    if (!motionData || !pictographData.letter) {
      return null;
    }

    const motion = motionData;
    const letter = pictographData.letter;

    // Generate orientation key using validated logic
    const oriKey = this.generateOrientationKey(motion, pictographData);

    // Get grid mode (default to diamond)
    const gridMode = pictographData.grid_mode || "diamond";

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
        return { x: adjustmentValues[0], y: adjustmentValues[1] };
      }
    }

    // Second, try motion-type-specific adjustment (for letters like I)
    const motionTypeKey = motionData.motion_type?.toLowerCase() || "";

    if (motionTypeKey in turnData) {
      const adjustmentValues = turnData[motionTypeKey];
      if (Array.isArray(adjustmentValues) && adjustmentValues.length === 2) {
        return { x: adjustmentValues[0], y: adjustmentValues[1] };
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
    letter: string,
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
        const response = await fetch(basePath);
        if (!response.ok) {
          console.debug(
            `No special placement file for ${gridMode}/${oriKey}/${letter}: ${response.status} ${response.statusText}`,
          );
          // Mark as empty to avoid re-fetching repeatedly
          this.specialPlacements[gridMode][oriKey][letter] = {};
          return;
        }
        const data = (await response.json()) as Record<string, unknown>;
        this.specialPlacements[gridMode][oriKey][letter] = data;
        console.debug(
          `Loaded special placements for ${gridMode}/${oriKey}/${letter}`,
        );
      } catch (error) {
        console.debug(
          `Failed to load special placements for ${gridMode}/${oriKey}/${letter} from ${basePath}:`,
          error,
        );
        this.specialPlacements[gridMode][oriKey][letter] = {};
      }
    } catch (error) {
      console.error("Error ensuring special placement data:", error);
    }
  }

  /**
   * Generate orientation key matching the ori_key_generator logic.
   *
   * This determines which subfolder of special placements to use:
   * - from_layer1: Basic orientations
   * - from_layer2: Layer 2 orientations
   * - from_layer3_blue1_red2: Mixed orientations with blue on layer 1, red on layer 2
   * - from_layer3_blue2_red1: Mixed orientations with blue on layer 2, red on layer 1
   */
  private generateOrientationKey(
    _motion: MotionData,
    pictographData: PictographData,
  ): string {
    try {
      const blueMotion = pictographData.motions?.blue;
      const redMotion = pictographData.motions?.red;

      if (blueMotion && redMotion) {
        const blueEndOri = blueMotion.end_ori || "in";
        const redEndOri = redMotion.end_ori || "in";

        const blueLayer = ["in", "out"].includes(blueEndOri) ? 1 : 2;
        const redLayer = ["in", "out"].includes(redEndOri) ? 1 : 2;

        if (blueLayer === 1 && redLayer === 1) {
          return "from_layer1";
        }
        if (blueLayer === 2 && redLayer === 2) {
          return "from_layer2";
        }
        if (blueLayer === 1 && redLayer === 2) {
          return "from_layer3_blue1_red2";
        }
        if (blueLayer === 2 && redLayer === 1) {
          return "from_layer3_blue2_red1";
        }
        return "from_layer1";
      }
    } catch (error) {
      console.debug("Error generating orientation key:", error);
    }

    return "from_layer1";
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
      console.debug("Error generating turns tuple:", error);
      return "(0, 0)";
    }
  }
}
