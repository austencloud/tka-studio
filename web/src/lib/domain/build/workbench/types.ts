/**
 * Sequence Service Interfaces
 *
 * Interfaces for sequence management, creation, updates, and domain logic.
 * This includes both service contracts and related data structures.
 *
 * Also includes page layout services for printable sequence card creation.
 */
// ============================================================================
// IMPORTS
// ============================================================================
import type { GridMode } from "$domain";
import type { SequenceData } from "../../core/SequenceData";

// ============================================================================
// DATA CONTRACTS (Domain Models)
// ============================================================================

export interface SequenceCreateRequest {
  name: string;
  length: number;
  gridMode?: GridMode;
  propType?: string;
}

export interface DeleteResult {
  success: boolean;
  deletedSequence: SequenceData | null;
  affectedSequences: SequenceData[];
  error?: string;
}

export interface DeleteConfirmationData {
  sequence: SequenceData;
  relatedSequences: SequenceData[];
  hasVariations: boolean;
  willFixVariationNumbers: boolean;
}
