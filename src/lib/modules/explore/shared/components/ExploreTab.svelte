<script lang="ts">
  import type { IDeviceDetector, SequenceData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import type { ResponsiveSettings } from "$shared/device/domain/models/device-models";
  import { onMount } from "svelte";
  import { openSpotlightViewer } from "../../../../shared/application/state/app-state.svelte";
  import { navigationState } from "../../../../shared/navigation/state/navigation-state.svelte";
  import ErrorBanner from "../../../create/shared/components/ErrorBanner.svelte";

  import type { IExploreThumbnailService } from "../../display";
  import { SequenceDisplayPanel } from "../../display/components";
  import FilterModal from "../../filtering/components/FilterModal.svelte";
  import CompactFilterPanel from "../../filtering/components/CompactFilterPanel.svelte";
  import { SimpleNavigationSidebar } from "../../navigation/components";
  import UsersExplorePanel from "../../users/components/UsersExplorePanel.svelte";
  import CollectionsExplorePanel from "../../collections/components/CollectionsExplorePanel.svelte";
  import { createExploreState } from "../state/explore-state-factory.svelte";
  import ExploreDeleteDialog from "./ExploreDeleteDialog.svelte";
  import ExploreLayout from "./ExploreLayout.svelte";

  type ExploreTabType = "sequences" | "users" | "collections";

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
  let activeTab = $state<ExploreTabType>("sequences");
  // Remove isInitialized blocking state - show UI immediately with skeletons

  // Services
  let deviceDetector: IDeviceDetector | null = null;

  // Reactive responsive settings from DeviceDetector
  let responsiveSettings = $state<ResponsiveSettings | null>(null);

  // ✅ PURE RUNES: Portrait mode detection using DeviceDetector
  const isPortraitMobile = $derived(
    responsiveSettings?.isMobile &&
      responsiveSettings?.orientation === "portrait"
  );

  // ✅ SYNC WITH BOTTOM NAVIGATION STATE
  // This effect syncs the local tab state with the global navigation state
  $effect(() => {
    const navTab = navigationState.activeTab;

    // Map navigation state to local explore tab
    if (navTab === "sequences" || navTab === "explore") {
      activeTab = "sequences";
    } else if (navTab === "users") {
      activeTab = "users";
    } else if (navTab === "collections") {
      activeTab = "collections";
    }
  });

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
    openSpotlightViewer(sequence, thumbnailService);

    // Also update URL for sharing/bookmarking
    import("$shared/navigation/utils/sheet-router").then(
      ({ openSpotlight }) => {
        openSpotlight(sequence.id);
      }
    );
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

  onMount(() => {
    console.log("✅ ExploreTab: Mounted");

    // Initialize DeviceDetector service
    let cleanup: (() => void) | undefined;
    try {
      deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);
      responsiveSettings = deviceDetector.getResponsiveSettings();

      // Store cleanup function from onCapabilitiesChanged
      cleanup = deviceDetector.onCapabilitiesChanged(() => {
        responsiveSettings = deviceDetector!.getResponsiveSettings();
      });
    } catch (error) {
      console.warn("ExploreTab: Failed to resolve DeviceDetector", error);
    }

    // Load initial data through gallery state (non-blocking)
    // UI shows immediately with skeletons while data loads
    galleryState
      .loadAllSequences()
      .then(() => {
        console.log("✅ ExploreTab: Data loaded");
      })
      .catch((err) => {
        console.error("❌ ExploreTab: Data loading failed:", err);
        error =
          err instanceof Error
            ? err.message
            : "Failed to load gallery sequences";
      });

    // Return cleanup function if it exists
    return cleanup;
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
<div class="explore-content">
  <!-- Tab Content - Bottom navigation controls the active tab -->
  <div class="tab-content">
    {#if activeTab === "sequences"}
      <ExploreLayout>
        {#snippet sortControls()}
          <CompactFilterPanel
            currentFilter={galleryState.currentFilter}
            onFilterChange={galleryState.handleFilterChange}
            onOpenAdvanced={galleryState.openFilterModal}
          />
        {/snippet}

        {#snippet navigationSidebar()}
          <SimpleNavigationSidebar
            currentSortMethod={galleryState.currentSortMethod}
            availableSections={galleryState.availableNavigationSections}
            onSectionClick={galleryState.scrollToSection}
            isHorizontal={isPortraitMobile || false}
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
        availableSequenceLengths={galleryState.availableSequenceLengths}
        onFilterChange={galleryState.handleFilterChange}
        onClose={galleryState.closeFilterModal}
      />
    {:else if activeTab === "users"}
      <UsersExplorePanel />
    {:else if activeTab === "collections"}
      <CollectionsExplorePanel />
    {/if}
  </div>
</div>

<style>
  .explore-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
  }

  .tab-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    min-height: 0;
  }
</style>
