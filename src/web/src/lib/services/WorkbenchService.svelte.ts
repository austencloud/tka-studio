/**
 * Workbench Service (Runes-based)
 *
 * Main coordinator service for the sequence workbench.
 * Manages interactions between beat frame, sequence state, and UI.
 */

import { createBeatData, createPictographData, GridMode } from "../domain";
import { beatFrameService } from "./BeatFrameService.svelte";
import { sequenceStateService } from "./SequenceStateService.svelte";

class WorkbenchService {
  // Workbench state
  #isInitialized = $state<boolean>(false);
  #mode = $state<"view" | "edit" | "construct">("construct");

  // Derived state
  readonly isInitialized = $derived(this.#isInitialized);
  readonly mode = $derived(this.#mode);
  readonly currentSequence = $derived(sequenceStateService.currentSequence);
  readonly selectedBeat = $derived(sequenceStateService.selectedBeat);

  // Actions
  initialize(): void {
    if (this.#isInitialized) return;

    // Start with no sequence - just the START tile will be shown
    // Desktop parity: show empty workbench until user loads/creates a sequence
    this.#isInitialized = true;
  }

  setMode(mode: "view" | "edit" | "construct"): void {
    this.#mode = mode;
  }

  // Beat interactions
  handleBeatClick(index: number): void {
    sequenceStateService.selectBeat(index);
  }

  handleBeatDoubleClick(index: number): void {
    if (this.#mode === "construct") {
      this.editBeat(index);
    }
  }

  handleBeatHover(index: number): void {
    beatFrameService.setHoveredBeat(index);
  }

  handleBeatLeave(): void {
    beatFrameService.clearHoveredBeat();
  }

  // Beat editing
  editBeat(index: number): void {
    const sequence = sequenceStateService.currentSequence;
    if (!sequence || index < 0 || index >= sequence.beats.length) return;

    const beat = sequence.beats[index];

    // For now, just create a simple pictograph
    if (beat?.is_blank) {
      const pictographData = createPictographData({
        letter: "A", // Default letter
        beat: index + 1,
      });

      const updatedBeat = createBeatData({
        ...beat,
        is_blank: false,
        pictograph_data: pictographData,
      });

      sequenceStateService.updateBeat(index, updatedBeat);
    }
  }

  clearBeat(index: number): void {
    const sequence = sequenceStateService.currentSequence;
    if (!sequence || index < 0 || index >= sequence.beats.length) return;

    const beat = sequence.beats[index];
    const clearedBeat = createBeatData({
      ...beat,
      is_blank: true,
      pictograph_data: null,
    });

    sequenceStateService.updateBeat(index, clearedBeat);
  }

  // Sequence management
  createNewSequence(name: string = "New Sequence", length: number = 16): void {
    sequenceStateService.createNewSequence(name, length);
  }

  // Grid configuration
  setGridMode(mode: GridMode): void {
    beatFrameService.setConfig({
      gridMode: mode,
    });
  }

  setBeatSize(size: number): void {
    beatFrameService.setConfig({ beatSize: size });
  }

  setColumns(columns: number): void {
    beatFrameService.setConfig({ columns });
  }
}

// Singleton instance
export const workbenchService = new WorkbenchService();
