/**
 * Browse Filter State Service
 *
 * Focused microservice for managing browse filter state in isolation.
 * Handles reactive filter state without business logic.
 */

import type { FilterType, FilterValue, SequenceData } from "$shared/domain";
import type { IBrowseService } from "../services/contracts";

export interface IBrowseFilterState {
  // Reactive state getters
  readonly currentFilter: { type: FilterType; value: FilterValue } | null;
  readonly isFilterActive: boolean;

  // Actions
  setFilter(type: FilterType, value: FilterValue): void;
  clearFilter(): void;

  // Apply filter using service (reactive)
  applyCurrentFilter(
    sequences: SequenceData[],
    browseService: IBrowseService
  ): Promise<SequenceData[]>;
}

export class BrowseFilterState implements IBrowseFilterState {
  // Private reactive state
  #currentFilter = $state<{ type: FilterType; value: FilterValue } | null>(
    null
  );

  // Reactive getters
  get currentFilter() {
    return this.#currentFilter;
  }

  get isFilterActive() {
    return this.#currentFilter !== null;
  }

  // Actions
  setFilter(type: FilterType, value: FilterValue): void {
    this.#currentFilter = { type, value };
  }

  clearFilter(): void {
    this.#currentFilter = null;
  }

  // Apply filter using business service
  async applyCurrentFilter(
    sequences: SequenceData[],
    browseService: IBrowseService
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
