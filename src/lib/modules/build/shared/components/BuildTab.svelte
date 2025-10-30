<script lang="ts">
  /**
   * Build Tab Component - REFACTORED
   *
   * Master container for the Build tab interface.
   * Orchestrates Workspace, Tool Panel, and various modal panels.
   *
   * REFACTORING:
   * - Extracted service initialization to ServiceInitializer
   * - Extracted panel logic to coordinator components
   * - Consolidated reactive effects into manager modules
   * - Reduced from 19 functions to 6 core handlers
   * - Reduced from 8+ effects to 5 managed effects
   *
   * Domain: Build Module - Tab Container
   */

  import {
    createComponentLogger,
    ensureContainerInitialized,
    ErrorBanner,
    FloatingFullscreenButton,
    GridMode,
    navigationState,
    type PictographData
  } from "$shared";
  import { onMount } from "svelte";
  import OptionFilterPanel from "../../construct/option-picker/option-viewer/components/OptionFilterPanel.svelte";
  import ToolPanel from '../../tool-panel/core/ToolPanel.svelte';
  import WorkspacePanel from '../../workspace-panel/core/WorkspacePanel.svelte';
  import ButtonPanel from '../../workspace-panel/shared/components/ButtonPanel.svelte';
  import type { BuildTabServices } from "../services/ServiceInitializer";
  import { ServiceInitializer } from "../services/ServiceInitializer";
  import { getBuildTabEventService } from "../services/implementations/BuildTabEventService";
  import { createBuildTabState, createConstructTabState } from "../state";
  import type { createBuildTabState as BuildTabStateType } from "../state/build-tab-state.svelte";
  import type { createConstructTabState as ConstructTabStateType } from "../state/construct-tab-state.svelte";
  import {
    createAutoEditPanelEffect,
    createLayoutEffects,
    createNavigationSyncEffects,
    createPanelHeightTracker,
    createPWAEngagementEffect,
    createSingleBeatEditEffect
  } from "../state/managers";
  import { createPanelCoordinationState } from "../state/panel-coordination-state.svelte";
  import type { IToolPanelMethods } from "../types/build-tab-types";
  import {
    AnimationCoordinator,
    EditCoordinator,
    SequenceActionsCoordinator,
    ShareCoordinator
  } from "./coordinators";
  import LoadingOverlay from './LoadingOverlay.svelte';

  const logger = createComponentLogger('BuildTab');

  // Type aliases for state objects
  type BuildTabState = ReturnType<typeof BuildTabStateType>;
  type ConstructTabState = ReturnType<typeof ConstructTabStateType>;

  // Props
  let { onTabAccessibilityChange }: {
    onTabAccessibilityChange?: (canAccessEditAndExport: boolean) => void
  } = $props();

  // Services
  let services: BuildTabServices | null = $state(null);

  // State
  let buildTabState: BuildTabState | null = $state(null);
  let constructTabState: ConstructTabState | null = $state(null);

  // Panel coordination state
  let panelState = createPanelCoordinationState();

  // Animation state
  let animatingBeatNumber = $state<number | null>(null);

  // Layout state
  let shouldUseSideBySideLayout = $state<boolean>(false);

  // UI state
  let isLoading = $state(false);
  let error = $state<string | null>(null);
  let servicesInitialized = $state<boolean>(false);

  // Panel refs
  let toolPanelElement: HTMLElement | null = $state(null);
  let toolPanelRef: IToolPanelMethods | null = $state(null);
  let buttonPanelElement: HTMLElement | null = $state(null);

  // Sequence actions sheet state
  let showSequenceActionsSheet = $state(false);

  // Cleanup functions for effects
  let effectCleanups: (() => void)[] = [];

  // Derived: Toggle always shows in ButtonPanel
  const shouldShowToggleInButtonPanel = $derived(() => true);

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

  // Effect: Setup all managed effects when services are initialized
  $effect(() => {
    if (!servicesInitialized || !buildTabState || !services) return;

    // Clean up previous effects
    effectCleanups.forEach(cleanup => cleanup());
    effectCleanups = [];

    // Navigation sync effects
    const navigationCleanup = createNavigationSyncEffects({
      buildTabState,
      navigationState,
      navigationSyncService: services.navigationSyncService
    });
    effectCleanups.push(navigationCleanup);

    // Layout effects
    const layoutCleanup = createLayoutEffects({
      layoutService: services.layoutService,
      onLayoutChange: (layout) => { shouldUseSideBySideLayout = layout; }
    });
    effectCleanups.push(layoutCleanup);

    // Auto edit panel effects
    const autoEditCleanup = createAutoEditPanelEffect({ buildTabState, panelState });
    effectCleanups.push(autoEditCleanup);

    const singleBeatCleanup = createSingleBeatEditEffect({ buildTabState, panelState });
    effectCleanups.push(singleBeatCleanup);

    // PWA engagement tracking
    const pwaCleanup = createPWAEngagementEffect({ buildTabState });
    effectCleanups.push(pwaCleanup);

    // Cleanup on unmount
    return () => {
      effectCleanups.forEach(cleanup => cleanup());
      effectCleanups = [];
    };
  });

  // Effect: Track panel heights
  $effect(() => {
    if (!toolPanelElement && !buttonPanelElement) return;

    const cleanup = createPanelHeightTracker({
      toolPanelElement,
      buttonPanelElement,
      panelState
    });

    return cleanup;
  });

  // Component initialization
  onMount(async () => {
    if (!ensureContainerInitialized()) {
      error = "Dependency injection container not initialized";
      return;
    }

    isLoading = true;

    try {
      // Resolve all services
      services = ServiceInitializer.resolveServices();

      // Wait a tick to ensure component context is fully established
      await new Promise(resolve => setTimeout(resolve, 0));

      // Create state objects
      buildTabState = createBuildTabState(
        services.sequenceService,
        services.sequencePersistenceService
      );

      constructTabState = createConstructTabState(
        services.buildTabService,
        buildTabState.sequenceState,
        services.sequencePersistenceService,
        buildTabState,
        navigationState
      );

      // Initialize services
      await ServiceInitializer.initializeServices(services);

      // Initialize state with persistence
      await buildTabState.initializeWithPersistence();
      await constructTabState.initializeConstructTab();

      // Mark services as initialized
      servicesInitialized = true;

      // Configure event callbacks
      const buildTabEventService = getBuildTabEventService();

      buildTabEventService.setSequenceStateCallbacks(
        () => buildTabState!.sequenceState.getCurrentSequence(),
        (sequence) => buildTabState!.sequenceState.setCurrentSequence(sequence)
      );

      buildTabEventService.setAddOptionToHistoryCallback(
        (beatIndex, beatData) => buildTabState!.addOptionToHistory(beatIndex, beatData)
      );

      buildTabEventService.setPushUndoSnapshotCallback(
        (type, metadata) => buildTabState!.pushUndoSnapshot(type, metadata)
      );

      // Load start positions
      await services.startPositionService.getDefaultStartPositions(GridMode.DIAMOND);

      logger.success("BuildTab initialized successfully");
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to initialize BuildTab";
      error = errorMessage;
      console.error("BuildTab: Initialization error:", err);
    } finally {
      isLoading = false;
    }
  });

  // Event handlers
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

  function handleOpenSharePanel() {
    panelState.openSharePanel();
  }

  async function handleClearSequence() {
    if (!buildTabState) return;

    try {
      buildTabState.pushUndoSnapshot('CLEAR_SEQUENCE', {
        description: 'Clear sequence'
      });

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

  function handleOpenFilterPanel() {
    panelState.openFilterPanel();
  }

  function handleOpenSequenceActions() {
    showSequenceActionsSheet = true;
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
        {animatingBeatNumber}
        isMobilePortrait={services.layoutService.isMobilePortrait()}
        onPlayAnimation={handlePlayAnimation}
        animationStateRef={toolPanelRef?.getAnimationStateRef?.()}
      />

      <div bind:this={buttonPanelElement}>
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
      </div>

      <!-- Animation Coordinator -->
      <AnimationCoordinator
        {buildTabState}
        {panelState}
        bind:animatingBeatNumber
      />
    </div>

    <!-- Tool Panel -->
    <div class="tool-panel-container" bind:this={toolPanelElement}>
      <ToolPanel
        bind:this={toolPanelRef}
        {buildTabState}
        {constructTabState}
        onOptionSelected={handleOptionSelected}
        isSideBySideLayout={() => shouldUseSideBySideLayout}
        onPracticeBeatIndexChange={(index) => { panelState.setPracticeBeatIndex(index); }}
        onOpenFilters={handleOpenFilterPanel}
      />
    </div>
  </div>

  <!-- Edit Coordinator -->
  <EditCoordinator
    {buildTabState}
    {panelState}
    beatOperationsService={services.beatOperationsService}
    {shouldUseSideBySideLayout}
    onError={(err) => { error = err; }}
  />

  <!-- Option Filter Panel -->
  {#if panelState.isFilterPanelOpen}
    <OptionFilterPanel
      isOpen={panelState.isFilterPanelOpen}
      isContinuousOnly={constructTabState.isContinuousOnly}
      onClose={() => { panelState.closeFilterPanel(); }}
      onToggleContinuous={(isContinuousOnly: boolean) => {
        constructTabState?.setContinuousOnly(isContinuousOnly);
      }}
    />
  {/if}

  <!-- Share Coordinator -->
  <ShareCoordinator
    {buildTabState}
    {panelState}
    shareService={services.shareService}
  />

  <!-- Sequence Actions Coordinator -->
  <SequenceActionsCoordinator
    {buildTabState}
    {panelState}
    bind:show={showSequenceActionsSheet}
  />

  <!-- Floating Fullscreen Button -->
  <FloatingFullscreenButton />
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
