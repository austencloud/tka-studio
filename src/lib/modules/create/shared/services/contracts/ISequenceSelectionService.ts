/**
 * Service for managing sequence beat and start position selection
 */
import type {
  ArrowPosition,
  BeatData,
  PictographData,
  SequenceData,
} from "$shared";

export interface ISequenceSelectionService {
  /**
   * Set the selected beat index
   */
  setSelectedBeat(
    sequenceData: SequenceData | null,
    index: number | null
  ): boolean;

  /**
   * Clear all selections
   */
  clearSelection(): void;

  /**
   * Check if a beat index is valid for the given sequence
   */
  isValidBeatIndex(sequenceData: SequenceData | null, index: number): boolean;

  /**
   * Select the start position for editing
   */
  selectStartPositionForEditing(): void;

  /**
   * Check if the given beat index is selected
   */
  isBeatSelected(selectedIndex: number | null, targetIndex: number): boolean;

  /**
   * Get beat data by index, handling selection logic
   */
  getSelectedBeatData(
    sequenceData: SequenceData | null,
    selectedBeatIndex: number | null,
    selectedStartPosition: PictographData | null,
    isStartPositionSelected: boolean
  ): BeatData | null;

  /**
   * Get beat at specific index
   */
  getBeat(sequenceData: SequenceData | null, index: number): BeatData | null;
}
