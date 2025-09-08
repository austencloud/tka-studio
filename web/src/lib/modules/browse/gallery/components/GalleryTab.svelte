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
  // Import layout and UI components
  import type { SequenceData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { showSpotlight } from "../../../../shared/application/state/app-state.svelte";
  import ErrorBanner from "../../../build/shared/components/ErrorBanner.svelte";
  import type { SequenceDeleteConfirmationData } from "../domain";
  import type {
    IFavoritesService,
    IFilterPersistenceService,
    IGalleryPanelManager,
    IGalleryService,
    IGalleryThumbnailService,
    INavigationService,
    ISectionService,
    ISequenceIndexService,
  } from "../services/contracts";
  import type { ISequenceDeleteService } from "../services/contracts/ISequenceDeleteService";
  import { createPanelState } from "../state/gallery-panel-state.svelte";
  import { createBrowseState } from "../state/gallery-state-factory.svelte";
  import DeleteConfirmationDialog from "./GalleryDeleteConfirmationDialog.svelte";
  import GalleryLayout from "./GalleryLayout.svelte";
  import BrowseLoadingOverlay from "./GalleryLoadingOverlay.svelte";
  import GalleryPanel from "./GalleryPanel.svelte";
  import NavigationSidebar from "./NavigationSidebar.svelte";

  // ============================================================================
  // SERVICE RESOLUTION
  // ============================================================================

  const galleryService = resolve(TYPES.IGalleryService) as IGalleryService;
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
  const deleteService = resolve(
    TYPES.IDeleteService
  ) as ISequenceDeleteService;
  const panelManager = resolve(
    TYPES.IGalleryPanelManager
  ) as IGalleryPanelManager;

  // ============================================================================
  // STATE MANAGEMENT
  // ============================================================================

  const browseState = createBrowseState(
    galleryService,
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
  let selectedSequence = $state<SequenceData | null>(null);
  let deleteConfirmationData = $state<SequenceDeleteConfirmationData | null>(
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
    console.log(
      "🎬 BrowseTab: handleSequenceAction called with:",
      action,
      "for sequence:",
      sequence.id
    );
    switch (action) {
      case "select":
        console.log("📋 BrowseTab: Handling select action");
        handleSequenceSelect(sequence);
        break;
      case "delete":
        console.log("🗑️ BrowseTab: Handling delete action");
        handleSequenceDelete(sequence);
        break;
      case "fullscreen":
        handleSpotlightView(sequence);
        break;
      case "favorite":
        console.log("⭐ BrowseTab: Handling favorite action");
        browseState.toggleFavorite(sequence.id);
        break;
      default:
        console.warn("⚠️ BrowseTab: Unknown action:", action);
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

  function handleSpotlightView(sequence: SequenceData) {
    showSpotlight(sequence, thumbnailService);
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
    <GalleryLayout {panelState} onNavigationResize={handleNavigationResize}>
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
    </GalleryLayout>
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
