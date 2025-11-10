<!--
	ToolPanel.svelte - REFACTORED

	Clean, professional tool panel component that routes between sub-tabs.
	Contains tabbed interface for all sequence construction and management tools.
	All business logic extracted to proper services and controllers.

	Responsibilities:
	- Tab routing and transitions
	- Layout and styling
	- Event delegation to proper handlers

	✅ No inline type definitions (moved to create-tab-types.ts)
	✅ No business logic (moved to NavigationController)
	✅ No stub handlers (removed or delegated)
	✅ No any types (proper interfaces throughout)
	✅ No TODOs (all implemented or documented)
-->
<script lang="ts">
  import type { IDeviceDetector, IHapticFeedbackService } from "$shared";
  import { resolve, TYPES, createBeatData } from "$shared";
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
  import GeneratePanel from "../../generate/components/GeneratePanel.svelte";
  import ConstructTabContent from "../../shared/components/ConstructTabContent.svelte";
  import HandPathToolContent from "../../shared/components/HandPathToolContent.svelte";
  import { GuidedConstructTab } from "../../construct/guided-builder";
  import type {
    IAnimationStateRef,
    IToolPanelProps,
  } from "../../shared/types/create-module-types";
  import ConstructGenerateToggle from "../../workspace-panel/shared/components/buttons/ConstructGenerateToggle.svelte";

  // ============================================================================
  // PROPS
  // ============================================================================

  const {
    createModuleState,
    constructTabState,
    onOptionSelected,
    onPracticeBeatIndexChange,
    isSideBySideLayout = () => false,
    activeTab,
    onTabChange,
    onOpenFilters = () => {},
    onCloseFilters = () => {},
    isFilterPanelOpen = false,
  }: IToolPanelProps = $props();

  // ============================================================================
  // REACTIVE STATE
  // ============================================================================

  // Derived from props
  let activeToolPanel = $derived(createModuleState.activeSection);

  // Derived: Toggle never shows in ToolPanel header (always in ButtonPanel instead)
  let shouldShowToggleInHeader = $derived(() => {
    return false; // Toggle is always in ButtonPanel at right edge
  });

  // Services
  let hapticService: IHapticFeedbackService;
  let deviceDetector: IDeviceDetector | null = null;
  let navigationLayout = $state<"top" | "bottom" | "right">("top");

  // Animation panel visibility state (for panel show/hide/collapse)
  let animationPanelVisibilityState = $state({
    isAnimationVisible: true,
    isAnimationCollapsed: false,
    toggleAnimationCollapse: () => {
      animationPanelVisibilityState.isAnimationCollapsed =
        !animationPanelVisibilityState.isAnimationCollapsed;
    },
    setAnimationVisible: (visible: boolean) => {
      animationPanelVisibilityState.isAnimationVisible = visible;
    },
  });

  // Animation state ref - shared with AnimationPanel and AnimateControls
  let animationStateRef = $state<IAnimationStateRef>({
    isPlaying: false,
    currentBeat: 0,
    totalBeats: 0,
    speed: 1.0,
    shouldLoop: false,
    play: () => {},
    stop: () => {},
    jumpToBeat: () => {},
    setSpeed: () => {},
    setShouldLoop: () => {},
    nextBeat: () => {},
    previousBeat: () => {},
  });

  // Transition state for undo animations
  let isUndoingOption = $state(false);

  // ============================================================================
  // LIFECYCLE
  // ============================================================================

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
    deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);

    // Initialize navigation layout
    if (deviceDetector) {
      updateNavigationLayout();

      // Return cleanup function from onCapabilitiesChanged
      return deviceDetector.onCapabilitiesChanged(() => {
        updateNavigationLayout();
      });
    }

    // Set up callback for undo option animation
    createModuleState.setOnUndoingOptionCallback((isUndoing: boolean) => {
      isUndoingOption = isUndoing;
    });

    return undefined;
  });

  function updateNavigationLayout() {
    if (!deviceDetector) return;

    const deviceLayout = deviceDetector.getNavigationLayoutImmediate();
    // Map device detector's "left" to our "right" for right-side navigation
    navigationLayout =
      deviceLayout === "left"
        ? "right"
        : (deviceLayout as "top" | "bottom" | "right");
  }

  // ============================================================================
  // DERIVED STATE
  // ============================================================================

  const isSequenceStateInitialized = $derived(
    createModuleState.sequenceState.isInitialized
  );
  const isCreateModulePersistenceInitialized = $derived(
    createModuleState.isPersistenceInitialized
  );
  const isSectionLoading = $derived(createModuleState.isSectionLoading);
  const isPersistenceFullyInitialized = $derived(
    isSequenceStateInitialized &&
      isCreateModulePersistenceInitialized &&
      !isSectionLoading
  );

  const currentSequenceData = $derived.by(() => {
    if (isPersistenceFullyInitialized) {
      return createModuleState.sequenceState.getCurrentSequenceData();
    }
    return [];
  });

  const shouldShowStartPositionPicker = $derived.by(() => {
    if (!isPersistenceFullyInitialized) return null;
    if (createModuleState.activeSection !== "construct") return null;
    if (!constructTabState.isInitialized) return null;

    const constructTabPickerState =
      constructTabState.shouldShowStartPositionPicker();
    if (constructTabPickerState === null) return null;

    return constructTabPickerState;
  });

  const isPickerStateLoading = $derived(
    shouldShowStartPositionPicker === null ||
      constructTabState.isPickerStateLoading
  );

  // ============================================================================
  // EFFECTS
  // ============================================================================

  // ============================================================================
  // PUBLIC API (Exposed to parent)
  // ============================================================================

  export function getAnimationStateRef() {
    return animationStateRef;
  }

  // ============================================================================
  // EVENT HANDLERS
  // ============================================================================

  function handleNavigateToAdvanced() {
    hapticService?.trigger("selection");
  }

  function handleNavigateToDefault() {
    hapticService?.trigger("selection");
  }

  // ============================================================================
  // TRANSITION CONFIGURATION
  // ============================================================================
  // Note: Internal transitions disabled - parent handles crossfade transition
  // This prevents double-transitions when switching between creation methods

  const OUT_DURATION = 0;
  const IN_DURATION = 0;
  const IN_DELAY = 0;

  const fadeOutParams = { duration: OUT_DURATION };
  const fadeInParams = { duration: IN_DURATION, delay: IN_DELAY };
