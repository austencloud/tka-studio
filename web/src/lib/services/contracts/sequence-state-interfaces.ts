/**
 * Sequence State Service Interfaces
 *
 * Pure TypeScript interfaces for sequence state management services.
 * Extracted from SequenceStateService.svelte.ts to enable clean architecture.
 */
// ============================================================================
// SERVICE INTERFACES
// ============================================================================
/**
 * Pure business logic service for sequence state management
 */
import type {
  BeatData,
  SequenceData,
  SequenceStatistics,
  ValidationResult,
} from "$domain";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface ISequenceStateService {
  // Sequence management
  createNewSequence(name: string, length?: number): SequenceData;
  validateSequence(sequence: SequenceData): ValidationResult;

  // Beat operations
  addBeat(sequence: SequenceData, beatData?: Partial<BeatData>): SequenceData;
  removeBeat(sequence: SequenceData, beatIndex: number): SequenceData;
  updateBeat(
    sequence: SequenceData,
    beatIndex: number,
    beatData: Partial<BeatData>
  ): SequenceData;
  insertBeat(
    sequence: SequenceData,
    beatIndex: number,
    beatData?: Partial<BeatData>
  ): SequenceData;

  // Beat selection helpers
  isValidBeatIndex(sequence: SequenceData | null, beatIndex: number): boolean;
  getSelectedBeat(
    sequence: SequenceData | null,
    beatIndex: number
  ): BeatData | null;

  // Sequence transformations
  clearSequence(sequence: SequenceData): SequenceData;
  duplicateSequence(sequence: SequenceData, newName?: string): SequenceData;
  setStartPosition(
    sequence: SequenceData,
    startPosition: BeatData
  ): SequenceData;

  // Sequence operations
  mirrorSequence(sequence: SequenceData): SequenceData;
  swapColors(sequence: SequenceData): SequenceData;
  rotateSequence(
    sequence: SequenceData,
    direction: "clockwise" | "counterclockwise"
  ): SequenceData;

  // Validation and utilities
  generateSequenceWord(sequence: SequenceData): string;
  calculateSequenceDuration(sequence: SequenceData): number;
  getSequenceStatistics(sequence: SequenceData): SequenceStatistics;
}

export interface ISequenceStateConfigService {
  getDefaultBeatData(): BeatData;
  getDefaultSequenceLength(): number;
  getMaxSequenceLength(): number;
  validateSequenceName(name: string): ValidationResult;
  validateBeatData(beatData: Partial<BeatData>): ValidationResult;
}
