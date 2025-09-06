/**
 * Browse Navigation State Service
 *
 * Focused microservice for managing browse navigation state.
 * Handles navigation mode and sections without business logic.
 */

import type { NavigationSectionConfig } from "$lib/modules/browse/gallery/domain";
import { GalleryNavigationMode } from "$lib/modules/browse/gallery/domain";

export interface IBrowseNavigationState {
  // Reactive state getters
  readonly GalleryNavigationMode: GalleryNavigationMode;
  readonly navigationSections: NavigationSectionConfig[];

  // Actions
  setGalleryNavigationMode(mode: GalleryNavigationMode): void;
  setNavigationSections(sections: NavigationSectionConfig[]): void;
  goToFilterSelection(): void;
  goToSequenceBrowser(): void;
}

export class BrowseNavigationState implements IBrowseNavigationState {
  // Private reactive state
  #GalleryNavigationMode = $state<GalleryNavigationMode>(
    GalleryNavigationMode.FILTER_SELECTION
  );
  #navigationSections = $state<NavigationSectionConfig[]>([]);

  // Reactive getters
  get GalleryNavigationMode() {
    return this.#GalleryNavigationMode;
  }

  get navigationSections() {
    return this.#navigationSections;
  }

  // Actions
  setGalleryNavigationMode(mode: GalleryNavigationMode): void {
    this.#GalleryNavigationMode = mode;
  }

  setNavigationSections(sections: NavigationSectionConfig[]): void {
    this.#navigationSections = sections;
  }

  goToFilterSelection(): void {
    this.#GalleryNavigationMode = GalleryNavigationMode.FILTER_SELECTION;
  }

  goToSequenceBrowser(): void {
    this.#GalleryNavigationMode = GalleryNavigationMode.SEQUENCE_BROWSER;
  }
}
