/**
 * Workbench Beat Operations Service
 *
 * Handles beat manipulation operations specific to the workbench/construction interface.
 * These operations are UI-driven and separate from core sequence CRUD operations.
 */

import type { BeatData, SequenceData } from "$domain";
import type {
  IPersistenceService,
  ISequenceService,
} from "$lib/services/contracts/sequence-interfaces";
import { inject, injectable } from "inversify";
import { TYPES } from "../../inversify/types";

export interface IWorkbenchBeatOperationsService {
  addBeat(
    sequenceId: string,
    beatData?: Partial<BeatData>
  ): Promise<SequenceData>;
  setConstructionStartPosition(
    sequenceId: string,
    startPosition: BeatData
  ): Promise<SequenceData>;
}

@injectable()
export class WorkbenchBeatOperationsService
  implements IWorkbenchBeatOperationsService
{
  constructor(
    @inject(TYPES.ISequenceService)
    private readonly sequenceService: ISequenceService,

    @inject(TYPES.IPersistenceService)
    private readonly persistenceService: IPersistenceService
  ) {}

  /**
   * Add a beat to a sequence and return the updated sequence
   */
  async addBeat(
    sequenceId: string,
    beatData?: Partial<BeatData>
  ): Promise<SequenceData> {
    try {
      const sequence = await this.sequenceService.getSequence(sequenceId);
      if (!sequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }

      // Create new beat with next beat number
      const nextBeatNumber = sequence.beats.length + 1;
      const newBeat: BeatData = {
        id: crypto.randomUUID(),
        beatNumber: nextBeatNumber,
        duration: 1.0,
        blueReversal: false,
        redReversal: false,
        isBlank: true,
        pictographData: null,
        ...beatData,
      };

      const updatedSequence = {
        ...sequence,
        beats: [...sequence.beats, newBeat],
      } as SequenceData;

      await this.persistenceService.saveSequence(updatedSequence);
      return updatedSequence;
    } catch (error) {
      console.error("Failed to add beat:", error);
      throw new Error(
        `Failed to add beat: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Set the start position for sequence construction
   */
  async setConstructionStartPosition(
    sequenceId: string,
    startPosition: BeatData
  ): Promise<SequenceData> {
    try {
      const sequence = await this.sequenceService.getSequence(sequenceId);
      if (!sequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }

      const updatedSequence = {
        ...sequence,
        startPosition: startPosition,
      } as SequenceData;

      await this.persistenceService.saveSequence(updatedSequence);
      return updatedSequence;
    } catch (error) {
      console.error("Failed to set construction start position:", error);
      throw new Error(
        `Failed to set start position: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }
}
