<script lang="ts">
  import type { IDeviceDetector, SequenceData } from "$shared";
  import { resolve, TYPES, AnimationSheetCoordinator } from "$shared";
  import type { ResponsiveSettings } from "$shared/device/domain/models/device-models";
  import { onMount, setContext } from "svelte";
  import { fade } from "svelte/transition";
  import { navigationState } from "../../../../shared/navigation/state/navigation-state.svelte";
  import ErrorBanner from "../../../create/shared/components/ErrorBanner.svelte";

  import type { IExploreThumbnailService } from "../../display";
  import UsersExplorePanel from "../../users/components/UsersExplorePanel.svelte";
  import CollectionsExplorePanel from "../../collections/components/CollectionsExplorePanel.svelte";
  import { createExploreState } from "../state/explore-state-factory.svelte";
  import ExploreDeleteDialog from "./ExploreDeleteDialog.svelte";
  import ExploreSequencesTab from "./ExploreSequencesTab.svelte";
  import { explorerScrollState } from "../state/ExplorerScrollState.svelte";
  import { ExplorerScrollBehaviorService } from "../services/implementations/ExplorerScrollBehaviorService";
  import { desktopSidebarState } from "../../../../shared/layout/desktop-sidebar-state.svelte";
  import { galleryControlsManager } from "../state/gallery-controls-state.svelte";
  import { useExploreHandlers } from "../composables/useExploreHandlers.svelte";

  type ExploreModuleType = "sequences" | "users" | "collections";

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
  let activeTab = $state<ExploreModuleType>("sequences");
  let showAnimator = $state<boolean>(false);

  // Services
  let deviceDetector: IDeviceDetector | null = null;

  // Reactive responsive settings from DeviceDetector
  let responsiveSettings = $state<ResponsiveSettings | null>(null);

  // ✅ PURE RUNES: Device detection for UI adaptation
  const isMobile = $derived(
    responsiveSettings?.isMobile || responsiveSettings?.isTablet || false
  );

  // Desktop sidebar visibility (to hide top section when sidebar is visible)
  const showDesktopSidebar = $derived(desktopSidebarState.isVisible);

  // ✅ Calculate drawer width for 60/40 split (grid gets 60%, detail panel gets 40% of remaining space)
  // Use actual sidebar width which reflects collapsed state (220px expanded, 64px collapsed, 0px hidden)
  const sidebarWidth = $derived(
    showDesktopSidebar ? desktopSidebarState.width : 0
  );
  // Keep drawer width constant to avoid flashing when opening/closing
  const drawerWidth = $derived(
    !isMobile
      ? `calc((100vw - ${sidebarWidth}px) * 0.4)` // Detail panel takes 40% of remaining space
      : "min(600px, 90vw)"
  );

  // Debug: Log drawer width changes
  $effect(() => {
    console.log(
      "🔧 Drawer width updated:",
      drawerWidth,
      "| Sidebar:",
      sidebarWidth,
      "px",
      "| Collapsed:",
      desktopSidebarState.isCollapsed
    );
  });

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

  // ✅ SYNC ANIMATION MODAL STATE
  // This effect syncs the local showAnimator state with galleryState
  $effect(() => {
    showAnimator = galleryState.isAnimationModalOpen;
  });

  // ✅ SYNC CLOSE HANDLER
  // When showAnimator is closed, inform galleryState
  $effect(() => {
    if (!showAnimator && galleryState.isAnimationModalOpen) {
      galleryState.closeAnimationModal();
    }
  });

  // ============================================================================
  // SCROLL BEHAVIOR (UI Visibility Control)
  // ============================================================================

  // Create scroll behavior service instance
  const scrollBehaviorService = new ExplorerScrollBehaviorService(
    explorerScrollState
  );

  // Track last scroll position for the container
  let lastContainerScrollTop = $state(0);

  // Reactive UI visibility state
  const isUIVisible = $derived(explorerScrollState.isUIVisible);

  // Debug: Log sidebar state changes
  $effect(() => {
    console.log(
      "📊 Sidebar state:",
      showDesktopSidebar,
      "| isVisible:",
      desktopSidebarState.isVisible
    );
  });

  // Provide scroll visibility context for child components
  setContext("explorerScrollVisibility", {
    getVisible: () => explorerScrollState.isUIVisible,
    hide: () => scrollBehaviorService.forceHideUI(),
    show: () => scrollBehaviorService.forceShowUI(),
  });

  // Provide gallery state for TopBar controls via global reactive state
  // (Context doesn't work for siblings, so we use module-level $state)
  $effect(() => {
    galleryControlsManager.set({
      get currentFilter() {
        return galleryState.currentFilter;
      },
      get currentSortMethod() {
        return galleryState.currentSortMethod;
      },
      get availableNavigationSections() {
        return galleryState.availableNavigationSections;
      },
      onFilterChange: galleryState.handleFilterChange,
      onSortMethodChange: (method: string) => galleryState.handleSortChange(method as any, "asc"),
      scrollToSection: galleryState.scrollToSection,
      openFilterModal: () => galleryState.openFilterModal(),
    });
  });

  // Handle scroll events from the scrollable container
  function handleContainerScroll(event: CustomEvent<{ scrollTop: number }>) {
    const { scrollTop } = event.detail;
    scrollBehaviorService.handleContainerScroll(
      scrollTop,
      lastContainerScrollTop
    );
    lastContainerScrollTop = scrollTop;
  }

  // ============================================================================
  // EVENT HANDLERS (Coordination)
  // ============================================================================

  const handlers = useExploreHandlers({
    galleryState,
    setSelectedSequence: (seq) => (selectedSequence = seq),
    setDeleteConfirmationData: (data) => (deleteConfirmationData = data),
    setError: (err) => (error = err),
    thumbnailService,
  });

  // ============================================================================
  // LIFECYCLE (Coordination)
  // ============================================================================

  onMount(() => {
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
      console.warn("ExploreModule: Failed to resolve DeviceDetector", error);
    }

    // Load initial data through gallery state (non-blocking)
    // UI shows immediately with skeletons while data loads
    galleryState
      .loadAllSequences()
      .then(() => {
        // console.log("✅ ExploreModule: Data loaded");
      })
      .catch((err) => {
        console.error("❌ ExploreModule: Data loading failed:", err);
        error =
          err instanceof Error
            ? err.message
            : "Failed to load gallery sequences";
      });

    // Return cleanup function
    return () => {
      cleanup?.();
      galleryControlsManager.clear();
    };
  });
