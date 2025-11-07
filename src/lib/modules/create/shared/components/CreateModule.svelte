<script lang="ts">
  /**
   * ============================================================================
   * CreateModule - Composition Root for Create Module
   * ============================================================================
   *
   * This is the COMPOSITION ROOT for the Create module. It orchestrates:
   * - Dependency injection and service initialization
   * - Context provision for child components
   * - Reactive effect coordination
   * - Event handling delegation
   * - Layout management
   *
   * ARCHITECTURAL PATTERN: Composition Root
   * ========================================
   * This component intentionally has more responsibilities than typical
   * presentational components because it serves as the application shell
   * for the Create module. This is appropriate and follows clean architecture
   * principles for composition roots.
   *
   * RESPONSIBILITIES:
   * =================
   * 1. SERVICE ORCHESTRATION
   *    - Resolve all required services via DI container
   *    - Initialize state objects (CreateModuleState, constructTabState)
   *    - Set up service lifecycle (initialization, cleanup)
   *
   * 2. CONTEXT PROVISION
   *    - Provide CreateModuleContext to all child components
   *    - Expose reactive state, services, and layout info via context
   *    - Legacy support: panelState via Svelte context
   *
   * 3. EFFECT COORDINATION
   *    - Delegate all reactive effects to CreateModuleEffectCoordinator
   *    - Manage effect lifecycle (setup, cleanup)
   *    - Coordinate cross-cutting concerns (layout, navigation, PWA, etc.)
   *
   * 4. EVENT HANDLING
   *    - Delegate all business logic to handler services
   *    - Manage component-level state (error, animation, UI flags)
   *    - Wire up parent callbacks (onTabAccessibilityChange, onCurrentWordChange)
   *
   * 5. LAYOUT MANAGEMENT
   *    - Track side-by-side vs stacked layout state
   *    - Coordinate with ResponsiveLayoutService
   *    - Provide layout context to child components
   *
   * 6. SESSION STATE MANAGEMENT
   *    - Track creation method selection via CreationMethodPersistenceService
   *    - Sync with workspace empty state for welcome screen visibility
   *
   * CHILD COMPONENTS:
   * =================
   * - CreationWelcomeScreen: Initial welcome/prompt screen
   * - CreationWorkspaceArea: Main pictograph workspace
   * - CreationToolPanelSlot: Tool panel (construct/generate/practice tabs)
   * - ButtonPanel: Action buttons (play, share, clear, etc.)
   * - Coordinators: Modal/panel coordinators (Edit, Share, Animation, etc.)
   *
   * SERVICES USED:
   * ==============
   * - ICreateModuleInitializationService: One-time initialization
   * - ICreateModuleHandlers: Event handling delegation
   * - ICreationMethodPersistenceService: Session storage for creation method
   * - ICreateModuleEffectCoordinator: Reactive effect orchestration
   * - IResponsiveLayoutService: Layout detection and management
   * - Plus all services in CreateModuleServices interface
   *
   *
   * WHY THIS COMPONENT IS LONGER:
   * ==============================
   * This component is intentionally 400-500 lines because:
   * 1. It's a composition root (application shell)
   * 2. It needs to orchestrate DI, context, and lifecycle
   * 3. All business logic is extracted to services
   * 4. All UI logic is extracted to child components
   * 5. Further extraction would scatter initialization flow
   *
   * DO NOT try to make this component smaller by:
   * - Splitting initialization into multiple components
   * - Moving DI resolution to child components
   * - Scattering context setup across multiple files
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
  } from "$shared";
  import { onMount, setContext } from "svelte";
  import { fade } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import ErrorBanner from "./ErrorBanner.svelte";
  import ButtonPanel from "../../workspace-panel/shared/components/ButtonPanel.svelte";
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
  import { AnimationSheetCoordinator } from "$shared/coordinators";
  import HandPathSettingsView from "./HandPathSettingsView.svelte";
  import CreationWelcomeScreen from "./CreationWelcomeScreen.svelte";
  import CreationWorkspaceArea from "./CreationWorkspaceArea.svelte";
  import CreationToolPanelSlot from "./CreationToolPanelSlot.svelte";

  const logger = createComponentLogger("CreateModule");

  // ============================================================================
  // TYPE DEFINITIONS
  // ============================================================================

  type CreateModuleState = ReturnType<typeof CreateModuleStateType>;
  type ConstructTabState = ReturnType<typeof ConstructTabStateType>;

  // ============================================================================
  // PROPS (Parent Callbacks)
  // ============================================================================
  let {
    onTabAccessibilityChange,
    onCurrentWordChange,
  }: {
    onTabAccessibilityChange?: (canAccessEditAndExport: boolean) => void;
    onCurrentWordChange?: (word: string) => void;
  } = $props();

  // ============================================================================
  // DEPENDENCY INJECTION - Services resolved in onMount
  // ============================================================================

  let services: CreateModuleServices | null = $state(null);
  let handlers: ICreateModuleHandlers | null = $state(null);
  let creationMethodPersistence: ICreationMethodPersistenceService | null =
    $state(null);
  let effectCoordinator: ICreateModuleEffectCoordinator | null = $state(null);

  // ============================================================================
  // STATE OBJECTS - Initialized via CreateModuleInitializationService
  // ============================================================================

  let CreateModuleState: CreateModuleState | null = $state(null);
  let constructTabState: ConstructTabState | null = $state(null);

  // ============================================================================
  // PANEL COORDINATION STATE - Manages panel open/close state
  // ============================================================================

  let panelState = createPanelCoordinationState();

  // Make panelState available to all descendants via context (legacy support)
  setContext("panelState", panelState);

  // ============================================================================
  // CONTEXT PROVISION - CreateModuleContext with reactive getters
  // ============================================================================
  // This must be at top level during component initialization.
  // Provides reactive access to state, services, and layout for all descendants.

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
    layout: {
      get shouldUseSideBySideLayout() {
        return shouldUseSideBySideLayout;
      },
      isMobilePortrait: () => {
        if (!services) {
          throw new Error("Services not yet initialized");
        }
        return services.layoutService.isMobilePortrait();
      },
    },
    handlers: {
      onError: (err: string) => {
        error = err;
      },
    },
  });

  // ============================================================================
  // COMPONENT STATE
  // ============================================================================

  // Animation state - tracks currently animating beat
  let animatingBeatNumber = $state<number | null>(null);

  // Layout state - managed by ResponsiveLayoutService
  let shouldUseSideBySideLayout = $state<boolean>(false);

  // UI state
  let error = $state<string | null>(null);
  let servicesInitialized = $state<boolean>(false);

  // Session state - creation method selection (persisted to sessionStorage)
  let hasSelectedCreationMethod = $state(false);

  // Panel references for height tracking
  let toolPanelElement: HTMLElement | null = $state(null);
  let toolPanelRef: IToolPanelMethods | null = $state(null);
  let buttonPanelElement: HTMLElement | null = $state(null);

  // Effect lifecycle management
  let effectCleanup: (() => void) | null = null;

  // ============================================================================
  // DERIVED STATE - Computed values based on reactive state
  // ============================================================================

  // Orientation for creation cue (horizontal in side-by-side, vertical in stacked)
  const creationCueOrientation = $derived(() => {
    return shouldUseSideBySideLayout ? "horizontal" : "vertical";
  });

  // Mood for creation cue (changes based on whether user has selected method)
  const creationCueMood = $derived(() => {
    if (!CreateModuleState) return "default";
    return CreateModuleState.getCreationCueMood(hasSelectedCreationMethod);
  });

  // Check if workspace is empty (no beats and no start position)
  const isWorkspaceEmpty = $derived(() => {
    if (!CreateModuleState) return true;
    return CreateModuleState.isWorkspaceEmpty();
  });

  // ============================================================================
  // REACTIVE EFFECTS
  // ============================================================================

  /**
   * Effect: Sync workspace empty state to navigation
   * Controls creation method selector visibility based on workspace state
   */
  $effect(() => {
    // IMPORTANT: Only sync after persistence is initialized to avoid flash of wrong state
    if (!CreateModuleState?.isPersistenceInitialized) return;

    const shouldShow = isWorkspaceEmpty() && !hasSelectedCreationMethod;
    navigationState.setCreationMethodSelectorVisible(shouldShow);
  });

  /**
   * Effect: Notify parent of tab accessibility changes
   * Enables/disables Edit and Export tabs based on workspace state
   */
  $effect(() => {
    if (!CreateModuleState) return;

    const canAccess = CreateModuleState.canAccessEditTab;
    logger.log("Tab accessibility:", { canAccess });

    if (onTabAccessibilityChange) {
      onTabAccessibilityChange(canAccess);
    }
  });

  /**
   * Effect: Setup all managed effects using EffectCoordinator
   *
   * Delegates all reactive effect setup to CreateModuleEffectCoordinator service.
   * This includes:
   * - Navigation synchronization
   * - Layout management
   * - Auto edit panel behavior
   * - Single beat edit mode
   * - PWA engagement tracking
   * - Current word display updates
   * - Panel height tracking
   */
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

    // Clean up previous effects
    if (effectCleanup) {
      effectCleanup();
      effectCleanup = null;
    }

    // Set up all effects via coordinator
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
      },
      ...(onCurrentWordChange ? { onCurrentWordChange } : {}),
      toolPanelElement,
      buttonPanelElement,
    });

    // Cleanup on unmount
    return () => {
      if (effectCleanup) {
        effectCleanup();
        effectCleanup = null;
      }
    };
  });

  // ============================================================================
  // LIFECYCLE - Component Initialization
  // ============================================================================

  /**
   * onMount: Initialize all services and state
   *
   * This is the composition root's initialization sequence:
   * 1. Verify DI container is initialized
   * 2. Resolve CreateModuleInitializationService
   * 3. Initialize all services and state objects
   * 4. Resolve handler services
   * 5. Resolve persistence and effect coordinator services
   * 6. Configure event callbacks
   * 7. Restore session state (creation method selection)
   */
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

      // Initialize handlers service
      handlers = resolve<ICreateModuleHandlers>(TYPES.ICreateModuleHandlers);

      // Initialize creation method persistence service
      creationMethodPersistence = resolve<ICreationMethodPersistenceService>(
        TYPES.ICreationMethodPersistenceService
      );

      // Initialize effect coordinator service
      effectCoordinator = resolve<ICreateModuleEffectCoordinator>(
        TYPES.ICreateModuleEffectCoordinator
      );

      // Read initial creation method selection state
      hasSelectedCreationMethod =
        creationMethodPersistence.hasUserSelectedMethod();

      // Mark services as initialized
      servicesInitialized = true;

      // Configure event callbacks via service
      initService.configureEventCallbacks(CreateModuleState, panelState);

      // Configure clear sequence callback via service
      initService.configureClearSequenceCallback(
        CreateModuleState,
        constructTabState
      );

      // If persistence restored existing data, treat creation method as selected
      if (
        !hasSelectedCreationMethod &&
        CreateModuleState &&
        !CreateModuleState.isWorkspaceEmpty()
      ) {
        logger.log(
          "📦 Marking creation method as selected due to restored data"
        );
        hasSelectedCreationMethod = true;
        creationMethodPersistence.markMethodSelected();
      }

      logger.log("✅ CreateModule state after initialization:", {
        servicesInitialized,
        isPersistenceInitialized:
          CreateModuleState?.isPersistenceInitialized ?? false,
        hasSelectedCreationMethod,
        isWorkspaceEmpty: CreateModuleState?.isWorkspaceEmpty() ?? true,
        isCreationMethodSelectorVisible:
          navigationState.isCreationMethodSelectorVisible,
      });

      // Context is already set up at top level with reactive getters
      // Services, CreateModuleState, and constructTabState are now initialized
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

  // ============================================================================
  // EVENT HANDLERS - Delegated to Service Layer
  // ============================================================================
  // All business logic is handled by services.
  // These functions only manage component-level state and service delegation.

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

  function handleCreationMethodSelected(method: BuildModeId) {
    if (!handlers || !creationMethodPersistence) return;
    handlers.handleCreationMethodSelected(
      method,
      CreateModuleState,
      navigationState,
      () => {
        hasSelectedCreationMethod = true;
        creationMethodPersistence!.markMethodSelected();
      }
    );
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
              <!-- Layout 1: Welcome screen when selector is visible -->
              <CreationWelcomeScreen
                orientation={creationCueOrientation()}
                mood={creationCueMood()}
              />
            {:else}
              <!-- Layout 2: Actual workspace when method is selected -->
              {@const animStateRef = toolPanelRef?.getAnimationStateRef?.()}
              <CreationWorkspaceArea
                {animatingBeatNumber}
                onPlayAnimation={handlePlayAnimation}
                {...animStateRef ? { animationStateRef: animStateRef } : {}}
              />
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
                onPlayAnimation={handlePlayAnimation}
                onClearSequence={handleClearSequence}
                onShare={handleOpenSharePanel}
                onSequenceActionsClick={handleOpenSequenceActions}
              />
            </div>
          {/if}

          <!-- Animation Coordinator -->
          <AnimationSheetCoordinator
            sequence={CreateModuleState.sequenceState.currentSequence}
            bind:isOpen={panelState.isAnimationPanelOpen}
            bind:animatingBeatNumber
            combinedPanelHeight={panelState.combinedPanelHeight}
          />
        </div>

        <!-- Tool Panel or Creation Method Screen -->
        <div class="tool-panel-container" bind:this={toolPanelElement}>
          <CreationToolPanelSlot
            bind:toolPanelRef
            onMethodSelected={handleCreationMethodSelected}
            onOptionSelected={handleOptionSelected}
            onPracticeBeatIndexChange={(index) => {
              panelState.setPracticeBeatIndex(index);
            }}
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

  /* Styles moved to extracted components:
   * - Welcome screen styles → CreationWelcomeScreen.svelte
   * - Workspace panel wrapper → CreationWorkspaceArea.svelte
   */

  .tool-panel-container {
    flex: 4;
    min-width: 0;
    position: relative; /* For absolutely positioned creation method selector */
  }

  /* Tool panel styles moved to CreationToolPanelSlot.svelte */

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
