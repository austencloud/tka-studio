/**
 * Sequence Animation Orchestrator
 *
 * Lightweight coordinator that orchestrates focused services.
 * Single responsibility: Coordinate animation services and manage sequence lifecycle.
 */

import type {
    BeatData,
    PropState,
    PropStates,
    SequenceData,
    SequenceMetadata,
} from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type {
    IAnimationStateManager,
    IBeatCalculator,
    IPropInterpolator,
    ISequenceAnimationOrchestrator,
} from "../contracts";

/**
 * Lightweight Animation Orchestrator
 * Coordinates focused services instead of doing everything itself
 */
@injectable()
export class SequenceAnimationOrchestrator
  implements ISequenceAnimationOrchestrator
{
  private beats: readonly BeatData[] = [];
  private totalBeats = 0;
  private metadata: SequenceMetadata = { word: "", author: "", totalBeats: 0 };
  private initialized = false;
  private currentBeatIndex = 0;

  constructor(
    @inject(TYPES.IAnimationStateService)
    private readonly animationStateService: IAnimationStateManager,
    @inject(TYPES.IBeatCalculationService)
    private readonly beatCalculationService: IBeatCalculator,
    @inject(TYPES.IPropInterpolationService)
    private readonly propInterpolationService: IPropInterpolator
  ) {}

  /**
   * Initialize with domain sequence data (PURE DOMAIN!)
   */
  initializeWithDomainData(sequenceData: SequenceData): boolean {
    try {
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

      this.initializePropStates();
      this.initialized = true;
      return true;
    } catch (error) {
      console.error(
        "SequenceAnimationOrchestrator: Failed to initialize:",
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

    // Store current beat index for letter retrieval
    this.currentBeatIndex = beatState.currentBeatIndex;

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

    // Use focused service to update prop states
    this.animationStateService.updatePropStates(interpolationResult);
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
    if (!this.beats || this.beats.length === 0) {
      console.warn(
        "SequenceAnimationOrchestrator: No beats available, using fallback"
      );
      this.animationStateService.resetPropStates();
      return;
    }

    // Use first beat for initial state
    const firstBeat = this.beats[0];
    const initialAngles =
      this.propInterpolationService.calculateInitialAngles(firstBeat);

    if (initialAngles.isValid) {
      this.animationStateService.setPropStates(
        {
          centerPathAngle: initialAngles.blueAngles.centerPathAngle,
          staffRotationAngle: initialAngles.blueAngles.staffRotationAngle,
          // x,y are optional - only set for dash motions
        },
        {
          centerPathAngle: initialAngles.redAngles.centerPathAngle,
          staffRotationAngle: initialAngles.redAngles.staffRotationAngle,
          // x,y are optional - only set for dash motions
        }
      );
    } else {
      console.warn(
        "SequenceAnimationOrchestrator: Failed to calculate initial angles"
      );
      this.animationStateService.resetPropStates();
    }
  }

  /**
   * Get current prop states
   */
  getCurrentPropStates(): PropStates {
    return this.animationStateService.getPropStates();
  }

  /**
   * Get the letter for the current beat
   */
  getCurrentLetter(): import("$shared").Letter | null {
    if (!this.initialized || this.beats.length === 0) {
      return null;
    }

    // Clamp beat index to valid range
    const beatIndex = Math.max(0, Math.min(this.currentBeatIndex, this.beats.length - 1));
    const currentBeat = this.beats[beatIndex];

    return currentBeat?.letter || null;
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
    this.currentBeatIndex = 0;
    this.animationStateService.resetPropStates();
  }
}
