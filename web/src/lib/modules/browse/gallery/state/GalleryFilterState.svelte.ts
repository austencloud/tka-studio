/**
 * Browse Filter State Service
 *
 * Focused microservice for managing browse filter state in isolation.
 * Handles reactive filter state without business logic.
 */

import type { SequenceData } from "../../../../shared/domain";
import type { GalleryFilterType } from "../domain/enums";
import type { GalleryFilterValue } from "../domain/types/gallery-types";
import type { IGalleryService } from "../services/contracts";

export interface IGalleryFilterState {
  // Reactive state getters
  readonly currentFilter: {
    type: GalleryFilterType;
    value: GalleryFilterValue;
  } | null;
  readonly isFilterActive: boolean;

  // Actions
  setFilter(type: GalleryFilterType, value: GalleryFilterValue): void;
  clearFilter(): void;

  // Apply filter using service (reactive)
  applyCurrentFilter(
    sequences: SequenceData[],
    browseService: IGalleryService
  ): Promise<SequenceData[]>;
}

export class GalleryFilterState implements IGalleryFilterState {
  // Private reactive state
  #currentFilter = $state<{
    type: GalleryFilterType;
    value: GalleryFilterValue;
  } | null>(null);

  // Reactive getters
  get currentFilter() {
    return this.#currentFilter;
  }

  get isFilterActive() {
    return this.#currentFilter !== null;
  }

  // Actions
  setFilter(type: GalleryFilterType, value: GalleryFilterValue): void {
    this.#currentFilter = { type, value };
  }

  clearFilter(): void {
    this.#currentFilter = null;
  }

  // Apply filter using business service
  async applyCurrentFilter(
    sequences: SequenceData[],
    browseService: IGalleryService
  ): Promise<SequenceData[]> {
    if (!this.#currentFilter) {
      return sequences;
    }

    return browseService.applyFilter(
      sequences,
      this.#currentFilter.type,
      this.#currentFilter.value
    );
  }
}
