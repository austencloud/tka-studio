/**
 * Browse State Factory - Clean Architecture
 *
 * Creates a clean, focused browse state using microservices.
 * Replaces the 738-line monolith with focused, testable services.
 */

import type {
  BrowseDeleteConfirmationData,
  GalleryLoadingState,
  NavigationItem,
  NavigationSectionConfig,
} from "$browse/domain";
import { NavigationMode } from "$browse/domain";
import type { GalleryFilterValue } from "$browse/domain/types";
import { FilterType } from "$lib/modules/browse/gallery/domain/enums/gallery-enums";
import type { SequenceData } from "$shared/domain";
import type {
  IDeleteService,
  IFavoritesService,
  IFilterPersistenceService,
  IGalleryService,
  INavigationService,
  ISectionService,
  ISequenceIndexService,
  IThumbnailService,
} from "../services/contracts";
import { BrowseFilterState } from "./BrowseFilterState.svelte";
import { BrowseNavigationState } from "./BrowseNavigationState.svelte";
import { BrowseSearchState } from "./BrowseSearchState.svelte";
import { BrowseSelectionState } from "./BrowseSelectionState.svelte";
import { BrowseStateCoordinator } from "./BrowseStateCoordinator.svelte";
import { GalleryDisplayStateService } from "./GalleryDisplayState.svelte";

export interface BrowseState {
  // State microservices (reactive)
  readonly filterState: BrowseFilterState;
  readonly navigationState: BrowseNavigationState;
  readonly selectionState: BrowseSelectionState;
  readonly displayState: GalleryDisplayStateService;
  readonly searchState: BrowseSearchState;

  // Coordinator (orchestration)
  readonly coordinator: BrowseStateCoordinator;

  // Convenience getters (derived from microservices)
  readonly currentFilter: {
    type: FilterType;
    value: GalleryFilterValue;
  } | null;
  readonly isLoading: boolean;
  readonly hasError: boolean;
  readonly displayedSequences: SequenceData[];
  readonly navigationMode: NavigationMode;
  readonly navigationSections: NavigationSectionConfig[]; // NavigationSectionConfig type not available
  readonly selectedSequence: SequenceData | null;

  // Additional properties needed by BrowseTab
  readonly allSequences: SequenceData[];
  readonly filteredSequences: SequenceData[];
  readonly loadingState: GalleryLoadingState; // From displayState
  readonly searchQuery: string;

  // Delegation methods (common operations)
  loadAllSequences(): Promise<void>;
  applyFilter(type: FilterType, value: GalleryFilterValue): Promise<void>;
  searchSequences(query: string): Promise<void>;
  selectSequence(sequence: SequenceData): Promise<void>;
  backToFilters(): Promise<void>;
  clearError(): void;

  // Filter persistence methods
  restoreSavedState(): Promise<void>;
  clearSavedState(): Promise<void>;

  // Additional methods expected by event handlers
  clearSelection(): void;
  toggleFavorite(sequenceId: string): Promise<void>;
  prepareDeleteSequence(sequence: SequenceData): void;
  confirmDeleteSequence(): Promise<void>;
  cancelDeleteSequence(): void;

  // Navigation methods
  toggleNavigationSection(sectionId: string): void;
  setActiveNavigationItem(sectionId: string, itemId: string): void;
  filterSequencesByNavigation(
    item: unknown,
    sectionType: string
  ): Promise<SequenceData[]>;

  // Delete operations (delegated to existing delete service)
  readonly deleteConfirmation: BrowseDeleteConfirmationData | null;
  readonly showDeleteDialog: boolean;
}

