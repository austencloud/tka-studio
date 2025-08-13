/**
 * Sequence State Service (Runes-based)
 *
 * Central state management for sequence data using Svelte 5 runes.
 * Replaces stores with modern reactive patterns.
 */

import type { BeatData, SequenceData } from "../domain";
import { createSequenceData, updateSequenceData } from "../domain/SequenceData";

class SequenceStateService {
  // Core sequence state
  #currentSequence = $state<SequenceData | null>(null);
  #selectedBeatIndex = $state<number>(-1);
  #isLoading = $state<boolean>(false);
  #error = $state<string | null>(null);

  // Derived state
  readonly currentSequence = $derived(this.#currentSequence);
  readonly selectedBeatIndex = $derived(this.#selectedBeatIndex);
  readonly selectedBeat = $derived(() => {
    if (this.#currentSequence && this.#selectedBeatIndex >= 0) {
      return this.#currentSequence.beats[this.#selectedBeatIndex] ?? null;
    }
    return null;
  });
  readonly isLoading = $derived(this.#isLoading);
  readonly error = $derived(this.#error);
  readonly hasSequence = $derived(() => this.#currentSequence !== null);
  readonly beatCount = $derived(() => this.#currentSequence?.beats.length ?? 0);

  // Actions
  setCurrentSequence(sequence: SequenceData | null): void {
    this.#currentSequence = sequence;
    this.#selectedBeatIndex = -1; // Reset selection
    this.#error = null;
  }

  selectBeat(index: number): void {
    if (
      this.#currentSequence &&
      index >= 0 &&
      index < this.#currentSequence.beats.length
    ) {
      this.#selectedBeatIndex = index;
    } else {
      this.#selectedBeatIndex = -1;
    }
  }

  updateBeat(index: number, beatData: BeatData): void {
    if (
      !this.#currentSequence ||
      index < 0 ||
      index >= this.#currentSequence.beats.length
    ) {
      return;
    }

    const newBeats = [...this.#currentSequence.beats];
    newBeats[index] = beatData;

    this.#currentSequence = updateSequenceData(this.#currentSequence, {
      beats: newBeats,
    });
  }

  addBeat(beatData: BeatData): void {
    if (!this.#currentSequence) return;

    const newBeats = [...this.#currentSequence.beats, beatData];
    this.#currentSequence = updateSequenceData(this.#currentSequence, {
      beats: newBeats,
    });
  }

  removeBeat(index: number): void {
    if (
      !this.#currentSequence ||
      index < 0 ||
      index >= this.#currentSequence.beats.length
    ) {
      return;
    }

    const newBeats = this.#currentSequence.beats.filter((_, i) => i !== index);
    this.#currentSequence = updateSequenceData(this.#currentSequence, {
      beats: newBeats,
    });

    // Adjust selection if needed
    if (this.#selectedBeatIndex >= newBeats.length) {
      this.#selectedBeatIndex = newBeats.length - 1;
    }
  }

  setLoading(loading: boolean): void {
    this.#isLoading = loading;
  }

  setError(error: string | null): void {
    this.#error = error;
  }

  clearError(): void {
    this.#error = null;
  }

  setStartPosition(startPosition: BeatData): void {
    if (!this.#currentSequence) return;

    this.#currentSequence = updateSequenceData(this.#currentSequence, {
      start_position: startPosition,
    });
  }

  createNewSequence(name: string, length: number = 16): void {
    const sequence = createSequenceData({
      name,
      beats: Array.from({ length }, (_, i) => ({
        id: crypto.randomUUID(),
        beat_number: i + 1,
        duration: 1.0,
        blue_reversal: false,
        red_reversal: false,
        is_blank: true,
        metadata: {},
      })),
    });

    this.setCurrentSequence(sequence);
  }
}

// Singleton instance
export const sequenceStateService = new SequenceStateService();
