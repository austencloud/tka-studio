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
  createGridData,
  createArrowData,
  createPropData,
  createMotionData,
} from "$lib/domain";
import {
  GridMode,
  MotionType,
  Location,
  Orientation,
  RotationDirection,
  ArrowType,
  PropType,
} from "$lib/domain/enums";
import type { MotionTesterState } from "../state/motion-tester-state.svelte";
import type { IMotionTesterCsvLookupService } from "$lib/services/di/interfaces/motion-tester-interfaces";

export interface IAnimatedPictographDataService {
  createAnimatedPictographData(
    motionState: MotionTesterState
  ): Promise<PictographData | null>;
}

export class AnimatedPictographDataService
  implements IAnimatedPictographDataService
{
  constructor(private csvLookupService?: IMotionTesterCsvLookupService) {}
  /**
   * Creates complete pictograph data for animated display using current motion parameters.
   * Uses CSV lookup service to find the correct letter and pictograph data.
   */
  async createAnimatedPictographData(
    motionState: MotionTesterState
  ): Promise<PictographData | null> {
    try {
      const gridMode = this.getGridMode(motionState.gridType);

      // Try to use CSV lookup service first for accurate letter detection
      if (this.csvLookupService) {
        console.log("🔍 Using CSV lookup service for pictograph generation...");

        const csvPictograph =
          await this.csvLookupService.findMatchingPictograph(
            motionState.blueMotionParams,
            motionState.redMotionParams,
            gridMode
          );

        if (csvPictograph) {
          console.log(
            `✅ CSV lookup successful! Found letter: ${csvPictograph.letter}`
          );

          // Update metadata to include animation progress
          csvPictograph.metadata = {
            ...csvPictograph.metadata,
            source: "motion_tester_csv_lookup",
            grid_type: motionState.gridType,
            progress: motionState.animationState.progress,
          };

          return csvPictograph;
        } else {
          console.warn(
            "⚠️ CSV lookup failed, falling back to manual generation..."
          );
        }
      } else {
        console.warn(
          "⚠️ CSV lookup service not available, using manual generation..."
        );
      }

      // Fallback: Create pictograph manually (original logic)
      const gridData = createGridData({ grid_mode: gridMode });

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
        "blue"
      );
      const redProps = this.createPropDataFromMotion(
        motionState.redMotionParams,
        "red"
      );

      // Create arrow data based on motion parameters
      const blueArrows = this.createArrowDataFromMotion(
        motionState.blueMotionParams,
        "blue"
      );
      const redArrows = this.createArrowDataFromMotion(
        motionState.redMotionParams,
        "red"
      );

      const pictographData = createPictographData({
        id: "motion-tester-fallback-pictograph",
        grid_data: gridData,
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
        letter: "?", // Unknown letter when CSV lookup fails
        beat: 1,
        is_blank: false,
        is_mirrored: false,
        metadata: {
          source: "motion_tester_fallback",
          grid_type: motionState.gridType,
          progress: motionState.animationState.progress,
        },
      });

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
  private createCompleteMotionData(motionParams: any): MotionData {
    return createMotionData({
      motion_type: this.mapMotionType(motionParams.motionType),
      start_loc: this.mapLocation(motionParams.startLoc),
      end_loc: this.mapLocation(motionParams.endLoc),
      start_ori: this.mapOrientation(motionParams.startOri),
      end_ori: this.mapOrientation(motionParams.endOri),
      prop_rot_dir: this.mapRotationDirection(motionParams.propRotDir),
      turns: motionParams.turns,
      is_visible: true,
    });
  }

  /**
   * Creates prop data based on motion parameters
   */
  private createPropDataFromMotion(
    motionParams: any,
    color: "blue" | "red"
  ): PropData {
    return createPropData({
      prop_type: PropType.STAFF, // Default to staff for motion tester
      color: color,
      location: this.mapLocation(motionParams.startLoc),
      orientation: this.mapOrientation(motionParams.startOri),
      rotation_direction: this.mapRotationDirection(motionParams.propRotDir),
      is_visible: true,
    });
  }

  /**
   * Creates arrow data based on motion parameters
   */
  private createArrowDataFromMotion(
    motionParams: any,
    color: "blue" | "red"
  ): ArrowData {
    return createArrowData({
      arrow_type: color === "blue" ? ArrowType.BLUE : ArrowType.RED,
      color: color,
      motion_type: motionParams.motionType,
      start_orientation: motionParams.startOri,
      end_orientation: motionParams.endOri,
      rotation_direction: motionParams.propRotDir,
      turns: motionParams.turns,
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
}
