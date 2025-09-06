<!--
Enhanced Browse Tab with Unified Panel Management

Integrates panel management service with runes for:
- Unified collapse/expand logic for both panels
- Splitter-based resizing
- Persistent panel state
- Reactive UI updates
-->
<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import SpotlightViewer from "./../../spotlight/components/SpotlightViewer.svelte";
  // Import layout and UI components
  import type { SequenceData } from "../../../../shared/domain";
  import { resolve, TYPES } from "../../../../shared/inversify";
  import GalleryPanel from "../../gallery/components/GalleryPanel.svelte";
  import NavigationSidebar from "../../gallery/components/NavigationSidebar.svelte";
  import type {
    IDeleteService,
    IFavoritesService,
    IFilterPersistenceService,
    IGalleryPanelManager,
    IGalleryService,
    IGalleryThumbnailService,
    INavigationService,
    ISectionService,
    ISequenceIndexService,
  } from "../../gallery/services/contracts";
  import { createPanelState } from "../../gallery/state/gallery-panel-state.svelte";
  import { createBrowseState } from "../../gallery/state/gallery-state-factory.svelte";
  import type { BrowseDeleteConfirmationData } from "../domain/models";
  import BrowseLayout from "./BrowseLayout.svelte";
  import BrowseLoadingOverlay from "./BrowseLoadingOverlay.svelte";
  import DeleteConfirmationDialog from "./DeleteConfirmationDialog.svelte";
  import ErrorBanner from "./ErrorBanner.svelte";

  // ============================================================================
  // SERVICE RESOLUTION
  // ============================================================================

  const browseService = resolve(TYPES.IGalleryService) as IGalleryService;
  const thumbnailService = resolve(
    TYPES.IGalleryThumbnailService
  ) as IGalleryThumbnailService;
  const sequenceIndexService = resolve(
    TYPES.ISequenceIndexService
  ) as ISequenceIndexService;
  const favoritesService = resolve(
    TYPES.IFavoritesService
  ) as IFavoritesService;
  const navigationService = resolve(
    TYPES.INavigationService
  ) as INavigationService;
  const filterPersistenceService = resolve(
    TYPES.IFilterPersistenceService
  ) as IFilterPersistenceService;
  const sectionService = resolve(TYPES.ISectionService) as ISectionService;
  const deleteService = resolve(TYPES.IDeleteService) as IDeleteService;
  const panelManager = resolve(
    TYPES.IGalleryPanelManager
  ) as IGalleryPanelManager;

  // ============================================================================
  // STATE MANAGEMENT
  // ============================================================================

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

  const panelState = createPanelState(panelManager);

  // ============================================================================
  // COMPONENT STATE
  // ============================================================================

  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let showDeleteDialog = $state(false);
  let showFullscreenViewer = $state(false);
  let selectedSequence = $state<SequenceData | null>(null);
  let deleteConfirmationData = $state<BrowseDeleteConfirmationData | null>(
    null
  );

  // ============================================================================
  // EVENT HANDLERS
  // ============================================================================

  function handleSequenceSelect(sequence: SequenceData) {
    selectedSequence = sequence;
    browseState.selectSequence(sequence);
    console.log("✅ BrowseTab: Sequence selected:", sequence);
  }

  function handleSequenceAction(action: string, sequence: SequenceData) {
    switch (action) {
      case "select":
        handleSequenceSelect(sequence);
        break;
      case "delete":
        handleSequenceDelete(sequence);
        break;
      case "fullscreen":
        handleFullscreenView(sequence);
        break;
      case "favorite":
        browseState.toggleFavorite(sequence.id);
        break;
      default:
        console.warn("✅ BrowseTab: Unknown action:", action);
    }
  }

  async function handleSequenceDelete(sequence: SequenceData) {
    selectedSequence = sequence;
    try {
      // Use the delete service to prepare confirmation data
      const allSequences = browseState.allSequences || [];
      deleteConfirmationData = {
        sequence: sequence,
        relatedSequences: [], // TODO: Calculate related sequences properly
        hasVariations: false, // TODO: Check for variations properly
        willFixVariationNumbers: false, // TODO: Check if variation number fixing is needed
      };
      showDeleteDialog = true;
      console.log("✅ BrowseTab: Delete requested:", sequence);
    } catch (err) {
      console.error(
        "❌ BrowseTab: Failed to prepare delete confirmation:",
        err
      );
      error =
        err instanceof Error
          ? err.message
          : "Failed to prepare delete confirmation";
    }
  }

  async function handleDeleteConfirm() {
    if (selectedSequence && deleteConfirmationData) {
      try {
        console.log("✅ BrowseTab: Delete confirmed:", selectedSequence);
        // TODO: Implement proper delete service call
        // await deleteService.deleteSequence(selectedSequence, browseState.sequences || []);
        // await browseState.loadSequences(); // Reload sequences after delete
      } catch (err) {
        console.error("❌ BrowseTab: Delete failed:", err);
        error =
          err instanceof Error ? err.message : "Failed to delete sequence";
      }
    }
    showDeleteDialog = false;
    selectedSequence = null;
    deleteConfirmationData = null;
  }

  function handleDeleteCancel() {
    showDeleteDialog = false;
    selectedSequence = null;
    deleteConfirmationData = null;
  }

  function handleFullscreenView(sequence: SequenceData) {
    selectedSequence = sequence;
    showFullscreenViewer = true;
  }

  function handleFullscreenClose() {
    showFullscreenViewer = false;
    selectedSequence = null;
  }

  function handleNavigationResize(width: number) {
    console.log("✅ BrowseTab: Navigation resized:", width);
    panelState.setNavigationWidth(width);
  }

  // ============================================================================
  // LIFECYCLE
  // ============================================================================

  onMount(async () => {
    console.log("✅ BrowseTab: Mounted");
    isLoading = true;

    try {
      // Load initial data
      await browseState.loadAllSequences();

      console.log("✅ BrowseTab: Initialization complete");
    } catch (err) {
      console.error("❌ BrowseTab: Initialization failed:", err);
      error =
        err instanceof Error ? err.message : "Failed to initialize browse tab";
    } finally {
      isLoading = false;
    }
  });

  onDestroy(() => {
    console.log("✅ BrowseTab: Cleanup");
    panelState?.cleanup();
  });
