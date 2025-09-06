/**
 * Browse State Coordinator
 *
 * Orchestrates browse state microservices and handles complex operations
 * that require coordination between multiple services.
 */

import type { SequenceData } from "../../../../shared/domain";
import type { IGalleryDisplayState } from "../../shared/state/BrowseDisplayState.svelte";
import type { IBrowseNavigationState } from "../../shared/state/BrowseNavigationState.svelte";
import type { IBrowseSelectionState } from "../../shared/state/BrowseSelectionState.svelte";
import type { GalleryFilterType, GallerySortMethod } from "../domain/enums";
import type { GalleryFilterValue } from "../domain/types/gallery-types";
import type {
  IFavoritesService,
  IFilterPersistenceService,
  IGalleryService,
  IGalleryThumbnailService,
  INavigationService,
  ISequenceIndexService,
} from "../services/contracts";
import type { IGalleryState } from "./gallery-state-contracts";
import type { IGalleryFilterState } from "./GalleryFilterState.svelte";
import type { IGallerySearchState } from "./GallerySearchState.svelte";

export class GalleryState implements IGalleryState {
  // Internal sequence state
  #allSequences = $state<SequenceData[]>([]);
  #filteredSequences = $state<SequenceData[]>([]);
  #displayedSequences = $state<SequenceData[]>([]);
  #currentSort = $state<GallerySortMethod>("ALPHABETICAL" as GallerySortMethod);

  constructor(
    private filterState: IGalleryFilterState,
    private navigationState: IBrowseNavigationState,
    private selectionState: IBrowseSelectionState,
    private displayState: IGalleryDisplayState,
    private searchState: IGallerySearchState,
    private browseService: IGalleryService,
    private navigationService: INavigationService,
    private sequenceIndexService: ISequenceIndexService,
    private favoritesService: IFavoritesService,
    private thumbnailService: IGalleryThumbnailService,
    private filterPersistenceService: IFilterPersistenceService
  ) {}

  // Reactive getters
  get allSequences() {
    return this.#allSequences;
  }

  get filteredSequences() {
    return this.#filteredSequences;
  }

  get displayedSequences() {
    return this.#displayedSequences;
  }

  // Core operations
  async loadAllSequences(): Promise<void> {
    try {
      this.displayState.setLoading(true, "Loading sequences...");

      // Delegate to business service
      const sequences = await this.browseService.loadSequenceMetadata();

      // Update internal state
      this.#allSequences = sequences;
      this.#filteredSequences = sequences;
      this.#displayedSequences = sequences;

      // Generate navigation sections
      await this.generateNavigationSections();

      this.displayState.setLoading(false);
    } catch (error) {
      this.displayState.setError(
        error instanceof Error ? error.message : "Failed to load sequences"
      );
    }
  }

  async applyFilter(
    type: GalleryFilterType,
    value: GalleryFilterValue
  ): Promise<void> {
    try {
      this.displayState.setLoading(true, "Applying filter...");

      // Update filter state
      this.filterState.setFilter(type, value);

      // Save filter state for persistence
      await this.saveCurrentFilterState(type, value);

      // Apply filter using business service
      const filtered = await this.filterState.applyCurrentFilter(
        this.#allSequences,
        this.browseService
      );

      // Apply current sort
      const sorted = await this.browseService.sortSequences(
        filtered,
        this.#currentSort
      );

      // Update state
      this.#filteredSequences = filtered;
      this.#displayedSequences = sorted;
      this.navigationState.goToSequenceBrowser();

      this.displayState.setLoading(false);
    } catch (error) {
      this.displayState.setError(
        error instanceof Error ? error.message : "Failed to apply filter"
      );
    }
  }

  async searchSequences(query: string): Promise<void> {
    try {
      this.searchState.setSearchQuery(query);

      if (!query.trim()) {
        // Reset to filtered sequences if no search query
        this.#displayedSequences = this.#filteredSequences;
        return;
      }

      this.displayState.setLoading(true, "Searching...");

      // Delegate search to service
      const searchResults =
        await this.sequenceIndexService.searchSequences(query);

      // Filter search results by current filter if one is applied
      let results = searchResults;
      if (this.filterState.isFilterActive) {
        results = await this.filterState.applyCurrentFilter(
          searchResults,
          this.browseService
        );
      }

      // Apply current sort
      const sorted = await this.browseService.sortSequences(
        results,
        this.#currentSort
      );

      this.#displayedSequences = sorted;
      this.displayState.setLoading(false);
    } catch (error) {
      this.displayState.setError(
        error instanceof Error ? error.message : "Search failed"
      );
    }
  }

