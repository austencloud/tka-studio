/**
 * Option Data Service Interface
 *
 * Interface for managing motion options and compatibility.
 * Handles filtering, validation, and conversion of motion options.
 */

import type {
  DifficultyLevel,
  MotionType,
  PictographData,
  SequenceData,
  ValidationResult,
} from "$shared/domain";
import type { FilterCriteria } from "$shared/services";

// Import FilterCriteria from the OptionFilterer implementation

export interface IOptionDataService {
  getNextOptions(
    currentSequence: SequenceData,
    filters?: FilterCriteria
  ): Promise<PictographData[]>;
  filterOptionsByDifficulty(
    options: PictographData[],
    level: DifficultyLevel
  ): PictographData[];
  validateOptionCompatibility(
    option: PictographData,
    sequence: SequenceData
  ): ValidationResult;
  getAvailableMotionTypes(): MotionType[];
  convertCsvRowToPictographData(
    row: Record<string, string>,
    index: number
  ): PictographData | null;
}
