/**
 * Start Position Service Interface
 *
 * Interface for managing sequence start positions.
 * Handles validation, retrieval, and setting of start positions.
 */

import type {
  BeatData,
  GridMode,
  PictographData,
  ValidationResult,
} from "$domain";

export interface IStartPositionService {
  getAvailableStartPositions(
    propType: string,
    gridMode: GridMode
  ): Promise<BeatData[]>;
  setStartPosition(startPosition: BeatData): Promise<void>;
  validateStartPosition(position: BeatData): ValidationResult;
  getDefaultStartPositions(gridMode: GridMode): Promise<PictographData[]>;

  // State properties for reactive state management
  readonly startPositions: PictographData[];
  readonly selectedPosition: PictographData | null;
  readonly isLoading: boolean;
  readonly error: string | null;

  // Additional methods for state management
  selectStartPosition(position: PictographData): Promise<void>;
}
