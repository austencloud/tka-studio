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
  startLocation: string;
  endLocation: string;
  startOri: string;
  endOrientation: string;
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

        // Update prop locations to match current motion parameters (even for cached results)
        const updatedBlueProps = this.createPropDataFromMotion(
          motionState.blueMotionParams,
          MotionColor.BLUE
        );
        const updatedRedProps = this.createPropDataFromMotion(
          motionState.redMotionParams,
          MotionColor.RED
        );

        // Update motion data to match current motion parameters (even for cached results)
        const updatedBlueMotion = this.createMotionDataFromParams(
          motionState.blueMotionParams
        );
        const updatedRedMotion = this.createMotionDataFromParams(
          motionState.redMotionParams
        );

        // Return cached result with updated prop/motion data and progress
        return {
          ...cached,
          props: {
            blue: updatedBlueProps,
            red: updatedRedProps,
          },
          motions: {
            blue: updatedBlueMotion,
            red: updatedRedMotion,
          },
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

        // Update prop locations to match current motion parameters
        const updatedBlueProps = this.createPropDataFromMotion(
          motionState.blueMotionParams,
          MotionColor.BLUE
        );
        const updatedRedProps = this.createPropDataFromMotion(
          motionState.redMotionParams,
          MotionColor.RED
        );

        // Update motion data to match current motion parameters
        const updatedBlueMotion = this.createMotionDataFromParams(
          motionState.blueMotionParams
        );
        const updatedRedMotion = this.createMotionDataFromParams(
          motionState.redMotionParams
        );

        // Create new pictograph with updated metadata, prop locations, and motion data
        const updatedPictograph = {
          ...csvPictograph,
          props: {
            blue: updatedBlueProps,
            red: updatedRedProps,
          },
          motions: {
            blue: updatedBlueMotion,
            red: updatedRedMotion,
          },
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
      console.log("🔧 Creating fallback pictograph with manual generation...");
      const domainGridData = createDomainGridData({ gridMode: gridMode });

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
        gridData: domainGridData,
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
        letter: "?", // Use placeholder letter when CSV lookup fails
        beat: 1,
        isBlank: false,
        isMirrored: false,
        metadata: {
          source: "motion_tester_fallback",
          grid_type: motionState.gridType,
          progress: motionState.animationState.progress,
        },
      });

      console.log("✅ Fallback pictograph created successfully with letter: ?");

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
      motionType: this.mapMotionType(motionParams.motionType),
      startLocation: this.mapLocation(motionParams.startLocation),
      endLocation: this.mapLocation(motionParams.endLocation),
      startOrientation: this.mapOrientation(motionParams.startOri),
      endOrientation: this.mapOrientation(motionParams.endOrientation),
      rotationDirection: this.mapRotationDirection(
        motionParams.rotationDirection
      ),
      turns: turns,
      isVisible: true,
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
      propType: PropType.STAFF, // Default to staff for motion tester
      color: color,
      location: this.mapLocation(motionParams.endLocation), // Use END location for prop positioning
      orientation: this.mapOrientation(motionParams.endOrientation), // Use END orientation
      rotationDirection: this.mapRotationDirection(
        motionParams.rotationDirection
      ),
      isVisible: true,
    });
  }

  /**
   * Creates motion data based on motion parameters
   */
  private createMotionDataFromParams(motionParams: MotionParams): MotionData {
    return {
      motionType: this.mapMotionType(motionParams.motionType),
      startLocation: this.mapLocation(motionParams.startLocation),
      endLocation: this.mapLocation(motionParams.endLocation),
      startOrientation: this.mapOrientation(motionParams.startOri),
      endOrientation: this.mapOrientation(motionParams.endOrientation),
      rotationDirection: this.mapRotationDirection(
        motionParams.rotationDirection
      ),
      turns: motionParams.turns,
      isVisible: true,
    };
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
      arrowType: color === MotionColor.BLUE ? ArrowType.BLUE : ArrowType.RED,
      color: color,
      motionType: motionParams.motionType,
      start_orientation: motionParams.startOri,
      end_orientation: motionParams.endOrientation,
      rotationDirection: motionParams.rotationDirection,
      turns: turns,
      location: this.mapLocation(motionParams.startLocation),
      isVisible: true,
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
    if (!location) {
      console.warn(
        `⚠️ mapLocation: location is null/undefined, defaulting to NORTH`
      );
      return Location.NORTH;
    }

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
        console.warn(
          `⚠️ mapLocation: unknown location "${location}", defaulting to NORTH`
        );
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
      case "noRotation":
      case "noRotation":
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
      blue.startLocation,
      blue.endLocation,
      blue.motionType,
      blue.turns,
      blue.rotationDirection,
      blue.startOri,
      blue.endOrientation,
      red.startLocation,
      red.endLocation,
      red.motionType,
      red.turns,
      red.rotationDirection,
      red.startOri,
      red.endOrientation,
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
        startLocation: blueParams.startLocation,
        endLocation: blueParams.endLocation,
        rotationDirection: blueParams.rotationDirection,
        turns: blueParams.turns,
      });
      console.log("🔍 Red params:", {
        motionType: redParams.motionType,
        startLocation: redParams.startLocation,
        endLocation: redParams.endLocation,
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
    const csvEndLoc = row[`${color}endLocation`];

    // Normalize values for comparison
    const motionTypeMatch =
      this.normalizeMotionType(csvMotionType) ===
      this.normalizeMotionType(params.motionType);
    const startLocMatch =
      this.normalizeLocation(csvStartLoc) ===
      this.normalizeLocation(params.startLocation);
    const endLocMatch =
      this.normalizeLocation(csvEndLoc) ===
      this.normalizeLocation(params.endLocation);

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
