/**
 * Standalone Ported Engine
 *
 * This engine ports the exact working logic from the standalone HTML animator.
 * DO NOT MODIFY the core animation logic - it's proven to work.
 */

import type { PropState } from "../../types/core.js";
import {
  lerpAngle,
  calculateStepEndpoints,
  type StepDefinition,
} from "../../utils/standalone-math.js";

// Grid constants from standalone
const GRID_VIEWBOX_SIZE = 950;
const GRID_CENTER = GRID_VIEWBOX_SIZE / 2;
const GRID_HALFWAY_POINT_OFFSET = 151.5;

export interface SequenceMetadata {
  word: string;
  author: string;
  totalBeats: number;
}

/**
 * Standalone Ported Animation Engine
 * Uses exact logic from working standalone HTML animator
 */
export class SequenceAnimationEngine {
  private parsedSteps: StepDefinition[] = [];
  private totalBeats = 0;
  private metadata: SequenceMetadata = { word: "", author: "", totalBeats: 0 };

  // Prop states
  private bluePropState: PropState = {
    centerPathAngle: 0,
    staffRotationAngle: 0,
    x: 0,
    y: 0,
  };

  private redPropState: PropState = {
    centerPathAngle: 0,
    staffRotationAngle: 0,
    x: 0,
    y: 0,
  };

  /**
   * Initialize with sequence data in standalone format
   */
  initialize(sequenceData: any[]): boolean {
    try {
      console.log(
        "StandalonePortedEngine: Initializing with data:",
        sequenceData,
      );

      if (!Array.isArray(sequenceData) || sequenceData.length < 3) {
        throw new Error("Invalid sequence data format");
      }

      // Extract metadata (index 0)
      const meta = sequenceData[0] || {};
      this.metadata = {
        word: meta.word || "",
        author: meta.author || "",
        totalBeats: sequenceData.length - 2, // Subtract metadata and start position
      };

      // Extract steps (index 2 onwards)
      this.parsedSteps = sequenceData;
      this.totalBeats = this.metadata.totalBeats;

      console.log(
        "StandalonePortedEngine: Parsed steps:",
        this.parsedSteps.length,
      );
      console.log("StandalonePortedEngine: Total beats:", this.totalBeats);

      this.initializePropStates();
      return true;
    } catch (error) {
      console.error("StandalonePortedEngine: Failed to initialize:", error);
      return false;
    }
  }

  /**
   * Reset to initial state
   */
  reset(): void {
    this.initializePropStates();
  }

  /**
   * Calculate state for given beat using exact standalone logic
   */
  calculateState(currentBeat: number): void {
    if (this.parsedSteps.length === 0 || this.totalBeats === 0) {
      console.warn("StandalonePortedEngine: No sequence data available");
      return;
    }

    // EXACT LOGIC FROM STANDALONE HTML - DO NOT MODIFY
    const clampedBeat = Math.max(0, Math.min(currentBeat, this.totalBeats));
    const currentAnimationStepIndex = Math.floor(
      clampedBeat === this.totalBeats ? this.totalBeats - 1 : clampedBeat,
    );
    const currentStepArrayIndex = currentAnimationStepIndex + 2; // Map beat 0..N-1 to array index 2..N+1
    const t =
      clampedBeat === this.totalBeats
        ? 1.0
        : clampedBeat - currentAnimationStepIndex;

    const stepDefinition = this.parsedSteps[currentStepArrayIndex];

    if (!stepDefinition) {
      console.error(
        `StandalonePortedEngine: No step definition for array index ${currentStepArrayIndex} (beat: ${clampedBeat})`,
      );
      return;
    }

    const blueEndpoints = calculateStepEndpoints(stepDefinition, "blue");
    const redEndpoints = calculateStepEndpoints(stepDefinition, "red");

    if (blueEndpoints && redEndpoints) {
      console.log(
        "🔧 [MOTION DEBUG] ===== CALCULATING STATE FOR BEAT",
        currentBeat,
        "=====",
      );
      console.log(
        "🔧 [MOTION DEBUG] Step definition:",
        JSON.stringify(stepDefinition, null, 2),
      );
      console.log("🔧 [MOTION DEBUG] Blue endpoints:", blueEndpoints);
      console.log("🔧 [MOTION DEBUG] Red endpoints:", redEndpoints);
      console.log("🔧 [MOTION DEBUG] Interpolation factor t:", t);

      // EXACT INTERPOLATION LOGIC FROM STANDALONE
      this.bluePropState.centerPathAngle = lerpAngle(
        blueEndpoints.startCenterAngle,
        blueEndpoints.targetCenterAngle,
        t,
      );
      this.bluePropState.staffRotationAngle = lerpAngle(
        blueEndpoints.startStaffAngle,
        blueEndpoints.targetStaffAngle,
        t,
      );
      this.redPropState.centerPathAngle = lerpAngle(
        redEndpoints.startCenterAngle,
        redEndpoints.targetCenterAngle,
        t,
      );
      this.redPropState.staffRotationAngle = lerpAngle(
        redEndpoints.startStaffAngle,
        redEndpoints.targetStaffAngle,
        t,
      );

      console.log("🔧 [MOTION DEBUG] After interpolation:");
      console.log("🔧 [MOTION DEBUG] Blue state:", { ...this.bluePropState });
      console.log("🔧 [MOTION DEBUG] Red state:", { ...this.redPropState });

      // Pro motion override removed - turns calculation now handled in calculateStepEndpoints
      console.log(
        "🔧 [MOTION DEBUG] Pro motion override removed - using calculated endpoints",
      );

      // Update coordinates from angles
      this.updateCoordinatesFromAngle(this.bluePropState);
      this.updateCoordinatesFromAngle(this.redPropState);

      console.log("🔧 [MOTION DEBUG] Final state after coordinate update:");
      console.log("🔧 [MOTION DEBUG] Blue final:", { ...this.bluePropState });
      console.log("🔧 [MOTION DEBUG] Red final:", { ...this.redPropState });
    } else {
      console.error(
        "StandalonePortedEngine: Could not calculate endpoints for step",
      );
    }
  }

