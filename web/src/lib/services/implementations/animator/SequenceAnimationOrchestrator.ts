/**
 * Sequence Animation Orchestrator
 *
 * Lightweight coordinator that orchestrates focused services.
 * Single responsibility: Coordinate animation services and manage sequence lifecycle.
 */

import type {
  IAnimationStateService,
  IBeatCalculationService,
  IPropInterpolationService,
  ISequenceAnimationOrchestrator,
  PropStates,
  SequenceMetadata,
} from "$contracts";
import type { BeatData, SequenceData } from "$domain";
import type { PropState } from "$lib/domain/animator/types/PropState.js";
import { TYPES } from "$lib/services/inversify/types";
import { inject, injectable } from "inversify";

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

  constructor(
    @inject(TYPES.IAnimationStateService)
    private readonly animationStateService: IAnimationStateService,
    @inject(TYPES.IBeatCalculationService)
    private readonly beatCalculationService: IBeatCalculationService,
    @inject(TYPES.IPropInterpolationService)
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

    // Debug logging removed for cleaner console output

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

    // Motion debug logs removed for cleaner output

    // Use focused service to update prop states
    // Final state debug logs removed
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
    // Initializing prop states
    if (!this.beats || this.beats.length === 0) {
      console.warn(
        "SequenceAnimationOrchestrator: No beats available, using fallback initialization"
      );
      this.animationStateService.resetPropStates();
    } else {
      // Use first beat for initial state (PURE DOMAIN!)
      const firstBeat = this.beats[0];
      // First beat data processed

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

    // Initial states calculated and applied
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
