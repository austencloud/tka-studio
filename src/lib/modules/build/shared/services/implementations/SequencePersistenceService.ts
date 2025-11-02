/**
 * Sequence Persistence Service Implementation
 *
 * Manages sequence state persistence that survives hot module replacement.
 * Uses the shared persistence service to store and restore sequence state.
 */

import type { ActiveBuildTab, IPersistenceService, PictographData, SequenceData } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { ISequencePersistenceService } from "../contracts";

@injectable()
export class SequencePersistenceService implements ISequencePersistenceService {
  constructor(
    @inject(TYPES.IPersistenceService) private persistenceService: IPersistenceService
  ) {}

  async initialize(): Promise<void> {
    try {
      // Ensure the persistence service is initialized
      await this.persistenceService.initialize();
    } catch (error) {
      console.error("❌ SequencePersistenceService: Failed to initialize:", error);
      throw error;
    }
  }

  async saveCurrentState(state: {
    currentSequence: SequenceData | null;
    selectedStartPosition: PictographData | null;
    hasStartPosition: boolean;
    activeBuildSection: ActiveBuildTab;
  }): Promise<void> {
    try {
      await this.persistenceService.saveCurrentSequenceState(state);
    } catch (error) {
      console.error("❌ SequencePersistenceService: Failed to save current state:", error);
      throw error;
    }
  }

  async loadCurrentState(): Promise<{
    currentSequence: SequenceData | null;
    selectedStartPosition: PictographData | null;
    hasStartPosition: boolean;
    activeBuildSection: ActiveBuildTab;
  } | null> {
    try {
      const state = await this.persistenceService.loadCurrentSequenceState();
      if (state) {
        // Ensure backward compatibility - add default activeBuildSection if missing
        return {
          currentSequence: state.currentSequence,
          selectedStartPosition: state.selectedStartPosition,
          hasStartPosition: state.hasStartPosition,
          activeBuildSection: (state as any).activeBuildSection || "construct"
        };
      }
      return state;
    } catch (error) {
      console.error("❌ SequencePersistenceService: Failed to load current state:", error);
      return null;
    }
  }

  async clearCurrentState(): Promise<void> {
    try {
      await this.persistenceService.clearCurrentSequenceState();
    } catch (error) {
      console.error("❌ SequencePersistenceService: Failed to clear current state:", error);
      throw error;
    }
  }

  async hasSavedState(): Promise<boolean> {
    try {
      const state = await this.persistenceService.loadCurrentSequenceState();
      return state !== null;
    } catch (error) {
      console.error("❌ SequencePersistenceService: Failed to check for saved state:", error);
      return false;
    }
  }

  async getLastSaveTimestamp(): Promise<number | null> {
    try {
      const state = await this.persistenceService.loadCurrentSequenceState();
      if (state && 'timestamp' in state) {
        return (state as any).timestamp;
      }
      return null;
    } catch (error) {
      console.error("❌ SequencePersistenceService: Failed to get last save timestamp:", error);
      return null;
    }
  }
}
