<!--
Enhanced Browse Tab with Unified Panel Management

Integrates panel management service with runes for:
- Unified collapse/expand logic for both panels
- Splitter-based resizing
- Persistent panel state
- Reactive UI updates
-->
<script lang="ts">
  import type { SequenceData } from "$shared/domain/core/models/sequence/SequenceData";
  import { NavigationMode } from "$shared/domain/enums/enums";
  import { resolve, TYPES } from "$shared/inversify/container";
  // TEMPORARY: Service interfaces commented out until container is restored
  // import type {
  //   IBrowsePanelManager,
  //   IBrowseService,
  //   IDeleteService,
  //   IFavoritesService,
  //   IFilterPersistenceService,
  //   INavigationService,
  //   ISectionService,
  //   ISequenceIndexService,
  //   IThumbnailService,
  // } from "$services";
  import {
    BROWSE_TAB_PANEL_CONFIGS,
    createBrowseState,
    createPanelState,
  } from "$shared/state/browse/browse-state-factory.svelte";
  import { onDestroy, onMount } from "svelte";

  // Import layout and UI components
  import BrowseLayout from "./BrowseLayout.svelte";
  import NavigationSidebar from "./NavigationSidebar.svelte";
  import PanelContainer from "./PanelContainer.svelte";
  import BrowseLoadingOverlay from "./BrowseLoadingOverlay.svelte";
  import DeleteConfirmationDialog from "./DeleteConfirmationDialog.svelte";
  import ErrorBanner from "./ErrorBanner.svelte";
  import FullscreenSequenceViewer from "./FullscreenSequenceViewer.svelte";

  // ============================================================================
  // SERVICE RESOLUTION - TEMPORARY DISABLED
  // ============================================================================

  // TEMPORARY: All service resolution commented out until container is restored
  // const browseService = resolve(TYPES.IBrowseService) as IBrowseService;
  // const thumbnailService = resolve(TYPES.IThumbnailService) as IThumbnailService;
  // const sequenceIndexService = resolve(TYPES.ISequenceIndexService) as ISequenceIndexService;
  // const favoritesService = resolve(TYPES.IFavoritesService) as IFavoritesService;
  // const navigationService = resolve(TYPES.INavigationService) as INavigationService;
  // const filterPersistenceService = resolve(TYPES.IFilterPersistenceService) as IFilterPersistenceService;
  // const sectionService = resolve(TYPES.ISectionService) as ISectionService;
  // const deleteService = resolve(TYPES.IDeleteService) as IDeleteService;
  // const panelManager = resolve(TYPES.IBrowsePanelManager) as IBrowsePanelManager;

  // ============================================================================
  // STATE MANAGEMENT - TEMPORARY DISABLED
  // ============================================================================

  // TEMPORARY: State creation commented out until services are restored
  // const browseState = createBrowseState(
  //   browseService,
  //   thumbnailService,
  //   sequenceIndexService,
  //   favoritesService,
  //   navigationService,
  //   filterPersistenceService,
  //   sectionService,
  //   deleteService
  // );

  // const panelState = createPanelState(panelManager, BROWSE_TAB_PANEL_CONFIGS);

  // ============================================================================
  // COMPONENT STATE - TEMPORARY PLACEHOLDERS
  // ============================================================================

  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let showDeleteDialog = $state(false);
  let showFullscreenViewer = $state(false);
  let selectedSequence = $state<SequenceData | null>(null);

  // ============================================================================
  // EVENT HANDLERS - TEMPORARY DISABLED
  // ============================================================================

  function handleSequenceSelect(sequence: SequenceData) {
    selectedSequence = sequence;
    console.log(
      "✅ BrowseTab: Sequence selected (services disabled):",
      sequence
    );
  }

  function handleSequenceDelete(sequence: SequenceData) {
    selectedSequence = sequence;
    showDeleteDialog = true;
    console.log(
      "✅ BrowseTab: Delete requested (services disabled):",
      sequence
    );
  }

  function handleDeleteConfirm() {
    if (selectedSequence) {
      console.log(
        "✅ BrowseTab: Delete confirmed (services disabled):",
        selectedSequence
      );
      // deleteService.deleteSequence(selectedSequence.id);
    }
    showDeleteDialog = false;
    selectedSequence = null;
  }

  function handleDeleteCancel() {
    showDeleteDialog = false;
    selectedSequence = null;
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
    console.log("✅ BrowseTab: Navigation resized (services disabled):", width);
    // panelState.updateNavigationWidth(width);
  }

  // ============================================================================
  // LIFECYCLE - TEMPORARY DISABLED
  // ============================================================================

  onMount(async () => {
    console.log("✅ BrowseTab: Mounted (services temporarily disabled)");

    // TEMPORARY: All initialization commented out
    try {
      // Initialize browse state
      // await browseState.initialize();

      // Load initial data
      // await browseState.loadSequences();

      console.log("✅ BrowseTab: Initialization complete (placeholder)");
    } catch (err) {
      console.error("❌ BrowseTab: Initialization failed:", err);
      error =
        err instanceof Error ? err.message : "Failed to initialize browse tab";
    }
  });

  onDestroy(() => {
    console.log("✅ BrowseTab: Cleanup (services disabled)");
    // browseState?.cleanup();
    // panelState?.cleanup();
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
    <!-- TEMPORARY: Simplified layout message -->
    <div class="temporary-message">
      <h2>📚 Browse Tab</h2>
      <p><strong>Status:</strong> Import paths fixed ✅</p>
      <p>Services temporarily disabled during import migration.</p>
      <p>This tab will be fully functional once the container is restored.</p>
      <div class="feature-list">
        <h3>Features (will be restored):</h3>
        <ul>
          <li>✅ Sequence browsing and filtering</li>
          <li>✅ Thumbnail grid with metadata</li>
          <li>✅ Fullscreen sequence viewer</li>
          <li>✅ Favorites management</li>
          <li>✅ Advanced search and sorting</li>
          <li>✅ Panel resizing and state persistence</li>
        </ul>
      </div>
    </div>

    <!-- ORIGINAL LAYOUT (commented out until services restored) -->
    <!-- <BrowseLayout
      {panelState}
      onNavigationResize={handleNavigationResize}
    >
      {#snippet navigationSidebar()}
        <NavigationSidebar
          navigationState={browseState.navigation}
          onNavigationChange={browseState.handleNavigationChange}
        />
      {/snippet}

      {#snippet centerPanel()}
        <PanelContainer
          browseState={browseState}
          onSequenceSelect={handleSequenceSelect}
          onSequenceDelete={handleSequenceDelete}
          onFullscreenView={handleFullscreenView}
        />
      {/snippet}
    </BrowseLayout> -->
  </div>

  <!-- Loading overlay -->
  {#if isLoading}
    <BrowseLoadingOverlay message="Loading sequences..." />
  {/if}

  <!-- Delete confirmation dialog -->
  {#if showDeleteDialog && selectedSequence}
    <DeleteConfirmationDialog
      sequence={selectedSequence}
      onConfirm={handleDeleteConfirm}
      onCancel={handleDeleteCancel}
    />
  {/if}

  <!-- Fullscreen viewer -->
  {#if showFullscreenViewer && selectedSequence}
    <FullscreenSequenceViewer
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

  .temporary-message {
    text-align: center;
    padding: 2rem;
    background: var(--color-surface-secondary, #f5f5f5);
    border-radius: 8px;
    border: 2px dashed var(--color-border, #ccc);
    max-width: 600px;
    margin: 2rem;
  }

  .temporary-message h2 {
    color: var(--color-text-primary, #333);
    margin-bottom: 1rem;
  }

  .temporary-message p {
    color: var(--color-text-secondary, #666);
    margin-bottom: 0.5rem;
  }

  .feature-list {
    margin-top: 1.5rem;
    text-align: left;
  }

  .feature-list h3 {
    color: var(--color-text-primary, #333);
    margin-bottom: 0.5rem;
  }

  .feature-list ul {
    color: var(--color-text-secondary, #666);
    padding-left: 1.5rem;
  }

  .feature-list li {
    margin-bottom: 0.25rem;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .temporary-message {
      margin: 1rem;
      padding: 1.5rem;
    }
  }
</style>
