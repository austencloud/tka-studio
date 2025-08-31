/**
 * Sequence Animation Engine Interface
 *
 * Interface for the core animation engine that handles sequence playback.
 * Manages prop states and animation calculations.
 */

import type { SequenceData } from "$domain";
import type { PropState } from "$lib/components/tabs/browse-tab/animator/types/PropState";

export interface ISequenceAnimationEngine {
  initializeWithDomainData(sequenceData: SequenceData): boolean;
  calculateState(currentBeat: number): void;
  getCurrentPropStates(): PropStates;
  getBluePropState(): PropState;
  getRedPropState(): PropState;
  getMetadata(): SequenceMetadata;
  isInitialized(): boolean;
  dispose(): void;
  reset(): void;
}

// Supporting types
export interface SequenceMetadata {
  word: string;
  author: string;
  totalBeats: number;
}

export interface PropStates {
  blue: PropState;
  red: PropState;
}
