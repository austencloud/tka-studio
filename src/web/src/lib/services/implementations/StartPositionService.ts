/**
 * Start Position Service - Implementation
 *
 * Provides start position management functionality for the construct workflow.
 * Based on the desktop StartPositionOrchestrator but simplified for web.
 */

import type { BeatData, PictographData } from "../../domain";
import {
  ArrowType,
  createArrowData,
  createBeatData,
  createGridData,
  createMotionData,
  createPictographData,
  createPropData,
  GridMode as DomainGridMode,
  MotionType as DomainMotionType,
  Location,
  Orientation,
  PropType,
  RotationDirection,
} from "../../domain";
import type {
  GridMode,
  IStartPositionService,
  ValidationResult,
} from "../interfaces";
import type { ValidationError } from "$lib/domain/sequenceCard";
export class StartPositionService implements IStartPositionService {
  private readonly DEFAULT_START_POSITIONS = {
    diamond: ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"],
    box: ["alpha2_alpha2", "beta4_beta4", "gamma12_gamma12"],
  };

  constructor() {
    console.log("🎯 StartPositionService initialized");
  }

  async getAvailableStartPositions(
    propType: string,
    gridMode: GridMode,
  ): Promise<BeatData[]> {
    console.log(
      `📍 Getting available start positions for ${propType} in ${gridMode} mode`,
    );

    try {
      const startPositionKeys = this.DEFAULT_START_POSITIONS[gridMode];

      const beatData: BeatData[] = startPositionKeys.map((key, index) => {
        return createBeatData({
          beat_number: 0,
          is_blank: false,
          pictograph_data: this.createStartPositionPictograph(
            key,
            index,
            gridMode,
          ),
        });
      });
      console.log(`✅ Generated ${beatData.length} start positions`);
      return beatData;
    } catch (error) {
      console.error("❌ Error getting start positions:", error);
      return [];
    }
  }

  async setStartPosition(startPosition: BeatData): Promise<void> {
    console.log(
      "🎯 Setting start position:",
      startPosition.pictograph_data?.id,
    );

    try {
      // Store in localStorage for persistence in the format OptionPicker expects
      if (typeof window !== "undefined") {
        // Check if localStorage already has the correct format (from StartPositionPicker)
        const existingData = localStorage.getItem("start_position");
        if (existingData) {
          try {
            const parsed = JSON.parse(existingData);
            // If it already has top-level endPos, don't overwrite it
            if (parsed.endPos) {
              console.log(
                "✅ Start position already in correct format, not overwriting",
              );
              return;
            }
          } catch {
            // If parsing fails, continue with saving new format
          }
        }

        // Create the format that OptionPicker expects
        const optionPickerFormat = {
          endPos: startPosition.metadata?.endPos || "alpha1", // Extract from metadata
          pictograph_data: startPosition.pictograph_data,
          letter: startPosition.pictograph_data?.letter,
          gridMode: "diamond", // Default
          isStartPosition: true,
          // Include the full beat data for compatibility
          ...startPosition,
        };

        localStorage.setItem(
          "start_position",
          JSON.stringify(optionPickerFormat),
        );
      }

      console.log("✅ Start position set successfully");
    } catch (error) {
      console.error("❌ Error setting start position:", error);
      throw new Error(
        `Failed to set start position: ${error instanceof Error ? error.message : "Unknown error"}`,
      );
    }
  }

  validateStartPosition(position: BeatData): ValidationResult {
    const errors: ValidationError[] = [];

    if (!position.pictograph_data) {
      errors.push({
        code: "MISSING_PICTOGRAPH_DATA",
        message: "Start position must have pictograph data",
        severity: "error",
      });
    }

    if (
      !position.pictograph_data?.motions?.blue &&
      !position.pictograph_data?.motions?.red
    ) {
      errors.push({
        code: "MISSING_MOTIONS",
        message: "Start position must have at least one motion",
        severity: "error",
      });
    }

    // Validate motion types are static for start positions
    if (
      position.pictograph_data?.motions?.blue?.motion_type !==
      DomainMotionType.STATIC
    ) {
      errors.push({
        code: "INVALID_BLUE_MOTION",
        message: "Blue motion must be static for start positions",
        severity: "error",
      });
    }

    if (
      position.pictograph_data?.motions?.red?.motion_type !==
      DomainMotionType.STATIC
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
    gridMode: GridMode,
  ): Promise<PictographData[]> {
    console.log(`📍 Getting default start positions for ${gridMode} mode`);

    try {
      const startPositionKeys = this.DEFAULT_START_POSITIONS[gridMode];

      const pictographData: PictographData[] = startPositionKeys.map(
        (key, index) =>
          this.createStartPositionPictograph(key, index, gridMode),
      );

      console.log(
        `✅ Generated ${pictographData.length} default start positions`,
      );
      return pictographData;
    } catch (error) {
      console.error("❌ Error getting default start positions:", error);
      return [];
    }
  }

  private createStartPositionPictograph(
    key: string,
    index: number,
    gridMode: GridMode,
  ): PictographData {
    // Determine letter based on position key
    let letter: string;
    if (key.includes("alpha")) letter = "α";
    else if (key.includes("beta")) letter = "β";
    else if (key.includes("gamma")) letter = "γ";
    else letter = key;

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
      console.warn(`⚠️ No position mapping found for ${key}, using fallback`);
    }

    const blueLocation = mapping?.blue || Location.SOUTH;
    const redLocation = mapping?.red || Location.NORTH;

    console.log(
      `🎯 Creating start position ${key} - Blue: ${blueLocation}, Red: ${redLocation}`,
    );

    // Create proper arrow data with location
    const blueArrow = createArrowData({
      arrow_type: ArrowType.BLUE,
      color: "blue",
      turns: 0,
      location: blueLocation,
    });

    const redArrow = createArrowData({
      arrow_type: ArrowType.RED,
      color: "red",
      turns: 0,
      location: redLocation,
    });

    // Create proper prop data with location
    const blueProp = createPropData({
      prop_type: PropType.STAFF,
      color: "blue",
      location: blueLocation,
    });

    const redProp = createPropData({
      prop_type: PropType.STAFF,
      color: "red",
      location: redLocation,
    });

    // Create proper motion data
    const blueMotion = createMotionData({
      motion_type: DomainMotionType.STATIC,
      prop_rot_dir: RotationDirection.NO_ROTATION,
      start_loc: blueLocation,
      end_loc: blueLocation,
      turns: 0,
      start_ori: Orientation.IN,
      end_ori: Orientation.IN,
    });

    const redMotion = createMotionData({
      motion_type: DomainMotionType.STATIC,
      prop_rot_dir: RotationDirection.NO_ROTATION,
      start_loc: redLocation,
      end_loc: redLocation,
      turns: 0,
      start_ori: Orientation.IN,
      end_ori: Orientation.IN,
    });

    const pictograph = createPictographData({
      id: `start-pos-${key}-${index}`,
      grid_data: createGridData({
        grid_mode:
          gridMode === "diamond" ? DomainGridMode.DIAMOND : DomainGridMode.BOX,
      }),
      arrows: { blue: blueArrow, red: redArrow },
      props: { blue: blueProp, red: redProp },
      motions: { blue: blueMotion, red: redMotion },
      letter,
      beat: index,
      is_blank: false,
      is_mirrored: false,
    });

    return pictograph;
  }
}
