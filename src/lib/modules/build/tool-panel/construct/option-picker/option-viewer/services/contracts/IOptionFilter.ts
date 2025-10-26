/**
 * Filter Service Contract
 *
 * Handles filtering of pictograph options by type, end position, and reversals.
 * Extracted from OptionPickerService for better separation of concerns.
 */

import type { PictographData } from "$shared";
import type { EndPositionFilter, ReversalFilter, TypeFilter } from "../../domain";



export interface IOptionFilter {
  /**
   * Apply type filtering to options
   */
  applyTypeFiltering(options: PictographData[], typeFilter: TypeFilter): PictographData[];

  /**
   * Apply end position filtering to options
   */
  applyEndPositionFiltering(options: PictographData[], endPositionFilter: EndPositionFilter): PictographData[];

  /**
   * Apply reversal filtering to options
   */
  applyReversalFiltering(options: PictographData[], reversalFilter: ReversalFilter): PictographData[];

  /**
   * Filter pictographs by letter type
   */
  filterPictographsByType(pictographs: PictographData[], letterType: string): PictographData[];
}
