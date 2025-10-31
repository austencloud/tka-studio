/**
 * Service for filtering gallery sequences
 */

import type { SequenceData } from "$shared";
import type { ExploreFilterValue } from "../../../../../shared/persistence/domain";
import { ExploreFilterType } from "../../../../../shared/persistence/domain";

export interface IExploreFilterService {
  /**
   * Apply a filter to a list of sequences
   */
  applyFilter(
    sequences: SequenceData[],
    filterType: ExploreFilterType,
    filterValue: ExploreFilterValue
  ): SequenceData[];

  /**
   * Get available filter options for a given filter type
   */
  getFilterOptions(
    filterType: ExploreFilterType,
    sequences: SequenceData[]
  ): string[];
}
