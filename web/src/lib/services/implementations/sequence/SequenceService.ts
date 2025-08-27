/**
 * Sequence Service - Application Layer
 *
 * Coordinates between domain logic and persistence for sequence operations.
 * This service orchestrates the business workflows for sequence management.
 *
 * Focused on core CRUD operations and domain coordination.
 * Workbench-specific operations moved to WorkbenchBeatOperationsService.
 * Import operations moved to SequenceImportService.
 */

import { injectable, inject } from "inversify";
import { TYPES } from "../../inversify/types";
import type { BeatData, SequenceData } from "$lib/domain";
import type {
  IPersistenceService,
  ISequenceDomainService,
  ISequenceService,
  ISequenceImportService,
  SequenceCreateRequest,
} from "../../interfaces/sequence-interfaces";

@injectable()
export class SequenceService implements ISequenceService {
  constructor(
    @inject(TYPES.ISequenceDomainService)
    private sequenceDomainService: ISequenceDomainService,
    @inject(TYPES.IPersistenceService)
    private persistenceService: IPersistenceService,
    @inject(TYPES.ISequenceImportService)
    private sequenceImportService?: ISequenceImportService
  ) {}

  /**
   * Create a new sequence
   */
  async createSequence(request: SequenceCreateRequest): Promise<SequenceData> {
    try {
      // Use domain service to create the sequence
      const sequence = this.sequenceDomainService.createSequence(request);
      await this.persistenceService.saveSequence(sequence);
      return sequence;
    } catch (error) {
      console.error("Failed to create sequence:", error);
      throw new Error(
        `Failed to create sequence: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Update a beat in a sequence
   */
  async updateBeat(
    sequenceId: string,
    beatIndex: number,
    beatData: BeatData
  ): Promise<void> {
    try {
      // Load the current sequence
      const currentSequence =
        await this.persistenceService.loadSequence(sequenceId);
      if (!currentSequence) {
        throw new Error(`Sequence ${sequenceId} not found`);
      }

      // Use domain service to update the beat
      const updatedSequence = this.sequenceDomainService.updateBeat(
        currentSequence,
        beatIndex,
        beatData
      );

      await this.persistenceService.saveSequence(updatedSequence);
    } catch (error) {
      console.error("Failed to update beat:", error);
      throw new Error(
        `Failed to update beat: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  /**
   * Get a sequence by ID
   */
  async getSequence(id: string): Promise<SequenceData | null> {
    try {
      let sequence = await this.persistenceService.loadSequence(id);

      // If sequence not found, try to import from PNG metadata if import service is available
      if (!sequence && this.sequenceImportService) {
        console.log(
          `🎬 Sequence ${id} not found, attempting to import from PNG metadata`
        );
        try {
          sequence = await this.sequenceImportService.importFromPNG(id);
          // Save it to persistence for future use
          if (sequence) {
            await this.persistenceService.saveSequence(sequence);
          }
        } catch (error) {
          console.error(`Failed to import sequence ${id} from PNG:`, error);
          // Don't return null here - let the error bubble up so calling code knows why it failed
          return null;
        }
      }

      return sequence;
    } catch (error) {
      console.error(`Failed to get sequence ${id}:`, error);
      return null;
    }
  }

  /**
   * Get all sequences
   */
  async getAllSequences(): Promise<SequenceData[]> {
    try {
      return await this.persistenceService.loadAllSequences();
    } catch (error) {
      console.error("Failed to get all sequences:", error);
      return [];
    }
  }
}
