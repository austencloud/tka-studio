/**
 * Sequence Animation Orchestrator Interface
 *
 * Interface for coordinating multiple animation services.
 * Higher-level orchestration of animation components.
 */

import type { Letter, SequenceData, SequenceMetadata } from "$shared";
import type { PropState, PropStates } from "../../domain";

export interface ISequenceAnimationOrchestrator {
  initializeWithDomainData(sequenceData: SequenceData): boolean;
  calculateState(currentBeat: number): void;
  getPropStates(): PropStates;
  getBluePropState(): PropState;
  getRedPropState(): PropState;
  getMetadata(): SequenceMetadata;
  getCurrentPropStates(): PropStates;
  getCurrentLetter(): Letter | null;
  isInitialized(): boolean;
  dispose(): void;
}
