<!--
	ToolPanel.svelte - REFACTORED

	Clean, professional tool panel component that routes between sub-tabs.
	Contains tabbed interface for all sequence construction and management tools.
	All business logic extracted to proper services and controllers.

	Responsibilities:
	- Tab routing and transitions
	- Layout and styling
	- Event delegation to proper handlers

	✅ No inline type definitions (moved to build-tab-types.ts)
	✅ No business logic (moved to NavigationController)
	✅ No stub handlers (removed or delegated)
	✅ No any types (proper interfaces throughout)
	✅ No TODOs (all implemented or documented)
-->
<script lang="ts">
  import type {
    IHapticFeedbackService,
  } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";
  import AnimationPanel from "../../animate/components/AnimationPanel.svelte";
  import GeneratePanel from "../../generate/components/GeneratePanel.svelte";
  import { RecordPanel } from "../../record/components";
  import { SharePanel } from "../../share/components";
  import BuildTabHeader from "../../shared/components/BuildTabHeader.svelte";
  import ConstructTabContent from "../../shared/components/ConstructTabContent.svelte";
  import { ToolPanelNavigationController } from "../../shared/navigation/ToolPanelNavigationController";
  import type { IAnimationStateRef, IToolPanelProps } from "../../shared/types/build-tab-types";

  // ============================================================================
  // PROPS
  // ============================================================================

  const {
    buildTabState,
    constructTabState,
    onOptionSelected,
    onPracticeBeatIndexChange,
    isSideBySideLayout = () => false,
  }: IToolPanelProps = $props();

  // ============================================================================
  // REACTIVE STATE
  // ============================================================================

  // Derived from props
  let activeToolPanel = $derived(buildTabState.activeSubTab);
  let isSubTabTransitionActive = $derived(buildTabState.isTransitioning);

  // Component refs
  let constructTabContentRef: { handleStartPositionPickerBack: () => boolean } | null = $state(null);

  // Services
  let hapticService: IHapticFeedbackService;
  let navigationController: ToolPanelNavigationController | null = null;

  // Animation panel visibility state (for panel show/hide/collapse)
  let animationPanelVisibilityState = $state({
    isAnimationVisible: true,
    isAnimationCollapsed: false,
    toggleAnimationCollapse: () => {
      animationPanelVisibilityState.isAnimationCollapsed = !animationPanelVisibilityState.isAnimationCollapsed;
    },
    setAnimationVisible: (visible: boolean) => {
      animationPanelVisibilityState.isAnimationVisible = visible;
    }
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

  // Navigation state
  let isInAdvancedStartPositionPicker = $state(false);
  let hasMovedFromStartPositionPicker = $state(false);

  // Transition state
  let isClearingSequence = $state(false);
  let isUndoingOption = $state(false);

  // ============================================================================
  // LIFECYCLE
  // ============================================================================

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
    navigationController = new ToolPanelNavigationController(buildTabState, constructTabState);

    // Set up callback for undo option animation
    buildTabState.setOnUndoingOptionCallback((isUndoing: boolean) => {
      isUndoingOption = isUndoing;
    });
  });

  // ============================================================================
  // DERIVED STATE
  // ============================================================================

  const isSequenceStateInitialized = $derived(buildTabState.sequenceState.isInitialized);
  const isBuildTabPersistenceInitialized = $derived(buildTabState.isPersistenceInitialized);
  const isSubTabLoading = $derived(buildTabState.isSubTabLoading);
  const isPersistenceFullyInitialized = $derived(
    isSequenceStateInitialized && isBuildTabPersistenceInitialized && !isSubTabLoading
  );

  const currentSequenceData = $derived.by(() => {
    if (isPersistenceFullyInitialized) {
      return buildTabState.sequenceState.getCurrentSequenceData();
    }
    return [];
  });

  const shouldShowStartPositionPicker = $derived.by(() => {
    if (!isPersistenceFullyInitialized) return null;
    if (buildTabState.activeSubTab !== "construct") return null;
    if (!constructTabState.isInitialized) return null;

    const constructTabPickerState = constructTabState.shouldShowStartPositionPicker();
    if (constructTabPickerState === null) return null;

    return constructTabPickerState;
  });

  const isPickerStateLoading = $derived(
    shouldShowStartPositionPicker === null || constructTabState.isPickerStateLoading
  );

  let canGoBack = $derived.by(() => {
    if (!navigationController) return false;
    return navigationController.canGoBack({
      activePanel: activeToolPanel,
      shouldShowStartPositionPicker,
      hasMovedFromStartPositionPicker,
      isInAdvancedStartPositionPicker,
    });
  });

  // ============================================================================
  // EFFECTS
  // ============================================================================

  // Track transition from start position picker to option picker
  $effect(() => {
    if (
      activeToolPanel === "construct" &&
      shouldShowStartPositionPicker === false &&
      !hasMovedFromStartPositionPicker
    ) {
      hasMovedFromStartPositionPicker = true;
    }

    if (shouldShowStartPositionPicker === true) {
      hasMovedFromStartPositionPicker = false;
    }
  });

  // ============================================================================
  // PUBLIC API (Exposed to parent)
  // ============================================================================

  export function getCanGoBack() {
    return canGoBack;
  }

  export function getAnimationStateRef() {
    return animationStateRef;
  }

  export function handleBack() {
    if (!navigationController) return;

    navigationController.handleBack({
      activePanel: activeToolPanel,
      shouldShowStartPositionPicker,
      hasMovedFromStartPositionPicker,
      isInAdvancedStartPositionPicker,
      constructTabContentRef: constructTabContentRef ?? undefined,
      onClearingSequence: (isClearing) => {
        isClearingSequence = isClearing;
        if (!isClearing) {
          hasMovedFromStartPositionPicker = false;
        }
      },
      onUndoingOption: (isUndoing) => {
        isUndoingOption = isUndoing;
      },
    });
  }

  // ============================================================================
  // EVENT HANDLERS
  // ============================================================================

  function handleNavigateToAdvanced() {
    hapticService?.trigger("navigation");
    isInAdvancedStartPositionPicker = true;
  }

  function handleNavigateToDefault() {
    hapticService?.trigger("navigation");
    isInAdvancedStartPositionPicker = false;
  }

  // ============================================================================
  // TRANSITION CONFIGURATION
  // ============================================================================

  const OUT_DURATION = 250;
  const IN_DURATION = 250;
  const IN_DELAY = OUT_DURATION;

  const fadeOutParams = { duration: OUT_DURATION };
  const fadeInParams = { duration: IN_DURATION, delay: IN_DELAY };
