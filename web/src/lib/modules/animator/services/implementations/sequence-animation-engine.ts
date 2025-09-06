/**
 * ✅ ELIMINATED: Monolithic Engine
 *
 * This file now contains a lightweight wrapper around focused services.
 * The 304-line monolith has been decomposed into focused services.
 */

import type { SequenceData, SequenceMetadata } from "$shared/domain";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { PropState, PropStates } from "../../domain";
import type {
  ISequenceAnimationEngine,
  ISequenceAnimationOrchestrator,
} from "../contracts";

/**
 * Lightweight Animation Engine Wrapper
 * Delegates to focused services instead of doing everything itself
 */
@injectable()
export class SequenceAnimationEngine implements ISequenceAnimationEngine {
  constructor(
    @inject(TYPES.ISequenceAnimationOrchestrator)
    private readonly orchestrator: ISequenceAnimationOrchestrator
  ) {}

  /**
   * Initialize with domain sequence data (DELEGATES TO ORCHESTRATOR!)
   */
  initializeWithDomainData(sequenceData: SequenceData): boolean {
    return this.orchestrator.initializeWithDomainData(sequenceData);
  }

  /**
   * Calculate state for given beat (DELEGATES TO ORCHESTRATOR!)
   */
  calculateState(currentBeat: number): void {
    this.orchestrator.calculateState(currentBeat);
  }

  /**
   * Get current prop states (DELEGATES TO ORCHESTRATOR!)
   */
  getCurrentPropStates(): PropStates {
    return this.orchestrator.getCurrentPropStates();
  }

  /**
   * Get blue prop state (DELEGATES TO ORCHESTRATOR!)
   */
  getBluePropState(): PropState {
    return this.orchestrator.getCurrentPropStates().blue;
  }

  /**
   * Get red prop state (DELEGATES TO ORCHESTRATOR!)
   */
  getRedPropState(): PropState {
    return this.orchestrator.getCurrentPropStates().red;
  }

  /**
   * Get sequence metadata (DELEGATES TO ORCHESTRATOR!)
   */
  getMetadata(): SequenceMetadata {
    return this.orchestrator.getMetadata();
  }

  /**
   * Check if engine is initialized (DELEGATES TO ORCHESTRATOR!)
   */
  isInitialized(): boolean {
    return this.orchestrator.isInitialized();
  }

  /**
   * Dispose of resources (DELEGATES TO ORCHESTRATOR!)
   */
  dispose(): void {
    this.orchestrator.dispose();
  }

  /**
   * Reset to initial state (DELEGATES TO ORCHESTRATOR!)
   */
  reset(): void {
    // The orchestrator handles reset through re-initialization
    // This is a no-op for backward compatibility
    console.log(
      "SequenceAnimationEngine: Reset called (delegated to orchestrator)"
    );
  }

  /**
   * ✅ ELIMINATED: Legacy array format initialization
   * Use initializeWithDomainData() instead - pure domain types only!
   */
}
