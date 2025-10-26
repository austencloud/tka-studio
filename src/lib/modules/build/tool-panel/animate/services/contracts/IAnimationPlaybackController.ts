/**
 * Animation Playback Controller Interface
 *
 * High-level orchestration service that manages animation playback.
 * Coordinates the animation engine, loop service, and state updates.
 */

import type { SequenceData } from "$shared";
import type { PropState } from "../../domain";
import type { AnimationPanelState } from "../../state/animation-panel-state.svelte";

export interface IAnimationPlaybackController {
  /**
   * Initialize with sequence data and bind to state
   * @param sequenceData The sequence to animate
   * @param state The animation panel state to manage
   */
  initialize(sequenceData: SequenceData, state: AnimationPanelState): boolean;

  /**
   * Start or pause playback
   */
  togglePlayback(): void;

  /**
   * Stop playback and reset to start
   */
  stop(): void;

  /**
   * Jump to a specific beat
   * @param beat Beat number to jump to
   */
  jumpToBeat(beat: number): void;

  /**
   * Move to next beat
   */
  nextBeat(): void;

  /**
   * Move to previous beat
   */
  previousBeat(): void;

  /**
   * Update playback speed
   * @param speed New speed multiplier
   */
  setSpeed(speed: number): void;

  /**
   * Get current prop states from engine
   */
  getCurrentPropStates(): { blue: PropState; red: PropState };

  /**
   * Clean up resources
   */
  dispose(): void;
}
