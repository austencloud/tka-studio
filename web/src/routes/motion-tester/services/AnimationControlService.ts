import type { PropState } from "$lib/animator";
import type { MotionTestParams } from "./MotionParameterService";
import type { IAnimationControlService } from "./interfaces";
import {
  createBeatData,
  createPictographData,
  createSequenceData,
} from "$lib/domain";
import type { SequenceData, MotionData } from "$lib/domain";
import {
  MotionType,
  Location,
  Orientation,
  RotationDirection,
  MotionColor,
} from "$lib/domain/enums";
import type { ISequenceAnimationEngine } from "$lib/services/di/interfaces/animator-interfaces";

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

export class AnimationControlService implements IAnimationControlService {
  private animationFrameId: number | null = null;
  private currentProgress: number = 0;
  private isInitialized: boolean = false;
  private propVisibility: PropVisibility = { blue: true, red: true };

  constructor(private readonly animationEngine: ISequenceAnimationEngine) {}

  // Initialize the animation engine with motion data
  async initializeEngine(
    blueParams: MotionTestParams,
    redParams: MotionTestParams
  ): Promise<boolean> {
    try {
      const sequence = this.createDualPropTestSequence(blueParams, redParams);
      this.isInitialized =
        this.animationEngine.initializeWithDomainData(sequence);
      return this.isInitialized;
    } catch (error) {
      console.error("Failed to initialize animation engine:", error);
      this.isInitialized = false;
      return false;
    }
  }

  // Create a test sequence with dual prop motion in domain format
  private createDualPropTestSequence(
    blueParams: MotionTestParams,
    redParams: MotionTestParams
  ): SequenceData {
    // Create a single beat with the test motion
    const testBeat = createBeatData({
      id: "test-beat-1",
      beat_number: 1,
      duration: 1,
      pictograph_data: createPictographData({
        id: "test-pictograph-1",
        letter: "TEST",
        motions: {
          blue: this.convertToMotionData(blueParams),
          red: this.convertToMotionData(redParams),
        },
      }),
    });

    // Create the sequence
    return createSequenceData({
      id: "motion-test-sequence",
      name: "Motion Test",
      word: "TEST",
      beats: [testBeat],
      metadata: {
        author: "Motion Tester",
        level: 1,
      },
    });
  }

  private convertToMotionData(params: MotionTestParams): MotionData {
    return {
      start_loc: params.startLoc as Location,
      end_loc: params.endLoc as Location,
      start_ori: params.startOri as Orientation,
      end_ori: params.endOri as Orientation,
      motion_type: params.motionType as MotionType,
      prop_rot_dir: params.rotationDirection as RotationDirection,
      turns: params.turns,
      is_visible: true, // ✅ Add required field for MotionData
    };
  }

  // Get current prop states
  getCurrentPropStates(): PropStates {
    const states = this.animationEngine.getCurrentPropStates();
    return {
      blue: states.blue,
      red: states.red,
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
  setPropVisibility(prop: MotionColor, visible: boolean): void {
    this.propVisibility[prop] = visible;
  }

  // Get prop visibility
  getPropVisibility(prop: MotionColor): boolean {
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
