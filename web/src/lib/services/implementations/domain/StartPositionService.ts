/**
 * Start Position Service - Implementation
 *
 * Provides start position management functionality for the construct workflow.
 * Based on the desktop StartPositionOrchestrator but simplified for web.
 */

import type { BeatData, PictographData } from "../../../domain";
import {
  MotionColor,
  createBeatData,
  createMotionData,
  createPictographData,
  GridMode,
  Location,
  MotionType,
  Orientation,
  PropType,
  RotationDirection,
} from "../../../domain";
import type { ValidationResult } from "../../interfaces/domain-types";
import type { IStartPositionService } from "../../interfaces/application-interfaces";
import type { ValidationError } from "$lib/domain/sequenceCard";
import { Letter } from "$lib/domain/Letter";

export class StartPositionService implements IStartPositionService {
  private readonly DEFAULT_START_POSITIONS = {
    diamond: ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"],
    box: ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"],
  };

  async getAvailableStartPositions(
    propType: string,
    gridMode: GridMode
  ): Promise<BeatData[]> {
    console.log(
      `📍 Getting available start positions for ${propType} in ${gridMode} mode`
    );

    try {
      const startPositionKeys = this.DEFAULT_START_POSITIONS[gridMode];

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
            pictographData: this.createStartPositionPictograph(
              key,
              index,
              GridMode.DIAMOND
            ),
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
          pictographData: this.createStartPositionPictograph(
            key,
            index,
            gridMode
          ),
        });
      });

      console.log(`✅ Generated ${beatData.length} available start positions`);
      return beatData;
    } catch (error) {
      console.error("❌ Error getting available start positions:", error);
      return [];
    }
  }

  async setStartPosition(startPosition: BeatData): Promise<void> {
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
        const optionPickerFormat = {
          endPosition: startPosition.metadata?.endPosition || "alpha1", // Extract from metadata
          pictographData: startPosition.pictographData,
          letter: startPosition.pictographData?.letter,
          gridMode: GridMode.DIAMOND, // Default
          isStartPosition: true,
          // Include the full beat data for compatibility
          ...startPosition,
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
      const startPositionKeys = this.DEFAULT_START_POSITIONS[gridMode];

      if (!startPositionKeys) {
        console.error(
          `Unsupported grid mode: ${gridMode}. Supported modes: ${Object.keys(this.DEFAULT_START_POSITIONS).join(", ")}`
        );
        // Fallback to diamond mode
        const fallbackKeys = this.DEFAULT_START_POSITIONS.diamond;

        const pictographData: PictographData[] = fallbackKeys.map(
          (key, index) =>
            this.createStartPositionPictograph(key, index, GridMode.DIAMOND)
        );

        return pictographData;
      }

      const pictographData: PictographData[] = startPositionKeys.map(
        (key, index) => this.createStartPositionPictograph(key, index, gridMode)
      );

      return pictographData;
    } catch (error) {
      console.error("Error getting default start positions:", error);
      return [];
    }
  }

  private createStartPositionPictograph(
    key: string,
    index: number,
    gridMode: GridMode
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
      gridMode,
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
