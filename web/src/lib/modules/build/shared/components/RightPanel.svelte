<!--
	RightPanel.svelte

	Right panel component extracted from ConstructTab.
	Contains the 4-tab interface with navigation and content areas.
-->
<script lang="ts">
  import GraphEditor from "../../edit/components/GraphEditor.svelte";
  import ExportPanel from "../../export/components/ExportPanel.svelte";

  import GeneratePanel from "../../generate/components/GeneratePanel.svelte";
// import { constructTabEventService } from "../../services/implementations"; // TODO: Implement service
// Import Svelte's built-in fade transition for consistency with main tabs
  import type {
    ActiveBuildTab,
    ArrowPlacementData,
    BeatData,
    PictographData,
  } from "$shared";
  import { fade } from "svelte/transition";
  import ConstructTabContent from "./ConstructTabContent.svelte";

  // Props from parent BuildTab
  const { buildTabState, constructTabState, onOptionSelected }: {
    // Master tab state (shared across all sub-tabs)
    buildTabState: {
      readonly isLoading: boolean;
      readonly error: string | null;
      readonly isTransitioning: boolean;
      readonly hasError: boolean;
      readonly hasSequence: boolean;
      readonly activeSubTab: ActiveBuildTab | null;
      readonly isPersistenceInitialized: boolean;
      readonly isSubTabLoading: boolean;
      readonly sequenceState: any; // TODO: Fix typing
      setLoading: (loading: boolean) => void;
      setTransitioning: (transitioning: boolean) => void;
      setError: (errorMessage: string | null) => void;
      clearError: () => void;
      setActiveRightPanel: (panel: ActiveBuildTab) => void;
    };
    // Construct sub-tab state (construct-specific)
    constructTabState: {
      readonly isLoading: boolean;
      readonly error: string | null;
      readonly isTransitioning: boolean;
      readonly hasError: boolean;
      readonly canSelectOptions: boolean;
      readonly showStartPositionPicker: boolean | null;
      readonly shouldShowStartPositionPicker: () => boolean | null;
      readonly isPickerStateLoading: boolean;
      readonly isInitialized: boolean;
      readonly selectedStartPosition: any; // TODO: Fix typing
      readonly startPositionStateService: any; // TODO: Fix typing
      setLoading: (loading: boolean) => void;
      setTransitioning: (transitioning: boolean) => void;
      setError: (errorMessage: string | null) => void;
      clearError: () => void;
      setShowStartPositionPicker: (show: boolean) => void;
      setSelectedStartPosition: (position: any) => void;
    };
    // Action handlers (start position selection handled by unified service)
    onOptionSelected: (option: PictographData) => Promise<void>;
  } = $props();

  // Reactive state from props
  let activeRightPanel = $derived(buildTabState.activeSubTab);
  let isSubTabTransitionActive = $derived(buildTabState.isTransitioning);

  // Reactive sequence data - CRITICAL: Must be derived for reactivity in Svelte 5
  // Wait for both sequence state and build tab persistence to be initialized before getting data
  const isSequenceStateInitialized = $derived(buildTabState.sequenceState.isInitialized);
  const isBuildTabPersistenceInitialized = $derived(buildTabState.isPersistenceInitialized);
  const isSubTabLoading = $derived(buildTabState.isSubTabLoading);
  const isPersistenceFullyInitialized = $derived(isSequenceStateInitialized && isBuildTabPersistenceInitialized && !isSubTabLoading);

  const currentSequenceData = $derived.by(() => {
    if (isPersistenceFullyInitialized) {
      return buildTabState.sequenceState.getCurrentSequenceData();
    }
    return [];
  });
  const shouldShowStartPositionPicker = $derived.by(() => {
    if (!isPersistenceFullyInitialized) return null; // Don't show anything until persistence is loaded
    if (buildTabState.activeSubTab !== "construct") return null; // Only show in construct tab

    // CRITICAL: Wait for construct tab state to be fully initialized
    // This prevents the flicker where we briefly show the wrong picker during persistence restoration
    if (!constructTabState.isInitialized) return null; // Still initializing construct tab state

    const constructTabPickerState = constructTabState.shouldShowStartPositionPicker();
    if (constructTabPickerState === null) return null; // Still loading construct tab state

    return constructTabPickerState;
  });
  const isPickerStateLoading = $derived(shouldShowStartPositionPicker === null || constructTabState.isPickerStateLoading);


  // Sequential fade timing - same as main tabs for consistency
  const OUT_DURATION = 250;
  const IN_DURATION = 250;
  const IN_DELAY = OUT_DURATION; // Wait for out transition to complete

  // Transition parameters - no need for $derived since these are constant
  const fadeOutParams = { duration: OUT_DURATION };
  const fadeInParams = { duration: IN_DURATION, delay: IN_DELAY };

  // Event handlers for child components
  function handleBeatModified(beatIndex: number, beatData: BeatData) {
    // constructTabEventService().handleBeatModified(beatIndex, beatData); // TODO: Implement service
    console.log("Beat modified:", beatIndex, beatData);
  }

  function handleArrowSelected(arrowData: {
    color: string;
    orientation?: string;
    turn_amount?: number;
    type: string;
  }) {
    // ✅ FIXED: ArrowPlacementData now only contains placement properties
    const fullArrowData: ArrowPlacementData = {
      positionX: 0,
      positionY: 0,
      rotationAngle: 0,
      coordinates: null,
      svgCenter: null,
      svgMirrored: false,
    };
    // constructTabEventService().handleArrowSelected(fullArrowData); // TODO: Implement service
    console.log("Arrow selected:", fullArrowData);
  }

  function handleExportSettingChanged(data: { setting: string; value: any }) {
    const event = new CustomEvent("settingChanged", { detail: data });
    // constructTabEventService().handleExportSettingChanged(event); // TODO: Implement service
    console.log("Export setting changed:", event);
  }

  function handlePreviewUpdateRequested(settings: any) {
    const event = new CustomEvent("previewUpdateRequested", {
      detail: settings,
    });
    // constructTabEventService().handlePreviewUpdateRequested(event); // TODO: Implement service
    console.log("Preview update requested:", event);
  }

  function handleExportRequested(data: { type: string; config: any }) {
    const event = new CustomEvent("exportRequested", { detail: data });
    // constructTabEventService().handleExportRequested(event); // TODO: Implement service
    console.log("Export requested:", event);
  }
