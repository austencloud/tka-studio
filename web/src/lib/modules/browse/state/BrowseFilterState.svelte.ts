/**
 * Browse Filter State Service
 *
 * Focused microservice for managing browse filter state in isolation.
 * Handles reactive filter state without business logic.
 */

import type {
  FilterType,
  GalleryFilterValue,
  SequenceData,
} from "$shared/domain";
import type { IGalleryService } from "../services/contracts";

export interface IBrowseFilterState {
  // Reactive state getters
  readonly currentFilter: {
    type: FilterType;
    value: GalleryFilterValue;
  } | null;
  readonly isFilterActive: boolean;

  // Actions
  setFilter(type: FilterType, value: GalleryFilterValue): void;
  clearFilter(): void;

  // Apply filter using service (reactive)
  applyCurrentFilter(
    sequences: SequenceData[],
    browseService: IGalleryService
  ): Promise<SequenceData[]>;
}

export class BrowseFilterState implements IBrowseFilterState {
  // Private reactive state
  #currentFilter = $state<{
    type: FilterType;
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
  setFilter(type: FilterType, value: GalleryFilterValue): void {
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
