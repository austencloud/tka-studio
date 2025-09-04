/**
 * Sequence Animation Engine Interface
 *
 * Interface for the core animation engine that handles sequence playback.
 * Manages prop states and animation calculations.
 */

import type { SequenceData, SequenceMetadata } from "$shared/domain";
import type { PropState, PropStates } from "../../domain";

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
