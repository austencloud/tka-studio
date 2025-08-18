/**
 * AnimatedPictographDataService - Service for creating animated pictograph data
 *
 * Handles the complex logic of transforming motion parameters into pictograph data
 * for animated display in the motion tester.
 */

import type {
  PictographData,
  ArrowData,
  PropData,
  MotionData,
} from "$lib/domain";
import {
  createPictographData,
  createArrowData,
  createPropData,
  createMotionData,
  createGridData as createDomainGridData,
} from "$lib/domain";
// import { createGridData } from "$lib/data/gridCoordinates.js";
import {
  GridMode,
  MotionType,
  Location,
  Orientation,
  RotationDirection,
  ArrowType,
  PropType,
  MotionColor,
} from "$lib/domain/enums";
import type { MotionTesterState } from "../state/motion-tester-state.svelte";
import type { IOptionDataService } from "$lib/services/interfaces/application-interfaces";
import type {
  CsvDataService,
  ParsedCsvRow,
} from "$lib/services/implementations/CsvDataService";
import type { IArrowPositioningOrchestrator } from "$lib/services/positioning/core-services";
import type { MotionTestParams } from "./MotionParameterService";

// Interface for motion parameters - matches MotionTestParams
interface MotionParams {
  motionType: string;
  startLoc: string;
  endLoc: string;
  startOri: string;
  endOri: string;
  rotationDirection: string;
  turns: number | "fl"; // Support both numeric turns and float like MotionTestParams
}

export interface IAnimatedPictographDataService {
  createAnimatedPictographData(
    motionState: MotionTesterState
  ): Promise<PictographData | null>;
}

