/**
 * Option Loader Service Contract
 *
 * Handles loading of available pictograph options based on sequence context.
 * Extracted from OptionPickerService for better separation of concerns.
 */

import type { PictographData } from "$shared";

export interface IOptionLoader {
  /**
   * Load available options based on current sequence
   */
  loadOptions(sequence: PictographData[]): Promise<PictographData[]>;
}