</script>

<!-- Error banner -->
{#if error}
  <ErrorBanner
    message={error}
    onDismiss={handlers.handleErrorDismiss}
    onRetry={handlers.handleRetry}
  />
{/if}

<!-- Delete confirmation dialog -->
{#if deleteConfirmationData}
  <ExploreDeleteDialog
    show={true}
    confirmationData={deleteConfirmationData}
    onConfirm={() => handlers.handleDeleteConfirm(deleteConfirmationData)}
    onCancel={handlers.handleDeleteCancel}
  />
{/if}

<!-- Animation Sheet Coordinator -->
<AnimationSheetCoordinator
  sequence={galleryState.sequenceToAnimate}
  bind:isOpen={showAnimator}
/>

<!-- Main layout - shows immediately with skeletons while data loads -->
<div class="explore-content">
  <!-- Tab Content - Bottom navigation controls the active tab -->
  <div class="tab-content">
    {#key activeTab}
      <div class="tab-panel" transition:fade={{ duration: 200 }}>
        {#if activeTab === "sequences"}
          <ExploreSequencesTab
            {isMobile}
            {isUIVisible}
            {showDesktopSidebar}
            {drawerWidth}
            {galleryState}
            {error}
            onSequenceAction={handlers.handleSequenceAction}
            onDetailPanelAction={handlers.handleDetailPanelAction}
            onCloseDetailPanel={handlers.handleCloseDetailPanel}
            onContainerScroll={handleContainerScroll}
          />
        {:else if activeTab === "users"}
          <UsersExplorePanel />
        {:else if activeTab === "collections"}
          <CollectionsExplorePanel />
        {/if}
      </div>
    {/key}
  </div>
</div>

<style>
  .explore-content {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
  }

  .tab-content {
    position: relative;
    flex: 1;
    min-height: 0;
    overflow: hidden;
  }

  .tab-panel {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
</style>
