/**
 * Start Position Selector Interface
 *
 * Responsible for selecting random start positions for sequence generation.
 */
import type { BeatData, GridMode } from "$shared";

export interface IStartPositionSelector {
  /**
   * Select a random start position for sequence generation
   * @param gridMode - Grid mode (diamond/box)
   * @returns Promise resolving to BeatData with beatNumber 0
   */
  selectStartPosition(gridMode: GridMode): Promise<BeatData>;
}
