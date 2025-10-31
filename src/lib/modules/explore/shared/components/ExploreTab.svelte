<script lang="ts">
  import type { SequenceData } from "$shared";
  import { ErrorBanner, resolve, TYPES } from "$shared";
  import { onDestroy, onMount } from "svelte";
  import { showSpotlight } from "../../../../shared/application/state/app-state.svelte";

  import type { IExploreThumbnailService } from "../../display";
  import { SequenceDisplayPanel } from "../../display/components";
  import SequenceAnimationModal from "../../display/components/SequenceAnimationModal.svelte";
  import FilterModal from "../../filtering/components/FilterModal.svelte";
  import SortControls from "../../filtering/components/SortControls.svelte";
  import { SimpleNavigationSidebar } from "../../navigation/components";
  import { createExploreState } from "../state/explore-state-factory.svelte";
  import ExploreLayout from "./ExploreLayout.svelte";
  import ExploreDeleteDialog from "./ExploreDeleteDialog.svelte";

  // ============================================================================
  // STATE MANAGEMENT (Shared Coordination)
  // ============================================================================

  const galleryState = createExploreState();
  const thumbnailService = resolve<IExploreThumbnailService>(
    TYPES.IExploreThumbnailService
  );

  // ✅ PURE RUNES: Local state
  let selectedSequence = $state<SequenceData | null>(null);
  let deleteConfirmationData = $state<any>(null);
  let error = $state<string | null>(null);
  // Remove isInitialized blocking state - show UI immediately with skeletons

  // ✅ PURE RUNES: Portrait mode detection for navigation layout
  let isPortraitMobile = $state(false);

  // Detect portrait mobile mode (narrow width, portrait orientation)
  function checkPortraitMobile() {
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const isPortrait = viewportHeight > viewportWidth;
    const hasNarrowWidth = viewportWidth < 600;
    isPortraitMobile = isPortrait && hasNarrowWidth;
  }

  // ============================================================================
  // EVENT HANDLERS (Coordination)
  // ============================================================================

  function handleSequenceSelect(sequence: SequenceData) {
    selectedSequence = sequence;
    galleryState.selectSequence(sequence);
    console.log("✅ ExploreTab: Sequence selected:", sequence);
  }

  async function handleSequenceAction(action: string, sequence: SequenceData) {
    console.log(
      "🎬 BrowseTab: handleSequenceAction called with:",
      action,
      "for sequence:",
      sequence.id
    );

    try {
      switch (action) {
        case "select":
          handleSequenceSelect(sequence);
          break;
        case "delete":
          handleSequenceDelete(sequence);
          break;
        case "favorite":
          await galleryState.toggleFavorite(sequence.id);
          break;
        case "fullscreen":
          handleSpotlightView(sequence);
          break;
        case "animate":
          galleryState.openAnimationModal(sequence);
          break;
        default:
          console.warn("⚠️ BrowseTab: Unknown action:", action);
      }
    } catch (err) {
      console.error("❌ BrowseTab: Action failed:", err);
      error =
        err instanceof Error ? err.message : `Failed to ${action} sequence`;
    }
  }

  function handleSequenceDelete(sequence: SequenceData) {
    deleteConfirmationData = {
      sequence: sequence,
      relatedSequences: [],
      totalCount: 1,
    };
  }

  function handleSpotlightView(sequence: SequenceData) {
    console.log("🎭 BrowseTab: Opening spotlight for sequence:", sequence.id);
    showSpotlight(sequence, thumbnailService);
  }

  async function handleDeleteConfirm() {
    if (!deleteConfirmationData?.sequence) return;

    try {
      // TODO: Implement actual delete logic
      console.log(
        "🗑️ BrowseTab: Deleting sequence:",
        deleteConfirmationData.sequence.id
      );
      deleteConfirmationData = null;
      // Refresh the sequence list
      await galleryState.loadAllSequences();
    } catch (err) {
      console.error("❌ BrowseTab: Delete failed:", err);
      error = err instanceof Error ? err.message : "Failed to delete sequence";
    }
  }

  function handleDeleteCancel() {
    deleteConfirmationData = null;
  }

  function handleErrorDismiss() {
    error = null;
  }

  function handleRetry() {
    error = null;
    galleryState.loadAllSequences();
  }

  // ============================================================================
  // LIFECYCLE (Coordination)
  // ============================================================================

  onMount(async () => {
    console.log("✅ ExploreTab: Mounted");

    // Set up portrait mode detection
    checkPortraitMobile();
    window.addEventListener("resize", checkPortraitMobile);
    window.addEventListener("orientationchange", checkPortraitMobile);

    try {
      // Load initial data through gallery state (non-blocking)
      // UI shows immediately with skeletons while data loads
      await galleryState.loadAllSequences();

      console.log("✅ ExploreTab: Data loaded");
    } catch (err) {
      console.error("❌ ExploreTab: Data loading failed:", err);
      error =
        err instanceof Error ? err.message : "Failed to load gallery sequences";
    }
  });

  onDestroy(() => {
    console.log("✅ ExploreTab: Cleanup");
    window.removeEventListener("resize", checkPortraitMobile);
    window.removeEventListener("orientationchange", checkPortraitMobile);
  });
</script>

<!-- Error banner -->
{#if error}
  <ErrorBanner
    show={true}
    message={error}
    onDismiss={handleErrorDismiss}
    onRetry={handleRetry}
  />
{/if}

<!-- Delete confirmation dialog -->
{#if deleteConfirmationData}
  <ExploreDeleteDialog
    show={true}
    confirmationData={deleteConfirmationData}
    onConfirm={handleDeleteConfirm}
    onCancel={handleDeleteCancel}
  />
{/if}

<!-- Main layout - shows immediately with skeletons while data loads -->
<div class="gallery-content">
  <ExploreLayout>
    {#snippet sortControls()}
      <SortControls
        currentSort={galleryState.currentSortMethod}
        sortDirection={galleryState.sortDirection}
        onSortChange={galleryState.handleSortChange}
        onFilterClick={galleryState.openFilterModal}
      />
    {/snippet}

    {#snippet navigationSidebar()}
      <SimpleNavigationSidebar
        currentSortMethod={galleryState.currentSortMethod}
        availableSections={galleryState.availableNavigationSections()}
        onSectionClick={galleryState.scrollToSection}
        isHorizontal={isPortraitMobile}
      />
    {/snippet}

    {#snippet centerPanel()}
      <SequenceDisplayPanel
        sequences={galleryState.displayedSequences}
        sections={galleryState.sequenceSections}
        isLoading={galleryState.isLoading}
        {error}
        showSections={galleryState.showSections}
        onAction={handleSequenceAction}
      />
    {/snippet}
  </ExploreLayout>

  <!-- Filter Modal -->
  <FilterModal
    isOpen={galleryState.isFilterModalOpen}
    currentFilter={galleryState.currentFilter}
    availableSequenceLengths={galleryState.availableSequenceLengths()}
    onFilterChange={galleryState.handleFilterChange}
    onClose={galleryState.closeFilterModal}
  />

  <!-- Animation Modal -->
  <SequenceAnimationModal
    sequence={galleryState.sequenceToAnimate}
    isOpen={galleryState.isAnimationModalOpen}
    onClose={galleryState.closeAnimationModal}
  />
</div>

<style>
  .gallery-content {
    height: 100%;
    /* Removed opacity animation - show immediately for zero-delay experience */
  }
</style>
