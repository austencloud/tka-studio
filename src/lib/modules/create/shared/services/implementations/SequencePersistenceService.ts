/**
 * Sequence Persistence Service Implementation
 *
 * Manages sequence state persistence that survives hot module replacement.
 * Uses the shared persistence service to store and restore sequence state.
 *
 * Each creation mode (Constructor, Generator, Assembler) has its own workspace
 * with independent localStorage persistence.
 */

import type { IPersistenceService } from "$shared";
import type { ActiveCreateModule, PictographData, SequenceData } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { ISequencePersistenceService } from "../contracts";

@injectable()
export class SequencePersistenceService implements ISequencePersistenceService {
  constructor(
    @inject(TYPES.IPersistenceService)
    private persistenceService: IPersistenceService
  ) {}

  /**
   * Get the current active mode from navigation state
   * Dynamically imported to avoid circular dependencies
   */
  private async getCurrentMode(): Promise<string> {
    try {
      const { navigationState } = await import("$shared");
      return navigationState.activeTab || "constructor";
    } catch (error) {
      console.warn(
        "⚠️ Failed to get current mode, defaulting to constructor:",
        error
      );
      return "constructor";
    }
  }

  async initialize(): Promise<void> {
    try {
      // Ensure the persistence service is initialized
      await this.persistenceService.initialize();
    } catch (error) {
      console.error(
        "❌ SequencePersistenceService: Failed to initialize:",
        error
      );
      throw error;
    }
  }

  async saveCurrentState(state: {
    currentSequence: SequenceData | null;
    selectedStartPosition: PictographData | null;
    hasStartPosition: boolean;
    activeBuildSection: ActiveCreateModule;
  }): Promise<void> {
    try {
      await this.persistenceService.saveCurrentSequenceState(state);
    } catch (error) {
      console.error(
        "❌ SequencePersistenceService: Failed to save current state:",
        error
      );
      throw error;
    }
  }

  async loadCurrentState(mode?: string): Promise<{
    currentSequence: SequenceData | null;
    selectedStartPosition: PictographData | null;
    hasStartPosition: boolean;
    activeBuildSection: ActiveCreateModule;
  } | null> {
    try {
      // Get current mode if not provided
      const targetMode = mode || (await this.getCurrentMode());

      const state =
        await this.persistenceService.loadCurrentSequenceState(targetMode);
      if (state) {
        // Ensure backward compatibility - add default activeBuildSection if missing
        return {
          currentSequence: state.currentSequence,
          selectedStartPosition: state.selectedStartPosition,
          hasStartPosition: state.hasStartPosition,
          activeBuildSection:
            (state as any).activeBuildSection ||
            (targetMode as ActiveCreateModule),
        };
      }
      return state;
    } catch (error) {
      console.error(
        "❌ SequencePersistenceService: Failed to load current state:",
        error
      );
      return null;
    }
  }

  async clearCurrentState(mode?: string): Promise<void> {
    try {
      await this.persistenceService.clearCurrentSequenceState(mode);
    } catch (error) {
      console.error(
        "❌ SequencePersistenceService: Failed to clear current state:",
        error
      );
      throw error;
    }
  }

  async hasSavedState(mode?: string): Promise<boolean> {
    try {
      const targetMode = mode || (await this.getCurrentMode());
      const state =
        await this.persistenceService.loadCurrentSequenceState(targetMode);
      return state !== null;
    } catch (error) {
      console.error(
        "❌ SequencePersistenceService: Failed to check for saved state:",
        error
      );
      return false;
    }
  }

  async getLastSaveTimestamp(mode?: string): Promise<number | null> {
    try {
      const targetMode = mode || (await this.getCurrentMode());
      const state =
        await this.persistenceService.loadCurrentSequenceState(targetMode);
      if (state && "timestamp" in state) {
        return (state as any).timestamp;
      }
      return null;
    } catch (error) {
      console.error(
        "❌ SequencePersistenceService: Failed to get last save timestamp:",
        error
      );
      return null;
    }
  }
}
