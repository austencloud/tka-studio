<script lang="ts">
  /**
   * Create Module Component - REFACTORED
   *
   * Master container for the Create module interface.
   * Orchestrates Workspace, Tool Panel, and various modal panels.
   *
   * REFACTORING:
   * - Extracted service initialization to ServiceInitializer
   * - Extracted panel logic to coordinator components
   * - Consolidated reactive effects into manager modules
   * - Reduced from 19 functions to 6 core handlers
   * - Reduced from 8+ effects to 5 managed effects
   *
   * Domain: Create module - Tab Container
   */

  import {
    createComponentLogger,
    ensureContainerInitialized,
    GridMode,
    navigationState,
    resolve,
    TYPES,
    type BuildModeId,
    type IDeviceDetector,
    type PictographData,
  } from "$shared";
  import { onMount, setContext } from "svelte";
  import { fade } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import ErrorBanner from "./ErrorBanner.svelte";
  import ToolPanel from "../../tool-panel/core/ToolPanel.svelte";
  import WorkspacePanel from "../../workspace-panel/core/WorkspacePanel.svelte";
  import ButtonPanel from "../../workspace-panel/shared/components/ButtonPanel.svelte";
  import type { CreateModuleServices } from "../services/ServiceInitializer";
  import type { ICreateModuleInitializationService } from "../services/contracts/ICreateModuleInitializationService";
  import { createCreateModuleState, createConstructTabState } from "../state";
  import type { createCreateModuleState as CreateModuleStateType } from "../state/create-module-state.svelte";
  import type { createConstructTabState as ConstructTabStateType } from "../state/construct-tab-state.svelte";
  import {
    createAutoEditPanelEffect,
    createCurrentWordDisplayEffect,
    createLayoutEffects,
    createNavigationSyncEffects,
    createPanelHeightTracker,
    createPWAEngagementEffect,
    createSingleBeatEditEffect,
  } from "../state/managers";
  import { createPanelCoordinationState } from "../state/panel-coordination-state.svelte";
  import type { IToolPanelMethods } from "../types/create-module-types";
  import {
    AnimationCoordinator,
    CAPCoordinator,
    ConfirmationDialogCoordinator,
    EditCoordinator,
    SequenceActionsCoordinator,
    ShareCoordinator,
  } from "./coordinators";
  import HandPathSettingsView from "./HandPathSettingsView.svelte";
  import { calculateGridLayout } from "../../workspace-panel/sequence-display/utils/grid-calculations";
  import CreationWelcomeScreen from "./CreationWelcomeScreen.svelte";
  import CreationWorkspaceArea from "./CreationWorkspaceArea.svelte";
  import CreationToolPanelSlot from "./CreationToolPanelSlot.svelte";
  import { executeClearSequenceWorkflow } from "../utils/clearSequenceWorkflow";

  const logger = createComponentLogger("CreateModule");

  // Type aliases for state objects
  type CreateModuleState = ReturnType<typeof CreateModuleStateType>;
  type ConstructTabState = ReturnType<typeof ConstructTabStateType>;

  // Props
  let {
    onTabAccessibilityChange,
    onCurrentWordChange,
  }: {
    onTabAccessibilityChange?: (canAccessEditAndExport: boolean) => void;
    onCurrentWordChange?: (word: string) => void;
  } = $props();

  // Services
  let services: CreateModuleServices | null = $state(null);
  let deviceDetector: IDeviceDetector | null = $state(null);

  // State
  let CreateModuleState: CreateModuleState | null = $state(null);
  let constructTabState: ConstructTabState | null = $state(null);

  // Panel coordination state
  let panelState = createPanelCoordinationState();

  // Make panelState available to all descendants via context
  setContext("panelState", panelState);

  // Animation state
  let animatingBeatNumber = $state<number | null>(null);

  // Layout state
  let shouldUseSideBySideLayout = $state<boolean>(false);

  // UI state
  let error = $state<string | null>(null);
  let servicesInitialized = $state<boolean>(false);

  // Panel refs
  let toolPanelElement: HTMLElement | null = $state(null);
  let toolPanelRef: IToolPanelMethods | null = $state(null);
  let buttonPanelElement: HTMLElement | null = $state(null);
  let workspaceContainerElement: HTMLElement | null = $state(null);

  // Workspace container dimensions for grid layout calculation
  let workspaceWidth = $state(0);
  let workspaceHeight = $state(0);

  // Sequence actions sheet state
  let showSequenceActionsSheet = $state(false);

  // Cleanup functions for effects
  let effectCleanups: (() => void)[] = [];

  // Track if user has selected a creation method (starts false, becomes true on selection)
  let hasSelectedCreationMethod = $state(false);

  // Derived: Calculate grid rows based on actual beat count and layout
  const gridRows = $derived(() => {
    if (!CreateModuleState?.sequenceState?.currentSequence) return 0;

    const beatCount = CreateModuleState.getCurrentBeatCount();
    if (beatCount === 0) return 0;

    // Calculate grid layout using the same logic as BeatGrid
    const gridLayout = calculateGridLayout(
      beatCount,
      workspaceWidth,
      workspaceHeight,
      deviceDetector,
      { isSideBySideLayout: shouldUseSideBySideLayout }
    );

    return gridLayout.rows;
  });

  // Derived: Dynamic flex ratios based on grid rows
  const flexRatios = $derived(() => {
    const rows = gridRows();

    // When creation method selector is visible, use collapsed state
    if (navigationState.isCreationMethodSelectorVisible) {
      return { workspace: 2, tool: 4 };
    }

    // Dynamic ratios based on row count
    if (rows === 0) {
      return { workspace: 2, tool: 4 }; // Empty state
    } else if (rows === 1) {
      return { workspace: 3, tool: 5 }; // 1 row: more tool space
    } else if (rows === 2) {
      return { workspace: 4, tool: 5 }; // 2 rows: balanced
    } else if (rows === 3) {
      return { workspace: 4.5, tool: 4.5 }; // 3 rows: equal
    } else {
      return { workspace: 5, tool: 4 }; // 4+ rows: more workspace space
    }
  });

  const creationCueOrientation = $derived(() => {
    return shouldUseSideBySideLayout ? "horizontal" : "vertical";
  });

  const creationCueMood = $derived(() => {
    if (!CreateModuleState) return "default";
    return CreateModuleState.getCreationCueMood(hasSelectedCreationMethod);
  });

  // Derived: Check if workspace is empty (no beats and no start position)
  const isWorkspaceEmpty = $derived(() => {
    if (!CreateModuleState) return true;
    return CreateModuleState.isWorkspaceEmpty();
  });

  // Effect: Sync workspace empty state to navigation (for hiding tabs)
  // Show selector only when workspace is empty AND user hasn't selected a method yet
  $effect(() => {
    const shouldShow = isWorkspaceEmpty() && !hasSelectedCreationMethod;
    navigationState.setCreationMethodSelectorVisible(shouldShow);
  });

  // Effect: Notify parent of tab accessibility changes
  $effect(() => {
    if (!CreateModuleState) return;

    const canAccess = CreateModuleState.canAccessEditTab;
    logger.log("Tab accessibility:", { canAccess });

    if (onTabAccessibilityChange) {
      onTabAccessibilityChange(canAccess);
    }
  });

  // Effect: Notify parent of current word changes (managed by CurrentWordDisplayManager)
  $effect(() => {
    if (!servicesInitialized || !CreateModuleState || !constructTabState) return;

    const cleanup = createCurrentWordDisplayEffect({
      CreateModuleState,
      constructTabState,
      hasSelectedCreationMethod: () => hasSelectedCreationMethod,
      onCurrentWordChange,
    });

    return cleanup;
  });

  // Effect: Setup all managed effects when services are initialized
  $effect(() => {
    if (!servicesInitialized || !CreateModuleState || !services) return;

    // Clean up previous effects
    effectCleanups.forEach((cleanup) => cleanup());
    effectCleanups = [];

    // Navigation sync effects
    const navigationCleanup = createNavigationSyncEffects({
      CreateModuleState,
      navigationState,
      navigationSyncService: services.navigationSyncService,
    });
    effectCleanups.push(navigationCleanup);

    // Layout effects
    const layoutCleanup = createLayoutEffects({
      layoutService: services.layoutService,
      onLayoutChange: (layout) => {
        shouldUseSideBySideLayout = layout;
      },
    });
    effectCleanups.push(layoutCleanup);

    // Auto edit panel effects
    const autoEditCleanup = createAutoEditPanelEffect({
      CreateModuleState,
      panelState,
    });
    effectCleanups.push(autoEditCleanup);

    const singleBeatCleanup = createSingleBeatEditEffect({
      CreateModuleState,
      panelState,
    });
    effectCleanups.push(singleBeatCleanup);

    // PWA engagement tracking
    const pwaCleanup = createPWAEngagementEffect({ CreateModuleState });
    effectCleanups.push(pwaCleanup);

    // Cleanup on unmount
    return () => {
      effectCleanups.forEach((cleanup) => cleanup());
      effectCleanups = [];
    };
  });

  // Effect: Track panel heights
  $effect(() => {
    if (!toolPanelElement && !buttonPanelElement) return;

    const cleanup = createPanelHeightTracker({
      toolPanelElement,
      buttonPanelElement,
      panelState,
    });

    return cleanup;
  });

  // Component initialization
  onMount(async () => {
    if (!ensureContainerInitialized()) {
      error = "Dependency injection container not initialized";
      return;
    }

    try {
      // Use CreateModuleInitializationService for clean initialization
      const initService = resolve<ICreateModuleInitializationService>(
        TYPES.ICreateModuleInitializationService
      );

      const result = await initService.initialize();

      // Unpack services and state from initialization result
      services = {
        sequenceService: result.sequenceService,
        sequencePersistenceService: result.sequencePersistenceService,
        startPositionService: result.startPositionService,
        CreateModuleService: result.CreateModuleService,
        layoutService: result.layoutService,
        navigationSyncService: result.navigationSyncService,
        beatOperationsService: result.beatOperationsService,
        shareService: resolve(TYPES.IShareService),
      };

      CreateModuleState = result.CreateModuleState;
      constructTabState = result.constructTabState;

      // Resolve device detector from layout service (it has it injected)
      deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);

      // Mark services as initialized
      servicesInitialized = true;

      // Configure event callbacks via service
      initService.configureEventCallbacks(CreateModuleState, panelState);

      // Configure clear sequence callback via service
      initService.configureClearSequenceCallback(
        CreateModuleState,
        constructTabState
      );

      logger.success("CreateModule initialized successfully");
    } catch (err) {
      const errorMessage =
        err instanceof Error
          ? err.message
          : "Failed to initialize CreateModule";
      error = errorMessage;
      console.error("CreateModule: Initialization error:", err);
    }
  });

  // Event handlers
  async function handleOptionSelected(option: PictographData): Promise<void> {
    try {
      if (!services?.CreateModuleService) {
        throw new Error("Create Module Service not initialized");
      }
      await services.CreateModuleService.selectOption(option);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to select option";
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

  function handleCreationMethodSelected(method: BuildModeId) {
    // Clear undo history when starting new creation session
    // This creates a clean mental model: each creation session is independent
    if (CreateModuleState) {
      CreateModuleState.clearUndoHistory();
    }

    // Mark that user has selected a creation method
    hasSelectedCreationMethod = true;
    // Switch to the selected tab
    navigationState.setActiveTab(method);
    // The effect will automatically hide the selector based on hasSelectedCreationMethod
  }

  function handleOpenCAPPanel(
    currentType: any,
    selectedComponents: Set<any>,
    onChange: (capType: any) => void
  ) {
    panelState.openCAPPanel(currentType, selectedComponents, onChange);
  }

  async function handleClearSequence() {
    if (!CreateModuleState || !constructTabState) return;

    try {
      await executeClearSequenceWorkflow({
        CreateModuleState,
        constructTabState,
        panelState,
        resetCreationMethodSelection: () => {
          hasSelectedCreationMethod = false;
        },
      });
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to clear sequence";
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
      services.beatOperationsService.removeBeat(beatIndex, CreateModuleState);
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : "Failed to remove beat";
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

{#if error}
  <ErrorBanner message={error} onDismiss={clearError} />
{:else if CreateModuleState && constructTabState && services}
  <div class="create-tab" class:side-by-side={shouldUseSideBySideLayout}>
    <!-- Hand Path Settings View (Pre-Start State) -->
    {#if navigationState.activeTab === "gestural" && !CreateModuleState?.handPathCoordinator?.isStarted}
      <HandPathSettingsView
        handPathCoordinator={CreateModuleState.handPathCoordinator}
      />
    {:else}
      <!-- Standard Workspace/Tool Panel Layout -->
      <div
        class="layout-wrapper"
        in:fade={{ duration: 500, delay: 250, easing: cubicOut }}
      >
        <!-- Workspace Panel -->
        <div
          class="workspace-container"
          class:hidden-workspace={navigationState.activeTab === "gestural" &&
            !CreateModuleState?.handPathCoordinator?.isStarted}
          class:collapsed={navigationState.isCreationMethodSelectorVisible}
        >
          <!-- Workspace Content Area -->
          <div class="workspace-content">
            {#if navigationState.isCreationMethodSelectorVisible}
              <!-- Layout 1: Inviting text when selector is visible -->
              <div
                class="welcome-screen"
                in:fade={{ duration: 400, delay: 200 }}
                out:fade={{ duration: 200 }}
              >
                <!-- Centered welcome content with undo button above -->
                <div
                  class="welcome-content"
                  class:horizontal-cue={creationCueOrientation() ===
                    "horizontal"}
                >
                  <!-- Undo button - centered above title -->
                  {#if CreateModuleState?.canUndo}
                    <button
                      class="welcome-undo-button"
                      onclick={() => CreateModuleState?.undo()}
                      transition:fade={{ duration: 200 }}
                      title={CreateModuleState.undoHistory[
                        CreateModuleState.undoHistory.length - 1
                      ]?.metadata?.description || "Undo last action"}
                    >
                      <svg
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        aria-hidden="true"
                      >
                        <path
                          d="M9 14L4 9L9 4"
                          stroke="currentColor"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                        <path
                          d="M4 9H15A6 6 0 0 1 15 21H13"
                          stroke="currentColor"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                      </svg>
                      <span>Undo</span>
                    </button>
                  {/if}

                  <CreationWelcomeCue
                    orientation={creationCueOrientation()}
                    mood={creationCueMood()}
                  />
                </div>
              </div>
            {:else}
              <!-- Layout 2: Actual workspace when method is selected -->
              <div
                class="workspace-panel-wrapper"
                in:fade={{ duration: 400, delay: 200 }}
                out:fade={{ duration: 300 }}
              >
                <WorkspacePanel
                  sequenceState={CreateModuleState.sequenceState}
                  createModuleState={CreateModuleState}
                  practiceBeatIndex={panelState.practiceBeatIndex}
                  {animatingBeatNumber}
                  isSideBySideLayout={shouldUseSideBySideLayout}
                  isMobilePortrait={services.layoutService.isMobilePortrait()}
                  onPlayAnimation={handlePlayAnimation}
                  animationStateRef={toolPanelRef?.getAnimationStateRef?.()}
                />
              </div>
            {/if}
          </div>

          <!-- Button Panel (hidden when creation method selector is visible) -->
          {#if navigationState.activeTab !== "gestural" && !navigationState.isCreationMethodSelectorVisible}
            <div
              class="button-panel-wrapper"
              bind:this={buttonPanelElement}
              in:fade={{ duration: 400, delay: 200 }}
              out:fade={{ duration: 300 }}
            >
              <ButtonPanel
                {CreateModuleState}
                showPlayButton={CreateModuleState.canShowActionButtons()}
                onPlayAnimation={handlePlayAnimation}
                isAnimating={panelState.isAnimationPanelOpen}
                canClearSequence={CreateModuleState.canClearSequence(
                  hasSelectedCreationMethod
                )}
                onClearSequence={handleClearSequence}
                onRemoveBeat={handleRemoveBeat}
                showShareButton={CreateModuleState.canShowActionButtons()}
                onShare={handleOpenSharePanel}
                isShareOpen={panelState.isSharePanelOpen}
                showSequenceActions={CreateModuleState.canShowActionButtons()}
                onSequenceActionsClick={handleOpenSequenceActions}
              />
            </div>
          {/if}

          <!-- Animation Coordinator -->
          <AnimationCoordinator
            {CreateModuleState}
            {panelState}
            bind:animatingBeatNumber
          />
        </div>

        <!-- Tool Panel or Creation Method Screen -->
        <div class="tool-panel-container" bind:this={toolPanelElement}>
          {#if navigationState.isCreationMethodSelectorVisible}
            <!-- Creation Method Selector (shown when workspace is empty and no method selected) -->
            <div
              class="creation-method-container"
              in:fade={{ duration: 400 }}
              out:fade={{ duration: 400 }}
            >
              <CreationMethodSelector
                onMethodSelected={handleCreationMethodSelected}
              />
            </div>
          {:else}
            <!-- Normal Tool Panel (shown after method selection or when workspace has content) -->
            <div
              class="tool-panel-wrapper"
              in:fade={{ duration: 400, delay: 200 }}
            >
              <ToolPanel
                bind:this={toolPanelRef}
                createModuleState={CreateModuleState}
                {constructTabState}
                onOptionSelected={handleOptionSelected}
                isSideBySideLayout={() => shouldUseSideBySideLayout}
                onPracticeBeatIndexChange={(index) => {
                  panelState.setPracticeBeatIndex(index);
                }}
                onOpenFilters={handleOpenFilterPanel}
                onCloseFilters={() => {
                  panelState.closeFilterPanel();
                }}
                isFilterPanelOpen={panelState.isFilterPanelOpen}
              />
            </div>
          {/if}
        </div>
      </div>
    {/if}
  </div>

  <!-- Edit Coordinator -->
  <EditCoordinator
    {CreateModuleState}
    {panelState}
    beatOperationsService={services.beatOperationsService}
    {shouldUseSideBySideLayout}
    onError={(err) => {
      error = err;
    }}
  />

  <!-- Share Coordinator -->
  <ShareCoordinator
    {CreateModuleState}
    {panelState}
    shareService={services.shareService}
  />

  <!-- Sequence Actions Coordinator -->
  <SequenceActionsCoordinator
    {CreateModuleState}
    {panelState}
    bind:show={showSequenceActionsSheet}
  />

  <!-- CAP Coordinator -->
  <CAPCoordinator {panelState} />

  <!-- Confirmation Dialog Coordinator -->
  <ConfirmationDialogCoordinator {CreateModuleState} />
{/if}

<style>
  .create-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    /* Navigation spacing handled by parent MainInterface.content-area */
    transition: background-color 200ms ease-out;
  }

  .create-tab.side-by-side {
    flex-direction: row;
  }

  .layout-wrapper {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
  }

  .create-tab.side-by-side .layout-wrapper {
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
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative; /* For absolutely positioned button panel */
    transition: flex 300ms cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Collapsed state: workspace container shrinks when creation method selector is visible */
  .workspace-container.collapsed {
    flex: 2;
  }

  /* Hide workspace container when in gestural mode and not started */
  .workspace-container.hidden-workspace {
    opacity: 0;
    pointer-events: none;
    transform: translateY(-20px);
    transition:
      opacity 300ms cubic-bezier(0.4, 0, 0.2, 1),
      transform 300ms cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Workspace content area - fills available space */
  .workspace-content {
    flex: 1;
    min-height: 0;
    position: relative; /* For absolute positioned children */
    overflow: hidden;
  }

  /* Button panel wrapper - absolutely positioned at bottom to prevent layout shift */
  .button-panel-wrapper {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 10;
  }

  /* Welcome screen (Layout 1) */
  .welcome-screen {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(
      135deg,
      rgba(102, 126, 234, 0.1) 0%,
      rgba(118, 75, 162, 0.1) 100%
    );
    backdrop-filter: blur(20px);
    border-radius: 12px;
    overflow: hidden;
  }

  .welcome-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    padding: 2rem;
    text-align: center;
  }

  .welcome-content.horizontal-cue {
    align-items: flex-start;
    text-align: left;
  }

  /* Welcome screen undo button - centered above title in natural flow */
  .welcome-undo-button {
    padding: 0.75rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;

    /* Match ButtonPanel undo button styling */
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;

    /* Smooth transitions */
    transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);

    /* Backdrop blur for better readability */
    backdrop-filter: blur(10px);
  }

  .welcome-undo-button:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    color: rgba(255, 255, 255, 1);
    transform: translateY(-2px);
  }

  .welcome-undo-button:active {
    transform: translateY(0);
  }

  .welcome-undo-button svg {
    flex-shrink: 0;
  }

  .welcome-undo-button span {
    white-space: nowrap;
  }

  /* Workspace panel wrapper (Layout 2) */
  .workspace-panel-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding-bottom: 80px; /* Space for button panel at bottom */
  }

  .tool-panel-container {
    flex: 4;
    min-width: 0;
    position: relative; /* For absolutely positioned creation method selector */
  }

  /* Creation method selector - absolutely positioned to prevent layout shift during transition */
  .creation-method-container {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    z-index: 10; /* Above tool panel */
  }

  /* Tool panel wrapper - normal flexbox layout */
  .tool-panel-wrapper {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
  }

  .create-tab.side-by-side .workspace-container {
    flex: 5;
  }

  /* Side-by-side layout: workspace container collapses differently */
  .create-tab.side-by-side .workspace-container.collapsed {
    flex: 2;
  }

  .create-tab.side-by-side .tool-panel-container {
    flex: 4;
  }
</style>
