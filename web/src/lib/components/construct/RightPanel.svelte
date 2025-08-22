<!--
	RightPanel.svelte

	Right panel component extracted from ConstructTab.
	Contains the 4-tab interface with navigation and content areas.
-->
<script lang="ts">
  import ExportPanel from "$components/export/ExportPanel.svelte";
  import GraphEditor from "$components/graph-editor/GraphEditor.svelte";
  import type { SequenceData } from "$lib/domain";
  import type { ArrowPlacementData } from "$lib/domain/ArrowPlacementData";
  import type { ActiveRightPanel } from "$lib/state/construct-tab-state.svelte";
  import { constructTabEventService } from "$services/implementations/construct/ConstructTabEventService";
  import BuildTabContent from "./BuildTabContent.svelte";
  import ConstructTabNavigation from "./ConstructTabNavigation.svelte";
  import GeneratePanel from "./generate/GeneratePanel.svelte";
  // Import Svelte's built-in fade transition for consistency with main tabs
  import type { BeatData } from "$lib/domain";
  import { getAnimationSettings } from "$lib/utils/animation-control";
  import { shouldAnimate } from "$lib/utils/simple-fade";
  import { fade } from "svelte/transition";

  // Props from parent ConstructTab
  interface Props {
    constructTabState: {
      activeRightPanel: ActiveRightPanel;
      isSubTabTransitionActive: boolean;
      setActiveRightPanel: (tab: ActiveRightPanel) => void;
      // Sequence state for GraphEditor
      currentSequence: SequenceData | null;
      selectedBeatIndex: number | null;
      selectedBeatData: BeatData | null;
    };
  }

  const { constructTabState }: Props = $props();

  // Reactive state from props
  let activeRightPanel = $derived(constructTabState.activeRightPanel);
  let isSubTabTransitionActive = $derived(
    constructTabState.isSubTabTransitionActive
  );
  let animationSettings = $derived(getAnimationSettings());

  // Sequential fade timing - same as main tabs for consistency
  const OUT_DURATION = 250;
  const IN_DURATION = 250;
  const IN_DELAY = OUT_DURATION; // Wait for out transition to complete

  // Transition parameters using runes
  let fadeOutParams = $derived(
    shouldAnimate(animationSettings)
      ? { duration: OUT_DURATION }
      : { duration: 0 }
  );
  let fadeInParams = $derived(
    shouldAnimate(animationSettings)
      ? { duration: IN_DURATION, delay: IN_DELAY }
      : { duration: 0 }
  );

  // Event handlers for child components
  function handleBeatModified(beatIndex: number, beatData: BeatData) {
    constructTabEventService().handleBeatModified(beatIndex, beatData);
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
    constructTabEventService().handleArrowSelected(fullArrowData);
  }

  function handleGraphEditorVisibilityChanged(isVisible: boolean) {
    // Handle graph editor visibility changes if needed
    console.log("Graph editor visibility changed:", isVisible);
  }

  function handleExportSettingChanged(data: { setting: string; value: any }) {
    const event = new CustomEvent("settingChanged", { detail: data });
    constructTabEventService().handleExportSettingChanged(event);
  }

  function handlePreviewUpdateRequested(settings: any) {
    const event = new CustomEvent("previewUpdateRequested", {
      detail: settings,
    });
    constructTabEventService().handlePreviewUpdateRequested(event);
  }

  function handleExportRequested(data: { type: string; config: any }) {
    const event = new CustomEvent("exportRequested", { detail: data });
    constructTabEventService().handleExportRequested(event);
  }
</script>

<div class="right-panel" data-testid="right-panel">
  <!-- Tab Navigation -->
  <ConstructTabNavigation
    {activeRightPanel}
    setActiveRightPanel={constructTabState.setActiveRightPanel}
  />

  <!-- Tab Content with Sequential Fade Transitions -->
  <div class="tab-content">
    {#key activeRightPanel}
      <div
        class="sub-tab-content"
        in:fade={fadeInParams}
        out:fade={fadeOutParams}
      >
        {#if activeRightPanel === "build"}
          <BuildTabContent />
        {:else if activeRightPanel === "generate"}
          <GeneratePanel />
        {:else if activeRightPanel === "edit"}
          <div class="panel-header">
            <h2>Graph Editor</h2>
            <p>Advanced sequence editing tools</p>
          </div>
          <div class="panel-content graph-editor-content">
            <GraphEditor
              currentSequence={constructTabState.currentSequence}
              selectedBeatIndex={constructTabState.selectedBeatIndex}
              selectedBeatData={constructTabState.selectedBeatData}
              onBeatModified={handleBeatModified}
              onArrowSelected={handleArrowSelected}
              onVisibilityChanged={handleGraphEditorVisibilityChanged}
            />
          </div>
        {:else if activeRightPanel === "export"}
          <ExportPanel
            currentSequence={constructTabState.currentSequence}
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

  .panel-header {
    flex-shrink: 0;
    padding: var(--spacing-lg);
    background: var(--muted) / 30;
    border-bottom: 1px solid var(--border);
    text-align: center;
  }

  .panel-header h2 {
    margin: 0 0 var(--spacing-sm) 0;
    color: var(--foreground);
    font-size: var(--font-size-xl);
    font-weight: 500;
  }

  .panel-header p {
    margin: 0;
    color: var(--muted-foreground);
    font-size: var(--font-size-sm);
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

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .panel-header {
      padding: var(--spacing-md);
    }
  }
</style>
