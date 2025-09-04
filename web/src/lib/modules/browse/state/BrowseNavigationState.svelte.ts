/**
 * Browse Navigation State Service
 *
 * Focused microservice for managing browse navigation state.
 * Handles navigation mode and sections without business logic.
 */

import type { NavigationSectionConfig } from "$browse/domain";
import { NavigationMode } from "$browse/domain";

export interface IBrowseNavigationState {
  // Reactive state getters
  readonly navigationMode: NavigationMode;
  readonly navigationSections: NavigationSectionConfig[];

  // Actions
  setNavigationMode(mode: NavigationMode): void;
  setNavigationSections(sections: NavigationSectionConfig[]): void;
  goToFilterSelection(): void;
  goToSequenceBrowser(): void;
}

export class BrowseNavigationState implements IBrowseNavigationState {
  // Private reactive state
  #navigationMode = $state<NavigationMode>(NavigationMode.FILTER_SELECTION);
  #navigationSections = $state<NavigationSectionConfig[]>([]);

  // Reactive getters
  get navigationMode() {
    return this.#navigationMode;
  }

  get navigationSections() {
    return this.#navigationSections;
  }

  // Actions
  setNavigationMode(mode: NavigationMode): void {
    this.#navigationMode = mode;
  }

  setNavigationSections(sections: NavigationSectionConfig[]): void {
    this.#navigationSections = sections;
  }

  goToFilterSelection(): void {
    this.#navigationMode = NavigationMode.FILTER_SELECTION;
  }

  goToSequenceBrowser(): void {
    this.#navigationMode = NavigationMode.SEQUENCE_BROWSER;
  }
}