export function createBrowseState(
  browseService: IGalleryService,
  thumbnailService: IThumbnailService,
  sequenceIndexService: ISequenceIndexService,
  favoritesService: IFavoritesService,
  navigationService: INavigationService,
  _filterPersistenceService: IFilterPersistenceService,
  _sectionService: ISectionService,
  _deleteService: IDeleteService
): BrowseState {
  // Create focused microservices - actual instances instead of empty objects
  const filterStateImpl = new BrowseFilterState();
  const navigationState = new BrowseNavigationState();
  const selectionState = new BrowseSelectionState();
  const displayStateImpl = new GalleryDisplayStateService();
  const searchState = new BrowseSearchState();

  // Create adapter for filter state to match coordinator interface
  const filterState = {
    get currentFilter() {
      return filterStateImpl.currentFilter;
    },
    get isFilterActive() {
      return filterStateImpl.isFilterActive;
    },
    setFilter(type: string, value: unknown) {
      filterStateImpl.setFilter(
        type as FilterType,
        value as GalleryFilterValue
      );
    },
    clearFilter() {
      filterStateImpl.clearFilter();
    },
    async applyCurrentFilter(sequences: SequenceData[]) {
      return filterStateImpl.applyCurrentFilter(sequences, browseService);
    },
  };

  // Create adapter for display state to match coordinator interface
  const displayState = {
    get isLoading() {
      return displayStateImpl.isLoading;
    },
    get hasError() {
      return displayStateImpl.hasError;
    },
    get loadingState() {
      return displayStateImpl.loadingState;
    },
    setLoading(loading: boolean, operation?: string) {
      displayStateImpl.setLoading(loading, operation);
    },
    setError(error: string | null) {
      displayStateImpl.setError(error);
    },
    clearError() {
      displayStateImpl.clearError();
    },
  };

  // Create coordinator with proper dependencies
  const coordinator = new BrowseStateCoordinator(
    filterState,
    navigationState,
    selectionState,
    displayState,
    searchState,
    browseService,
    navigationService,
    sequenceIndexService,
    favoritesService,
    thumbnailService,
    _filterPersistenceService
  );

  // Delete state (delegate to existing services)
  const deleteConfirmation = $state<BrowseDeleteConfirmationData | null>(null);
  const showDeleteDialog = $state<boolean>(false);

  return {
    // Expose microservices
    filterState: filterStateImpl,
    navigationState,
    selectionState,
    displayState: displayStateImpl,
    searchState,
    coordinator,

    // Convenience getters (reactive)
    get currentFilter() {
      return filterState.currentFilter;
    },
    get isLoading() {
      return displayState.isLoading;
    },
    get hasError() {
      return displayState.hasError;
    },
    get displayedSequences() {
      return coordinator.displayedSequences;
    },
    get navigationMode() {
      return navigationState.navigationMode;
    },
    get navigationSections() {
      return navigationState.navigationSections;
    },
    get selectedSequence() {
      return selectionState.selectedSequence;
    },

    // Additional properties
    get allSequences() {
      return coordinator.allSequences;
    },
    get filteredSequences() {
      return coordinator.filteredSequences;
    },
    get loadingState() {
      return displayState.loadingState;
    },
    get searchQuery() {
      return searchState.searchQuery;
    },

    // Delete state (TODO: Refactor delete logic into microservice)
    get deleteConfirmation() {
      return deleteConfirmation;
    },
    get showDeleteDialog() {
      return showDeleteDialog;
    },

    // Delegation methods
    async loadAllSequences() {
      await coordinator.loadAllSequences();
    },

    async applyFilter(type: FilterType, value: GalleryFilterValue) {
      await coordinator.applyFilter(type, value);
    },

    async searchSequences(query: string) {
      await coordinator.searchSequences(query);
    },

    async selectSequence(sequence: SequenceData) {
      await coordinator.selectSequence(sequence);
    },

    async backToFilters() {
      await coordinator.backToFilters();
    },

    clearError() {
      displayState.clearError();
    },

    // Filter persistence methods
    async restoreSavedState() {
      await coordinator.restoreSavedState();
    },

    async clearSavedState() {
      await coordinator.clearSavedState();
    },

    // Additional methods expected by event handlers
    clearSelection() {
      selectionState.clearSelection();
    },

    async toggleFavorite(sequenceId: string) {
      // TODO: Implement via coordinator - delegate to FavoritesService
      console.log("Toggle favorite:", sequenceId);
    },

    prepareDeleteSequence(sequence: SequenceData) {
      // TODO: Implement delete confirmation logic
      console.log("Prepare delete:", sequence.id);
    },

    async confirmDeleteSequence() {
      // TODO: Implement delete confirmation logic
      console.log("Confirm delete");
    },

    cancelDeleteSequence() {
      // TODO: Implement delete confirmation logic
      console.log("Cancel delete");
    },

    // Navigation methods
    toggleNavigationSection(sectionId: string) {
      // TODO: Implement navigation section toggle
      console.log("Toggle navigation section:", sectionId);
    },

    setActiveNavigationItem(sectionId: string, itemId: string) {
      console.log("Set active navigation item:", sectionId, itemId);

      // Prevent infinite loops by checking if this item is already active
      const currentSections = navigationState.navigationSections;
      const section = currentSections.find(
        (s: NavigationSectionConfig) => s.id === sectionId
      );
      if (!section) return;

      const item = section.items.find((i: NavigationItem) => i.id === itemId);
      if (!item || item.isActive) {
        // Item is already active, don't trigger another update
        return;
      }

      // Update navigation sections with new active state
      const updatedSections = navigationService.setActiveItem(
        sectionId,
        itemId,
        currentSections
      );
      navigationState.setNavigationSections(updatedSections);
    },

    async filterSequencesByNavigation(item: unknown, sectionType: string) {
      console.log("🔍 Filter by navigation:", item, sectionType);

      // Cast item to NavigationItem type
      const navigationItem = item as import("../services").NavigationItem;

      if (!navigationItem) {
        console.warn("No navigation item provided");
        return [];
      }

      // Use NavigationService to get sequences for this item
      const filteredSequences = navigationService.getSequencesForNavigationItem(
        navigationItem,
        sectionType as
          | "date"
          | "length"
          | "letter"
          | "level"
          | "author"
          | "favorites",
        coordinator.allSequences
      );

      console.log(
        `✅ Navigation filter applied: ${filteredSequences.length} sequences found`
      );

      // Update the filter state
      const filterType =
        sectionType === "letter" ? "starting_letter" : sectionType;
      filterState.setFilter(filterType as FilterType, navigationItem.value);

      // Update the coordinator's displayed sequences
      await coordinator.applyFilter(
        filterType as FilterType,
        navigationItem.value
      );

      return filteredSequences;
    },
  };
}
