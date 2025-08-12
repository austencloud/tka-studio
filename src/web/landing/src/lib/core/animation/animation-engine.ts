// Animation engine for the pictograph animator

import type { AnimationState, PropState, StepDefinition } from "./types";
import { calculateStepEndpoints } from "./sequence-processor";
import {
  lerpAngle,
  calculateProIsolationStaffAngle,
  mapPositionToAngle,
} from "./math-utils";
import { PI } from "./constants";

export class AnimationEngine {
  private animationState: AnimationState;
  private parsedSteps: StepDefinition[] = [];
  private bluePropState: PropState;
  private redPropState: PropState;
  private onRender: () => void;
  private onUIUpdate: () => void;
  private onAnimationEnd?: () => void;

  constructor(
    bluePropState: PropState,
    redPropState: PropState,
    onRender: () => void,
    onUIUpdate: () => void,
    onAnimationEnd?: () => void
  ) {
    this.animationState = {
      isPlaying: false,
      currentBeat: 0,
      speed: 1.0,
      continuousLoop: false,
      totalBeats: 0,
      lastTimestamp: null,
      animationFrameId: null,
    };
    this.bluePropState = bluePropState;
    this.redPropState = redPropState;
    this.onRender = onRender;
    this.onUIUpdate = onUIUpdate;
    this.onAnimationEnd = onAnimationEnd;
  }

  // Getters for reactive state
  get isPlaying() {
    return this.animationState.isPlaying;
  }
  get currentBeat() {
    return this.animationState.currentBeat;
  }
  get speed() {
    return this.animationState.speed;
  }
  get continuousLoop() {
    return this.animationState.continuousLoop;
  }
  get totalBeats() {
    return this.animationState.totalBeats;
  }

  // Setters
  setSpeed(speed: number) {
    this.animationState.speed = Math.max(0.01, speed);
  }

  setContinuousLoop(loop: boolean) {
    this.animationState.continuousLoop = loop;
  }

  setParsedSteps(steps: StepDefinition[], totalBeats: number) {
    this.parsedSteps = steps;
    this.animationState.totalBeats = totalBeats;
  }

  // Animation loop
  private animationLoop = (timestamp: number) => {
    console.log("🎦 LOOP: Animation frame called", {
      isPlaying: this.animationState.isPlaying,
      timestamp,
    });
    if (!this.animationState.isPlaying) {
      console.log("⚠️ LOOP: Not playing, exiting");
      return;
    }

    if (this.animationState.lastTimestamp === null)
      this.animationState.lastTimestamp = timestamp;
    const deltaTime = timestamp - this.animationState.lastTimestamp;
    this.animationState.lastTimestamp = timestamp;
    const effectiveSpeed = Math.max(0.01, this.animationState.speed);
    const oldBeat = this.animationState.currentBeat;
    this.animationState.currentBeat += (deltaTime / 1000) * effectiveSpeed;

    console.log("🎦 LOOP: Beat update", {
      oldBeat,
      newBeat: this.animationState.currentBeat,
      deltaTime,
      effectiveSpeed,
    });

    // Loop Handling
    if (this.animationState.currentBeat >= this.animationState.totalBeats) {
      if (this.animationState.continuousLoop) {
        this.animationState.currentBeat = 0;
        this.animationState.lastTimestamp = timestamp;
        console.log("🔁 LOOP: Looping back to time 0");
      } else {
        this.animationState.currentBeat = this.animationState.totalBeats;
        this.pause();
        console.log("🏁 LOOP: Animation ended.");
        this.updateBeat(this.animationState.currentBeat, true);
        this.onUIUpdate();
        if (this.onAnimationEnd) this.onAnimationEnd();
        return;
      }
    }

    // State Calculation for Current Frame
    this.updatePropStates();
    this.onRender();
    this.onUIUpdate();

    if (this.animationState.isPlaying) {
      this.animationState.animationFrameId = requestAnimationFrame(
        this.animationLoop
      );
    }
  };