  /**
   * Initialize prop states to start position using exact standalone logic
   */
  private initializePropStates(): void {
    console.log(
      "🔧 [MOTION DEBUG] StandalonePortedEngine: Initializing prop states",
    );
    console.log(
      "🔧 [MOTION DEBUG] Parsed steps length:",
      this.parsedSteps.length,
    );

    if (!this.parsedSteps || this.parsedSteps.length < 2) {
      console.warn(
        "🔧 [MOTION DEBUG] No parsed steps available, using fallback initialization",
      );
      // Fallback to hardcoded positions
      this.bluePropState = {
        centerPathAngle: 0,
        staffRotationAngle: Math.PI, // 'in' orientation
        x: 0,
        y: 0,
      };
      this.redPropState = {
        centerPathAngle: Math.PI, // Opposite side
        staffRotationAngle: 0, // 'in' orientation
        x: 0,
        y: 0,
      };
    } else {
      // EXACT LOGIC FROM STANDALONE ANIMATOR - Use index 1 for initial state
      const startStateStep = this.parsedSteps[1];
      console.log(
        "🔧 [MOTION DEBUG] Start state step:",
        JSON.stringify(startStateStep, null, 2),
      );

      const blueStartEndpoints = calculateStepEndpoints(startStateStep, "blue");
      const redStartEndpoints = calculateStepEndpoints(startStateStep, "red");

      console.log(
        "🔧 [MOTION DEBUG] Blue start endpoints:",
        blueStartEndpoints,
      );
      console.log("🔧 [MOTION DEBUG] Red start endpoints:", redStartEndpoints);

      if (blueStartEndpoints) {
        this.bluePropState.centerPathAngle =
          blueStartEndpoints.startCenterAngle;
        this.bluePropState.staffRotationAngle =
          blueStartEndpoints.startStaffAngle;
      } else {
        console.warn("🔧 [MOTION DEBUG] No blue endpoints, using fallback");
        this.bluePropState.centerPathAngle = 0; // mapPositionToAngle("s") equivalent
        this.bluePropState.staffRotationAngle =
          this.bluePropState.centerPathAngle + Math.PI;
      }

      if (redStartEndpoints) {
        this.redPropState.centerPathAngle = redStartEndpoints.startCenterAngle;
        this.redPropState.staffRotationAngle =
          redStartEndpoints.startStaffAngle;
      } else {
        console.warn("🔧 [MOTION DEBUG] No red endpoints, using fallback");
        this.redPropState.centerPathAngle = Math.PI; // mapPositionToAngle("n") equivalent
        this.redPropState.staffRotationAngle =
          this.redPropState.centerPathAngle + Math.PI;
      }
    }

    this.updateCoordinatesFromAngle(this.bluePropState);
    this.updateCoordinatesFromAngle(this.redPropState);

    console.log("🔧 [MOTION DEBUG] Initial State Set:", {
      blue: { ...this.bluePropState },
      red: { ...this.redPropState },
    });
  }

  /**
   * Update x,y coordinates from center path angle
   * FIXED: Use exact same logic as standalone animator with grid center offset
   */
  private updateCoordinatesFromAngle(propState: PropState): void {
    const radius = GRID_HALFWAY_POINT_OFFSET; // 151.5
    const centerX = GRID_CENTER; // 475
    const centerY = GRID_CENTER; // 475

    // EXACT LOGIC FROM STANDALONE ANIMATOR
    propState.x = centerX + Math.cos(propState.centerPathAngle) * radius;
    propState.y = centerY + Math.sin(propState.centerPathAngle) * radius;
  }

  // Public getters
  getBluePropState(): PropState {
    return { ...this.bluePropState };
  }

  getRedPropState(): PropState {
    return { ...this.redPropState };
  }

  getTotalBeats(): number {
    return this.totalBeats;
  }

  getMetadata(): SequenceMetadata {
    return { ...this.metadata };
  }
}
