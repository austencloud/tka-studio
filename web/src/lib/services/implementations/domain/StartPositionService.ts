/**
 * Start Position Service - Implementation
 *
 * Provides start position management functionality for the construct workflow.
 * Based on the desktop StartPositionOrchestrator but simplified for web.
 */

import { Letter } from "$lib/domain/Letter";
import type { ValidationError } from "$lib/domain/SequenceCard";
import type { BeatData, PictographData } from "../../../domain";
import {
  createBeatData,
  createMotionData,
  createPictographData,
  GridMode,
  Location,
  MotionColor,
  MotionType,
  Orientation,
  PropType,
  RotationDirection,
} from "../../../domain";
import type { IStartPositionService } from "../../interfaces/application-interfaces";
import type { ValidationResult } from "../../interfaces/domain-types";
import { PositionMappingService } from "../movement/PositionMappingService";

export class StartPositionService implements IStartPositionService {
  private readonly DEFAULT_START_POSITIONS: Record<string, string[]> = {
    [GridMode.DIAMOND]: ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"],
    [GridMode.BOX]: ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"],
    // SKEWED mode doesn't have separate start positions - it's determined by individual motions
  };

  private positionService = new PositionMappingService();

  async getAvailableStartPositions(
    propType: string,
    gridMode: GridMode
  ): Promise<BeatData[]> {
    console.log(
      `📍 Getting available start positions for ${propType} in ${gridMode} mode`
    );

    try {
      // For SKEWED mode, default to diamond positions
      const actualGridMode =
        gridMode === GridMode.SKEWED ? GridMode.DIAMOND : gridMode;
      const startPositionKeys = this.DEFAULT_START_POSITIONS[actualGridMode];

      if (!startPositionKeys) {
        console.error(
          `❌ Unsupported grid mode: ${gridMode}. Supported modes: ${Object.keys(this.DEFAULT_START_POSITIONS).join(", ")}`
        );
        // Fallback to diamond mode
        const fallbackKeys = this.DEFAULT_START_POSITIONS.diamond;
        console.log(`🔄 Falling back to diamond mode`);

        const beatData: BeatData[] = fallbackKeys.map((key, index) => {
          return createBeatData({
            beatNumber: 0,
            isBlank: false,
            pictographData: this.createStartPositionPictograph(key, index),
          });
        });

        console.log(
          `✅ Generated ${beatData.length} available start positions (fallback)`
        );
        return beatData;
      }

      const beatData: BeatData[] = startPositionKeys.map((key, index) => {
        return createBeatData({
          beatNumber: 0,
          isBlank: false,
          pictographData: this.createStartPositionPictograph(key, index),
        });
      });

      console.log(`✅ Generated ${beatData.length} available start positions`);
      return beatData;
    } catch (error) {
      console.error("❌ Error getting available start positions:", error);
      return [];
    }
  }