export class AnimatedPictographDataService
  implements IAnimatedPictographDataService
{
  private cache = new Map<string, PictographData>();

  constructor(
    private csvDataService: CsvDataService,
    private optionDataService: IOptionDataService,
    private arrowPositioningService: IArrowPositioningOrchestrator
  ) {}
  /**
   * Creates complete pictograph data for animated display using current motion parameters.
   * Uses CSV lookup service to find the correct letter and pictograph data.
   * Includes caching to prevent redundant calculations.
   */
  async createAnimatedPictographData(
    motionState: MotionTesterState
  ): Promise<PictographData | null> {
    try {
      // Create cache key from motion parameters (excluding animation progress)
      const cacheKey = this.createCacheKey(motionState);

      // Check cache first
      if (this.cache.has(cacheKey)) {
        const cached = this.cache.get(cacheKey);
        if (!cached) {
          throw new Error(
            "Cache inconsistency: key exists but value is undefined"
          );
        }
        // Update progress in metadata for cached result
        return {
          ...cached,
          metadata: {
            ...cached.metadata,
            progress: motionState.animationState.progress,
          },
        };
      }

      const gridMode = this.getGridMode(motionState.gridType);

      // Try to use CSV lookup for accurate letter detection
      console.log("🔍 Using CSV lookup service for pictograph generation...");

      const csvPictograph = await this.findMatchingPictographFromCsv(
        motionState.blueMotionParams,
        motionState.redMotionParams,
        gridMode
      );

      if (csvPictograph) {
        console.log(
          `✅ CSV lookup successful! Found letter: ${csvPictograph.letter}`
        );

        // Create new pictograph with updated metadata
        const updatedPictograph = {
          ...csvPictograph,
          metadata: {
            ...csvPictograph.metadata,
            source: "motion_tester_csv_lookup",
            grid_type: motionState.gridType,
            progress: motionState.animationState.progress,
          },
        };

        // Cache the result (without progress for reusability)
        const cacheableResult = {
          ...csvPictograph,
          metadata: {
            ...csvPictograph.metadata,
            progress: 0, // Don't cache progress
          },
        };
        this.cache.set(cacheKey, cacheableResult);

        return updatedPictograph;
      } else {
        console.warn(
          "⚠️ CSV lookup failed, falling back to manual generation..."
        );
      }

      // Fallback: Create pictograph manually (original logic)
      // const gridModeString = gridMode === GridMode.DIAMOND ? "diamond" : "box";
      // const coordinatesGridData = createGridData(gridModeString);
      const domainGridData = createDomainGridData({ grid_mode: gridMode });

      // Create complete motion data
      const blueMotionData = this.createCompleteMotionData(
        motionState.blueMotionParams
      );
      const redMotionData = this.createCompleteMotionData(
        motionState.redMotionParams
      );

      // Create proper prop data with locations
      const blueProps = this.createPropDataFromMotion(
        motionState.blueMotionParams,
        MotionColor.BLUE
      );
      const redProps = this.createPropDataFromMotion(
        motionState.redMotionParams,
        MotionColor.RED
      );

      // Create arrow data based on motion parameters
      const blueArrows = this.createArrowDataFromMotion(
        motionState.blueMotionParams,
        MotionColor.BLUE
      );
      const redArrows = this.createArrowDataFromMotion(
        motionState.redMotionParams,
        MotionColor.RED
      );

      const pictographData = createPictographData({
        id: "motion-tester-fallback-pictograph",
        grid_data: domainGridData,
        arrows: {
          blue: blueArrows,
          red: redArrows,
        },
        props: {
          blue: blueProps,
          red: redProps,
        },
        motions: {
          blue: blueMotionData,
          red: redMotionData,
        },
        letter: (() => {
          throw new Error(
            `CSV lookup failed for motion parameters: ${JSON.stringify({
              blueMotion: blueMotionData.motion_type,
              blueStartLoc: blueMotionData.start_loc,
              blueEndLoc: blueMotionData.end_loc,
              blueTurns: blueMotionData.turns,
              redMotion: redMotionData.motion_type,
              redStartLoc: redMotionData.start_loc,
              redEndLoc: redMotionData.end_loc,
              redTurns: redMotionData.turns,
            })}. All combinations should exist in CSV data.`
          );
        })(),
        beat: 1,
        is_blank: false,
        is_mirrored: false,
        metadata: {
          source: "motion_tester_fallback",
          grid_type: motionState.gridType,
          progress: motionState.animationState.progress,
        },
      });

      // Cache the fallback result (without progress for reusability)
      const cacheableResult = {
        ...pictographData,
        metadata: {
          ...pictographData.metadata,
          progress: 0, // Don't cache progress
        },
      };
      this.cache.set(cacheKey, cacheableResult);

      return pictographData;
    } catch (error) {
      console.error("Error creating animated pictograph data:", error);
      return null;
    }
  }

  private getGridMode(gridType: string): GridMode {
    return gridType === "diamond" ? GridMode.DIAMOND : GridMode.BOX;
  }

  /**
   * Creates complete motion data using the domain factory function
   */
  private createCompleteMotionData(motionParams: MotionParams): MotionData {
    // Handle "fl" (float) turns by converting to 0.5
    const turns = motionParams.turns === "fl" ? 0.5 : motionParams.turns;

    return createMotionData({
      motion_type: this.mapMotionType(motionParams.motionType),
      start_loc: this.mapLocation(motionParams.startLoc),
      end_loc: this.mapLocation(motionParams.endLoc),
      start_ori: this.mapOrientation(motionParams.startOri),
      end_ori: this.mapOrientation(motionParams.endOri),
      prop_rot_dir: this.mapRotationDirection(motionParams.rotationDirection),
      turns: turns,
      is_visible: true,
    });
  }

  /**
   * Creates prop data based on motion parameters
   */
  private createPropDataFromMotion(
    motionParams: MotionParams,
    color: MotionColor
  ): PropData {
    return createPropData({
      prop_type: PropType.STAFF, // Default to staff for motion tester
      color: color,
      location: this.mapLocation(motionParams.endLoc), // Use END location for prop positioning
      orientation: this.mapOrientation(motionParams.endOri), // Use END orientation
      rotation_direction: this.mapRotationDirection(
        motionParams.rotationDirection
      ),
      is_visible: true,
    });
  }

  /**
   * Creates arrow data based on motion parameters
   */
  private createArrowDataFromMotion(
    motionParams: MotionParams,
    color: MotionColor
  ): ArrowData {
    // Handle "fl" (float) turns by converting to 0.5
    const turns = motionParams.turns === "fl" ? 0.5 : motionParams.turns;

    return createArrowData({
      arrow_type: color === MotionColor.BLUE ? ArrowType.BLUE : ArrowType.RED,
      color: color,
      motion_type: motionParams.motionType,
      start_orientation: motionParams.startOri,
      end_orientation: motionParams.endOri,
      rotation_direction: motionParams.rotationDirection,
      turns: turns,
      location: this.mapLocation(motionParams.startLoc),
      is_visible: true,
    });
  }

  // Mapping methods to convert motion tester parameters to domain enums
  private mapMotionType(motionType: string): MotionType {
    if (!motionType) return MotionType.STATIC;
    switch (motionType.toLowerCase()) {
      case "pro":
        return MotionType.PRO;
      case "anti":
        return MotionType.ANTI;
      case "float":
        return MotionType.FLOAT;
      case "dash":
        return MotionType.DASH;
      case "static":
        return MotionType.STATIC;
      default:
        return MotionType.STATIC;
    }
  }

  private mapLocation(location: string): Location {
    if (!location) return Location.NORTH;
    switch (location.toLowerCase()) {
      case "n":
        return Location.NORTH;
      case "e":
        return Location.EAST;
      case "s":
        return Location.SOUTH;
      case "w":
        return Location.WEST;
      case "ne":
        return Location.NORTHEAST;
      case "se":
        return Location.SOUTHEAST;
      case "sw":
        return Location.SOUTHWEST;
      case "nw":
        return Location.NORTHWEST;
      default:
        return Location.NORTH;
    }
  }

  private mapOrientation(orientation: string): Orientation {
    if (!orientation) return Orientation.IN;
    switch (orientation.toLowerCase()) {
      case "in":
        return Orientation.IN;
      case "out":
        return Orientation.OUT;
      case "clock":
        return Orientation.CLOCK;
      case "counter":
        return Orientation.COUNTER;
      default:
        return Orientation.IN;
    }
  }

  private mapRotationDirection(rotationDir: string): RotationDirection {
    if (!rotationDir) return RotationDirection.NO_ROTATION;
    switch (rotationDir.toLowerCase()) {
      case "cw":
      case "clockwise":
        return RotationDirection.CLOCKWISE;
      case "ccw":
      case "counter_clockwise":
        return RotationDirection.COUNTER_CLOCKWISE;
      case "no_rot":
      case "no_rotation":
        return RotationDirection.NO_ROTATION;
      default:
        return RotationDirection.NO_ROTATION;
    }
  }

  /**
   * Creates a cache key from motion state parameters (excluding animation progress)
   */
  private createCacheKey(motionState: MotionTesterState): string {
    const blue = motionState.blueMotionParams;
    const red = motionState.redMotionParams;

    return [
      motionState.gridType,
      blue.startLoc,
      blue.endLoc,
      blue.motionType,
      blue.turns,
      blue.rotationDirection,
      blue.startOri,
      blue.endOri,
      red.startLoc,
      red.endLoc,
      red.motionType,
      red.turns,
      red.rotationDirection,
      red.startOri,
      red.endOri,
    ].join("|");
  }

  /**
   * Find matching pictograph from CSV data using existing services
   */
  private async findMatchingPictographFromCsv(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
    gridMode: GridMode
  ): Promise<PictographData | null> {
    try {
      // Ensure CSV data is loaded
      await this.csvDataService.loadCsvData();

      if (!this.csvDataService.isReady()) {
        console.error("❌ CSV data service not ready");
        return null;
      }

      // Get parsed CSV data for the grid mode
      const csvRows = this.csvDataService.getParsedData(gridMode);

      if (!csvRows || csvRows.length === 0) {
        console.error(`❌ No CSV data available for grid mode: ${gridMode}`);
        return null;
      }

      console.log(
        `🔍 Searching ${csvRows.length} CSV rows for matching motion parameters...`
      );
      console.log("🔍 Blue params:", {
        motionType: blueParams.motionType,
        startLoc: blueParams.startLoc,
        endLoc: blueParams.endLoc,
        rotationDirection: blueParams.rotationDirection,
        turns: blueParams.turns,
      });
      console.log("🔍 Red params:", {
        motionType: redParams.motionType,
        startLoc: redParams.startLoc,
        endLoc: redParams.endLoc,
        rotationDirection: redParams.rotationDirection,
        turns: redParams.turns,
      });

      // Find exact match based on motion parameters (excluding rotationDirection)
      const matchingRow = csvRows.find((row: ParsedCsvRow) => {
        const blueMatch = this.matchesMotionParams(
          row,
          MotionColor.BLUE,
          blueParams
        );
        const redMatch = this.matchesMotionParams(
          row,
          MotionColor.RED,
          redParams
        );
        return blueMatch && redMatch;
      });

      if (matchingRow) {
        console.log(
          `✅ Found exact match for letter "${matchingRow.letter}":`,
          matchingRow
        );

        // Convert CSV row to PictographData using existing proven pipeline
        const pictographData =
          this.optionDataService.convertCsvRowToPictographData(
            matchingRow,
            0 // index
          );

        if (pictographData) {
          console.log(
            `🎯 Successfully created pictograph for letter "${matchingRow.letter}":`,
            pictographData
          );

          // Update arrow data to match motion data using positioning pipeline
          // const gridModeString =
          //   GridMode.DIAMOND === GridMode.DIAMOND ? "diamond" : "box";
          // const coordinatesGridData = createGridData(gridModeString);
          const updatedPictographWithPositions =
            this.arrowPositioningService.calculateAllArrowPositions(
              pictographData
            );

          console.log(
            "✅ CSV lookup successful! Found letter:",
            matchingRow.letter
          );
          console.log("🎯 Arrow data updated to match motion data");
          return updatedPictographWithPositions;
        } else {
          console.error("❌ Failed to convert CSV row to pictograph data");
          return null;
        }
      }

      console.warn("⚠️ No exact match found in CSV data");
      return null;
    } catch (error) {
      console.error("❌ Error finding matching CSV row:", error);
      return null;
    }
  }

  /**
   * Check if a CSV row matches motion parameters for a specific color
   */
  private matchesMotionParams(
    row: ParsedCsvRow,
    color: MotionColor,
    params: MotionTestParams
  ): boolean {
    const csvMotionType = row[`${color}MotionType`];
    const csvStartLoc = row[`${color}StartLoc`];
    const csvEndLoc = row[`${color}EndLoc`];

    // Normalize values for comparison
    const motionTypeMatch =
      this.normalizeMotionType(csvMotionType) ===
      this.normalizeMotionType(params.motionType);
    const startLocMatch =
      this.normalizeLocation(csvStartLoc) ===
      this.normalizeLocation(params.startLoc);
    const endLocMatch =
      this.normalizeLocation(csvEndLoc) ===
      this.normalizeLocation(params.endLoc);

    // Note: rotationDirection is calculated after CSV lookup, not used for matching
    return motionTypeMatch && startLocMatch && endLocMatch;
  }

  /**
   * Normalize motion type for comparison
   */
  private normalizeMotionType(motionType: string): string {
    return motionType.toLowerCase().trim();
  }

  /**
   * Normalize location for comparison
   */
  private normalizeLocation(location: string): string {
    return location.toLowerCase().trim();
  }
}