  private updatePropStates() {
    const clampedBeat = Math.max(
      0,
      Math.min(this.animationState.currentBeat, this.animationState.totalBeats)
    );
    const currentAnimationStepIndex = Math.floor(
      clampedBeat === this.animationState.totalBeats
        ? this.animationState.totalBeats - 1
        : clampedBeat
    );
    const currentStepArrayIndex = currentAnimationStepIndex + 2;
    const t =
      clampedBeat === this.animationState.totalBeats
        ? 1.0
        : clampedBeat - currentAnimationStepIndex;

    const stepDefinition = this.parsedSteps[currentStepArrayIndex];

    console.log("🎦 LOOP: Step calculation", {
      clampedBeat,
      currentAnimationStepIndex,
      currentStepArrayIndex,
      t,
      stepDefinition: !!stepDefinition,
    });

    if (!stepDefinition) {
      console.error(
        `❌ LOOP: No step definition for array index ${currentStepArrayIndex} (beat: ${clampedBeat})`
      );
      this.pause();
      return;
    }

    const blueEndpoints = calculateStepEndpoints(stepDefinition, "blue");
    const redEndpoints = calculateStepEndpoints(stepDefinition, "red");

    if (blueEndpoints && redEndpoints) {
      this.bluePropState.centerPathAngle = lerpAngle(
        blueEndpoints.startCenterAngle,
        blueEndpoints.targetCenterAngle,
        t
      );
      this.bluePropState.staffRotationAngle = lerpAngle(
        blueEndpoints.startStaffAngle,
        blueEndpoints.targetStaffAngle,
        t
      );
      this.redPropState.centerPathAngle = lerpAngle(
        redEndpoints.startCenterAngle,
        redEndpoints.targetCenterAngle,
        t
      );
      this.redPropState.staffRotationAngle = lerpAngle(
        redEndpoints.startStaffAngle,
        redEndpoints.targetStaffAngle,
        t
      );

      if (stepDefinition.blue_attributes.motion_type === "pro") {
        this.bluePropState.staffRotationAngle = calculateProIsolationStaffAngle(
          this.bluePropState.centerPathAngle,
          stepDefinition.blue_attributes.prop_rot_dir
        );
      }
      if (stepDefinition.red_attributes.motion_type === "pro") {
        this.redPropState.staffRotationAngle = calculateProIsolationStaffAngle(
          this.redPropState.centerPathAngle,
          stepDefinition.red_attributes.prop_rot_dir
        );
      }

      console.log("🎦 LOOP: Updated prop states", {
        blue: {
          centerAngle: this.bluePropState.centerPathAngle,
          staffAngle: this.bluePropState.staffRotationAngle,
        },
        red: {
          centerAngle: this.redPropState.centerPathAngle,
          staffAngle: this.redPropState.staffRotationAngle,
        },
      });
    } else {
      console.error(
        `❌ LOOP: Could not calculate endpoints for step index ${currentStepArrayIndex}`
      );
    }
  }

  // Control functions
  play() {
    console.log("▶️ PLAY: Starting animation...");
    if (this.animationState.isPlaying) {
      console.log("⚠️ PLAY: Already playing, ignoring");
      return;
    }
    console.log("▶️ PLAY: Setting isPlaying to true");
    this.animationState.isPlaying = true;
    this.animationState.lastTimestamp = null;
    console.log("▶️ PLAY: Starting animation frame loop...");
    this.animationState.animationFrameId = requestAnimationFrame(
      this.animationLoop
    );
    console.log("✅ PLAY: Animation started!");
  }

  pause() {
    console.log("⏸️ PAUSE: Pausing animation...");
    if (!this.animationState.isPlaying) {
      console.log("⚠️ PAUSE: Not playing, ignoring");
      return;
    }
    this.animationState.isPlaying = false;
    if (this.animationState.animationFrameId) {
      cancelAnimationFrame(this.animationState.animationFrameId);
      this.animationState.animationFrameId = null;
      console.log("⏸️ PAUSE: Cancelled animation frame");
    }
    console.log("✅ PAUSE: Animation paused!");
  }

