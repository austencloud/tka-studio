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
  import CreationMethodSelector from "../../workspace-panel/components/CreationMethodSelector.svelte";

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
    } catch (err) {
      error =
        err instanceof Error ? err.message : "Failed to initialize CreateModule";
      console.error("CreateModule: Initialization error:", err);
    }
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

  <!-- CAP Coordinator -->
  <CAPCoordinator />

  <!-- Confirmation Dialog Coordinator -->
  <ConfirmationDialogCoordinator />
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
</style>
