<!--
Enhanced Browse Tab with Unified Panel Management

Integrates panel management service with runes for:
- Unified collapse/expand logic for both panels
- Splitter-based resizing
- Persistent panel state
- Reactive UI updates
-->
<script lang="ts">
  import type {
    IBrowsePanelManager,
    IBrowseService,
    IDeleteService,
    IFavoritesService,
    IFilterPersistenceService,
    INavigationService,
    ISectionService,
    ISequenceIndexService,
    IThumbnailService,
  } from "$contracts";
  import type { SequenceData } from "$domain";
  import { NavigationMode } from "$domain";
  import { resolve, TYPES } from "$lib/services/inversify/container";
  import {
    BROWSE_TAB_PANEL_CONFIGS,
    createBrowseState,
    createPanelState,
  } from "$state";
  import { onDestroy, onMount } from "svelte";
  // Enhanced components
  import BrowseLayout from "./BrowseLayout.svelte";
  import NavigationSidebar from "./NavigationSidebar.svelte";
  // Existing components
  import DeleteConfirmationDialog from "./DeleteConfirmationDialog.svelte";
  import ErrorBanner from "./ErrorBanner.svelte";
  import FilterSelectionPanel from "./FilterSelectionPanel.svelte";
  import FullscreenSequenceViewer from "./FullscreenSequenceViewer.svelte";
  import LoadingOverlay from "./BrowseLoadingOverlay.svelte";
  import PanelContainer from "./PanelContainer.svelte";
  import SequenceBrowserPanel from "./browser/SequenceBrowserPanel.svelte";
  // Event handlers
  import { createBrowseEventHandlers } from "./browse-event-handlers";
  import { createNavigationEventHandlers } from "./navigation-event-handlers";

  // ✅ RESOLVE SERVICES: Get services from DI container
  const browseService = resolve(TYPES.IBrowseService) as IBrowseService;
  const thumbnailService = resolve(
    TYPES.IThumbnailService
  ) as IThumbnailService;
  const sequenceIndexService = resolve<ISequenceIndexService>(
    TYPES.ISequenceIndexService
  );
  const favoritesService = resolve(
    TYPES.IFavoritesService
  ) as IFavoritesService;
  const navigationService = resolve(
    TYPES.INavigationService
  ) as INavigationService;
  const filterPersistenceService = resolve<IFilterPersistenceService>(
    TYPES.IFilterPersistenceService
  );
  const sectionService = resolve(TYPES.ISectionService) as ISectionService;
  const deleteService = resolve(TYPES.IDeleteService) as IDeleteService;
  const panelManagementService = resolve<IBrowsePanelManager>(
    TYPES.IPanelManagementService
  );

  // ✅ REGISTER PANELS IMMEDIATELY: Configure panel management before creating state
  panelManagementService.registerPanel(
    "navigation",
    BROWSE_TAB_PANEL_CONFIGS.navigation
  );

  // ✅ CREATE STATE MANAGERS: Runes-based reactive state
  const browseState = createBrowseState(
    browseService,
    thumbnailService,
    sequenceIndexService,
    favoritesService,
    navigationService,
    filterPersistenceService,
    sectionService,
    deleteService
  );

  const panelState = createPanelState(panelManagementService);

  // ✅ PURE RUNES: Local UI state
  let currentPanelIndex = $state(0); // 0 = filter selection, 1 = sequence browser
  let showFullscreenViewer = $state(false); // Fullscreen sequence viewer state
  let fullscreenSequence = $state<SequenceData | undefined>(undefined); // Current sequence for fullscreen

  // ✅ DERIVED RUNES: Computed UI state from browse state
  let selectedFilter = $derived(browseState.currentFilter);
  let isLoading = $derived(browseState.isLoading);
  let hasError = $derived(browseState.hasError);
  let sequences = $derived(browseState.displayedSequences);
  let navigationMode = $derived(browseState.navigationMode);
  let navigationSections = $derived(browseState.navigationSections);
  let deleteConfirmation = $derived(browseState.deleteConfirmation);
  let showDeleteDialog = $derived(browseState.showDeleteDialog);

  // ✅ EFFECT: Sync navigation mode with panel index
  $effect(() => {
    if (navigationMode === NavigationMode.FILTER_SELECTION) {
      currentPanelIndex = 0;
    } else if (navigationMode === NavigationMode.SEQUENCE_BROWSER) {
      currentPanelIndex = 1;
    }
  });

  // Load initial data when component mounts
  onMount(async () => {
    try {
      await browseState.loadAllSequences();
    } catch (error) {
      console.error("❌ Failed to load browse data:", error);
    }
  });

  // Cleanup on destroy
  onDestroy(() => {
    panelState.cleanup();
  });

  // ✅ EVENT HANDLERS: Create event handlers using extracted functions
  const browseEventHandlers = createBrowseEventHandlers(
    browseState,
    (index) => {
      currentPanelIndex = index;
    }
  );

  const navigationEventHandlers = createNavigationEventHandlers(
    browseState,
    (index) => {
      currentPanelIndex = index;
    },
    () => {
      panelState.toggleNavigationCollapse();
    }
  );

  // Destructure handlers for easier use
  const {
    handleFilterSelected,
    handleBackToFilters,
    handleSequenceAction: originalHandleSequenceAction,
    handleConfirmDelete,
    handleCancelDelete,
    handleClearError,
  } = browseEventHandlers;

  const {
    handleNavigationSectionToggle,
    handleNavigationItemClick,
    handleToggleNavigationCollapse,
  } = navigationEventHandlers;

  // ✅ FULLSCREEN HANDLERS
  function handleCloseFullscreen() {
    showFullscreenViewer = false;
    fullscreenSequence = undefined;
  }

  // ✅ SEQUENCE ACTION HANDLER: Handle sequence actions
  function handleSequenceAction(action: string, sequence: SequenceData) {
    if (action === "edit") {
      // Close fullscreen and handle edit
      handleCloseFullscreen();
      originalHandleSequenceAction(action, sequence);
    } else if (action === "save") {
      // Handle save action
      originalHandleSequenceAction(action, sequence);
    } else if (action === "delete") {
      // Close fullscreen and handle delete
      handleCloseFullscreen();
      originalHandleSequenceAction(action, sequence);
    } else if (action === "fullscreen") {
      // Handle fullscreen action
      fullscreenSequence = sequence;
      showFullscreenViewer = true;
    } else {
      // Pass through other actions to original handler
      originalHandleSequenceAction(action, sequence);
    }
  }

  // ✅ RESIZE HANDLERS: For panel width changes
  function handleNavigationResize(width: number) {
    // Additional logic if needed when navigation panel is resized
  }