  reset() {
    this.pause();
    this.animationState.currentBeat = 0;
    this.initializeState();
    this.onRender();
    this.onUIUpdate();
  }

  updateBeat(newBeat: number, renderImmediately = true) {
    this.animationState.currentBeat = Math.max(
      0,
      Math.min(parseFloat(newBeat.toString()), this.animationState.totalBeats)
    );

    const clampedBeat = this.animationState.currentBeat;
    const currentAnimationStepIndex = Math.floor(
      clampedBeat === this.animationState.totalBeats
        ? this.animationState.totalBeats - 1
        : clampedBeat
    );
    const currentStepArrayIndex = currentAnimationStepIndex + 2;
    const t =
      clampedBeat === this.animationState.totalBeats
        ? 1.0
        : clampedBeat - currentAnimationStepIndex;
    const stepDef = this.parsedSteps[currentStepArrayIndex];

    if (stepDef) {
      const blueEP = calculateStepEndpoints(stepDef, "blue");
      const redEP = calculateStepEndpoints(stepDef, "red");
      if (blueEP && redEP) {
        this.bluePropState.centerPathAngle = lerpAngle(
          blueEP.startCenterAngle,
          blueEP.targetCenterAngle,
          t
        );
        this.bluePropState.staffRotationAngle = lerpAngle(
          blueEP.startStaffAngle,
          blueEP.targetStaffAngle,
          t
        );
        this.redPropState.centerPathAngle = lerpAngle(
          redEP.startCenterAngle,
          redEP.targetCenterAngle,
          t
        );
        this.redPropState.staffRotationAngle = lerpAngle(
          redEP.startStaffAngle,
          redEP.targetStaffAngle,
          t
        );
        if (stepDef.blue_attributes.motion_type === "pro") {
          this.bluePropState.staffRotationAngle =
            calculateProIsolationStaffAngle(
              this.bluePropState.centerPathAngle,
              stepDef.blue_attributes.prop_rot_dir
            );
        }
        if (stepDef.red_attributes.motion_type === "pro") {
          this.redPropState.staffRotationAngle =
            calculateProIsolationStaffAngle(
              this.redPropState.centerPathAngle,
              stepDef.red_attributes.prop_rot_dir
            );
        }
      }
    } else if (this.animationState.currentBeat === 0) {
      this.initializeState();
    } else {
      console.warn(
        `Could not find step definition for beat ${this.animationState.currentBeat} (index ${currentStepArrayIndex})`
      );
    }

    if (renderImmediately) this.onRender();
  }

  // Initialize prop states from sequence start
  initializeState() {
    if (!this.parsedSteps || this.parsedSteps.length < 2) return;
    const startStateStep = this.parsedSteps[1];
    const blueStartEndpoints = calculateStepEndpoints(startStateStep, "blue");
    const redStartEndpoints = calculateStepEndpoints(startStateStep, "red");

    if (blueStartEndpoints) {
      this.bluePropState.centerPathAngle = blueStartEndpoints.startCenterAngle;
      this.bluePropState.staffRotationAngle =
        blueStartEndpoints.startStaffAngle;
    } else {
      this.bluePropState.centerPathAngle = mapPositionToAngle("s");
      this.bluePropState.staffRotationAngle =
        this.bluePropState.centerPathAngle + PI;
    }

    if (redStartEndpoints) {
      this.redPropState.centerPathAngle = redStartEndpoints.startCenterAngle;
      this.redPropState.staffRotationAngle = redStartEndpoints.startStaffAngle;
    } else {
      this.redPropState.centerPathAngle = mapPositionToAngle("n");
      this.redPropState.staffRotationAngle =
        this.redPropState.centerPathAngle + PI;
    }

    console.log("Initial State Set (from original beat 0 def):", {
      blue: { ...this.bluePropState },
      red: { ...this.redPropState },
    });
  }
}