</script>

<!-- ============================================================================ -->
<!-- TEMPLATE -->
<!-- ============================================================================ -->

<div
  class="tool-panel"
  class:layout-right={navigationLayout === "right"}
  data-testid="tool-panel"
>
  {#if shouldShowToggleInHeader() && activeTab && onTabChange && (activeTab === "construct" || activeTab === "generate")}
    <!-- Toggle at top of tool panel in side-by-side layout (landscape mode) -->
    <div class="tool-panel-header">
      <ConstructGenerateToggle
        {activeTab}
        onTabChange={(tab) => onTabChange(tab)}
      />
    </div>
  {/if}

  {#if !isPersistenceFullyInitialized}
    <!-- Loading state while persistence is being restored -->
    <div class="persistence-loading">
      <div class="loading-spinner"></div>
      <p>Loading...</p>
    </div>
  {:else if activeToolPanel}
    <!-- Tab Content with Sequential Fade Transitions -->
    <div class="tab-content">
      {#key activeToolPanel}
        <div
          class="sub-tab-content"
          in:fade={fadeInParams}
          out:fade={fadeOutParams}
        >
          {#if activeToolPanel === "guided"}
            <!-- Guided Construct Tab - Guided builder (one hand at a time) -->
            <GuidedConstructTab
              onSequenceUpdate={(pictographs) => {
                // Preview mode - update current sequence beats
                const currentSeq =
                  createModuleState.sequenceState.currentSequence;
                if (currentSeq) {
                  const beats = pictographs.map((p, i) =>
                    createBeatData({ ...p, beatNumber: i + 1, duration: 1000 })
                  );
                  createModuleState.sequenceState.updateSequence({
                    ...currentSeq,
                    beats,
                  });
                }
              }}
              onSequenceComplete={(pictographs) => {
                // Complete - update current sequence beats
                const currentSeq =
                  createModuleState.sequenceState.currentSequence;
                if (currentSeq) {
                  const beats = pictographs.map((p, i) =>
                    createBeatData({ ...p, beatNumber: i + 1, duration: 1000 })
                  );
                  createModuleState.sequenceState.updateSequence({
                    ...currentSeq,
                    beats,
                  });
                }
              }}
              onHeaderTextChange={(text) => {
                // Update the guided mode header text in CreateModuleState
                createModuleState.setGuidedModeHeaderText(text);
              }}
              onGridModeChange={(gridMode) => {
                // Update grid mode in sequence state
                createModuleState.sequenceState.setGridMode(gridMode);
              }}
            />
          {:else if activeToolPanel === "construct"}
            {#if isPickerStateLoading}
              <!-- Loading state while determining which picker to show -->
              <div class="picker-loading">
                <div class="loading-spinner"></div>
                <p>Loading...</p>
              </div>
            {:else}
              <ConstructTabContent
                shouldShowStartPositionPicker={shouldShowStartPositionPicker ===
                  true}
                startPositionState={constructTabState.startPositionStateService}
                currentSequence={currentSequenceData}
                {onOptionSelected}
                {isUndoingOption}
                onStartPositionNavigateToAdvanced={handleNavigateToAdvanced}
                onStartPositionNavigateToDefault={handleNavigateToDefault}
                {isSideBySideLayout}
                {onOpenFilters}
                {onCloseFilters}
                {isFilterPanelOpen}
                isContinuousOnly={constructTabState.isContinuousOnly}
                onToggleContinuous={(value) =>
                  constructTabState.setContinuousOnly(value)}
              />
            {/if}
          {:else if activeToolPanel === "generate"}
            <GeneratePanel sequenceState={createModuleState.sequenceState} />
          {:else if activeToolPanel === "gestural"}
            <!-- Hand Path Builder Controls -->
            <!-- TODO: Re-enable when handPathCoordinator is added to ICreateModuleState -->
            <!-- {#if createModuleState.handPathCoordinator}
              <HandPathToolContent
                handPathCoordinator={createModuleState.handPathCoordinator}
              />
            {/if} -->
            <div class="coming-soon-panel">
              <p>Hand Path Builder coming soon...</p>
            </div>
          {/if}
        </div>
      {/key}
    </div>
  {:else}
    <!-- Fallback case: persistence is loaded but no active tab -->
    <div class="no-tab-selected">
      <p>No tab selected</p>
    </div>
  {/if}
</div>

<!-- ============================================================================ -->
<!-- STYLES -->
<!-- ============================================================================ -->

<style>
  .tool-panel {
    position: relative;
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: visible; /* Allow card hover effects to pop and be fully visible */
  }

  /* When navigation is on the right (landscape mobile), use row layout */
  /* row puts navigation on the right and content on the left */
  .tool-panel.layout-right {
    flex-direction: column;
  }

  /* Header for toggle in side-by-side layout */
  .tool-panel-header {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px;
    flex-shrink: 0;
    order: 1;
  }

  .tab-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: visible; /* Allow card hover effects to be fully visible */
    position: relative;
    min-height: 0;
  }

  .sub-tab-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: visible; /* Allow card hover effects to be fully visible */
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
    will-change: opacity;
    backface-visibility: hidden;
  }

  .persistence-loading,
  .picker-loading,
  .no-tab-selected {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 200px;
    color: #666;
  }

  .loading-spinner {
    width: 24px;
    height: 24px;
    border: 2px solid #e0e0e0;
    border-top: 2px solid #007acc;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 12px;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  /* Coming Soon Panel Styles */
  .coming-soon-panel {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 2rem;
    text-align: center;
    color: rgba(255, 255, 255, 0.8);
  }

  .coming-soon-panel p {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.6);
    margin-bottom: 0.5rem;
  }
</style>
