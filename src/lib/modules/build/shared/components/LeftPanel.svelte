<!--
	LeftPanel.svelte

	Left panel component extracted from ConstructTab.
	Contains the workbench with horizontal button panel at the bottom.
-->
<script lang="ts">
  import { BuildWorkbench } from "../../workbench/shared/components";
  import ButtonPanel from "../../workbench/shared/components/ButtonPanel.svelte";

  // Props
  let {
    sequenceState,
    onClearSequence,
    buildTabState,
    practiceBeatIndex = null,

    // Button panel props
    canGoBack = false,
    onBack,
    canRemoveBeat = false,
    onRemoveBeat,
    selectedBeatIndex = null,
    selectedBeatData = null,
    canEditBeat = false,
    onEditBeat,
    canClearSequence = false,
    canSaveSequence = false,
    onSaveSequence,
    showFullScreen = true,

    // Animation state ref (for animate tab)
    animationStateRef = null,

    // Layout mode
    isSideBySideLayout = false
  }: {
    sequenceState?: any; // TODO: Type this properly
    onClearSequence?: () => Promise<void>;
    buildTabState?: any; // TODO: Type this properly
    practiceBeatIndex?: number | null;

    // Button panel props
    canGoBack?: boolean;
    onBack?: () => void;
    canRemoveBeat?: boolean;
    onRemoveBeat?: (beatIndex: number) => void;
    selectedBeatIndex?: number | null;
    selectedBeatData?: any;
    canEditBeat?: boolean;
    onEditBeat?: () => void;
    canClearSequence?: boolean;
    canSaveSequence?: boolean;
    onSaveSequence?: () => void;
    showFullScreen?: boolean;

    // Animation state ref
    animationStateRef?: any | null;

    // Layout mode
    isSideBySideLayout?: boolean;
  } = $props();

  // Derived state for current tab
  const isAnimateTab = $derived(buildTabState?.activeSubTab === "animate");
</script>

<div class="left-panel" data-testid="left-panel">
  <div class="workbench-container">
    <BuildWorkbench {sequenceState} {onClearSequence} {buildTabState} {practiceBeatIndex} {animationStateRef} {isSideBySideLayout} />
  </div>

  <!-- Button Panel at bottom (context-aware) -->
  <div class="button-panel-container">
    {#if isAnimateTab}
      <!-- Animate tab: Show Undo, Remove Beat, Edit Beat, Clear Sequence, and Fullscreen buttons -->
      <ButtonPanel
        {buildTabState}
        {canRemoveBeat}
        {onRemoveBeat}
        {selectedBeatIndex}
        {selectedBeatData}
        {canEditBeat}
        {onEditBeat}
        canClearSequence={canClearSequence}
        onClearSequence={onClearSequence}
        sequenceData={sequenceState?.currentSequence}
        showFullScreen={showFullScreen}
      />
    {:else}
      <!-- Default build controls -->
      <ButtonPanel
        {buildTabState}
        {canGoBack}
        {onBack}
        {canRemoveBeat}
        {onRemoveBeat}
        {selectedBeatIndex}
        {selectedBeatData}
        {canEditBeat}
        {onEditBeat}
        {canClearSequence}
        onClearSequence={onClearSequence}
        {canSaveSequence}
        {onSaveSequence}
        sequenceData={sequenceState?.currentSequence}
        {showFullScreen}
      />
    {/if}
  </div>

</div>

<style>
  .left-panel {
    position: relative;
    flex: 1;
    display: flex;
    flex-direction: column; /* Always stack workbench above buttons */
    /* Transparent background to show beautiful background without blur */
    background: transparent;
    border: none;
    border-radius: var(--border-radius);
    overflow: hidden;
    border-radius: 12px;
  }

  .workbench-container {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .button-panel-container {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px 0;
    width: 100%;
    flex-shrink: 0; /* Prevent buttons from shrinking */
  }
</style>
