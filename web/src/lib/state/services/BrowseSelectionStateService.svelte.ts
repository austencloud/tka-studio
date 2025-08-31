/**
 * Browse Selection State Service
 *
 * Focused microservice for managing sequence selection state.
 * Handles current selection without business logic.
 */

import type { SequenceData } from "$domain";

export interface IBrowseSelectionStateService {
  // Reactive state getters
  readonly selectedSequence: SequenceData | null;
  readonly hasSelection: boolean;

  // Actions
  selectSequence(sequence: SequenceData): void;
  clearSelection(): void;
}

export class BrowseSelectionStateService
  implements IBrowseSelectionStateService
{
  // Private reactive state
  #selectedSequence = $state<SequenceData | null>(null);

  // Reactive getters
  get selectedSequence() {
    return this.#selectedSequence;
  }

  get hasSelection() {
    return this.#selectedSequence !== null;
  }

  // Actions
  selectSequence(sequence: SequenceData): void {
    this.#selectedSequence = sequence;
  }

  clearSelection(): void {
    this.#selectedSequence = null;
  }
}
