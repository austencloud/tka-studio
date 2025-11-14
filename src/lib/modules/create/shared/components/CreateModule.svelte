<script lang="ts">
  /**
   * CreateModule - Composition Root for Create Module
   * See: docs/architecture/create-module-composition-root.md for detailed architecture documentation
   *
   * Domain: Create module - Composition Root
   */

  import {
    createComponentLogger,
    ensureContainerInitialized,
    navigationState,
    resolve,
    TYPES,
    type BuildModeId,
    type PictographData,
    setAnyPanelOpen,
    setSideBySideLayout,
    AnimationSheetCoordinator,
    Drawer,
    ConfirmDialog,
  } from "$shared";
  import { onMount, setContext, tick } from "svelte";
  import ErrorBanner from "./ErrorBanner.svelte";
  import type { CreateModuleServices } from "../services/ServiceInitializer";
  import type { ICreateModuleInitializationService } from "../services/contracts/ICreateModuleInitializationService";
  import type { ICreateModuleHandlers } from "../services/contracts/ICreateModuleHandlers";
  import type { ICreationMethodPersistenceService } from "../services/contracts/ICreationMethodPersistenceService";
  import type { ICreateModuleEffectCoordinator } from "../services/contracts/ICreateModuleEffectCoordinator";
  import type { createCreateModuleState as CreateModuleStateType } from "../state/create-module-state.svelte";
  import type { createConstructTabState as ConstructTabStateType } from "../state/construct-tab-state.svelte";
  import { setCreateModuleContext } from "../context";
  import { createPanelCoordinationState } from "../state/panel-coordination-state.svelte";
  import { setCreateModuleStateRef } from "../state/create-module-state-ref.svelte";
  import type { IToolPanelMethods } from "../types/create-module-types";
  import {
    CAPCoordinator,
    EditCoordinator,
    SequenceActionsCoordinator,
    ShareCoordinator,
  } from "./coordinators";
  import ConfirmationDialogCoordinator from "./coordinators/ConfirmationDialogCoordinator.svelte";
  import HandPathSettingsView from "./HandPathSettingsView.svelte";
  import StandardWorkspaceLayout from "./StandardWorkspaceLayout.svelte";
  import CreationMethodSelector from "../workspace-panel/components/CreationMethodSelector.svelte";

  const logger = createComponentLogger("CreateModule");

  type CreateModuleState = ReturnType<typeof CreateModuleStateType>;
  type ConstructTabState = ReturnType<typeof ConstructTabStateType>;

  // ============================================================================
  // PROPS
  // ============================================================================
  let {
    onTabAccessibilityChange,
    onCurrentWordChange,
  }: {
    onTabAccessibilityChange?: (canAccessEditAndExport: boolean) => void;
    onCurrentWordChange?: (word: string) => void;
  } = $props();

  // ============================================================================
  // SERVICES & STATE (Resolved via DI)
  // ============================================================================
  let services: CreateModuleServices | null = $state(null);
  let handlers: ICreateModuleHandlers | null = $state(null);
  let creationMethodPersistence: ICreationMethodPersistenceService | null =
    $state(null);
  let effectCoordinator: ICreateModuleEffectCoordinator | null = $state(null);
  let CreateModuleState: CreateModuleState | null = $state(null);
  let constructTabState: ConstructTabState | null = $state(null);

  // ============================================================================
  // COMPONENT STATE
  // ============================================================================
  let panelState = createPanelCoordinationState();
  let animatingBeatNumber = $state<number | null>(null);
  let shouldUseSideBySideLayout = $state<boolean>(false);
  let error = $state<string | null>(null);
  let servicesInitialized = $state<boolean>(false);
  let hasSelectedCreationMethod = $state(false);

  // Transfer confirmation dialog state
  let showTransferConfirmation = $state(false);
  let isMobile = $state(false);
  let sequenceToTransfer: PictographData[] | null = $state(null);
  let toolPanelElement: HTMLElement | null = $state(null);
  let toolPanelRef: IToolPanelMethods | null = $state(null);
  let buttonPanelElement: HTMLElement | null = $state(null);
  let effectCleanup: (() => void) | null = null;


  // ============================================================================
  // CONTEXT PROVISION
  // ============================================================================
  setContext("panelState", panelState);

  const layoutContext = {
    get shouldUseSideBySideLayout() {
      return shouldUseSideBySideLayout;
    },
    isMobilePortrait() {
      return services?.layoutService?.isMobilePortrait() ?? false;
    },
  };

  setCreateModuleContext({
    get CreateModuleState() {
      if (!CreateModuleState) {
        throw new Error("CreateModuleState not yet initialized");
      }
      return CreateModuleState;
    },
    get constructTabState() {
      if (!constructTabState) {
        throw new Error("constructTabState not yet initialized");
      }
      return constructTabState;
    },
    panelState,
    get services() {
      if (!services) {
        throw new Error("Services not yet initialized");
      }
      return services;
    },
    layout: layoutContext,
    handlers: {
      onError: (err: string) => {
        error = err;
      },
    },
  });

  // ============================================================================
  // DERIVED STATE
  // ============================================================================
  const isWorkspaceEmpty = $derived(() => {
    if (!CreateModuleState) return true;
    return CreateModuleState.isWorkspaceEmpty();
  });

  // ============================================================================
  // REACTIVE EFFECTS
  // ============================================================================

  // Sync workspace empty state to navigation
  $effect(() => {
    if (!CreateModuleState?.isPersistenceInitialized) return;
    const shouldShow = isWorkspaceEmpty() && !hasSelectedCreationMethod;
    navigationState.setCreationMethodSelectorVisible(shouldShow);
  });

  // Notify parent of tab accessibility changes
  $effect(() => {
    if (!CreateModuleState) return;
    const canAccess = CreateModuleState.canAccessEditTab;
    if (onTabAccessibilityChange) {
      onTabAccessibilityChange(canAccess);
    }
  });

  // Sync panel states and layout to global state
  $effect(() => {
    setAnyPanelOpen(panelState.isAnyPanelOpen);
    setSideBySideLayout(shouldUseSideBySideLayout);
  });

  // Setup all managed effects using EffectCoordinator
  $effect(() => {
    if (
      !servicesInitialized ||
      !CreateModuleState ||
      !constructTabState ||
      !services ||
      !effectCoordinator
    ) {
      return;
    }

    if (effectCleanup) {
      effectCleanup();
      effectCleanup = null;
    }

    effectCleanup = effectCoordinator.setupEffects({
      CreateModuleState,
      constructTabState,
      panelState,
      navigationState,
      layoutService: services.layoutService,
      navigationSyncService: services.navigationSyncService,
      hasSelectedCreationMethod: () => hasSelectedCreationMethod,
      onLayoutChange: (layout) => {
        shouldUseSideBySideLayout = layout;
        setSideBySideLayout(layout);
      },
      ...(onCurrentWordChange ? { onCurrentWordChange } : {}),
      toolPanelElement,
      buttonPanelElement,
    });

    return () => {
      if (effectCleanup) {
        effectCleanup();
        effectCleanup = null;
      }
    };
  });

  // ============================================================================
  // LIFECYCLE
  // ============================================================================
  onMount(async () => {
    if (!ensureContainerInitialized()) {
      error = "Dependency injection container not initialized";
      return;
    }

    try {
      const initService = resolve<ICreateModuleInitializationService>(
        TYPES.ICreateModuleInitializationService
      );

      const result = await initService.initialize();

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

      // Set global reference for keyboard shortcuts
      setCreateModuleStateRef({
        CreateModuleState,
        constructTabState,
        panelState,
      });

      handlers = resolve<ICreateModuleHandlers>(TYPES.ICreateModuleHandlers);
      creationMethodPersistence = resolve<ICreationMethodPersistenceService>(
        TYPES.ICreationMethodPersistenceService
      );
      effectCoordinator = resolve<ICreateModuleEffectCoordinator>(
        TYPES.ICreateModuleEffectCoordinator
      );

      hasSelectedCreationMethod =
        creationMethodPersistence.hasUserSelectedMethod();
      servicesInitialized = true;

      initService.configureEventCallbacks(CreateModuleState, panelState);
      initService.configureClearSequenceCallback(
        CreateModuleState,
        constructTabState
      );

      if (
        !hasSelectedCreationMethod &&
        CreateModuleState &&
        !CreateModuleState.isWorkspaceEmpty()
      ) {
        hasSelectedCreationMethod = true;
        creationMethodPersistence.markMethodSelected();
      }

      logger.success("CreateModule initialized successfully");

      // Check for pending edit sequence from Explorer module
      await tick(); // Ensure DOM is ready
      const pendingSequenceData = localStorage.getItem("tka-pending-edit-sequence");
      if (pendingSequenceData && CreateModuleState) {
        try {
          const sequence = JSON.parse(pendingSequenceData);
          console.log("📝 Loading pending edit sequence:", sequence.id);

          // Load the sequence into the workspace
          CreateModuleState.sequenceState.setCurrentSequence(sequence);

          // Clear the pending flag
          localStorage.removeItem("tka-pending-edit-sequence");

          // Mark that a creation method has been selected
          if (!hasSelectedCreationMethod) {
            hasSelectedCreationMethod = true;
            creationMethodPersistence.markMethodSelected();
          }

          logger.success("Loaded sequence for editing:", sequence.word || sequence.id);
        } catch (err) {
          console.error("❌ Failed to load pending edit sequence:", err);
          localStorage.removeItem("tka-pending-edit-sequence"); // Clear invalid data
        }
      }

      // Detect if we're on mobile for responsive dialog rendering
      const checkIsMobile = () => {
        isMobile = window.innerWidth < 768;
      };
      checkIsMobile();
      window.addEventListener("resize", checkIsMobile);

      // Cleanup resize listener on unmount
      return () => {
        window.removeEventListener("resize", checkIsMobile);
      };
    } catch (err) {
      error =
        err instanceof Error ? err.message : "Failed to initialize CreateModule";
      console.error("CreateModule: Initialization error:", err);
    }

    // Cleanup on unmount
    return () => {
      // Clear global reference for keyboard shortcuts
      setCreateModuleStateRef(null);
    };
  });

  // ============================================================================
  // EVENT HANDLERS (Delegated to Services)
  // ============================================================================
  async function handleOptionSelected(option: PictographData): Promise<void> {
    if (!handlers) {
      error = "Handlers service not initialized";
      return;
    }
    try {
      await handlers.handleOptionSelected(option);
    } catch (err) {
      error = err instanceof Error ? err.message : "Failed to select option";
    }
  }

  function clearError() {
    error = null;
  }

  function handlePlayAnimation() {
    if (!handlers) return;
    handlers.handlePlayAnimation(panelState);
  }

  function handleOpenSharePanel() {
    if (!handlers) return;
    handlers.handleOpenSharePanel(panelState);
  }

  async function handleCreationMethodSelected(method: BuildModeId) {
    if (!handlers || !creationMethodPersistence) return;

    // FIRST: Set the active tab (but keep selector visible)
    navigationState.setActiveTab(method);
    CreateModuleState?.clearUndoHistory();

    // Wait for Svelte to apply DOM updates
    await tick();

    // Wait multiple frames to ensure effects have completed and tool panel has fully rendered
    // Frame 1: Effect is scheduled
    await new Promise(resolve => requestAnimationFrame(resolve));
    // Frame 2: Effect executes and updates DOM
    await new Promise(resolve => requestAnimationFrame(resolve));
    // Frame 3: Browser paints the new content
    await new Promise(resolve => requestAnimationFrame(resolve));

    // THEN: Mark as selected (which triggers the crossfade via effect)
    hasSelectedCreationMethod = true;
    creationMethodPersistence.markMethodSelected();
  }

  async function handleClearSequence() {
    if (
      !handlers ||
      !CreateModuleState ||
      !constructTabState ||
      !creationMethodPersistence
    )
      return;

    try {
      await handlers.handleClearSequence({
        CreateModuleState,
        constructTabState,
        panelState,
        resetCreationMethodSelection: () => {
          hasSelectedCreationMethod = false;
          creationMethodPersistence!.resetSelection();
        },
        shouldResetCreationMethod: false, // Keep creation mode selected, just reset to start position picker
      });
    } catch (err) {
      error = err instanceof Error ? err.message : "Failed to clear sequence";
    }
  }

  function handleOpenFilterPanel() {
    if (!handlers) return;
    handlers.handleOpenFilterPanel(panelState);
  }

  function handleOpenSequenceActions() {
    if (!handlers) return;
    handlers.handleOpenSequenceActions(panelState);
  }

  /**
   * Handle Edit in Constructor - Transfer sequence from Generator to Constructor
   * This allows users to continue editing a generated sequence manually
   */
  async function handleEditInConstructor() {
    if (!CreateModuleState || !services) return;

    // Verify we're in Generator tab
    const currentTab = navigationState.activeTab;
    if (currentTab !== "generator") {
      console.warn("Edit in Constructor can only be used from Generator tab");
      return;
    }

    // Get the current sequence
    const currentSequence = CreateModuleState.sequenceState.currentSequence;
    if (!currentSequence) {
      console.warn("No sequence to transfer to Constructor");
      return;
    }

    // Check if Constructor workspace has existing content
    const constructorState = await services.sequencePersistenceService.loadCurrentState("constructor");
    const hasConstructorContent = constructorState?.currentSequence &&
                                   constructorState.currentSequence.beats.length > 0;

    if (hasConstructorContent) {
      // Store the sequence to transfer and show confirmation dialog
      sequenceToTransfer = currentSequence.beats.map(beat => ({
        ...beat,
        arrows: beat.arrows,
        grid: beat.grid,
      }));
      showTransferConfirmation = true;
      console.log("⚠️ Constructor has content - showing confirmation dialog");
    } else {
      // No conflict - proceed with transfer immediately
      await transferSequenceToConstructor(currentSequence);
    }
  }

  /**
   * Transfer sequence to Constructor workspace
   */
  async function transferSequenceToConstructor(sequence: any) {
    if (!services || !CreateModuleState) return;

    try {
      // Save the sequence to Constructor's localStorage key
      await services.sequencePersistenceService.saveCurrentState({
        currentSequence: sequence,
        selectedStartPosition: sequence.beats[0] || null,
        hasStartPosition: sequence.beats.length > 0,
        activeBuildSection: "constructor",
      });

      // Switch to Constructor tab
      navigationState.setActiveTab("constructor");

      console.log("✓ Transferred sequence to Constructor for editing");
    } catch (error) {
      console.error("❌ Failed to transfer sequence to Constructor:", error);
    }
  }

  /**
   * Handle confirmation of sequence transfer
   */
  async function handleConfirmTransfer() {
    if (!sequenceToTransfer || !CreateModuleState) return;

    const currentSequence = CreateModuleState.sequenceState.currentSequence;
    if (currentSequence) {
      await transferSequenceToConstructor(currentSequence);
    }

    // Reset state
    showTransferConfirmation = false;
    sequenceToTransfer = null;
  }

  /**
   * Handle cancellation of sequence transfer
   */
  function handleCancelTransfer() {
    showTransferConfirmation = false;
    sequenceToTransfer = null;
    console.log("❌ Sequence transfer cancelled by user");
  }
