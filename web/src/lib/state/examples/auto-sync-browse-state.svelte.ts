/**
 * Example Integration: Auto-Sync Browse State Factory
 *
 * This shows how to integrate the auto-sync functionality into your existing
 * createBrowseState factory. You can apply this same pattern to other factories.
 */

import { createBrowseAutoSync } from "$lib/state/utils/auto-sync-state.svelte";
import type {
  SequenceData,
  FilterType,
  FilterValue,
  BrowseLoadingState,
} from "$lib/services/interfaces/domain-types";
import type {
  IBrowseService,
  IDeleteService,
  IFavoritesService,
  IFilterPersistenceService,
  INavigationService,
  ISectionService,
  ISequenceIndexService,
  IThumbnailService,
  NavigationSection,
  DeleteConfirmationData,
} from "$lib/services/interfaces/browse-interfaces";
import { NavigationMode } from "$lib/domain/browse";

// ============================================================================
// AUTO-SYNC ENABLED BROWSE STATE
// ============================================================================

export function createAutoSyncBrowseState(
  browseService: IBrowseService,
  thumbnailService: IThumbnailService,
  sequenceIndexService: ISequenceIndexService,
  favoritesService: IFavoritesService,
  navigationService: INavigationService,
  filterPersistenceService: IFilterPersistenceService,
  sectionService: ISectionService,
  deleteService: IDeleteService
) {
  // Create auto-sync manager
  const autoSync = createBrowseAutoSync();

  // Load initial state from persistence
  const initialState = autoSync.load({
    // Filter state
    currentFilter: null as { type: FilterType; value: FilterValue } | null,

    // Display state
    displayedSequences: [] as SequenceData[],
    allSequences: [] as SequenceData[],
    filteredSequences: [] as SequenceData[],

    // Loading state
    isLoading: false,
    loadingState: {
      isLoading: false,
      currentOperation: "",
      error: null,
    } as BrowseLoadingState,

    // Navigation state
    navigationMode: NavigationMode.FILTER_SELECTION,
    navigationSections: [] as NavigationSection[],

    // Selection state
    selectedSequence: null as SequenceData | null,

    // Search state
    searchQuery: "",

    // Scroll state (for restoration)
    scrollPosition: { top: 0, left: 0 },

    // View state
    viewMode: "grid" as "grid" | "list",

    // Delete state
    deleteConfirmation: null as DeleteConfirmationData | null,
    showDeleteDialog: false,
  });

  // Reactive state
  const browseState = $state(initialState);

  // Setup auto-sync - this will automatically save any changes to browseState
  const cleanup = autoSync.sync(() => browseState);

  // ============================================================================
  // STATE GETTERS (Reactive)
  // ============================================================================

  return {
    // Direct state access for reactive subscriptions
    get currentFilter() {
      return (browseState as any).currentFilter;
    },
    get isLoading() {
      return (browseState as any).isLoading;
    },
    get displayedSequences() {
      return (browseState as any).displayedSequences;
    },
    get allSequences() {
      return (browseState as any).allSequences;
    },
    get filteredSequences() {
      return (browseState as any).filteredSequences;
    },
    get navigationMode() {
      return (browseState as any).navigationMode;
    },
    get navigationSections() {
      return (browseState as any).navigationSections;
    },
    get selectedSequence() {
      return (browseState as any).selectedSequence;
    },
    get searchQuery() {
      return (browseState as any).searchQuery;
    },
    get scrollPosition() {
      return (browseState as any).scrollPosition;
    },
    get viewMode() {
      return (browseState as any).viewMode;
    },
    get deleteConfirmation() {
      return (browseState as any).deleteConfirmation;
    },
    get showDeleteDialog() {
      return (browseState as any).showDeleteDialog;
    },
    get loadingState() {
      return (browseState as any).loadingState;
    },

    // Derived state
    get hasError() {
      return (browseState as any).loadingState.error !== null;
    },

    // ============================================================================
    // ACTIONS (Auto-synced)
    // ============================================================================

    async loadAllSequences() {
      (browseState as any).isLoading = true;
      (browseState as any).loadingState = {
        isLoading: true,
        currentOperation: "Loading sequences...",
        error: null,
      };
      // Auto-synced! ✅

      try {
        const sequences = await browseService.loadSequenceMetadata();

        (browseState as any).allSequences = sequences;
        (browseState as any).filteredSequences = sequences;
        (browseState as any).displayedSequences = sequences;
        (browseState as any).isLoading = false;
        (browseState as any).loadingState.isLoading = false;
        // All auto-synced! ✅

        // Generate navigation sections
        const favoriteIds = await favoritesService.getFavorites();
        const sections = await navigationService.generateNavigationSections(
          sequences,
          favoriteIds
        );
        (browseState as any).navigationSections = sections;
        // Auto-synced! ✅
      } catch (error) {
        (browseState as any).loadingState = {
          isLoading: false,
          currentOperation: "",
          error:
            error instanceof Error ? error.message : "Failed to load sequences",
        };
        (browseState as any).isLoading = false;
        // Auto-synced! ✅
      }
    },

    async applyFilter(type: FilterType, value: FilterValue) {
      (browseState as any).currentFilter = { type, value };
      (browseState as any).isLoading = true;
      // Auto-synced! ✅

      try {
        const filtered = await browseService.applyFilter(
          (browseState as any).allSequences,
          type,
          value
        );
        (browseState as any).filteredSequences = filtered;
        (browseState as any).displayedSequences = filtered;
        (browseState as any).navigationMode = NavigationMode.SEQUENCE_BROWSER;
        (browseState as any).isLoading = false;
        // All auto-synced! ✅
      } catch (error) {
        (browseState as any).loadingState.error =
          error instanceof Error ? error.message : "Filter failed";
        (browseState as any).isLoading = false;
        // Auto-synced! ✅
      }
    },

    async searchSequences(query: string) {
      (browseState as any).searchQuery = query;
      // Auto-synced! ✅

      if (!query.trim()) {
        (browseState as any).displayedSequences = (
          browseState as any
        ).filteredSequences;
        // Auto-synced! ✅
        return;
      }

      try {
        const searchResults = await sequenceIndexService.searchSequences(query);
        (browseState as any).displayedSequences = searchResults;
        // Auto-synced! ✅
      } catch (error) {
        (browseState as any).loadingState.error =
          error instanceof Error ? error.message : "Search failed";
        // Auto-synced! ✅
      }
    },

    selectSequence(sequence: SequenceData) {
      (browseState as any).selectedSequence = sequence;
      // Auto-synced! ✅
    },

    clearSelection() {
      (browseState as any).selectedSequence = null;
      // Auto-synced! ✅
    },

    setScrollPosition(position: { top: number; left: number }) {
      (browseState as any).scrollPosition = position;
      // Auto-synced with debouncing! ✅
    },

    setViewMode(mode: "grid" | "list") {
      (browseState as any).viewMode = mode;
      // Auto-synced! ✅
    },

    async backToFilters() {
      (browseState as any).navigationMode = NavigationMode.FILTER_SELECTION;
      (browseState as any).currentFilter = null;
      (browseState as any).searchQuery = "";
      (browseState as any).selectedSequence = null;
      (browseState as any).displayedSequences = (
        browseState as any
      ).allSequences;
      // All auto-synced! ✅
    },

    clearError() {
      (browseState as any).loadingState.error = null;
      // Auto-synced! ✅
    },

    // Delete operations
    prepareDeleteSequence(sequence: SequenceData) {
      (browseState as any).deleteConfirmation = {
        sequenceId: sequence.id,
        sequenceName: sequence.name,
        sequence: sequence,
        relatedSequences: [],
        hasVariations: false,
        willFixVariationNumbers: false,
      } as DeleteConfirmationData;
      (browseState as any).showDeleteDialog = true;
      // Auto-synced! ✅
    },

    cancelDeleteSequence() {
      (browseState as any).deleteConfirmation = null;
      (browseState as any).showDeleteDialog = false;
      // Auto-synced! ✅
    },

    async confirmDeleteSequence() {
      if (!(browseState as any).deleteConfirmation) return;

      try {
        await deleteService.deleteSequence(
          (browseState as any).deleteConfirmation.sequenceId,
          []
        );

        // Remove from sequences
        (browseState as any).allSequences = (
          browseState as any
        ).allSequences.filter(
          (seq: any) =>
            seq.id !== (browseState as any).deleteConfirmation!.sequenceId
        );
        (browseState as any).filteredSequences = (
          browseState as any
        ).filteredSequences.filter(
          (seq: any) =>
            seq.id !== (browseState as any).deleteConfirmation!.sequenceId
        );
        (browseState as any).displayedSequences = (
          browseState as any
        ).displayedSequences.filter(
          (seq: any) =>
            seq.id !== (browseState as any).deleteConfirmation!.sequenceId
        );

        // Clear delete state
        (browseState as any).deleteConfirmation = null;
        (browseState as any).showDeleteDialog = false;
        (browseState as any).selectedSequence = null;
        // All auto-synced! ✅
      } catch (error) {
        (browseState as any).loadingState.error =
          error instanceof Error ? error.message : "Delete failed";
        // Auto-synced! ✅
      }
    },

    // ============================================================================
    // MANUAL SYNC OPERATIONS
    // ============================================================================

    saveStateNow() {
      autoSync.saveNow(browseState);
    },

    clearPersistedState() {
      autoSync.clear();
    },

    // ============================================================================
    // CLEANUP
    // ============================================================================

    destroy() {
      cleanup();
    },
  };
}

