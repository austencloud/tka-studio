import type {
  DeleteConfirmationData,
  DeleteResult,
  SequenceData,
} from "../../../../../shared";

export interface IExploreDeleteService {
  /** Prepare deletion data for confirmation dialog */
  prepareDeleteConfirmation(
    sequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<DeleteConfirmationData>;

  /** Delete sequence and handle cleanup */
  deleteSequence(
    sequenceId: string,
    allSequences: SequenceData[]
  ): Promise<DeleteResult>;

  /** Fix variation numbers after deletion */
  fixVariationNumbers(
    deletedSequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<SequenceData[]>;

  /** Check if sequence can be safely deleted */
  canDeleteSequence(
    sequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<boolean>;

  /** Get sequences that would be affected by deletion */
  getAffectedSequences(
    sequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<SequenceData[]>;
}
