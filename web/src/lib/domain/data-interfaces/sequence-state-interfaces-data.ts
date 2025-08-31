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
import type { SequenceData } from "$domain";

// ============================================================================
// DATA CONTRACTS (Domain Models)
// ============================================================================

export interface SequenceStatistics {
  totalBeats: number;
  blankBeats: number;
  filledBeats: number;
  totalDuration: number;
  averageBeatDuration: number;
  hasStartPosition: boolean;
  reversalCount: {
    blue: number;
    red: number;
  };
}

export interface BeatOperationResult {
  success: boolean;
  sequence: SequenceData;
  error?: string;
}

export interface SequenceTransformOptions {
  preserveMetadata?: boolean;
  updateBeatNumbers?: boolean;
  validateResult?: boolean;
}
