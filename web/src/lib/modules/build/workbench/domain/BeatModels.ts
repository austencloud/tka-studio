/**
 * Beat Data Models
 *
 * Core data structures for individual beats in sequences.
 */

import type { PictographData } from "$shared/domain";

export interface BeatInfo {
  id: string;
  beatNumber: number; // Changed from 'number' to match workbench interface
  pictographData?: PictographData | null;
  timing?: number;
  notes?: string;
  isStartPosition?: boolean;
  metadata?: Record<string, unknown>;
}

export interface BeatSequence {
  beats: BeatInfo[];
  totalBeats: number;
  currentBeat?: number;
}

export interface BeatValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}

export interface BeatMetrics {
  complexity: number;
  difficulty: number;
  estimatedDuration: number;
}