// ============================================================================
// INTEGRATION INSTRUCTIONS
// ============================================================================

/*
To integrate this into your existing browse state factory:

1. Replace your current createBrowseState with createAutoSyncBrowseState
2. Remove manual persistence calls - everything auto-syncs now
3. Update your components to use the new factory

Example in BrowseTab.svelte:
```svelte
<script lang="ts">
  import { createAutoSyncBrowseState } from './path/to/auto-sync-browse-state';
  
  // Create auto-syncing browse state
  const browseState = createAutoSyncBrowseState(
    browseService,
    thumbnailService,
    // ... other services
  );
  
  // Use reactive getters
  $: sequences = (browseState as any).displayedSequences;
  $: isLoading = (browseState as any).isLoading;
  $: currentFilter = (browseState as any).currentFilter;
  
  // Actions automatically persist
  function handleFilter(type, value) {
    (browseState as any).applyFilter(type, value); // Auto-saves!
  }
  
  function handleScroll(e) {
    (browseState as any).setScrollPosition({
      top: e.target.scrollTop,
      left: e.target.scrollLeft
    }); // Auto-saves with debouncing!
  }
</script>
```

3. Remove all manual saveState() calls from your components
4. Remove BrowseTabStateManager - it's no longer needed
5. Enjoy automatic state persistence! 🎉
*/