</script>

<div class="browse-tab">
  <!-- Error banner -->
  <ErrorBanner
    show={hasError}
    message={browseState.loadingState.error || ""}
    onDismiss={handleClearError}
  />

  <!-- Enhanced layout with unified panel management -->
  <BrowseLayout
    {panelState}
    onNavigationResize={handleNavigationResize}
  >
    {#snippet navigationSidebar()}
      <NavigationSidebar
        sections={navigationSections}
        onSectionToggle={handleNavigationSectionToggle}
        onItemClick={handleNavigationItemClick}
        isCollapsed={panelState.isNavigationCollapsed}
        onToggleCollapse={handleToggleNavigationCollapse}
      />
    {/snippet}

    {#snippet centerPanel()}
      {#if currentPanelIndex === 0}
        <!-- Filter Selection Panel -->
        <PanelContainer panelName="filter-selection">
          <FilterSelectionPanel onFilterSelected={handleFilterSelected} />
        </PanelContainer>
      {:else if currentPanelIndex === 1}
        <!-- Sequence Browser Panel -->
        <PanelContainer panelName="sequence-browser">
          <SequenceBrowserPanel
            filter={selectedFilter}
            {sequences}
            {isLoading}
            onBackToFilters={handleBackToFilters}
            onAction={handleSequenceAction}
          />
        </PanelContainer>
      {/if}
    {/snippet}
  </BrowseLayout>

  <!-- Loading overlay for initial load -->
  <LoadingOverlay
    show={isLoading && sequences.length === 0}
    message="Loading sequence library..."
    detail={browseState.loadingState.currentOperation}
  />

  <!-- Delete Confirmation Dialog -->
  <DeleteConfirmationDialog
    confirmationData={deleteConfirmation}
    show={showDeleteDialog}
    onConfirm={handleConfirmDelete}
    onCancel={handleCancelDelete}
  />

  <!-- Fullscreen Sequence Viewer -->
  <FullscreenSequenceViewer
    show={showFullscreenViewer}
    {...fullscreenSequence ? { sequence: fullscreenSequence } : {}}
    {thumbnailService}
    onClose={handleCloseFullscreen}
    onAction={handleSequenceAction}
  />
</div>

<style>
  .browse-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    background: transparent;
    position: relative;
  }

  /* Global panel animation support */
  :global(.browse-tab .panel-transition) {
    transition: all var(--transition-normal);
  }

  /* Ensure proper stacking for overlays */
  .browse-tab :global(.loading-overlay),
  .browse-tab :global(.error-banner),
  .browse-tab :global(.delete-dialog),
  .browse-tab :global(.fullscreen-viewer) {
    z-index: 1000;
  }

  /* Panel state debugging (remove in production) */
  .browse-tab::after {
    content: "";
    position: fixed;
    top: 10px;
    right: 10px;
    width: 10px;
    height: 10px;
    background: var(--color-success);
    border-radius: 50%;
    z-index: 9999;
    opacity: 0;
    transition: opacity 0.3s;
  }
</style>
