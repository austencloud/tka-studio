/**
 * Service for sorting and grouping gallery sequences
 */

import type { SequenceData } from "$shared";
import { ExploreSortMethod } from "../../../shared/domain/enums";

export interface IExploreSortService {
  /**
   * Sort sequences by the specified method
   */
  sortSequences(
    sequences: SequenceData[],
    sortMethod: ExploreSortMethod
  ): SequenceData[];

  /**
   * Group sequences into sections based on sort method
   */
  groupSequencesIntoSections(
    sequences: SequenceData[],
    sortMethod: ExploreSortMethod
  ): Record<string, SequenceData[]>;
}
