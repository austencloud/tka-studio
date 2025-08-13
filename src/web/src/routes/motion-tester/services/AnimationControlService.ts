import { StandalonePortedEngine, type PropState } from "$lib/animator";
import type { MotionTestParams } from "./MotionParameterService";

export interface AnimationState {
  isPlaying: boolean;
  progress: number;
  currentBeat: number;
}

export interface PropVisibility {
  blue: boolean;
  red: boolean;
}

export interface PropStates {
  blue?: PropState;
  red?: PropState;
}

export class AnimationControlService {
  private animationEngine: StandalonePortedEngine;
  private animationFrameId: number | null = null;
  private currentProgress: number = 0;
  private isInitialized: boolean = false;
  private propVisibility: PropVisibility = { blue: true, red: true };

  constructor() {
    this.animationEngine = new StandalonePortedEngine();
  }

  // Initialize the animation engine with motion data
  async initializeEngine(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
  ): Promise<boolean> {
    try {
      const sequence = this.createDualPropTestSequence(blueParams, redParams);
      this.isInitialized = this.animationEngine.initialize(sequence);
      return this.isInitialized;
    } catch (error) {
      console.error("Failed to initialize animation engine:", error);
      this.isInitialized = false;
      return false;
    }
  }

  // Create a test sequence with dual prop motion in standalone array format
  private createDualPropTestSequence(
    blueParams: MotionTestParams,
    redParams: MotionTestParams,
  ) {
    return [
      // Index 0: Metadata
      {
        word: "TEST",
        author: "Motion Tester",
        totalBeats: 1,
      },
      // Index 1: Start position
      {
        beat: 0,
        letter: "START",
        letter_type: "start",
        blue_attributes: this.convertToAttributes(blueParams),
        red_attributes: this.convertToAttributes(redParams),
      },
      // Index 2: Motion step
      {
        beat: 1,
        letter: "TEST",
        letter_type: "motion",
        blue_attributes: this.convertToAttributes(blueParams),
        red_attributes: this.convertToAttributes(redParams),
      },
    ];
  }

  private convertToAttributes(params: MotionTestParams) {
    return {
      start_loc: params.startLoc,
      end_loc: params.endLoc,
      start_ori: params.startOri,
      end_ori: params.endOri,
      motion_type: params.motionType,
      prop_rot_dir: params.propRotDir,
      turns: params.turns,
    };
  }

  // Get current prop states
  getCurrentPropStates(): PropStates {
    return {
      blue: this.animationEngine.getBluePropState(),
      red: this.animationEngine.getRedPropState(),
    };
  }

  // Set animation progress (0-1)
  setProgress(progress: number): void {
    this.currentProgress = Math.max(0, Math.min(1, progress));
    // Calculate state for current progress
    const currentBeat = this.currentProgress * this.getTotalBeats();
    this.animationEngine.calculateState(currentBeat);
  }

  // Get current animation progress
  getProgress(): number {
    return this.currentProgress;
  }

  // Start animation playback
  startAnimation(): void {
    if (this.animationFrameId) {
      this.stopAnimation();
    }

    const animate = () => {
      const currentProgress = this.getProgress();
      if (currentProgress < 1) {
        // Animate over 2 seconds (0.016 per frame at 60fps = ~1 second, so 0.008 = ~2 seconds)
        this.setProgress(currentProgress + 0.008);
        this.animationFrameId = requestAnimationFrame(animate);
      } else {
        // Animation completed
        this.animationFrameId = null;
      }
    };

    this.animationFrameId = requestAnimationFrame(animate);
  }

  // Stop animation playback
  stopAnimation(): void {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }

  // Reset animation to beginning
  resetAnimation(): void {
    this.stopAnimation();
    this.setProgress(0);
  }

  // Check if animation is playing
  isPlaying(): boolean {
    return this.animationFrameId !== null;
  }

  // Get current beat based on progress
  getCurrentBeat(): number {
    return this.getProgress(); // For single beat motion, progress = beat
  }

  // Set prop visibility
  setPropVisibility(prop: "blue" | "red", visible: boolean): void {
    this.propVisibility[prop] = visible;
  }

  // Get prop visibility
  getPropVisibility(prop: "blue" | "red"): boolean {
    return this.propVisibility[prop];
  }

  // Check if engine is initialized
  isEngineInitialized(): boolean {
    return this.isInitialized;
  }

  // Get total beats
  getTotalBeats(): number {
    return 1; // Single beat for motion testing
  }

  // Cleanup resources
  dispose(): void {
    this.stopAnimation();
    // Additional cleanup if needed
  }
}
