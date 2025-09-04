/**
 * Browse Search State Service
 *
 * Focused microservice for managing search query state.
 * Handles search string and search mode without business logic.
 */

export interface IBrowseSearchState {
  // Reactive state getters
  readonly searchQuery: string;
  readonly isSearchActive: boolean;

  // Actions
  setSearchQuery(query: string): void;
  clearSearch(): void;
}

export class BrowseSearchState implements IBrowseSearchState {
  // Private reactive state
  #searchQuery = $state<string>("");

  // Reactive getters
  get searchQuery() {
    return this.#searchQuery;
  }

  get isSearchActive() {
    return this.#searchQuery.trim().length > 0;
  }

  // Actions
  setSearchQuery(query: string): void {
    this.#searchQuery = query;
  }

  clearSearch(): void {
    this.#searchQuery = "";
  }
}
