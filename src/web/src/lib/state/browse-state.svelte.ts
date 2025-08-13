/**
 * Browse State - Runes Implementation
 *
 * Reactive state management for browse functionality using Svelte 5 runes.
 * Wraps browse services for UI reactivity while keeping business logic in services.
 */

import {
  NavigationMode,
  SortMethod as SortMethodEnum,
  createDefaultDisplayState,
  createDefaultLoadingState,
} from "$lib/domain/browse";
import type {
  BrowseDisplayState,
  BrowseLoadingState,
  BrowseSequenceMetadata,
  DeleteConfirmationData,
  FilterType,
  FilterValue,
  IBrowseService,
  IDeleteService,
  // Advanced browse services
  IFavoritesService,
  IFilterPersistenceService,
  INavigationService,
  ISectionService,
  ISequenceIndexService,
  IThumbnailService,
  NavigationItem,
  NavigationSection,
  SectionConfiguration,
  SequenceSection,
  SortMethod,
} from "$lib/services/interfaces";
import { getBrowseStatePersistence } from "./appState.svelte";
import { getBrowseTabStateManager } from "./browseTabStateManager.svelte";

export function createBrowseState(
  browseService: IBrowseService,
  thumbnailService: IThumbnailService,
  sequenceIndexService: ISequenceIndexService,
  favoritesService: IFavoritesService,
  navigationService: INavigationService,
  _filterPersistenceService: IFilterPersistenceService,
  sectionService: ISectionService,
  deleteService: IDeleteService,
) {
  // ✅ STATE PERSISTENCE: Initialize state manager
  const stateManager = getBrowseTabStateManager();

  // ✅ PURE RUNES: Reactive state for UI
  let allSequences = $state<BrowseSequenceMetadata[]>([]);
  let filteredSequences = $state<BrowseSequenceMetadata[]>([]);
  let displayedSequences = $state<BrowseSequenceMetadata[]>([]);
  let selectedSequence = $state<BrowseSequenceMetadata | null>(null);

  // Advanced browse state
  let favorites = $state<Set<string>>(new Set());
  let navigationSections = $state<NavigationSection[]>([]);
  let sequenceSections = $state<SequenceSection[]>([]);
  let sectionConfiguration = $state<SectionConfiguration>({
    groupBy: "letter",
    sortMethod: SortMethodEnum.ALPHABETICAL,
    showEmptySections: false,
    expandedSections: new Set(["A", "B", "C"]),
  });
  let deleteConfirmation = $state<DeleteConfirmationData | null>(null);
  let showDeleteDialog = $state<boolean>(false);

  // Navigation and filtering state
  let currentFilter = $state<{ type: FilterType; value: FilterValue } | null>(
    null,
  );
  let currentSort = $state<SortMethod>(SortMethodEnum.ALPHABETICAL);
  let navigationMode = $state<NavigationMode>(NavigationMode.FILTER_SELECTION);

  // UI state
  const loadingState = $state<BrowseLoadingState>(createDefaultLoadingState());
  let displayState = $state<BrowseDisplayState>(createDefaultDisplayState());
  let searchQuery = $state<string>("");

  // ✅ DERIVED RUNES: Computed values
  const isLoading = $derived(loadingState.isLoading);
  const hasSequences = $derived(displayedSequences.length > 0);
  const hasError = $derived(loadingState.error !== null);
  const sequenceCount = $derived(displayedSequences.length);
  const sortedSections = $derived(() => {
    if (displayedSequences.length === 0) return {};
    // This will be computed by grouping sequences
    return groupSequencesBySection(displayedSequences, currentSort);
  });

  // Advanced derived values
  const favoritesCount = $derived(favorites.size);
  const hasNavigationSections = $derived(navigationSections.length > 0);
  const hasSequenceSections = $derived(sequenceSections.length > 0);
  const sectionStatistics = $derived(() => {
    if (sequenceSections.length === 0) return null;
    return {
      totalSections: sequenceSections.length,
      totalSequences: sequenceSections.reduce(
        (sum, section) => sum + section.count,
        0,
      ),
      expandedSections: sequenceSections.filter((section) => section.isExpanded)
        .length,
    };
  });

  // ✅ RUNES METHODS: UI state management that delegates to services
  async function loadAllSequences() {
    try {
      loadingState.isLoading = true;
      loadingState.currentOperation = "Loading sequences...";
      loadingState.error = null;

      // Delegate to service for business logic
      const sequences = await browseService.loadSequenceMetadata();

      // Update reactive state
      allSequences = sequences;
      filteredSequences = sequences;
      displayedSequences = sequences;

      // Load favorites and generate navigation sections
      await loadFavorites();
      await generateNavigationSections();
      await generateSequenceSections();

      // 📖 RESTORE STATE: Restore saved filter state after loading sequences
      await restoreFilterState();

      loadingState.isLoading = false;
      loadingState.loadedCount = sequences.length;
      loadingState.totalCount = sequences.length;
    } catch (error) {
      loadingState.isLoading = false;
      loadingState.error =
        error instanceof Error ? error.message : "Failed to load sequences";
    }
  }

  // 📖 RESTORE FILTER STATE: Restore saved filter state when Browse tab loads
  async function restoreFilterState() {
    try {
      // Try to load individual filter state first
      const savedFilterState =
        await getBrowseStatePersistence().loadFilterState();
      if (
        savedFilterState &&
        savedFilterState.type &&
        savedFilterState.value !== null
      ) {
        console.log("📖 Restoring filter state:", savedFilterState);

        const filterType = savedFilterState.type as string;
        const filterValue = savedFilterState.value;

        // Check if this is a navigation filter
        if (filterType.startsWith("navigation_")) {
          const sectionType = filterType.replace(
            "navigation_",
            "",
          ) as NavigationSection["type"];

          // Find the navigation item that matches the saved filter
          const matchingItem: NavigationItem = {
            id: `${sectionType}_${filterValue}`,
            label: String(filterValue),
            value: filterValue as string | number,
            count: 0, // Will be updated when navigation sections are generated
            isActive: true,
          };

          // Apply the navigation filter
          const filtered = navigationService.getSequencesForNavigationItem(
            matchingItem,
            sectionType,
            allSequences,
          );

          // Apply current sort
          const sorted = await browseService.sortSequences(
            filtered,
            currentSort,
          );

          // Update reactive state
          currentFilter = {
            type: filterType as FilterType,
            value: filterValue as FilterValue,
          };
          filteredSequences = filtered;
          displayedSequences = sorted;
          navigationMode = NavigationMode.SEQUENCE_BROWSER;

          console.log("✅ Navigation filter state restored successfully");
        } else {
          // Handle regular filters
          const filterTypeEnum = filterType as FilterType;
          const filterValueEnum = filterValue as FilterValue;

          // Apply the saved filter
          currentFilter = {
            type: filterTypeEnum,
            value: filterValueEnum,
          };

          // Apply the filter to sequences
          const filtered = await browseService.applyFilter(
            allSequences,
            filterTypeEnum,
            filterValueEnum,
          );

          // Apply current sort
          const sorted = await browseService.sortSequences(
            filtered,
            currentSort,
          );

          // Update reactive state
          filteredSequences = filtered;
          displayedSequences = sorted;
          navigationMode = NavigationMode.SEQUENCE_BROWSER;

          console.log("✅ Regular filter state restored successfully");
        }
      } else {
        console.log("📖 No saved filter state to restore");
      }
    } catch (error) {
      console.warn("⚠️ Failed to restore filter state:", error);
    }
  }

  async function applyFilter(filterType: FilterType, filterValue: FilterValue) {
    try {
      console.log(
        "🎯 browse-state.applyFilter() called with:",
        filterType,
        filterValue,
      );
      loadingState.isLoading = true;
      loadingState.currentOperation = "Applying filter...";

      // Update current filter state
      currentFilter = { type: filterType, value: filterValue };
      console.log("📝 Updated currentFilter:", currentFilter);

      // 💾 SAVE FILTER STATE: Persist filter state for cross-session memory
      await stateManager.saveFilterState(filterType, filterValue);
      console.log("💾 Filter state saved:", {
        type: filterType,
        value: filterValue,
      });

      console.log("📊 allSequences available:", allSequences.length, "items");

      // Delegate filtering to service
      const filtered = await browseService.applyFilter(
        allSequences,
        filterType,
        filterValue,
      );
      console.log("🔍 Filtered sequences received:", filtered.length, "items");

      // Apply current sort
      const sorted = await browseService.sortSequences(filtered, currentSort);
      console.log("📈 Sorted sequences:", sorted.length, "items");

      // Update reactive state
      filteredSequences = filtered;
      displayedSequences = sorted;
      navigationMode = NavigationMode.SEQUENCE_BROWSER;

      loadingState.isLoading = false;
    } catch (error) {
      loadingState.isLoading = false;
      loadingState.error =
        error instanceof Error ? error.message : "Failed to apply filter";
    }
  }

  async function updateSort(sortMethod: SortMethod) {
    try {
      currentSort = sortMethod;

      // Delegate sorting to service
      const sorted = await browseService.sortSequences(
        filteredSequences,
        sortMethod,
      );

      // Update reactive state
      displayedSequences = sorted;
    } catch (error) {
      loadingState.error =
        error instanceof Error ? error.message : "Failed to sort sequences";
    }
  }

  async function searchSequences(query: string) {
    try {
      searchQuery = query;

      if (!query.trim()) {
        // Reset to filtered sequences if no search query
        displayedSequences = filteredSequences;
        return;
      }

      loadingState.isLoading = true;
      loadingState.currentOperation = "Searching...";

      // Delegate search to service
      const searchResults = await sequenceIndexService.searchSequences(query);

      // Filter search results by current filter if one is applied
      let results = searchResults;
      if (currentFilter) {
        results = await browseService.applyFilter(
          searchResults,
          currentFilter.type,
          currentFilter.value,
        );
      }

      // Apply current sort
      const sorted = await browseService.sortSequences(results, currentSort);

      displayedSequences = sorted;
      loadingState.isLoading = false;
    } catch (error) {
      loadingState.isLoading = false;
      loadingState.error =
        error instanceof Error ? error.message : "Search failed";
    }
  }

  async function selectSequence(sequence: BrowseSequenceMetadata) {
    selectedSequence = sequence;

    // 💾 SAVE SELECTION STATE: Persist selected sequence for cross-session memory
    await stateManager.saveSelectionState(sequence.id, null);
    console.log("💾 Selection state saved:", sequence.id);
  }

  async function clearSelection() {
    selectedSequence = null;

    // 💾 CLEAR SELECTION STATE: Remove saved selection state
    await stateManager.saveSelectionState(null, null);
    console.log("🗑️ Selection state cleared");
  }

  async function backToFilters() {
    navigationMode = NavigationMode.FILTER_SELECTION;
    currentFilter = null;
    searchQuery = "";
    displayedSequences = allSequences;

    // 💾 CLEAR FILTER STATE: Remove saved filter state when going back to filters
    await stateManager.saveFilterState(null, null);
    console.log("🗑️ Filter state cleared");
  }

  async function preloadThumbnails(sequences: BrowseSequenceMetadata[]) {
    try {
      const thumbnailsToPreload = sequences
        .slice(0, 20) // Preload first 20 thumbnails
        .flatMap((seq) =>
          seq.thumbnails.map((thumb) => ({
            sequenceId: seq.id,
            thumbnailPath: thumb,
          })),
        );

      // Preload thumbnails individually
      for (const thumbnail of thumbnailsToPreload) {
        await thumbnailService.preloadThumbnail(
          thumbnail.sequenceId,
          thumbnail.thumbnailPath,
        );
      }
    } catch (error) {
      console.warn("Failed to preload thumbnails:", error);
    }
  }

  function getThumbnailUrl(sequenceId: string, thumbnailPath: string): string {
    return thumbnailService.getThumbnailUrl(sequenceId, thumbnailPath);
  }

  function updateDisplaySettings(settings: Partial<BrowseDisplayState>) {
    displayState = { ...displayState, ...settings };
  }

  function clearError() {
    loadingState.error = null;
  }

  // ✅ RUNES EFFECT: Auto-preload thumbnails when sequences change
  $effect(() => {
    if (displayedSequences.length > 0) {
      preloadThumbnails(displayedSequences);
    }
  });

  // Helper function for derived sections
  function groupSequencesBySection(
    sequences: BrowseSequenceMetadata[],
    sortMethod: SortMethod,
  ): Record<string, BrowseSequenceMetadata[]> {
    const sections: Record<string, BrowseSequenceMetadata[]> = {};

    for (const sequence of sequences) {
      const sectionKey = getSectionKey(sequence, sortMethod);
      if (!sections[sectionKey]) {
        sections[sectionKey] = [];
      }
      sections[sectionKey].push(sequence);
    }

    return sections;
  }

  function getSectionKey(
    sequence: BrowseSequenceMetadata,
    sortMethod: SortMethod,
  ): string {
    switch (sortMethod) {
      case SortMethodEnum.ALPHABETICAL:
        return sequence.word[0]?.toUpperCase() || "#";
      case SortMethodEnum.DIFFICULTY_LEVEL:
        return sequence.difficultyLevel || "Unknown";
      case SortMethodEnum.AUTHOR:
        return sequence.author || "Unknown";
      case SortMethodEnum.SEQUENCE_LENGTH: {
        const length = sequence.sequenceLength || 0;
        if (length <= 4) return "3-4 beats";
        if (length <= 6) return "5-6 beats";
        if (length <= 8) return "7-8 beats";
        return "9+ beats";
      }
      default:
        return "All";
    }
  }

  // Advanced browse methods
  async function loadFavorites() {
    try {
      const favoriteIds = await favoritesService.getFavorites();
      favorites = new Set(favoriteIds);
    } catch (error) {
      console.warn("Failed to load favorites:", error);
    }
  }

  async function toggleFavorite(sequenceId: string) {
    try {
      await favoritesService.toggleFavorite(sequenceId);
      if (favorites.has(sequenceId)) {
        favorites.delete(sequenceId);
      } else {
        favorites.add(sequenceId);
      }
      // Update navigation sections
      await generateNavigationSections();
    } catch (error) {
      console.error("Failed to toggle favorite:", error);
    }
  }

  async function generateNavigationSections() {
    try {
      const sections = await navigationService.generateNavigationSections(
        allSequences,
        Array.from(favorites),
      );
      navigationSections = sections;
    } catch (error) {
      console.error("Failed to generate navigation sections:", error);
    }
  }

  async function generateSequenceSections() {
    try {
      const sections = await sectionService.organizeSections(
        displayedSequences,
        sectionConfiguration,
      );
      sequenceSections = sections;
    } catch (error) {
      console.error("Failed to generate sequence sections:", error);
    }
  }

  function toggleNavigationSection(sectionId: string) {
    navigationSections = navigationService.toggleSectionExpansion(
      sectionId,
      navigationSections,
    );
  }

  function setActiveNavigationItem(sectionId: string, itemId: string) {
    navigationSections = navigationService.setActiveItem(
      sectionId,
      itemId,
      navigationSections,
    );
  }

  async function filterSequencesByNavigation(
    sectionType: NavigationSection["type"],
    item: NavigationItem,
  ): Promise<BrowseSequenceMetadata[]> {
    try {
      const filtered = navigationService.getSequencesForNavigationItem(
        item,
        sectionType,
        allSequences,
      );

      // Update displayed sequences
      displayedSequences = filtered;
      filteredSequences = filtered;

      // 💾 SAVE NAVIGATION FILTER STATE: Persist navigation filter for cross-session memory
      const filterType = `navigation_${sectionType}`;
      const filterValue = item.value;
      currentFilter = {
        type: filterType as FilterType,
        value: filterValue as FilterValue,
      };
      await stateManager.saveFilterState(filterType, filterValue);
      console.log("💾 Navigation filter state saved:", {
        type: filterType,
        value: filterValue,
      });

      return filtered;
    } catch (error) {
      console.error("Failed to filter sequences by navigation:", error);
      return [];
    }
  }

  function toggleSequenceSection(sectionId: string) {
    sequenceSections = sectionService.toggleSectionExpansion(
      sectionId,
      sequenceSections,
    );
  }

  async function updateSectionConfiguration(
    updates: Partial<SectionConfiguration>,
  ) {
    sectionConfiguration = sectionService.updateSectionConfiguration(
      sectionConfiguration,
      updates,
    );
    await generateSequenceSections();
  }

  async function prepareDeleteSequence(sequence: BrowseSequenceMetadata) {
    try {
      const confirmationData = await deleteService.prepareDeleteConfirmation(
        sequence,
        allSequences,
      );
      deleteConfirmation = confirmationData;
      showDeleteDialog = true;
    } catch (error) {
      console.error("Failed to prepare delete confirmation:", error);
    }
  }

  async function confirmDeleteSequence() {
    if (!deleteConfirmation) return;

    try {
      const result = await deleteService.deleteSequence(
        deleteConfirmation.sequence.id,
        allSequences,
      );

      if (result.success && deleteConfirmation) {
        const deletedSequenceId = deleteConfirmation.sequence.id;
        // Remove from sequences
        allSequences = allSequences.filter(
          (seq) => seq.id !== deletedSequenceId,
        );
        filteredSequences = filteredSequences.filter(
          (seq) => seq.id !== deletedSequenceId,
        );
        displayedSequences = displayedSequences.filter(
          (seq) => seq.id !== deletedSequenceId,
        );

        // Clear selection if deleted sequence was selected
        if (selectedSequence?.id === deletedSequenceId) {
          selectedSequence = null;
        }

        // Update navigation and sections
        await generateNavigationSections();
        await generateSequenceSections();
      }

      deleteConfirmation = null;
      showDeleteDialog = false;
    } catch (error) {
      console.error("Failed to delete sequence:", error);
    }
  }

  function cancelDeleteSequence() {
    deleteConfirmation = null;
    showDeleteDialog = false;
  }

  return {
    // ✅ REACTIVE STATE GETTERS
    get allSequences() {
      return allSequences;
    },
    get displayedSequences() {
      return displayedSequences;
    },
    get selectedSequence() {
      return selectedSequence;
    },
    get currentFilter() {
      return currentFilter;
    },
    get currentSort() {
      return currentSort;
    },
    get navigationMode() {
      return navigationMode;
    },
    get searchQuery() {
      return searchQuery;
    },

    // Advanced state getters
    get favorites() {
      return favorites;
    },
    get navigationSections() {
      return navigationSections;
    },
    get sequenceSections() {
      return sequenceSections;
    },
    get sectionConfiguration() {
      return sectionConfiguration;
    },
    get deleteConfirmation() {
      return deleteConfirmation;
    },
    get showDeleteDialog() {
      return showDeleteDialog;
    },

    // ✅ DERIVED STATE GETTERS
    get isLoading() {
      return isLoading;
    },
    get hasSequences() {
      return hasSequences;
    },
    get hasError() {
      return hasError;
    },
    get sequenceCount() {
      return sequenceCount;
    },
    get sortedSections() {
      return sortedSections;
    },
    get loadingState() {
      return loadingState;
    },
    get displayState() {
      return displayState;
    },

    // Advanced derived getters
    get favoritesCount() {
      return favoritesCount;
    },
    get hasNavigationSections() {
      return hasNavigationSections;
    },
    get hasSequenceSections() {
      return hasSequenceSections;
    },
    get sectionStatistics() {
      return sectionStatistics;
    },

    // ✅ ACTION METHODS
    loadAllSequences,
    applyFilter,
    updateSort,
    searchSequences,
    selectSequence,
    clearSelection,
    backToFilters,
    getThumbnailUrl,
    updateDisplaySettings,
    clearError,

    // Advanced action methods
    loadFavorites,
    toggleFavorite,
    generateNavigationSections,
    generateSequenceSections,
    toggleNavigationSection,
    setActiveNavigationItem,
    filterSequencesByNavigation,
    toggleSequenceSection,
    updateSectionConfiguration,
    prepareDeleteSequence,
    confirmDeleteSequence,
    cancelDeleteSequence,
  };
}

export type BrowseState = ReturnType<typeof createBrowseState>;