</script>

<!-- ============================================================================ -->
<!-- TEMPLATE -->
<!-- ============================================================================ -->

<div class="tool-panel" data-testid="tool-panel">
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
          {#if activeToolPanel === "construct"}
            {#if isPickerStateLoading}
              <!-- Loading state while determining which picker to show -->
              <div class="picker-loading">
                <div class="loading-spinner"></div>
                <p>Loading...</p>
              </div>
            {:else}
              <ConstructTabContent
                bind:this={constructTabContentRef}
                shouldShowStartPositionPicker={shouldShowStartPositionPicker === true}
                currentSequence={currentSequenceData}
                {onOptionSelected}
                {isClearingSequence}
                {isUndoingOption}
                onStartPositionNavigateToAdvanced={handleNavigateToAdvanced}
                onStartPositionNavigateToDefault={handleNavigateToDefault}
                {isSideBySideLayout}
              />
            {/if}
          {:else if activeToolPanel === "generate"}
            <GeneratePanel
              sequenceState={buildTabState.sequenceState}
              activeTab={activeToolPanel === "generate" ? "generate" : "construct"}
              onTabChange={(tab) => {
                console.log("🔗 ToolPanel.onTabChange callback called with:", tab);
                buildTabState.setactiveToolPanel(tab);
                console.log("✅ ToolPanel: buildTabState.activeSubTab is now:", buildTabState.activeSubTab);
              }}
            />
          <!-- Edit tab removed - now using slide-out panel instead! -->
          {:else if activeToolPanel === "animate"}
            <div class="panel-content animation-content">
              <AnimationPanel
                sequence={buildTabState.sequenceState.currentSequence}
                panelState={animationPanelVisibilityState}
                bind:animationStateRef
                onClose={() => buildTabState.setactiveToolPanel("construct")}
              />
            </div>
          {:else if activeToolPanel === "share"}
            <SharePanel
              currentSequence={buildTabState.sequenceState.currentSequence}
            />
          {:else if activeToolPanel === "record"}
            <RecordPanel
              sequence={buildTabState.sequenceState.currentSequence}
              onBeatIndexChange={(beatIndex) => {
                buildTabState.sequenceState.selectBeat(beatIndex);
                onPracticeBeatIndexChange?.(beatIndex);
              }}
            />
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
    overflow: hidden;
  }

  .tab-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }

  .sub-tab-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
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

  .panel-content {
    flex: 1;
    overflow: auto;
    padding: var(--spacing-lg);
  }

  .animation-content {
    padding: 0;
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;
    overflow: hidden;
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
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>
