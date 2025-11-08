/**
 * Interface for coordinating sequence state operations
 */
import type { ArrowPosition, PictographData, SequenceData } from "$shared";
import type { GridMode } from "$shared";

export interface SequenceStatistics {
  totalBeats: number;
  blankBeats: number;
  filledBeats: number;
  duration: number;
  hasTurns: boolean;
  hasReversals: boolean;
}

export interface ISequenceCoordinationService {
  /**
   * Get sequence statistics
   */
  getSequenceStatistics(sequence: SequenceData | null): SequenceStatistics;

  /**
   * Get sequence word/name
   */
  getSequenceWord(sequence: SequenceData | null): string;

  /**
   * Get sequence total duration
   */
  getSequenceDuration(sequence: SequenceData | null): number;

  /**
   * Get beat count for sequence
   */
  getBeatCount(sequence: SequenceData | null): number;

  /**
   * Check if sequence has beats
   */
  hasBeats(sequence: SequenceData | null): boolean;

  /**
   * Check if sequence has arrow positions
   */
  hasArrowPositions(arrowPositions: Map<string, ArrowPosition>): boolean;

  /**
   * Check if arrow positioning is complete
   */
  isArrowPositioningComplete(
    arrowPositions: Map<string, ArrowPosition>
  ): boolean;

  /**
   * Get current sequence data as pictograph array
   */
  getCurrentSequenceData(
    sequence: SequenceData | null,
    selectedStartPosition: PictographData | null
  ): PictographData[];
}
