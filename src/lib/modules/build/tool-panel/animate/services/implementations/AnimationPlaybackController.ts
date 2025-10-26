/**
 * Animation Playback Controller Implementation
 *
 * Orchestrates animation playback by coordinating:
 * - Animation engine (state calculations)
 * - Loop service (timing and frames)
 * - Panel state (UI updates)
 */

import { inject, injectable } from "inversify";
import type { SequenceData } from "../../../../../shared";
import { TYPES } from "$shared/inversify/types";
import type { PropState } from "../../domain";
import type { AnimationPanelState } from "../../state/animation-panel-state.svelte";
import type { IAnimationLoopService } from "../contracts/IAnimationLoopService";
import type { IAnimationPlaybackController } from "../contracts/IAnimationPlaybackController";
import type { ISequenceAnimationOrchestrator } from "../contracts/ISequenceAnimationOrchestrator";

@injectable()
export class AnimationPlaybackController implements IAnimationPlaybackController {
  private state: AnimationPanelState | null = null;
  private sequenceData: SequenceData | null = null;

  constructor(
    @inject(TYPES.ISequenceAnimationOrchestrator)
    private readonly animationEngine: ISequenceAnimationOrchestrator,
    @inject(TYPES.IAnimationLoopService)
    private readonly loopService: IAnimationLoopService
  ) {}

  initialize(sequenceData: SequenceData, state: AnimationPanelState): boolean {
    this.state = state;
    this.sequenceData = sequenceData;

    // Initialize animation engine with sequence data
    const success = this.animationEngine.initializeWithDomainData(sequenceData);
    if (!success) {
      return false;
    }

    // Get metadata from engine
    const metadata = this.animationEngine.getMetadata();
    state.setTotalBeats(metadata.totalBeats);
    state.setSequenceMetadata(metadata.word, metadata.author);

    // Reset playback state
    state.setCurrentBeat(0);
    state.setIsPlaying(false);

    // Update prop states
    this.updatePropStatesFromEngine();

    return true;
  }

  togglePlayback(): void {
    if (!this.state) return;

    if (this.state.isPlaying) {
      // Pause
      this.loopService.stop();
      this.state.setIsPlaying(false);
    } else {
      // Play
      this.state.setIsPlaying(true);
      this.loopService.start(
        (deltaTime) => this.onAnimationUpdate(deltaTime),
        this.state.speed
      );
    }
  }

  stop(): void {
    if (!this.state) return;

    // Stop animation loop
    this.loopService.stop();
    this.state.setIsPlaying(false);

    // Reset to start
    this.state.setCurrentBeat(0);

    // Re-initialize engine if we have sequence data
    if (this.sequenceData) {
      this.animationEngine.initializeWithDomainData(this.sequenceData);
    }

    // Update prop states
    this.updatePropStatesFromEngine();
  }

  jumpToBeat(beat: number): void {
    if (!this.state) return;

    // Stop any current playback
    this.loopService.stop();
    this.state.setIsPlaying(false);

    // Clamp beat to valid range
    const clampedBeat = Math.max(0, Math.min(beat, this.state.totalBeats));
    this.state.setCurrentBeat(clampedBeat);

    // Calculate state for this beat
    this.animationEngine.calculateState(clampedBeat);
    this.updatePropStatesFromEngine();
  }

  nextBeat(): void {
    if (!this.state) return;

    const nextBeat = this.state.currentBeat + 1;
    if (nextBeat < this.state.totalBeats) {
      this.jumpToBeat(nextBeat);
    }
  }

  previousBeat(): void {
    if (!this.state) return;

    const prevBeat = this.state.currentBeat - 1;
    if (prevBeat >= 0) {
      this.jumpToBeat(prevBeat);
    }
  }

  setSpeed(speed: number): void {
    if (!this.state) return;

    this.state.setSpeed(speed);

    // Update loop service if currently playing
    if (this.state.isPlaying) {
      this.loopService.setSpeed(speed);
    }
  }

  getCurrentPropStates(): { blue: PropState; red: PropState } {
    return this.animationEngine.getCurrentPropStates();
  }

  dispose(): void {
    this.loopService.stop();
    this.state = null;
    this.sequenceData = null;
  }

  private onAnimationUpdate(deltaTime: number): void {
    if (!this.state) return;

    // Calculate beat delta based on deltaTime (milliseconds)
    // NOTE: deltaTime is already adjusted by speed in AnimationLoopService
    // Assuming 60 BPM as default (1 beat per second)
    const DEFAULT_BPM = 60;
    const beatsPerSecond = DEFAULT_BPM / 60; // = 1.0
    const beatDelta = (deltaTime / 1000) * beatsPerSecond;
    const newBeat = this.state.currentBeat + beatDelta;

    // Debug logging to verify file is loaded
    if (this.state.currentBeat >= 4 && this.state.currentBeat < 5) {
      console.log(`🔧 FIXED VERSION: deltaTime=${deltaTime.toFixed(2)}ms, beatDelta=${beatDelta.toFixed(6)}, currentBeat=${this.state.currentBeat.toFixed(6)}`);
    }

    // Check if we've reached the end (add 1 beat buffer after last beat)
    const animationEndBeat = this.state.totalBeats + 1;

    if (newBeat > animationEndBeat) {
      if (this.state.shouldLoop) {
        // Loop back to start
        this.state.setCurrentBeat(0);

        // Re-initialize engine if needed
        if (this.sequenceData) {
          this.animationEngine.initializeWithDomainData(this.sequenceData);
        }
      } else {
        // Stop at end
        this.state.setCurrentBeat(this.state.totalBeats);
        this.loopService.stop();
        this.state.setIsPlaying(false);
      }
    } else {
      this.state.setCurrentBeat(newBeat);
    }

    // Calculate state for current beat
    this.animationEngine.calculateState(this.state.currentBeat);

    // Update prop states
    this.updatePropStatesFromEngine();
  }

  private updatePropStatesFromEngine(): void {
    if (!this.state) return;

    const states = this.animationEngine.getCurrentPropStates();

    this.state.setPropStates(states.blue, states.red);
  }
}
