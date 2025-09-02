/**
 * Sequence Animation Orchestrator Interface
 *
 * Interface for coordinating multiple animation services.
 * Higher-level orchestration of animation components.
 */

import type { SequenceData } from "$domain";
import type { PropState } from "$lib/components/tabs/browse-tab/animator/types/PropState";
import type { PropStates, SequenceMetadata } from "./ISequenceAnimationEngine";

export interface ISequenceAnimationOrchestrator {
  initializeWithDomainData(sequenceData: SequenceData): boolean;
  calculateState(currentBeat: number): void;
  getPropStates(): PropStates;
  getBluePropState(): PropState;
  getRedPropState(): PropState;
  getMetadata(): SequenceMetadata;
  getCurrentPropStates(): PropStates;
  isInitialized(): boolean;
  dispose(): void;
}
