import type { MotionData, SequenceData } from "$shared";
import {
  createMotionData,
  createPictographData,
  createSequenceData,
  GridLocation,
  MotionColor,
  MotionType,
  Orientation,
  PropType,
  RotationDirection,
  TYPES,
} from "$shared";
import { inject, injectable } from "inversify";
import type {
  IAnimationControlService,
  ISequenceAnimationEngine,
} from "../contracts";
import type { AnimatedMotionParams, PropStates } from "../../domain";
import { createBeatData } from "../../../build/workbench";

export interface AnimationState {
  isPlaying: boolean;
  progress: number;
  currentBeat: number;
}

export interface PropVisibility {
  blue: boolean;
  red: boolean;
}

@injectable()
export class AnimationControlService implements IAnimationControlService {
  private animationFrameId: number | null = null;
  private currentProgress: number = 0;
  private isInitialized: boolean = false;
  private propVisibility: PropVisibility = { blue: true, red: true };
  private isPlaying: boolean = false;
  private speed: number = 1.0;

  constructor(
    @inject(TYPES.ISequenceAnimationEngine)
    private readonly animationEngine: ISequenceAnimationEngine
  ) {}

  // IAnimationControlService implementation
  play(): void {
    this.isPlaying = true;
    console.log("Animation started");
  }

  pause(): void {
    this.isPlaying = false;
    console.log("Animation paused");
  }

  stop(): void {
    this.isPlaying = false;
    this.currentProgress = 0;
    console.log("Animation stopped");
  }

  seek(position: number): void {
    this.currentProgress = Math.max(0, Math.min(1, position));
    console.log(`Animation seeked to ${position}`);
  }

  setSpeed(speed: number): void {
    this.speed = Math.max(0.1, Math.min(5.0, speed));
    console.log(`Animation speed set to ${this.speed}`);
  }

  // Initialize the animation engine with motion data
  async initializeEngine(
    blueParams: AnimatedMotionParams,
    redParams: AnimatedMotionParams
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
    blueParams: AnimatedMotionParams,
    redParams: AnimatedMotionParams
  ): SequenceData {
    // Create a single beat with the test motion
    const testBeat = createBeatData({
      id: "test-beat-1",
      beatNumber: 1,
      duration: 1,
      pictographData: createPictographData({
        id: "test-pictograph-1",
        letter: null, // Test pictograph doesn't need a specific letter
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
        author: "Animator",
        level: 1,
      },
    });
  }

  private convertToMotionData(params: AnimatedMotionParams): MotionData {
    return createMotionData({
      startLocation: params.startLocation as GridLocation,
      endLocation: params.endLocation as GridLocation,
      startOrientation: params.startOrientation as Orientation,
      endOrientation: params.endOrientation as Orientation,
      motionType: params.motionType as MotionType,
      rotationDirection: params.rotationDirection as RotationDirection,
      turns: params.turns,
      isVisible: true,
      color: MotionColor.BLUE,
      propType: PropType.STAFF, // Default prop type
      arrowLocation: params.startLocation as GridLocation, // Will be calculated later
    });
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
  getIsPlaying(): boolean {
    return this.isPlaying;
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
