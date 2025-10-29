<script lang="ts">
  import {
    createComponentLogger,
    ensureContainerInitialized,
    ErrorBanner,
    GridMode,
    navigationState,
    resolve,
    TYPES,
    type PictographData
  } from "$shared";
  import { onMount } from "svelte";
  import AnimationPanel from "../../animate/components/AnimationPanel.svelte";
  import OptionFilterPanel from "../../construct/option-picker/option-viewer/components/OptionFilterPanel.svelte";
  import type { IStartPositionService } from "../../construct/start-position-picker/services/contracts";
  import { EditSlidePanel } from "../../edit/components";
  import ToolPanel from '../../tool-panel/core/ToolPanel.svelte';
  import WorkspacePanel from '../../workspace-panel/core/WorkspacePanel.svelte';
  import ButtonPanel from '../../workspace-panel/shared/components/ButtonPanel.svelte';
  import SequenceActionsSheet from '../../workspace-panel/shared/components/SequenceActionsSheet.svelte';
  import type {
    IBeatOperationsService,
    IBuildTabService,
    INavigationSyncService,
    IResponsiveLayoutService,
    ISequencePersistenceService,
    ISequenceService
  } from "../services/contracts";
  import { getBuildTabEventService } from "../services/implementations/BuildTabEventService";
  import { createBuildTabState, createConstructTabState } from "../state";
  import type { createBuildTabState as BuildTabStateType } from "../state/build-tab-state.svelte";
  import type { createConstructTabState as ConstructTabStateType } from "../state/construct-tab-state.svelte";
  import { createPanelCoordinationState } from "../state/panel-coordination-state.svelte";
  import type { BatchEditChanges, IToolPanelMethods } from "../types/build-tab-types";
  import LoadingOverlay from './LoadingOverlay.svelte';

  const logger = createComponentLogger('BuildTab');

  // Constants
  const START_POSITION_BEAT_NUMBER = 0; // Beat 0 = start position, beats 1+ are in the sequence

  // Type aliases for state objects
  type BuildTabState = ReturnType<typeof BuildTabStateType>;
  type ConstructTabState = ReturnType<typeof ConstructTabStateType>;

  // Props
  let { onTabAccessibilityChange }: {
    onTabAccessibilityChange?: (canAccessEditAndExport: boolean) => void
  } = $props();

  // Services - resolved directly from DI container
  let sequenceService: ISequenceService | null = $state(null);
  let sequencePersistenceService: ISequencePersistenceService | null = $state(null);
  let startPositionService: IStartPositionService | null = $state(null);
  let buildTabService: IBuildTabService | null = $state(null);
  let layoutService: IResponsiveLayoutService | null = $state(null);
  let navigationSyncService: INavigationSyncService | null = $state(null);
  let beatOperationsService: IBeatOperationsService | null = $state(null);

  // State
  let buildTabState: BuildTabState | null = $state(null);
  let constructTabState: ConstructTabState | null = $state(null);

  // Panel coordination state - centralized management
  let panelState = createPanelCoordinationState();

  // Layout state - managed by services
  let shouldUseSideBySideLayout = $state<boolean>(false);

  // UI state
  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let servicesInitialized = $state<boolean>(false);

  // Panel refs
  let toolPanelElement: HTMLElement | null = $state(null);
  let toolPanelRef: IToolPanelMethods | null = $state(null);

  // Derived: Toggle always shows in ButtonPanel (at right edge)
  const shouldShowToggleInButtonPanel = $derived(() => {
    // Always show toggle in ButtonPanel, regardless of layout
    return true;
  });

  // Derived: Allow clearing when a start position or beats exist
  const canClearSequence = $derived(() => {
    if (!buildTabState) return false;
    const sequenceState = buildTabState.sequenceState;
    if (!sequenceState) return false;
    const hasStart = sequenceState.hasStartPosition;
    const beatCount = sequenceState.currentSequence?.beats?.length ?? 0;
    return hasStart || beatCount > 0;
  });

  // Derived: Allow sharing when a sequence exists
  const canShareSequence = $derived(() => {
    if (!buildTabState) return false;
    return buildTabState.hasSequence;
  });

  // Effect: Notify parent of tab accessibility changes
  $effect(() => {
    if (!buildTabState) return;

    const canAccess = buildTabState.canAccessEditTab;
    logger.log("Tab accessibility:", { canAccess });

    if (onTabAccessibilityChange) {
      onTabAccessibilityChange(canAccess);
    }
  });

  // Effect: Sync navigation state TO build tab state
  $effect(() => {
    if (!buildTabState || !navigationSyncService) return;

    navigationSyncService.syncNavigationToBuildTab(
      buildTabState,
      navigationState
    );
  });

  // Effect: Sync build tab state BACK to navigation state
  $effect(() => {
    if (!buildTabState || !navigationSyncService) return;
    if (buildTabState.isUpdatingFromToggle) return;

    navigationSyncService.syncBuildTabToNavigation(
      buildTabState,
      navigationState
    );
  });

  // Effect: Handle responsive layout changes
  $effect(() => {
    if (!layoutService || !servicesInitialized) return;

    // Initialize layout service
    layoutService.initialize();

    // Subscribe to layout changes
    const unsubscribe = layoutService.onLayoutChange(() => {
      if (layoutService) {
        shouldUseSideBySideLayout = layoutService.shouldUseSideBySideLayout();
      }
    });

    // Initial layout calculation
    shouldUseSideBySideLayout = layoutService.shouldUseSideBySideLayout();

    // Cleanup
    return () => {
      unsubscribe();
      if (layoutService) {
        layoutService.dispose();
      }
    };
  });

  // Effect: Auto-open edit panel when multiple beats selected
  $effect(() => {
    if (!buildTabState) return;

    const selectedBeatNumbers = buildTabState.sequenceState?.selectedBeatNumbers;
    const selectedCount = selectedBeatNumbers?.size ?? 0;

    if (selectedCount > 1 && !panelState.isEditPanelOpen) {
      // Capture state reference for TypeScript null safety in closure
      const state = buildTabState;

      // Map beat numbers to beat data
      const beatNumbersArray = Array.from(selectedBeatNumbers).sort((a, b) => a - b);
      const beatsData = beatNumbersArray.map((beatNumber) => {
        if (beatNumber === START_POSITION_BEAT_NUMBER) {
          // Beat 0 is the start position
          return state.sequenceState.selectedStartPosition;
        } else {
          // Beats are numbered 1, 2, 3... but stored in array at indices 0, 1, 2...
          const beatIndex = beatNumber - 1;
          return state.sequenceState.currentSequence?.beats[beatIndex];
        }
      }).filter(Boolean); // Remove any null values

      logger.log(`Auto-opening batch edit panel: ${selectedCount} beats selected`);
      panelState.openBatchEditPanel(beatsData);
    }
  });

  // Effect: Track tool panel height for edit panel sizing
  $effect(() => {
    if (!toolPanelElement) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        panelState.setToolPanelHeight(entry.contentRect.height);
      }
    });

    resizeObserver.observe(toolPanelElement);
    return () => resizeObserver.disconnect();
  });

  // Component initialization - DIRECT SERVICE RESOLUTION
  onMount(async () => {
    if (!ensureContainerInitialized()) {
      error = "Dependency injection container not initialized";
      return;
    }

    isLoading = true;

    try {
      // Resolve all services directly from DI container
      sequenceService = resolve<ISequenceService>(TYPES.ISequenceService);
      sequencePersistenceService = resolve<ISequencePersistenceService>(TYPES.ISequencePersistenceService);
      startPositionService = resolve<IStartPositionService>(TYPES.IStartPositionService);
      buildTabService = resolve<IBuildTabService>(TYPES.IBuildTabService);
      layoutService = resolve<IResponsiveLayoutService>(TYPES.IResponsiveLayoutService);
      navigationSyncService = resolve<INavigationSyncService>(TYPES.INavigationSyncService);
      beatOperationsService = resolve<IBeatOperationsService>(TYPES.IBeatOperationsService);

      // Wait a tick to ensure component context is fully established
      await new Promise(resolve => setTimeout(resolve, 0));

      // Create state objects directly
      buildTabState = createBuildTabState(
        sequenceService,
        sequencePersistenceService
      );

      constructTabState = createConstructTabState(
        buildTabService,
        buildTabState.sequenceState,
        sequencePersistenceService,
        buildTabState,
        navigationState
      );

      // Initialize services
      await buildTabService.initialize();

      // Initialize state with persistence
      await buildTabState.initializeWithPersistence();
      await constructTabState.initializeConstructTab();

      // Mark services as initialized
      servicesInitialized = true;

      // Configure event callbacks
      const buildTabEventService = getBuildTabEventService();

      // Set up sequence state callbacks for BuildTabEventService
      buildTabEventService.setSequenceStateCallbacks(
        () => buildTabState!.sequenceState.getCurrentSequence(),
        (sequence) => buildTabState!.sequenceState.setCurrentSequence(sequence)
      );

      // Set up option history callback
      buildTabEventService.setAddOptionToHistoryCallback(
        (beatIndex, beatData) => buildTabState!.addOptionToHistory(beatIndex, beatData)
      );

      // Set up undo snapshot callback
      buildTabEventService.setPushUndoSnapshotCallback(
        (type, metadata) => buildTabState!.pushUndoSnapshot(type, metadata)
      );

      // Load start positions
      await startPositionService.getDefaultStartPositions(GridMode.DIAMOND);

      logger.success("BuildTab initialized successfully");
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to initialize BuildTab";
      error = errorMessage;
      console.error("❌ BuildTab: Initialization error:", err);
    } finally {
      isLoading = false;
    }
  });

  // Effect: Open edit panel when a beat is selected
  $effect(() => {
    // Guard: Don't run until buildTabState is initialized
    if (!buildTabState) return;

    const selectedBeatNumber = buildTabState.sequenceState.selectedBeatNumber;
    const selectedData = buildTabState.sequenceState.selectedBeatData;

    // If a beat is selected, open the edit panel
    if (selectedBeatNumber !== null && selectedData) {
      panelState.openEditPanel(selectedBeatNumber, selectedData);
      logger.log(`Opening edit panel for beat ${selectedBeatNumber}`);
    }
  });

  // Event handlers - delegate to services/state
  async function handleOptionSelected(option: PictographData): Promise<void> {
    try {
      if (!buildTabService) {
        throw new Error("Build tab service not initialized");
      }
      await buildTabService.selectOption(option);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to select option";
      error = errorMessage;
      logger.error("Error handling option selection:", err);
    }
  }

  function clearError() {
    error = null;
  }

  function handlePlayAnimation() {
    panelState.openAnimationPanel();
  }

  function handleOpenSharePanel() {
    panelState.openSharePanel();
  }

  function handleCloseSharePanel() {
    panelState.closeSharePanel();
  }

  async function handleClearSequence() {
    if (!buildTabState) return;

    try {
      if (constructTabState?.clearSequenceCompletely) {
        await constructTabState.clearSequenceCompletely();
      } else if (buildTabState.sequenceState?.clearSequenceCompletely) {
        await buildTabState.sequenceState.clearSequenceCompletely();
      } else if (buildTabState.sequenceState?.clearSequence) {
        buildTabState.sequenceState.clearSequence();
      }
      panelState.closeSharePanel();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to clear sequence";
      error = errorMessage;
      logger.error("Failed to clear sequence completely", err);
    }
  }

  function handleCloseAnimationPanel() {
    panelState.closeAnimationPanel();
  }

  function handleOpenFilterPanel() {
    panelState.openFilterPanel();
  }

  function handleRemoveBeat(beatIndex: number) {
    if (!beatOperationsService) {
      logger.warn("Beat operations service not initialized");
      return;
    }

    try {
      beatOperationsService.removeBeat(beatIndex, buildTabState);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to remove beat";
      error = errorMessage;
      logger.error("Failed to remove beat", err);
    }
  }

  function handleBatchApply(changes: BatchEditChanges) {
    if (!beatOperationsService) {
      logger.warn("Beat operations service not initialized");
      return;
    }

    try {
      beatOperationsService.applyBatchChanges(changes, buildTabState);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to apply changes";
      error = errorMessage;
      logger.error("Failed to apply batch changes", err);

      // Error recovery: Clear selection and close panel to prevent stuck UI
      buildTabState?.sequenceState.clearSelection();
      panelState.closeEditPanel();
    }
  }

  function handleOrientationChange(color: string, orientation: string) {
    if (!beatOperationsService) {
      logger.warn("Beat operations service not initialized");
      return;
    }

    const beatIndex = panelState.editPanelBeatIndex;
    if (beatIndex === null) {
      logger.warn("Cannot change orientation: no beat selected");
      return;
    }

    try {
      beatOperationsService.updateBeatOrientation(
        beatIndex,
        color,
        orientation,
        buildTabState,
        panelState
      );
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to update orientation";
      error = errorMessage;
      logger.error("Failed to update orientation", err);
    }
  }

  function handleTurnAmountChange(color: string, turnAmount: number) {
    if (!beatOperationsService) {
      logger.warn("Beat operations service not initialized");
      return;
    }

    const beatIndex = panelState.editPanelBeatIndex;
    if (beatIndex === null) {
      logger.warn("Cannot change turns: no beat selected");
      return;
    }

    try {
      beatOperationsService.updateBeatTurns(
        beatIndex,
        color,
        turnAmount,
        buildTabState,
        panelState
      );
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to update turns";
      error = errorMessage;
      logger.error("Failed to update turns", err);
    }
  }

  // Sequence Actions Sheet state and handlers
  let showSequenceActionsSheet = $state(false);

  function handleOpenSequenceActions() {
    showSequenceActionsSheet = true;
  }

  function handleCloseSequenceActions() {
    showSequenceActionsSheet = false;
  }

  function handleMirror() {
    // TODO: Implement mirror transformation
    logger.log("Mirror action triggered");
  }

  function handleRotate() {
    // TODO: Implement rotation transformation
    logger.log("Rotate action triggered");
  }

  function handleColorSwap() {
    // TODO: Implement color swap transformation
    logger.log("Color swap action triggered");
  }

  function handleCopyJSON() {
    if (!buildTabState?.sequenceState.currentSequence) return;
    navigator.clipboard.writeText(
      JSON.stringify(buildTabState.sequenceState.currentSequence, null, 2)
    );
    logger.log("Sequence JSON copied to clipboard");
  }