</script>

<div class="right-panel" data-testid="right-panel">
  {#if !isPersistenceFullyInitialized}
    <!-- Loading state while persistence is being restored -->
    <div class="persistence-loading">
      <div class="loading-spinner"></div>
      <p>Loading...</p>
    </div>
  {:else if activeRightPanel}
    <!-- Tab Content with Sequential Fade Transitions -->
    <div class="tab-content">
      {#key activeRightPanel}
        <div
          class="sub-tab-content"
          in:fade={fadeInParams}
          out:fade={fadeOutParams}
        >
          {#if activeRightPanel === "construct"}
            {#if isPickerStateLoading}
              <!-- Loading state while determining which picker to show -->
              <div class="picker-loading">
                <div class="loading-spinner"></div>
                <p>Loading...</p>
              </div>
            {:else}
              <ConstructTabContent
                shouldShowStartPositionPicker={shouldShowStartPositionPicker === true}
                currentSequence={currentSequenceData}
                {onOptionSelected}
              />
            {/if}
          {:else if activeRightPanel === "generate"}
            <GeneratePanel />
          {:else if activeRightPanel === "edit"}
            <div class="panel-content graph-editor-content">
              <GraphEditor
                currentSequence={buildTabState.sequenceState.currentSequence}
                selectedBeatIndex={buildTabState.sequenceState.selectedBeatIndex}
                selectedBeatData={buildTabState.sequenceState.selectedBeatData}
                onBeatModified={handleBeatModified}
                onArrowSelected={handleArrowSelected}
              />
            </div>
          {:else if activeRightPanel === "export"}
            <ExportPanel
              currentSequence={buildTabState.sequenceState.currentSequence}
              onsettingchanged={handleExportSettingChanged}
              onpreviewupdaterequested={handlePreviewUpdateRequested}
              onexportrequested={handleExportRequested}
            />
          {/if}
        </div>
      {/key}

      <!-- Debug sub-tab transition state -->
      {#if isSubTabTransitionActive}
        <div class="sub-tab-transition-debug">🎨 Sub-tab transitioning...</div>
      {/if}
    </div>
  {:else}
    <!-- Fallback case: persistence is loaded but no active tab -->
    <div class="no-tab-selected">
      <p>No tab selected</p>
    </div>
  {/if}
</div>

<style>
  .right-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    /* Transparent background to show beautiful background without blur */
    background: rgba(255, 255, 255, 0.05);
    /* backdrop-filter: blur(20px); - REMOVED to show background */
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
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
    /* Ensure smooth transitions without layout jumps */
    will-change: opacity;
    backface-visibility: hidden;
  }

  .panel-content {
    flex: 1;
    overflow: auto;
    padding: var(--spacing-lg);
  }

  .graph-editor-content {
    padding: 0;
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;
  }

  .sub-tab-transition-debug {
    position: absolute;
    top: 60px;
    right: 20px;
    background: rgba(138, 43, 226, 0.9);
    color: white;
    padding: 6px 12px;
    border-radius: 15px;
    font-size: 12px;
    font-weight: 600;
    z-index: 999;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    pointer-events: none;
  }

  .persistence-loading,
  .picker-loading {
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
