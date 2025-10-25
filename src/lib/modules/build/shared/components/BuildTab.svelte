<!--
Build Tab - Main construction interface

Provides two-panel layout matching desktop app:
- Left Panel: Workbench for sequence visualization
- Right Panel: 4-tab interface (Construct, Edit, Generate, Export)

Testing HMR persistence functionality
-->
<script lang="ts">
  import { createComponentLogger, ensureContainerInitialized, ErrorBanner, GridMode, navigationState, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { EditSlidePanel } from "../../edit/components";
  import type { IStartPositionService } from "../../construct/start-position-picker/services/contracts";
  import type { IBuildTabService, ISequencePersistenceService, ISequenceService } from "../services/contracts";
  import { getBuildTabEventService } from "../services/implementations/BuildTabEventService";
  import { createBuildTabState, createConstructTabState } from "../state";
  import LeftPanel from './LeftPanel.svelte';
  import LoadingOverlay from './LoadingOverlay.svelte';
  import RightPanel from './RightPanel.svelte';

  // Debug logger for this component
  const logger = createComponentLogger('BuildTab');

  // Props
  let { onTabAccessibilityChange }: { onTabAccessibilityChange?: (canAccessEditAndExport: boolean) => void } = $props();

  // Services - initialized after container is ready
  let sequenceService: ISequenceService | null = null;
  let sequencePersistenceService: ISequencePersistenceService | null = null;
  let startPositionService: IStartPositionService | null = null;
  let buildTabService: IBuildTabService | null = null;

  // Device detection services for responsive layout
  let deviceDetector: any = null;
  let viewportService: any = null;

  // State - initialized after services are ready
  let buildTabState: any = $state(null);
  let constructTabState: any = $state(null);

  // Navigation layout state
  let navigationLayout = $state<'top' | 'left'>('top');

  // Panel layout state - determines if panels should be side-by-side or stacked
  let shouldUseSideBySideLayout = $state<boolean>(true);

  // Trigger to force effect re-run when services are initialized
  let servicesInitialized = $state<boolean>(false);

  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let isTransitioning = $state(false);
  let practiceBeatIndex = $state<number | null>(null);

  // Reference to RightPanel for accessing canGoBack and handleBack
  let rightPanelRef: any = $state(null);

  // Edit slide panel state
  let isEditPanelOpen = $state(false);
  let editPanelBeatIndex = $state<number | null>(null);
  let editPanelBeatData = $state<any>(null);

  // Effect to notify parent of tab accessibility changes
  $effect(() => {
    // Guard: Don't run until buildTabState is initialized
    if (!buildTabState) return;

    const canAccess = buildTabState.canAccessEditTab;
    const hasStartPosition = buildTabState.sequenceState.hasStartPosition;
    const beatCount = buildTabState.sequenceState.beatCount();

    logger.log("Tab accessibility effect running:", {
      canAccess,
      hasStartPosition,
      beatCount,
      hasCallback: !!onTabAccessibilityChange
    });

    if (onTabAccessibilityChange) {
      onTabAccessibilityChange(canAccess);
    }
  });

  // Sync navigation state with build tab state
  $effect(() => {
    // Guard: Don't run until buildTabState is initialized
    if (!buildTabState) return;

    const currentMode = navigationState.currentSubMode;
    const buildTabCurrentMode = buildTabState.activeSubTab;

    logger.log("Navigation → BuildTab sync effect:", {
      currentMode,
      buildTabCurrentMode,
      isPersistenceInitialized: buildTabState.isPersistenceInitialized,
      isNavigatingBack: buildTabState.isNavigatingBack,
      shouldUpdate: currentMode !== buildTabCurrentMode && buildTabState.isPersistenceInitialized && !buildTabState.isNavigatingBack
    });

    // If navigation state differs from build tab state, update build tab
    // BUT skip if we're currently in a back navigation (to prevent loop)
    if (currentMode !== buildTabCurrentMode && buildTabState.isPersistenceInitialized && !buildTabState.isNavigatingBack) {
      // GUARD: Prevent navigation to Animate, Share, or Record tabs without a valid sequence
      // Note: Edit is no longer a tab - it's handled via slide-out panel
      if ((currentMode === "animate" || currentMode === "share" || currentMode === "record") && !buildTabState.canAccessEditTab) {
        console.warn(`🚫 Cannot access ${currentMode} tab without a sequence. Redirecting to construct.`);
        navigationState.setCurrentSubMode("construct");
        return;
      }

      logger.log("Updating buildTab state from navigation:", currentMode);
      // Use regular setActiveRightPanel to ADD to history (user clicked a tab)
      buildTabState.setActiveRightPanel(currentMode as any);
      logger.success("BuildTab state updated to:", buildTabState.activeSubTab);
    }
  });

  // Sync build tab state changes back to navigation state
  $effect(() => {
    // Guard: Don't run until buildTabState is initialized
    if (!buildTabState) return;

    const buildTabCurrentMode = buildTabState.activeSubTab;
    const navCurrentMode = navigationState.currentSubMode;

    if (buildTabCurrentMode && buildTabCurrentMode !== navCurrentMode) {
      navigationState.setCurrentSubMode(buildTabCurrentMode);
    }
  });

  // NOTE: Tab accessibility is now handled reactively in MainInterface.svelte
  // by watching sequence state and creating new tab arrays with updated disabled properties.
  // This avoids the infinite loop that occurred when mutating BUILD_MODES directly.

  // Initialize device detection services
  $effect(() => {
    if (!ensureContainerInitialized()) return;

    try {
      deviceDetector = resolve(TYPES.IDeviceDetector);
      viewportService = resolve(TYPES.IViewportService);
      servicesInitialized = true;
    } catch (error) {
      console.error("❌ BuildTab: Failed to initialize device detection services:", error);
    }
  });

  // Reactive viewport dimensions for the effect
  let viewportWidth = $state(0);
  let viewportHeight = $state(0);

  // Set up reactive viewport tracking
  $effect(() => {
    if (!viewportService || typeof window === 'undefined') return;

    // Initialize with current values
    viewportWidth = viewportService.width;
    viewportHeight = viewportService.height;

    // Subscribe to viewport changes
    const unsubscribe = viewportService.onViewportChange(() => {
      viewportWidth = viewportService!.width;
      viewportHeight = viewportService!.height;
    });

    return unsubscribe;
  });

  // Derived value for navigation layout - this will be reactive to device detector changes
  const currentNavigationLayout = $derived(() => {
    if (!deviceDetector) return 'top';
    return deviceDetector.getNavigationLayoutImmediate();
  });

  // Effect to track navigation layout changes and update panel layout accordingly
  $effect(() => {
    // Access servicesInitialized to make this effect reactive to service initialization
    const initialized = servicesInitialized;

    if (!deviceDetector || !viewportService) {
      return;
    }

    // Access reactive viewport dimensions to make this effect reactive to viewport changes

    // Update navigation layout when device detector changes
    navigationLayout = currentNavigationLayout();

    // Determine panel layout based on device type, orientation, and viewport size
    const isDesktop = deviceDetector.isDesktop();
    const isLandscapeMobile = deviceDetector.isLandscapeMobile();


    // Use side-by-side layout when:
    // 1. Desktop with sufficient width (responsive to window size)
    // 2. Landscape mobile (phone held sideways, including Z Fold landscape)
    // 3. Z Fold unfolded (detected as desktop but should always be side-by-side)

    // Check if viewport is wide enough for side-by-side layout
    const hasWideViewport = viewportWidth >= 1024; // Standard desktop breakpoint

    // Landscape detection: Use side-by-side for significantly landscape orientations
    const aspectRatio = viewportWidth / viewportHeight;
    const isSignificantlyLandscape = aspectRatio > 1.2; // Broader landscape detection (includes Z Fold range)

    // Z Fold specific: More flexible detection that accounts for browser UI
    const isLikelyZFoldUnfolded =
      viewportWidth >= 750 && viewportWidth <= 950 && // Wider range to account for browser UI
      aspectRatio > 1.1 && aspectRatio < 1.4; // Broader aspect ratio range

    const newSideBySideLayout = (isDesktop && hasWideViewport) || isLandscapeMobile || isLikelyZFoldUnfolded || isSignificantlyLandscape;
    shouldUseSideBySideLayout = newSideBySideLayout;
  });

  // Effect to handle start position selection events
  $effect(() => {
    // Guard: Don't run until constructTabState is initialized
    if (!constructTabState || typeof window === "undefined") return;

    const handleStartPositionSelected = async (event: CustomEvent) => {
      const pictographData = event.detail.startPosition;
      constructTabState.handleStartPositionSelected(pictographData);
    };

    window.addEventListener("start-position-selected", handleStartPositionSelected as unknown as EventListener);

    // Cleanup function
    return () => {
      window.removeEventListener("start-position-selected", handleStartPositionSelected as unknown as EventListener);
    };
  });

  // Effect to open edit panel when a beat is selected
  $effect(() => {
    // Guard: Don't run until buildTabState is initialized
    if (!buildTabState) return;

    const selectedIndex = buildTabState.sequenceState.selectedBeatIndex;
    const selectedData = buildTabState.sequenceState.selectedBeatData;

    // If a beat is selected, open the edit panel
    if (selectedIndex !== null && selectedData) {
      editPanelBeatIndex = selectedIndex;
      editPanelBeatData = selectedData;
      isEditPanelOpen = true;
      logger.log(`Opening edit panel for beat ${selectedIndex}`);
    } else if (selectedData && selectedData.beatNumber === 0) {
      // Start position is selected
      editPanelBeatIndex = -1; // Special index for start position
      editPanelBeatData = selectedData;
      isEditPanelOpen = true;
      logger.log("Opening edit panel for start position");
    }
  });



  async function handleOptionSelected(option: any): Promise<void> {
    try {
      if (!buildTabService) {
        throw new Error("Build tab service not initialized");
      }
      performance.mark('build-tab-service-start');
      // Delegate to Application Service - handles all business logic
      await buildTabService.selectOption(option);
      performance.mark('build-tab-service-complete');
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to select option";
      error = errorMessage;
      console.error("❌ BuildTab: Error handling option selection:", err);
    }
  }

  function clearError() {
  error = null;
  }

  function handleAddToDictionary() {
    // Save - to be implemented
  }

  // Button Panel Handlers
  function handleRemoveBeat(beatIndex: number) {
    if (!buildTabState) {
      console.warn("BuildTab: Cannot remove beat - build tab state not initialized");
      return;
    }

    // Check if removing start position (beatNumber === 0)
    const selectedBeat = buildTabState.sequenceState.selectedBeatData;
    if (selectedBeat && selectedBeat.beatNumber === 0) {
      // Push undo snapshot before clearing
      buildTabState.pushUndoSnapshot('CLEAR_SEQUENCE', {
        description: 'Clear sequence (removed start position)'
      });

      buildTabState.sequenceState.clearSequenceCompletely();
      buildTabState.setActiveRightPanel("construct");
      return;
    }

    // Calculate how many beats will be removed
    const currentSequence = buildTabState.sequenceState.currentSequence;
    const beatsToRemove = currentSequence ? currentSequence.beats.length - beatIndex : 0;

    // Push undo snapshot before removing beats
    buildTabState.pushUndoSnapshot('REMOVE_BEATS', {
      beatIndex,
      beatsRemoved: beatsToRemove,
      description: `Remove beat ${beatIndex} and ${beatsToRemove - 1} subsequent beats`
    });

    // Remove the beat and all subsequent beats with staggered animation
    buildTabState.sequenceState.removeBeatAndSubsequentWithAnimation(beatIndex, () => {
      // After animation completes, select the previous beat
      if (beatIndex > 0) {
        // Select the previous beat (beatIndex - 1)
        buildTabState.sequenceState.selectBeat(beatIndex - 1);
      } else {
        // If removing beat 0 (first beat), select start position
        buildTabState.sequenceState.selectStartPositionForEditing();
      }
    });
  }

  // ============================================================================
  // LIFECYCLE - TEMPORARY DISABLED
  // ============================================================================

  onMount(async () => {
  try {
    isLoading = true;

    // Ensure container is initialized first
    await ensureContainerInitialized();

    // Initialize services
    sequenceService = resolve(TYPES.ISequenceService) as ISequenceService;
    sequencePersistenceService = resolve(TYPES.ISequencePersistenceService) as ISequencePersistenceService;
    startPositionService = resolve(TYPES.IStartPositionService) as IStartPositionService;
    buildTabService = resolve(TYPES.IBuildTabService) as IBuildTabService;

    // Wait a tick to ensure component context is fully established
    await new Promise(resolve => setTimeout(resolve, 0));

    // Initialize state objects
    buildTabState = createBuildTabState(sequenceService, sequencePersistenceService);
    constructTabState = createConstructTabState(
      buildTabService,
      buildTabState.sequenceState,
      sequencePersistenceService,
      buildTabState, // Pass buildTabState so construct tab can access lastContentTab
      navigationState // Pass navigationState so construct tab can update navigation
    );

    // Initialize build tab service
    await buildTabService.initialize();

    // Initialize build tab state with persistence (includes sequence state)
    await buildTabState.initializeWithPersistence();

    // Initialize construct tab with persistence
    await constructTabState.initializeConstructTab();

    // Set up sequence state callbacks for BuildTabEventService
    const buildTabEventService = getBuildTabEventService();
    buildTabEventService.setSequenceStateCallbacks(
      () => buildTabState.sequenceState.getCurrentSequence(),
      (sequence) => buildTabState.sequenceState.setCurrentSequence(sequence)
    );

    // Set up option history callback
    buildTabEventService.setAddOptionToHistoryCallback(
      (beatIndex, beatData) => buildTabState.addOptionToHistory(beatIndex, beatData)
    );

    // Set up undo snapshot callback
    buildTabEventService.setPushUndoSnapshotCallback(
      (type, metadata) => buildTabState.pushUndoSnapshot(type, metadata)
    );

    // Load start positions using the service
    await startPositionService.getDefaultStartPositions(GridMode.DIAMOND);
  } catch (err) {
    console.error("❌ BuildTab: Initialization failed:", err);
    error = err instanceof Error ? err.message : "Failed to initialize build tab";
  } finally {
    isLoading = false;
  }
  });
</script>

<!-- ============================================================================ -->
<!-- TEMPLATE -->
<!-- ============================================================================ -->

<div class="build-tab" data-testid="build-tab">
  <!-- Error display -->
  {#if error}
  <ErrorBanner
    message={error}
    onDismiss={clearError}
  />
  {/if}



  {#if buildTabState && constructTabState}
  <div class="build-tab-layout" class:side-by-side={shouldUseSideBySideLayout} class:stacked={!shouldUseSideBySideLayout}>
  <!-- Left Panel: Workbench with integrated vertical button panel -->
  <LeftPanel
    sequenceState={buildTabState.sequenceState}
    onClearSequence={constructTabState.clearSequenceCompletely}
    {buildTabState}
    {practiceBeatIndex}
    canGoBack={rightPanelRef?.getCanGoBack?.() ?? false}
    onBack={() => rightPanelRef?.handleBack?.()}
    canRemoveBeat={buildTabState.sequenceState.hasStartPosition}
    onRemoveBeat={handleRemoveBeat}
    isSideBySideLayout={shouldUseSideBySideLayout}
    selectedBeatIndex={buildTabState.sequenceState.selectedBeatIndex}
    selectedBeatData={buildTabState.sequenceState.selectedBeatData}
    canEditBeat={buildTabState.sequenceState.selectedBeatData !== null}
    onEditBeat={() => {
      // Open the edit panel for the currently selected beat
      if (buildTabState.sequenceState.selectedBeatData) {
        isEditPanelOpen = true;
      }
    }}
    canClearSequence={buildTabState.sequenceState.hasStartPosition}
    canSaveSequence={buildTabState.sequenceState.hasStartPosition && buildTabState.sequenceState.beatCount() > 0}
    onSaveSequence={handleAddToDictionary}
    showFullScreen={true}
    animationStateRef={rightPanelRef?.getAnimationStateRef?.()}
  />



  <!-- Right Panel: 4-Tab interface matching desktop -->
  <RightPanel
    bind:this={rightPanelRef}
    {buildTabState}
    {constructTabState}
    onOptionSelected={handleOptionSelected}
    onPracticeBeatIndexChange={(index) => { practiceBeatIndex = index; }}
    isSideBySideLayout={() => shouldUseSideBySideLayout}
  />
  </div>
  {:else}
  <div class="loading-container">
    <LoadingOverlay message="Initializing build interface..." />
  </div>
  {/if}

  <!-- Loading overlay -->
  {#if isTransitioning}
  <LoadingOverlay message="Processing..." />
  {/if}

  <!-- Edit Slide Panel - Modern slide-out for editing beats -->
  {#if buildTabState}
  <EditSlidePanel
    isOpen={isEditPanelOpen}
    onClose={() => {
      isEditPanelOpen = false;
    }}
    selectedBeatIndex={editPanelBeatIndex}
    selectedBeatData={editPanelBeatData}
    onOrientationChanged={(color, orientation) => {
      if (editPanelBeatData) {
        buildTabState.sequenceState.updateBeatOrientation(color, orientation);
      }
    }}
    onTurnAmountChanged={(color, turnAmount) => {
      if (editPanelBeatData) {
        buildTabState.sequenceState.updateBeatTurnAmount(color, turnAmount);
      }
    }}
  />
  {/if}
</div>

<!-- ============================================================================ -->
<!-- STYLES -->
<!-- ============================================================================ -->

<style>
  .build-tab {
  display: flex;
  flex-direction: column;
  /* Multi-layer fallback for reliable viewport height */
  height: 100vh; /* Fallback 1: Static viewport height */
  height: var(--viewport-height, 100vh); /* Fallback 2: JS-calculated height */
  height: 100dvh; /* Preferred: Dynamic viewport height (when it works) */
  width: 100%;
  overflow: hidden;
  position: relative;
  }

  .build-tab-layout {
  flex: 1;
  display: grid;
  /* Grid layout will be set by CSS classes based on navigation layout */
  overflow: hidden;
  gap: var(--spacing-xs);
  padding: 8px;
  }

  /* Side-by-side layout (when navigation is on left - phone landscape) */
  .build-tab-layout.side-by-side {
    grid-template-columns: 1fr 1fr; /* 50/50 split between left panel and right panel */
  }

  /* Stacked layout (when navigation is on top - tablets, desktop, portrait) */
  .build-tab-layout.stacked {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr; /* Top panel (left), bottom panel (right) */
  }





  /* Note: Layout is controlled by dynamic CSS classes based on:
     - Desktop with wide viewport (>= 1024px)
     - Landscape mobile (phones held sideways)
     - Z Fold unfolded (flexible detection for browser UI variations)
     - Significantly landscape orientation (aspect ratio > 1.3)
     This ensures responsive behavior while preserving Z Fold functionality. */

  /* Ultra-narrow mobile (Z Fold 6 folded, narrow phones) - fallback spacing */
  @media (max-width: 480px) {
    .build-tab-layout {
      gap: var(--spacing-xs);
      padding: 4px;
    }
  }

  /* Z Fold 6 cover screen optimization - fallback spacing */
  @media (max-width: 320px) {
    .build-tab-layout {
      gap: 2px;
      padding: 2px;
    }
  }
</style>
