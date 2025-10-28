<!--
Build Tab - Main construction interface

Provides two-panel layout:
- Workspace Panel: Sequence display and action buttons
- Tool Panel: Tabbed interface (Construct, Generate, Animate, Share, Record)

This component is a pure composition layer - all business logic delegated to services.
-->
<script lang="ts">
  import {
    createComponentLogger,
    ensureContainerInitialized,
    ErrorBanner,
    navigationState,
    resolve,
    TYPES,
    type PictographData
  } from "$shared";
  import { onMount } from "svelte";
  import { EditSlidePanel } from "../../edit/components";
  import ToolPanel from '../../tool-panel/core/ToolPanel.svelte';
  import WorkspacePanel from '../../workspace-panel/core/WorkspacePanel.svelte';
  import ButtonPanel from '../../workspace-panel/shared/components/ButtonPanel.svelte';
  import InlineAnimatorPanel from '../../workspace-panel/shared/components/InlineAnimatorPanel.svelte';
  import type {
    IBuildTabInitializationService
  } from "../services/contracts";
  import type { BuildTabInitializationResult } from "../services/contracts/IBuildTabInitializationService";
  import type { createBuildTabState } from "../state/build-tab-state.svelte";
  import type { createConstructTabState } from "../state/construct-tab-state.svelte";
  import { createPanelCoordinationState } from "../state/panel-coordination-state.svelte";
  import type { BatchEditChanges, IToolPanelMethods } from "../types/build-tab-types";
  import LoadingOverlay from './LoadingOverlay.svelte';

  const logger = createComponentLogger('BuildTab');

  // Constants
  const START_POSITION_BEAT_NUMBER = 0; // Beat 0 = start position, beats 1+ are in the sequence

  // Type aliases for state objects
  type BuildTabState = ReturnType<typeof createBuildTabState>;
  type ConstructTabState = ReturnType<typeof createConstructTabState>;

  // Props
  let { onTabAccessibilityChange }: {
    onTabAccessibilityChange?: (canAccessEditAndExport: boolean) => void
  } = $props();

  // Services - all resolved via initialization service
  let initializationService: IBuildTabInitializationService | null = $state(null);
  let services: BuildTabInitializationResult | null = $state(null);

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

  // Derived: Is mobile portrait mode (for floating button logic)
  const isMobilePortrait = $derived(() => {
    return !shouldUseSideBySideLayout;
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
    if (!buildTabState || !services?.navigationSyncService) return;

    services.navigationSyncService.syncNavigationToBuildTab(
      buildTabState,
      navigationState
    );
  });

  // Effect: Sync build tab state BACK to navigation state
  $effect(() => {
    if (!buildTabState || !services?.navigationSyncService) return;
    if (buildTabState.isUpdatingFromToggle) return;

    services.navigationSyncService.syncBuildTabToNavigation(
      buildTabState,
      navigationState
    );
  });

  // Effect: Handle responsive layout changes
  $effect(() => {
    if (!services?.layoutService || !servicesInitialized) return;

    const layoutService = services.layoutService;

    // Initialize layout service
    layoutService.initialize();

    // Subscribe to layout changes
    const unsubscribe = layoutService.onLayoutChange(() => {
      shouldUseSideBySideLayout = layoutService.shouldUseSideBySideLayout();
    });

    // Initial layout calculation
    shouldUseSideBySideLayout = layoutService.shouldUseSideBySideLayout();

    // Cleanup
    return () => {
      unsubscribe();
      layoutService.dispose();
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

  // Component initialization
  onMount(async () => {
    if (!ensureContainerInitialized()) {
      error = "Dependency injection container not initialized";
      return;
    }

    isLoading = true;

    try {
      // Use initialization service for all startup logic
      if (!initializationService) {
        initializationService = resolve<IBuildTabInitializationService>(
          TYPES.IBuildTabInitializationService
        );
      }

      const initResult = await initializationService.initialize();

      // Store all services and state from initialization
      services = initResult;
      buildTabState = initResult.buildTabState;
      constructTabState = initResult.constructTabState;

      // Mark services as initialized
      servicesInitialized = true;

      // Configure event callbacks via initialization service
      initializationService.configureEventCallbacks(buildTabState, panelState);

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
      if (!services?.buildTabService) {
        throw new Error("Build tab service not initialized");
      }
      await services.buildTabService.selectOption(option);
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
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to clear sequence";
      error = errorMessage;
      logger.error("Failed to clear sequence completely", err);
    }
  }

  function handleCloseAnimationPanel() {
    panelState.closeAnimationPanel();
  }

  function handleRemoveBeat(beatIndex: number) {
    if (!services?.beatOperationsService) {
      logger.warn("Beat operations service not initialized");
      return;
    }
    
    try {
      services.beatOperationsService.removeBeat(beatIndex, buildTabState);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to remove beat";
      error = errorMessage;
      logger.error("Failed to remove beat", err);
    }
  }

  function handleBatchApply(changes: BatchEditChanges) {
    if (!services?.beatOperationsService) {
      logger.warn("Beat operations service not initialized");
      return;
    }
    
    try {
      services.beatOperationsService.applyBatchChanges(changes, buildTabState);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to apply changes";
      error = errorMessage;
      logger.error("Failed to apply batch changes", err);
    }
  }
</script>

{#if isLoading}
  <LoadingOverlay message="Initializing Build Tab..." />
{:else if error}
  <ErrorBanner message={error} onDismiss={clearError} />
{:else if buildTabState && constructTabState && services}
  <div class="build-tab" class:side-by-side={shouldUseSideBySideLayout}>
    <!-- Workspace Panel -->
    <div class="workspace-container">
      <WorkspacePanel
        sequenceState={buildTabState.sequenceState}
        {buildTabState}
        practiceBeatIndex={panelState.practiceBeatIndex}
        isMobilePortrait={isMobilePortrait()}
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
      />

      {#if panelState.isAnimationPanelOpen}
        <InlineAnimatorPanel
          sequence={buildTabState.sequenceState.currentSequence}
          onClose={handleCloseAnimationPanel}
        />
      {/if}
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
        />
      {/if}
    </div>
  </div>

  <!-- Edit Slide Panel - Positioned outside grid layout to slide over content -->
  {#if panelState.isEditPanelOpen && buildTabState}
    <EditSlidePanel
      isOpen={panelState.isEditPanelOpen}
      selectedBeatNumber={panelState.editPanelBeatIndex}
      selectedBeatData={panelState.editPanelBeatData}
      selectedBeatsData={panelState.editPanelBeatsData}
      toolPanelHeight={panelState.toolPanelHeight}
      onClose={() => {
        panelState.closeEditPanel();
        // Exit multi-select mode when closing panel
        const selectedCount = buildTabState?.sequenceState.selectedBeatNumbers?.size ?? 0;
        if (selectedCount > 0) {
          buildTabState?.sequenceState.exitMultiSelectMode();
        }
      }}
      onOrientationChanged={(color, orientation) => {
        const beatData = panelState.editPanelBeatData;
        const beatIndex = panelState.editPanelBeatIndex;

        if (beatData && beatIndex !== null) {
          // Get current motion data for the color
          const currentMotion = beatData.motions?.[color] || {};

          // Create updated beat data with new orientation
          const updatedBeatData = {
            ...beatData,
            motions: {
              ...beatData.motions,
              [color]: {
                ...currentMotion,
                startOrientation: orientation,
              }
            }
          };

          // Beat 0 = start position, beats 1+ are in array at indices 0, 1, 2...
          if (beatIndex === START_POSITION_BEAT_NUMBER) {
            buildTabState?.sequenceState.setStartPosition(updatedBeatData);
          } else {
            const arrayIndex = beatIndex - 1;
            buildTabState?.sequenceState.updateBeat(arrayIndex, updatedBeatData);
          }
        }
      }}
      onTurnAmountChanged={(color, turnAmount) => {
        const beatData = panelState.editPanelBeatData;
        const beatIndex = panelState.editPanelBeatIndex;

        if (beatData && beatIndex !== null) {
          // Get current motion data for the color
          const currentMotion = beatData.motions?.[color] || {};

          // Create updated beat data with new turn amount
          const updatedBeatData = {
            ...beatData,
            motions: {
              ...beatData.motions,
              [color]: {
                ...currentMotion,
                turns: turnAmount,
              }
            }
          };

          // Beat 0 = start position, beats 1+ are in array at indices 0, 1, 2...
          if (beatIndex === START_POSITION_BEAT_NUMBER) {
            buildTabState?.sequenceState.setStartPosition(updatedBeatData);
          } else {
            const arrayIndex = beatIndex - 1;
            buildTabState?.sequenceState.updateBeat(arrayIndex, updatedBeatData);
          }
        }
      }}
      onBatchApply={handleBatchApply}
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
    flex: 5;
    min-height: 0;
  }

  .tool-panel-container {
    flex: 4;
    min-width: 0;
  }

  .build-tab.side-by-side .workspace-container {
    flex: 1;
  }

  .build-tab.side-by-side .tool-panel-container {
    flex: 1;
  }
</style>