</script>

{#if isLoading}
  <LoadingOverlay message="Initializing Build Tab..." />
{:else if error}
  <ErrorBanner message={error} onDismiss={clearError} />
{:else if buildTabState && constructTabState}
  <div class="build-tab" class:side-by-side={shouldUseSideBySideLayout}>
    <!-- Workspace Panel -->
    <div class="workspace-container">
      <WorkspacePanel
        sequenceState={buildTabState.sequenceState}
        {buildTabState}
        practiceBeatIndex={panelState.practiceBeatIndex}
        isMobilePortrait={layoutService?.isMobilePortrait() ?? false}
        onPlayAnimation={handlePlayAnimation}
        animationStateRef={toolPanelRef?.getAnimationStateRef?.()}
      />

      <ButtonPanel
        {buildTabState}
        showToggle={shouldShowToggleInButtonPanel()}
        activeTab={buildTabState.activeSubTab as 'construct' | 'generate'}
        onTabChange={(tab) => buildTabState?.setactiveToolPanel(tab)}
        showPlayButton={buildTabState.hasSequence}
        onPlayAnimation={handlePlayAnimation}
        isAnimating={panelState.isAnimationPanelOpen}
        canClearSequence={canClearSequence()}
        onClearSequence={handleClearSequence}
        onRemoveBeat={handleRemoveBeat}
        showShareButton={canShareSequence()}
        onShare={handleOpenSharePanel}
        isShareOpen={panelState.isSharePanelOpen}
        showSequenceActions={buildTabState.hasSequence}
        onSequenceActionsClick={handleOpenSequenceActions}
      />

      <AnimationPanel
        sequence={buildTabState.sequenceState.currentSequence}
        show={panelState.isAnimationPanelOpen}
        onClose={handleCloseAnimationPanel}
        toolPanelHeight={panelState.toolPanelHeight}
      />
    </div>

    <!-- Tool Panel -->
    <div class="tool-panel-container" bind:this={toolPanelElement}>
      {#if buildTabState && constructTabState}
        <ToolPanel
          bind:this={toolPanelRef}
          buildTabState={buildTabState}
          constructTabState={constructTabState}
          onOptionSelected={handleOptionSelected}
          isSideBySideLayout={() => shouldUseSideBySideLayout}
          onPracticeBeatIndexChange={(index) => { panelState.setPracticeBeatIndex(index); }}
          onOpenFilters={handleOpenFilterPanel}
        />
      {/if}
    </div>
  </div>

  <!-- Edit Slide Panel - Positioned outside grid layout to slide over content -->
  {#if buildTabState}
    <EditSlidePanel
      isOpen={panelState.isEditPanelOpen}
      selectedBeatNumber={panelState.editPanelBeatIndex}
      selectedBeatData={panelState.editPanelBeatData}
      selectedBeatsData={panelState.editPanelBeatsData}
      toolPanelHeight={panelState.toolPanelHeight}
      isSideBySideLayout={shouldUseSideBySideLayout}
      onClose={() => {
        panelState.closeEditPanel();
        // Exit multi-select mode when closing panel
        const selectedCount = buildTabState?.sequenceState.selectedBeatNumbers?.size ?? 0;
        if (selectedCount > 0) {
          buildTabState?.sequenceState.exitMultiSelectMode();
        }
      }}
      onOrientationChanged={handleOrientationChange}
      onTurnAmountChanged={handleTurnAmountChange}
      onBatchApply={handleBatchApply}
    />
  {/if}

  <!-- Option Filter Panel - Positioned outside grid layout to slide over content -->
  {#if panelState.isFilterPanelOpen && constructTabState}
    <OptionFilterPanel
      isOpen={panelState.isFilterPanelOpen}
      isContinuousOnly={constructTabState.isContinuousOnly}
      onClose={() => {
        panelState.closeFilterPanel();
      }}
      onToggleContinuous={(isContinuousOnly: boolean) => {
        if (constructTabState) {
          constructTabState.setContinuousOnly(isContinuousOnly);
        }
      }}
    />
  {/if}

  <!-- Sequence Actions Sheet - Positioned outside grid layout to slide over content -->
  {#if buildTabState}
    <SequenceActionsSheet
      show={showSequenceActionsSheet}
      hasSequence={buildTabState.hasSequence}
      toolPanelHeight={panelState.toolPanelHeight}
      onMirror={handleMirror}
      onRotate={handleRotate}
      onColorSwap={handleColorSwap}
      onSave={() => {
        // TODO: Implement save
        logger.log("Save action triggered");
      }}
      onCopyJSON={handleCopyJSON}
      onClose={handleCloseSequenceActions}
    />
  {/if}
{/if}

<style>
  .build-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
  }

  .build-tab.side-by-side {
    flex-direction: row;
  }

  .workspace-container,
  .tool-panel-container {
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .workspace-container {
    flex: 3;
    min-height: 0;
  }

  .tool-panel-container {
    flex: 2;
    min-width: 0;
  }

  .build-tab.side-by-side .workspace-container {
    flex: 3;
  }

  .build-tab.side-by-side .tool-panel-container {
    flex: 2;
  }
</style>
