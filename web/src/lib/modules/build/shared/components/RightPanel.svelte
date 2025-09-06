<!--
	RightPanel.svelte

	Right panel component extracted from ConstructTab.
	Contains the 4-tab interface with navigation and content areas.
-->
<script lang="ts">
  import GraphEditor from "../../edit/components/GraphEditor.svelte";
  import ExportPanel from "../../export/components/ExportPanel.svelte";

  import ConstructTabContent from "../../construct/shared/components/ConstructTabContent.svelte";
  import GeneratePanel from "../../generate/components/GeneratePanel.svelte";
// import { constructTabEventService } from "../../services/implementations"; // TODO: Implement service
  import ConstructTabNavigation from "./BuildTabNavigation.svelte";
// Import Svelte's built-in fade transition for consistency with main tabs
  import type {
    ActiveBuildTab,
    ArrowPlacementData,
    BeatData,
    PictographData,
  } from "$shared/domain";
  import { getAnimationSettings } from "$shared/utils";
  import { fade } from "svelte/transition";

  // Props from parent BuildTab
  interface Props {
    // Master tab state (shared across all sub-tabs)
    buildTabState: {
      readonly isLoading: boolean;
      readonly error: string | null;
      readonly isTransitioning: boolean;
      readonly hasError: boolean;
      readonly hasSequence: boolean;
      readonly activeSubTab: ActiveBuildTab;
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
      readonly showStartPositionPicker: boolean;
      readonly shouldShowStartPositionPicker: () => boolean;
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
  }

  const { buildTabState, constructTabState, onOptionSelected }: Props =
    $props();

  // Reactive state from props
  let activeRightPanel = $derived(buildTabState.activeSubTab);
  let isSubTabTransitionActive = $derived(buildTabState.isTransitioning);

  let animationSettings = $derived(getAnimationSettings());

  // Sequential fade timing - same as main tabs for consistency
  const OUT_DURATION = 250;
  const IN_DURATION = 250;
  const IN_DELAY = OUT_DURATION; // Wait for out transition to complete

  // Transition parameters using runes
  let fadeOutParams = $derived(
    animationSettings.animationsEnabled
      ? { duration: OUT_DURATION }
      : { duration: 0 }
  );
  let fadeInParams = $derived(
    animationSettings.animationsEnabled
      ? { duration: IN_DURATION, delay: IN_DELAY }
      : { duration: 0 }
  );

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
  <!-- Tab Navigation -->
  <ConstructTabNavigation
    activeBuildSubTab={activeRightPanel}
    setActiveBuildSubTab={buildTabState.setActiveRightPanel}
  />

  <!-- Tab Content with Sequential Fade Transitions -->
  <div class="tab-content">
    {#key activeRightPanel}
      <div
        class="sub-tab-content"
        in:fade={fadeInParams}
        out:fade={fadeOutParams}
      >
        {#if activeRightPanel === "construct"}
          <ConstructTabContent
            shouldShowStartPositionPicker={constructTabState.shouldShowStartPositionPicker()}
            {onOptionSelected}
          />
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
</style>