  async setStartPosition(startPositionBeat: BeatData): Promise<void> {
    try {
      // Store in localStorage for persistence in the format OptionPicker expects
      if (typeof window !== "undefined") {
        // Check if localStorage already has the correct format (from StartPositionPicker)
        const existingData = localStorage.getItem("startPosition");
        if (existingData) {
          try {
            const parsed = JSON.parse(existingData);
            // If it already has top-level endPosition, don't overwrite it
            if (parsed.endPosition) {
              return;
            }
          } catch {
            // If parsing fails, continue with saving new format
          }
        }

        // Create the format that OptionPicker expects
        if (!startPositionBeat.pictographData) {
          console.warn("⚠️ Start position beat missing pictographData");
          return;
        }

        const pictographData = startPositionBeat.pictographData;

        // Compute endPosition from motion data
        const endPosition =
          pictographData.motions?.blue && pictographData.motions?.red
            ? this.positionService.getPositionFromLocations(
                pictographData.motions.blue.endLocation,
                pictographData.motions.red.endLocation
              )
            : null;

        const { pictographData: _, ...beatWithoutPictographData } =
          startPositionBeat;
        const optionPickerFormat = {
          endPosition,
          pictographData,
          letter: pictographData.letter,
          gridMode: GridMode.DIAMOND, // Default
          isStartPosition: true,
          ...beatWithoutPictographData,
        };

        localStorage.setItem(
          "startPosition",
          JSON.stringify(optionPickerFormat)
        );
      }
    } catch (error) {
      console.error("Error setting start position:", error);
      throw new Error(
        `Failed to set start position: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  validateStartPosition(position: BeatData): ValidationResult {
    const errors: ValidationError[] = [];

    if (!position.pictographData) {
      errors.push({
        code: "MISSING_pictographData",
        message: "Start position must have pictograph data",
        severity: "error",
      });
    }

    if (
      !position.pictographData?.motions?.blue &&
      !position.pictographData?.motions?.red
    ) {
      errors.push({
        code: "MISSING_MOTIONS",
        message: "Start position must have at least one motion",
        severity: "error",
      });
    }

    // Validate motion types are static for start positions
    if (
      position.pictographData?.motions?.blue?.motionType !== MotionType.STATIC
    ) {
      errors.push({
        code: "INVALID_BLUE_MOTION",
        message: "Blue motion must be static for start positions",
        severity: "error",
      });
    }

    if (
      position.pictographData?.motions?.red?.motionType !== MotionType.STATIC
    ) {
      errors.push({
        code: "INVALID_RED_MOTION",
        message: "Red motion must be static for start positions",
        severity: "error",
      });
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings: [],
    };
  }

  async getDefaultStartPositions(
    gridMode: GridMode
  ): Promise<PictographData[]> {
    try {
      // For SKEWED mode, default to diamond positions
      const actualGridMode =
        gridMode === GridMode.SKEWED ? GridMode.DIAMOND : gridMode;
      const startPositionKeys = this.DEFAULT_START_POSITIONS[actualGridMode];

      if (!startPositionKeys) {
        console.error(
          `Unsupported grid mode: ${gridMode}. Supported modes: ${Object.keys(this.DEFAULT_START_POSITIONS).join(", ")}`
        );
        // Fallback to diamond mode
        const fallbackKeys = this.DEFAULT_START_POSITIONS.diamond;

        const pictographData: PictographData[] = fallbackKeys.map(
          (key, index) => this.createStartPositionPictograph(key, index)
        );

        return pictographData;
      }

      const pictographData: PictographData[] = startPositionKeys.map(
        (key, index) => this.createStartPositionPictograph(key, index)
      );

      return pictographData;
    } catch (error) {
      console.error("Error getting default start positions:", error);
      return [];
    }
  }

  private createStartPositionPictograph(
    key: string,
    index: number
  ): PictographData {
    // ✅ CENTRALIZED: Use PictographDataFactory for consistent creation

    // Determine letter based on position key
    let letter: Letter;
    if (key.includes("alpha")) letter = Letter.ALPHA;
    else if (key.includes("beta")) letter = Letter.BETA;
    else if (key.includes("gamma")) letter = Letter.GAMMA;
    else letter = Letter.ALPHA; // Default fallback

    // Use correct locations based on legacy position mappings
    // From PatternGenerator.ts and positions_map.py
    const positionMappings: Record<string, { blue: Location; red: Location }> =
      {
        alpha1_alpha1: { blue: Location.SOUTH, red: Location.NORTH }, // Alpha1: Blue=South, Red=North
        beta5_beta5: { blue: Location.SOUTH, red: Location.SOUTH }, // Beta5: Blue=South, Red=South
        gamma11_gamma11: { blue: Location.SOUTH, red: Location.EAST }, // Gamma11: Blue=South, Red=East
        // Box mode positions
        alpha2_alpha2: { blue: Location.SOUTHWEST, red: Location.NORTHEAST }, // Alpha2: Blue=Southwest, Red=Northeast
        beta4_beta4: { blue: Location.SOUTHEAST, red: Location.SOUTHEAST }, // Beta4: Blue=Southeast, Red=Southeast
        gamma12_gamma12: { blue: Location.NORTHWEST, red: Location.NORTHEAST }, // Gamma12: Blue=Northwest, Red=Northeast
      };

    const mapping = positionMappings[key];
    if (!mapping) {
      console.warn(`No position mapping found for ${key}, using fallback`);
    }

    const blueLocation = mapping?.blue || Location.SOUTH;
    const redLocation = mapping?.red || Location.NORTH;

    // ✅ DIRECT DOMAIN CONSTRUCTOR: No factory needed - positions auto-derived
    return createPictographData({
      id: `start-pos-${key}-${index}`,
      letter,
      motions: {
        blue: createMotionData({
          motionType: MotionType.STATIC,
          rotationDirection: RotationDirection.NO_ROTATION,
          startLocation: blueLocation,
          endLocation: blueLocation,
          turns: 0,
          startOrientation: Orientation.IN,
          endOrientation: Orientation.IN,
          color: MotionColor.BLUE,
          isVisible: true,
          propType: PropType.STAFF,
          arrowLocation: blueLocation, // Will be calculated by positioning system
        }),
        red: createMotionData({
          motionType: MotionType.STATIC,
          rotationDirection: RotationDirection.NO_ROTATION,
          startLocation: redLocation,
          endLocation: redLocation,
          turns: 0,
          startOrientation: Orientation.IN,
          endOrientation: Orientation.IN,
          color: MotionColor.RED,
          isVisible: true,
          propType: PropType.STAFF,
          arrowLocation: redLocation, // Will be calculated by positioning system
        }),
      },
      isBlank: false,
    });
  }
}