  async updateSort(sortMethod: GallerySortMethod): Promise<void> {
    try {
      this.#currentSort = sortMethod;

      // Delegate sorting to service
      const sorted = await this.browseService.sortSequences(
        this.#filteredSequences,
        sortMethod
      );

      this.#displayedSequences = sorted;
    } catch (error) {
      this.displayState.setError(
        error instanceof Error ? error.message : "Failed to sort sequences"
      );
    }
  }

  async backToFilters(): Promise<void> {
    this.navigationState.goToFilterSelection();
    this.filterState.clearFilter();
    this.searchState.clearSearch();
    this.#displayedSequences = this.#allSequences;
  }

  async selectSequence(sequence: SequenceData): Promise<void> {
    this.selectionState.selectSequence(sequence);
  }

  async generateNavigationSections(): Promise<void> {
    try {
      // Get favorites
      const favoriteIds = await this.favoritesService.getFavorites();

      // Generate navigation sections using service
      const sections = await this.navigationService.generateNavigationSections(
        this.#allSequences,
        favoriteIds
      );

      this.navigationState.setNavigationSections(sections);
    } catch (error) {
      console.error("Failed to generate navigation sections:", error);
    }
  }

  // ============================================================================
  // FILTER PERSISTENCE METHODS
  // ============================================================================

  /**
   * Save the current filter state for persistence across page refreshes
   */
  private async saveCurrentFilterState(
    type: GalleryFilterType,
    value: GalleryFilterValue
  ): Promise<void> {
    try {
      // Create a browse state with the current filter
      const browseState: import("../../shared/state/browse-state-models").BrowseState =
        {
          filterType: type,
          filterValues: value,
          selectedSequence: null,
          selectedVariation: null,
          sortMethod: this.#currentSort,
        };

      await this.filterPersistenceService.saveBrowseState(browseState);
      console.log(`💾 Saved filter state: ${type} = ${value}`);
    } catch (error) {
      console.warn("Failed to save filter state:", error);
    }
  }

  /**
   * Restore saved filter state and apply it
   */
  async restoreSavedState(): Promise<void> {
    try {
      const browseState = await this.filterPersistenceService.loadBrowseState();

      if (
        browseState &&
        browseState.filterType &&
        browseState.filterValues !== null
      ) {
        const { filterType, filterValues } = browseState;
        console.log(
          `🔄 Restoring filter state: ${filterType} = ${filterValues}`
        );

        // Apply the saved filter without saving it again (to avoid recursion)
        await this.applySavedFilter(filterType, filterValues);
      }
    } catch (error) {
      console.warn("Failed to restore saved state:", error);
    }
  }

  /**
   * Apply a saved filter without triggering another save operation
   */
  private async applySavedFilter(
    type: GalleryFilterType,
    value: GalleryFilterValue
  ): Promise<void> {
    try {
      this.displayState.setLoading(true, "Restoring filter...");

      // Update filter state without saving
      this.filterState.setFilter(type, value);

      // Apply filter using business service
      const filtered = await this.filterState.applyCurrentFilter(
        this.#allSequences,
        this.browseService
      );

      // Apply current sort
      const sorted = await this.browseService.sortSequences(
        filtered,
        this.#currentSort
      );

      // Update state
      this.#filteredSequences = filtered;
      this.#displayedSequences = sorted;
      this.navigationState.goToSequenceBrowser();

      this.displayState.setLoading(false);

      console.log(`✅ Restored filter: ${filtered.length} sequences found`);
    } catch (error) {
      this.displayState.setError(
        error instanceof Error ? error.message : "Failed to restore filter"
      );
    }
  }

  /**
   * Clear all saved filter state
   */
  async clearSavedState(): Promise<void> {
    try {
      // Use saveBrowseState with null values to clear
      const emptyBrowseState: import("../../shared/state/browse-state-models").BrowseState =
        {
          filterType: null,
          filterValues: null,
          selectedSequence: null,
          selectedVariation: null,
          sortMethod: this.#currentSort,
        };
      await this.filterPersistenceService.saveBrowseState(emptyBrowseState);
      console.log("🗑️ Cleared all saved filter state");
    } catch (error) {
      console.warn("Failed to clear saved state:", error);
    }
  }
}
