/**
 * Browse State Coordinator
 *
 * Orchestrates browse state microservices and handles complex operations
 * that require coordination between multiple services.
 */

import { NavigationMode } from "$browse/domain";
import type {
  FilterType,
  FilterValue,
  GallerySortMethod,
  SequenceData,
} from "$shared/domain";
import type {
  IBrowseService,
  IFavoritesService,
  IFilterPersistenceService,
  INavigationService,
  ISequenceIndexService,
  IThumbnailService,
} from "../services/contracts";
import type { IBrowseNavigationState } from "./BrowseNavigationState.svelte";
import type { IBrowseSearchState } from "./BrowseSearchState.svelte";
import type { IBrowseSelectionState } from "./BrowseSelectionState.svelte";

// Interfaces defined locally to avoid circular imports
interface IBrowseFilterState {
  setFilter(type: string, value: unknown): void;
  applyCurrentFilter(sequences: SequenceData[]): Promise<SequenceData[]>;
  clearFilter(): void;
  isFilterActive: boolean;
}

interface IGalleryDisplayState {
  setLoading(loading: boolean, operation?: string): void;
  setError(error: string | null): void;
}

export interface IBrowseStateCoordinator {
  // Core operations
  loadAllSequences(): Promise<void>;
  applyFilter(type: FilterType, value: FilterValue): Promise<void>;
  searchSequences(query: string): Promise<void>;
  updateSort(sortMethod: GallerySortMethod): Promise<void>;
  backToFilters(): Promise<void>;

  // Selection operations
  selectSequence(sequence: SequenceData): Promise<void>;

  // Navigation operations
  generateNavigationSections(): Promise<void>;

  // Filter persistence operations
  restoreSavedState(): Promise<void>;
  clearSavedState(): Promise<void>;

  // Reactive getters
  readonly allSequences: SequenceData[];
  readonly filteredSequences: SequenceData[];
  readonly displayedSequences: SequenceData[];
}

export class BrowseStateCoordinator implements IBrowseStateCoordinator {
  // Internal sequence state
  #allSequences = $state<SequenceData[]>([]);
  #filteredSequences = $state<SequenceData[]>([]);
  #displayedSequences = $state<SequenceData[]>([]);
  #currentSort = $state<GallerySortMethod>("ALPHABETICAL" as GallerySortMethod);

  constructor(
    private filterState: IBrowseFilterState,
    private navigationState: IBrowseNavigationState,
    private selectionState: IBrowseSelectionState,
    private displayState: IGalleryDisplayState,
    private searchState: IBrowseSearchState,
    private browseService: IBrowseService,
    private navigationService: INavigationService,
    private sequenceIndexService: ISequenceIndexService,
    private favoritesService: IFavoritesService,
    private thumbnailService: IThumbnailService,
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

  async applyFilter(type: FilterType, value: FilterValue): Promise<void> {
    try {
      this.displayState.setLoading(true, "Applying filter...");

      // Update filter state
      this.filterState.setFilter(type, value);

      // Save filter state for persistence
      await this.saveCurrentFilterState(type, value);

      // Apply filter using business service
      const filtered = await this.filterState.applyCurrentFilter(
        this.#allSequences
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
        results = await this.filterState.applyCurrentFilter(searchResults);
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
    type: FilterType,
    value: FilterValue
  ): Promise<void> {
    try {
      // Create a browse state with the current filter
      const browseState: import("$domain").BrowseState = {
        filterType: type,
        filterValues: value,
        selectedSequence: null,
        selectedVariation: null,
        navigationMode: NavigationMode.SEQUENCE_BROWSER,
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
    type: FilterType,
    value: FilterValue
  ): Promise<void> {
    try {
      this.displayState.setLoading(true, "Restoring filter...");

      // Update filter state without saving
      this.filterState.setFilter(type, value);

      // Apply filter using business service
      const filtered = await this.filterState.applyCurrentFilter(
        this.#allSequences
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
      const emptyBrowseState: import("$domain").BrowseState = {
        filterType: null,
        filterValues: null,
        selectedSequence: null,
        selectedVariation: null,
        navigationMode: NavigationMode.FILTER_SELECTION,
        sortMethod: this.#currentSort,
      };
      await this.filterPersistenceService.saveBrowseState(emptyBrowseState);
      console.log("🗑️ Cleared all saved filter state");
    } catch (error) {
      console.warn("Failed to clear saved state:", error);
    }
  }
}
