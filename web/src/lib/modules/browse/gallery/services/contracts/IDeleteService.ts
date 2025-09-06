import type { SequenceData } from "$shared/domain";
import type {
  DeleteConfirmationData,
  DeleteResult,
} from "../../../../build/workbench";

/**
 * Service for managing sequence deletion operations
 */
export interface IDeleteService {
  prepareDeleteConfirmation(
    sequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<DeleteConfirmationData>;
  deleteSequence(
    sequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<DeleteResult>;
  fixVariationNumbers(
    deletedSequence: SequenceData,
    allSequences: SequenceData[]
  ): Promise<SequenceData[]>;
}
