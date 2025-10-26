/**
 * Start Position Service Interface
 *
 * Simplified interface focused on core functionality.
 */

import type { BeatData, GridMode, PictographData } from "$shared";

export interface IStartPositionService {
  // Core functionality - load and select positions
  getStartPositions(gridMode: GridMode): Promise<PictographData[]>;
  getDefaultStartPositions(gridMode: GridMode): Promise<PictographData[]>;
  getAllStartPositionVariations(gridMode: GridMode): Promise<PictographData[]>;
  selectStartPosition(position: PictographData): Promise<void>;

  // System method for setting start position in sequence
  setStartPosition(startPosition: BeatData): Promise<void>;
}
