/**
 * IStartPositionService.ts - Start Position Service Interface
 */

import type { PictographData } from "$lib/domain/PictographData";
import type { BeatData } from "$lib/domain/BeatData";
import type { ValidationResult } from "$lib/services/interfaces/domain-types";
import { GridMode } from "$lib/domain/enums";

export interface IStartPositionService {
  // Data operations
  getDefaultStartPositions(gridMode: GridMode): Promise<PictographData[]>;
  
  // Selection operations
  selectStartPosition(position: PictographData): Promise<void>;
  
  // Validation
  validateStartPosition(position: BeatData): ValidationResult;
  
  // State access (readonly)
  readonly startPositions: PictographData[];
  readonly selectedPosition: PictographData | null;
  readonly isLoading: boolean;
  readonly error: string | null;
  
  // State mutations
  setLoading(loading: boolean): void;
  setError(error: string | null): void;
  clearSelection(): void;
}
