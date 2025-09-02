/**
 * Workbench Coordination Service Implementation
 *
 * Coordinates interactions between different services for workbench operations.
 * This service orchestrates calls to other services but contains no reactive state.
 */

import type {
  IWorkbenchCoordinationService,
  IWorkbenchService,
} from "$contracts";
import type {
  BeatClickResult,
  BeatEditResult,
  ConfigurationResult,
  SequenceCreationResult,
  SequenceData,
  WorkbenchMode,
} from "$domain";
import { GridMode } from "$domain";
import { TYPES } from "$lib/services/inversify/types";
import { inject, injectable } from "inversify";

@injectable()
export class WorkbenchCoordinationService
  implements IWorkbenchCoordinationService
{
  constructor(
    @inject(TYPES.IWorkbenchService) private workbenchService: IWorkbenchService
  ) {}

  // ============================================================================
  // SERVICE COORDINATION
  // ============================================================================

  handleBeatClick(beatIndex: number, mode: WorkbenchMode): BeatClickResult {
    const shouldSelect = this.workbenchService.shouldSelectBeatOnClick(
      mode,
      beatIndex
    );

    return {
      shouldSelect,
      beatIndex,
    };
  }

  handleBeatHover(_beatIndex: number): void {
    // This will be handled by the beat frame service through the state layer
    // No business logic needed here - just a pass-through
  }

  handleBeatLeave(): void {
    // This will be handled by the beat frame service through the state layer
    // No business logic needed here - just a pass-through
  }

  // ============================================================================
  // BEAT OPERATIONS COORDINATION
  // ============================================================================

  editBeat(
    beatIndex: number,
    sequence: SequenceData | null,
    mode: WorkbenchMode
  ): BeatEditResult {
    if (!this.workbenchService.canEditBeat(sequence, beatIndex, mode)) {
      return {
        success: false,
        error: "Cannot edit beat: invalid index, mode, or sequence",
      };
    }

    if (!sequence) {
      return {
        success: false,
        error: "Cannot edit beat: sequence is null",
      };
    }

    const beat = sequence.beats[beatIndex];
    // TODO: Implement these methods in IWorkbenchService
    // const editAction = this.workbenchService.getBeatEditAction(beat);
    // const updatedBeat = this.workbenchService.applyBeatEditAction(beat, editAction);
    const updatedBeat = beat; // Placeholder

    return {
      success: true,
      updatedBeat,
    };
  }

  clearBeat(beatIndex: number, sequence: SequenceData | null): BeatEditResult {
    if (!this.workbenchService.canClearBeat(sequence, beatIndex)) {
      return {
        success: false,
        error: "Cannot clear beat: invalid index or beat is already blank",
      };
    }

    if (!sequence) {
      return { success: false, error: "No sequence available" };
    }

    const beat = sequence.beats[beatIndex];
    const clearedBeat = this.workbenchService.createClearedBeatData(beat);

    return {
      success: true,
      updatedBeat: clearedBeat,
    };
  }

  // ============================================================================
  // SEQUENCE OPERATIONS COORDINATION
  // ============================================================================

  createNewSequence(name?: string, length?: number): SequenceCreationResult {
    const params = this.workbenchService.createSequenceCreationParams(
      name,
      length
    );
    const validation = this.workbenchService.validateSequenceCreation(
      params.name,
      params.length
    );

    if (!validation.isValid) {
      return {
        success: false,
        error: validation.errors.join(", "),
      };
    }

    // The actual sequence creation will be handled by the sequence state service
    // This service just validates and prepares the parameters
    return {
      success: true,
    };
  }

  // ============================================================================
  // CONFIGURATION COORDINATION
  // ============================================================================

  setGridMode(mode: GridMode): ConfigurationResult {
    // Validation logic - the actual setting will be handled by beat frame service
    if (!Object.values(GridMode).includes(mode)) {
      return {
        success: false,
        error: `Invalid grid mode: ${mode}`,
      };
    }

    return {
      success: true,
    };
  }

  setBeatSize(size: number): ConfigurationResult {
    if (!this.workbenchService.validateBeatSizeChange(0, size)) {
      return {
        success: false,
        error: `Invalid beat size: ${size}. Must be between 50 and 300.`,
      };
    }

    return {
      success: true,
    };
  }
}
