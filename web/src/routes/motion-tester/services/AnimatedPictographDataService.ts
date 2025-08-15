/**
 * AnimatedPictographDataService - Service for creating animated pictograph data
 *
 * Handles the complex logic of transforming motion parameters into pictograph data
 * for animated display in the motion tester.
 */

import type { PictographData } from "$lib/domain/types";
import { createPictographData, createGridData } from "$lib/domain";
import {
  GridMode,
  MotionType,
  Location,
  Orientation,
  RotationDirection,
} from "$lib/domain/enums";
import type { MotionTesterState } from "../state/motion-tester-state.svelte";

export interface IAnimatedPictographDataService {
  createAnimatedPictographData(
    motionState: MotionTesterState
  ): PictographData | null;
}

export class AnimatedPictographDataService
  implements IAnimatedPictographDataService
{
  /**
   * Creates pictograph data for animated display using current motion parameters
   * and animation progress from the motion tester state.
   */
  createAnimatedPictographData(
    motionState: MotionTesterState
  ): PictographData | null {
    try {
      const gridMode = this.getGridMode(motionState.gridType);
      const gridData = createGridData({ grid_mode: gridMode });

      // Debug: Log motion parameters (using snapshot to avoid Svelte warnings)
      console.log(
        "🔍 Motion Tester Debug - Blue Motion Params:",
        JSON.parse(JSON.stringify(motionState.blueMotionParams))
      );
      console.log(
        "🔍 Motion Tester Debug - Red Motion Params:",
        JSON.parse(JSON.stringify(motionState.redMotionParams))
      );

      const blueMotionData = this.createMotionData(
        motionState.blueMotionParams
      );
      const redMotionData = this.createMotionData(motionState.redMotionParams);

      // Debug: Log created motion data
      console.log("🔍 Motion Tester Debug - Blue Motion Data:", blueMotionData);
      console.log("🔍 Motion Tester Debug - Red Motion Data:", redMotionData);

      const pictographData = createPictographData({
        id: "motion-tester-animated-pictograph",
        grid_data: gridData,
        arrows: {},
        props: {},
        motions: {
          blue: blueMotionData,
          red: redMotionData,
        },
        letter: "T", // T for "Tester"
        beat: 1,
        is_blank: false,
        is_mirrored: false,
        metadata: {
          source: "motion_tester_animated",
          grid_type: motionState.gridType,
          progress: motionState.animationState.progress,
        },
      });

      // Debug: Log final pictograph data
      console.log(
        "🔍 Motion Tester Debug - Final Pictograph Data:",
        pictographData
      );

      return pictographData;
    } catch (error) {
      console.error("Error creating animated pictograph data:", error);
      return null;
    }
  }

  private getGridMode(gridType: string): GridMode {
    return gridType === "diamond" ? GridMode.DIAMOND : GridMode.BOX;
  }

  private createMotionData(motionParams: any) {
    return {
      motion_type: motionParams.motionType as MotionType,
      start_loc: motionParams.startLoc as Location,
      end_loc: motionParams.endLoc as Location,
      start_ori: motionParams.startOri as Orientation,
      end_ori: motionParams.endOri as Orientation,
      prop_rot_dir: motionParams.propRotDir as RotationDirection,
      turns: motionParams.turns,
      is_visible: true,
    };
  }
}
