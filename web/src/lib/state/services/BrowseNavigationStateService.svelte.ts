/**
 * Browse Navigation State Service
 *
 * Focused microservice for managing browse navigation state.
 * Handles navigation mode and sections without business logic.
 */

import type { NavigationSection } from "$contracts";
import { NavigationMode } from "$domain";

export interface IBrowseNavigationStateService {
  // Reactive state getters
  readonly navigationMode: NavigationMode;
  readonly navigationSections: NavigationSection[];

  // Actions
  setNavigationMode(mode: NavigationMode): void;
  setNavigationSections(sections: NavigationSection[]): void;
  goToFilterSelection(): void;
  goToSequenceBrowser(): void;
}

export class BrowseNavigationStateService
  implements IBrowseNavigationStateService
{
  // Private reactive state
  #navigationMode = $state<NavigationMode>(NavigationMode.FILTER_SELECTION);
  #navigationSections = $state<NavigationSection[]>([]);

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

  setNavigationSections(sections: NavigationSection[]): void {
    this.#navigationSections = sections;
  }

  goToFilterSelection(): void {
    this.#navigationMode = NavigationMode.FILTER_SELECTION;
  }

  goToSequenceBrowser(): void {
    this.#navigationMode = NavigationMode.SEQUENCE_BROWSER;
  }
}
