/**
 * Sequence Animation Orchestrator
 *
 * Lightweight coordinator that orchestrates focused services.
 * Single responsibility: Coordinate animation services and manage sequence lifecycle.
 */

import type { SequenceData, BeatData } from "$lib/domain";
import type { PropState } from "../../../components/animator/types/PropState.js";
import type {
  ISequenceAnimationOrchestrator,
  IAnimationStateService,
  IBeatCalculationService,
  IPropInterpolationService,
  SequenceMetadata,
  PropStates,
} from "$lib/services/di/interfaces/animator-interfaces";

/**
 * Lightweight Animation Orchestrator
 * Coordinates focused services instead of doing everything itself
 */
export class SequenceAnimationOrchestrator
  implements ISequenceAnimationOrchestrator
{
  private beats: readonly BeatData[] = [];
  private totalBeats = 0;
  private metadata: SequenceMetadata = { word: "", author: "", totalBeats: 0 };
  private initialized = false;

  constructor(
    private readonly animationStateService: IAnimationStateService,
    private readonly beatCalculationService: IBeatCalculationService,
    private readonly propInterpolationService: IPropInterpolationService
  ) {}

  /**
   * Initialize with domain sequence data (PURE DOMAIN!)
   */
  initializeWithDomainData(sequenceData: SequenceData): boolean {
    try {
      console.log(
        "SequenceAnimationOrchestrator: Initializing with domain data:",
        sequenceData
      );

      if (!sequenceData.beats || sequenceData.beats.length === 0) {
        throw new Error("No beats found in sequence data");
      }

      // Validate beats using focused service
      if (!this.beatCalculationService.validateBeats(sequenceData.beats)) {
        throw new Error("Invalid beat data structure");
      }

      // Extract metadata from domain data
      this.metadata = {
        word: sequenceData.word || sequenceData.name || "",
        author: (sequenceData.metadata?.author as string) || "",
        totalBeats: sequenceData.beats.length,
      };

      // Store domain beats directly - NO CONVERSION!
      this.beats = sequenceData.beats;
      this.totalBeats = this.metadata.totalBeats;

      console.log(
        "SequenceAnimationOrchestrator: Stored beats directly:",
        this.beats.length
      );
      console.log(
        "SequenceAnimationOrchestrator: Total beats:",
        this.totalBeats
      );

      this.initializePropStates();
      this.initialized = true;
      return true;
    } catch (error) {
      console.error(
        "SequenceAnimationOrchestrator: Failed to initialize with domain data:",
        error
      );
      return false;
    }
  }

  /**
   * Calculate animation state for given beat using focused services
   */
  calculateState(currentBeat: number): void {
    if (this.beats.length === 0 || this.totalBeats === 0) {
      console.warn("SequenceAnimationOrchestrator: No sequence data available");
      return;
    }

    // Use focused service for beat calculations
    const beatState = this.beatCalculationService.calculateBeatState(
      currentBeat,
      this.beats,
      this.totalBeats
    );

    if (!beatState.isValid) {
      console.error("SequenceAnimationOrchestrator: Invalid beat state");
      return;
    }

    console.log(
      "🔧 [MOTION DEBUG] ===== CALCULATING STATE FOR BEAT",
      currentBeat,
      "====="
    );
    console.log(
      "🔧 [MOTION DEBUG] Current beat data:",
      JSON.stringify(beatState.currentBeatData, null, 2)
    );

    // Use focused service for interpolation
    const interpolationResult =
      this.propInterpolationService.interpolatePropAngles(
        beatState.currentBeatData,
        beatState.beatProgress
      );

    if (!interpolationResult.isValid) {
      console.error(
        "SequenceAnimationOrchestrator: Invalid interpolation result"
      );
      return;
    }

    const motionData = this.propInterpolationService.getMotionData(
      beatState.currentBeatData
    );
    const endpoints = this.propInterpolationService.getEndpoints(
      beatState.currentBeatData
    );

    console.log("🔧 [MOTION DEBUG] Blue motion:", motionData.blue);
    console.log("🔧 [MOTION DEBUG] Red motion:", motionData.red);
    console.log("🔧 [MOTION DEBUG] Blue endpoints:", endpoints.blue);
    console.log("🔧 [MOTION DEBUG] Red endpoints:", endpoints.red);
    console.log(
      "🔧 [MOTION DEBUG] Interpolation factor t:",
      beatState.beatProgress
    );

    // Use focused service to update prop states
    const finalStates =
      this.animationStateService.updatePropStates(interpolationResult);
    console.log("🔧 [MOTION DEBUG] Final state after coordinate update:");
    console.log("🔧 [MOTION DEBUG] Blue final:", finalStates.blue);
    console.log("🔧 [MOTION DEBUG] Red final:", finalStates.red);
  }

  /**
   * Get current prop states
   */
  getPropStates(): PropStates {
    return this.animationStateService.getPropStates();
  }

  /**
   * Get blue prop state
   */
  getBluePropState(): PropState {
    return this.animationStateService.getBluePropState();
  }

  /**
   * Get red prop state
   */
  getRedPropState(): PropState {
    return this.animationStateService.getRedPropState();
  }

  /**
   * Get sequence metadata
   */
  getMetadata(): SequenceMetadata {
    return { ...this.metadata };
  }

  /**
   * Initialize prop states using focused services
   */
  private initializePropStates(): void {
    console.log(
      "🔧 [MOTION DEBUG] SequenceAnimationOrchestrator: Initializing prop states"
    );
    console.log("🔧 [MOTION DEBUG] Beats length:", this.beats.length);

    if (!this.beats || this.beats.length === 0) {
      console.warn(
        "🔧 [MOTION DEBUG] No beats available, using fallback initialization"
      );
      this.animationStateService.resetPropStates();
    } else {
      // Use first beat for initial state (PURE DOMAIN!)
      const firstBeat = this.beats[0];
      console.log(
        "🔧 [MOTION DEBUG] First beat data:",
        JSON.stringify(firstBeat, null, 2)
      );

      // Use focused service for initial angle calculation
      const initialAngles =
        this.propInterpolationService.calculateInitialAngles(firstBeat);

      if (initialAngles.isValid) {
        this.animationStateService.setPropStates(
          {
            centerPathAngle: initialAngles.blueAngles.centerPathAngle,
            staffRotationAngle: initialAngles.blueAngles.staffRotationAngle,
            x: 0, // Will be calculated by AnimationStateService
            y: 0, // Will be calculated by AnimationStateService
          },
          {
            centerPathAngle: initialAngles.redAngles.centerPathAngle,
            staffRotationAngle: initialAngles.redAngles.staffRotationAngle,
            x: 0, // Will be calculated by AnimationStateService
            y: 0, // Will be calculated by AnimationStateService
          }
        );
      } else {
        console.warn(
          "🔧 [MOTION DEBUG] Failed to calculate initial angles, using fallback"
        );
        this.animationStateService.resetPropStates();
      }
    }

    const initialStates = this.animationStateService.getPropStates();
    console.log("🔧 [MOTION DEBUG] Initial blue state:", initialStates.blue);
    console.log("🔧 [MOTION DEBUG] Initial red state:", initialStates.red);
  }

  /**
   * Get current prop states
   */
  getCurrentPropStates(): PropStates {
    return this.animationStateService.getPropStates();
  }

  /**
   * Check if orchestrator is initialized
   */
  isInitialized(): boolean {
    return this.initialized;
  }

  /**
   * Dispose of resources and reset state
   */
  dispose(): void {
    this.beats = [];
    this.totalBeats = 0;
    this.metadata = { word: "", author: "", totalBeats: 0 };
    this.initialized = false;
    this.animationStateService.resetPropStates();
  }
}