</script>

<!-- ============================================================================ -->
<!-- TEMPLATE -->
<!-- ============================================================================ -->

<div class="browse-tab" data-testid="browse-tab">
  <!-- Error display -->
  {#if error}
    <ErrorBanner message={error} onDismiss={() => (error = null)} />
  {/if}

  <!-- Main layout with panels -->
  <div class="browse-content">
    <BrowseLayout {panelState} onNavigationResize={handleNavigationResize}>
      {#snippet navigationSidebar()}
        <NavigationSidebar
          sections={browseState.navigationSections}
          onSectionToggle={browseState.toggleNavigationSection}
          onItemClick={browseState.setActiveGalleryNavigationItem}
        />
      {/snippet}

      {#snippet centerPanel()}
        <GalleryPanel
          sequences={browseState.displayedSequences}
          isLoading={browseState.isLoading}
          onBackToFilters={browseState.backToFilters}
          onAction={handleSequenceAction}
        />
      {/snippet}
    </BrowseLayout>
  </div>

  <!-- Loading overlay -->
  {#if isLoading}
    <BrowseLoadingOverlay message="Loading sequences..." />
  {/if}

  <!-- Delete confirmation dialog -->
  {#if showDeleteDialog && deleteConfirmationData}
    <DeleteConfirmationDialog
      confirmationData={deleteConfirmationData}
      show={showDeleteDialog}
      onConfirm={handleDeleteConfirm}
      onCancel={handleDeleteCancel}
    />
  {/if}

  <!-- Fullscreen viewer -->
  {#if showFullscreenViewer && selectedSequence}
    <SpotlightViewer
      sequence={selectedSequence}
      onClose={handleFullscreenClose}
    />
  {/if}
</div>

<!-- ============================================================================ -->
<!-- STYLES -->
<!-- ============================================================================ -->

<style>
  .browse-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    position: relative;
  }

  .browse-content {
    flex: 1;
    display: flex;
    overflow: hidden;
    justify-content: center;
    align-items: center;
  }
</style>