</script>

{#if error}
  <ErrorBanner message={error} onDismiss={clearError} />
{:else if CreateModuleState && constructTabState && services && CreateModuleState.isPersistenceInitialized}
  <div class="create-tab">
    <!-- Hand Path Settings View (Pre-Start State) -->
    {#if navigationState.activeTab === "gestural" && !CreateModuleState?.handPathCoordinator?.isStarted}
      <HandPathSettingsView
        handPathCoordinator={CreateModuleState.handPathCoordinator}
      />
    {:else}
      <!-- Crossfade wrapper for smooth transitions -->
      <div class="transition-wrapper">
        <!-- Creation Method Selector -->
        <div
          class="transition-view"
          class:active={navigationState.isCreationMethodSelectorVisible}
          class:inactive={!navigationState.isCreationMethodSelectorVisible}
        >
          <CreationMethodSelector onMethodSelected={handleCreationMethodSelected} />
        </div>

        <!-- Standard Workspace/Tool Panel Layout -->
        <div
          class="transition-view"
          class:active={!navigationState.isCreationMethodSelectorVisible}
          class:inactive={navigationState.isCreationMethodSelectorVisible}
        >
          <StandardWorkspaceLayout
            {shouldUseSideBySideLayout}
            {CreateModuleState}
            {panelState}
            bind:animatingBeatNumber
            bind:toolPanelRef
            bind:buttonPanelElement
            bind:toolPanelElement
            onPlayAnimation={handlePlayAnimation}
            onClearSequence={handleClearSequence}
            onShare={handleOpenSharePanel}
            onSequenceActionsClick={handleOpenSequenceActions}
            onEditInConstructor={handleEditInConstructor}
            onOptionSelected={handleOptionSelected}
            onOpenFilters={handleOpenFilterPanel}
            onCloseFilters={() => {
              panelState.closeFilterPanel();
            }}
          />
        </div>
      </div>
    {/if}
  </div>

  <!-- Edit Coordinator -->
  <EditCoordinator />

  <!-- Share Coordinator -->
  <ShareCoordinator />

  <!-- Sequence Actions Coordinator -->
  <SequenceActionsCoordinator />

  <!-- Animation Coordinator - Rendered outside stacking context to appear above navigation -->
  {#if CreateModuleState}
    <AnimationSheetCoordinator
      sequence={CreateModuleState.sequenceState.currentSequence}
      bind:isOpen={panelState.isAnimationPanelOpen}
      bind:animatingBeatNumber
      combinedPanelHeight={panelState.combinedPanelHeight}
    />
  {/if}

  <!-- CAP Coordinator -->
  <CAPCoordinator />

  <!-- Confirmation Dialog Coordinator -->
  <ConfirmationDialogCoordinator />

  <!-- Sequence Transfer Confirmation Dialog -->
  {#if isMobile}
    <!-- Mobile: Bottom Sheet -->
    <Drawer
      isOpen={showTransferConfirmation}
      onClose={handleCancelTransfer}
      title="Replace Constructor Content?"
    >
      {#snippet content()}
        <div class="transfer-confirmation-content">
          <p class="confirmation-message">
            The Constructor workspace already has content. Transferring this sequence will replace it.
          </p>
          <div class="confirmation-actions">
            <button class="cancel-button" onclick={handleCancelTransfer}>
              Cancel
            </button>
            <button class="confirm-button" onclick={handleConfirmTransfer}>
              Replace & Transfer
            </button>
          </div>
        </div>
      {/snippet}
    </Drawer>
  {:else}
    <!-- Desktop: Confirm Dialog -->
    <ConfirmDialog
      bind:isOpen={showTransferConfirmation}
      title="Replace Constructor Content?"
      message="The Constructor workspace already has content. Transferring this sequence will replace it."
      confirmText="Replace & Transfer"
      cancelText="Cancel"
      variant="warning"
      onConfirm={handleConfirmTransfer}
      onCancel={handleCancelTransfer}
    />
  {/if}
{/if}

<style>
  .create-tab {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    transition: background-color 200ms ease-out;
  }

  /* Crossfade transition system */
  .transition-wrapper {
    position: relative;
    flex: 1;
    min-height: 0;
    overflow: hidden;
  }

  .transition-view {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    transition: opacity 400ms cubic-bezier(0.4, 0, 0.2, 1);
  }

  .transition-view.active {
    opacity: 1;
    pointer-events: auto;
    z-index: 1;
  }

  .transition-view.inactive {
    opacity: 0;
    pointer-events: none;
    z-index: 0;
  }

  /* Transfer Confirmation Dialog Styles */
  .transfer-confirmation-content {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .confirmation-message {
    color: rgba(255, 255, 255, 0.9);
    font-size: 16px;
    line-height: 1.6;
    margin: 0;
  }

  .confirmation-actions {
    display: flex;
    gap: 12px;
    justify-content: flex-end;
  }

  .confirmation-actions button {
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 15px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 2px solid transparent;
    min-width: 120px;
  }

  .cancel-button {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.9);
    border-color: rgba(255, 255, 255, 0.2);
  }

  .cancel-button:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
  }

  .confirm-button {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    border-color: rgba(255, 255, 255, 0.2);
  }

  .confirm-button:hover {
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .confirmation-actions {
      flex-direction: column;
    }

    .confirmation-actions button {
      width: 100%;
    }
  }
</style>
