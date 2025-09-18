<script lang="ts">
  import { type SequenceState } from "../../../shared/state/sequence-state.svelte";
  import SequenceDisplay from "../../sequence-display/components/SequenceDisplay.svelte";
  import { SequenceToolbar } from "../../sequence-toolkit/components";

  // Props
  let {
    sequenceState: externalSequenceState,
    onClearSequence
  } = $props<{
    sequenceState?: SequenceState;
    onClearSequence?: () => Promise<void>;
  }>();

  // Use external sequence state directly
  const sequenceState = externalSequenceState;

  // Reactive values that depend on sequence state
  const hasSequence = $derived(
    (sequenceState?.hasStartPosition ?? false) ||
    (sequenceState?.currentSequence?.beats.length ?? 0) > 0
  );

  function handleDeleteBeat() {
    if (!sequenceState) return;
    const idx = sequenceState.selectedBeatIndex;
    if (idx !== null && idx >= 0) {
      // TODO: Replace with WorkbenchBeatOperationsService.removeBeat
      // For now, use the state service directly
      sequenceState.removeBeat(idx);
    }
  }

  async function handleClearSequence() {
    if (onClearSequence) {
      await onClearSequence();
    } else if (sequenceState) {
      // Fallback to sequence state clear
      sequenceState.clearSequence();
    }
  }

  function handleBeatSelected(index: number) {
    if (!sequenceState) return;
    // TODO: Implement beat selection logic
    console.log("🎵 Beat selected:", index);
  }

  // Advanced button actions (to be wired to services later)
  function handleAddToDictionary() {
    console.log("Add to Gallery - to be implemented");
  }

  function handleSpotlight() {
    console.log("Fullscreen - to be implemented");
  }

  function handleMirror() {
    console.log("Mirror sequence - to be implemented");
  }

  function handleSwapColors() {
    console.log("Swap colors - to be implemented");
  }

  function handleRotate() {
    console.log("Rotate sequence - to be implemented");
  }

  function handleCopyJson() {
    if (!sequenceState) return;
    const seq = sequenceState.currentSequence;
    if (seq) {
      navigator.clipboard.writeText(JSON.stringify(seq, null, 2));
      console.log("Copied sequence JSON to clipboard");
    }
  }
</script>

{#if sequenceState}
<div class="build-workbench">
  <div class="main-layout">
    <div class="left-vbox">
      <SequenceDisplay {sequenceState} onBeatSelected={handleBeatSelected} />
    </div>
    <div class="workbench-button-panel">
      <SequenceToolbar
        hasSelection={false}
        {hasSequence}
        onDeleteBeat={handleDeleteBeat}
        onClearSequence={handleClearSequence}
        onAddToDictionary={handleAddToDictionary}
        onFullscreen={handleSpotlight}
        onMirror={handleMirror}
        onSwapColors={handleSwapColors}
        onRotate={handleRotate}
        onCopyJson={handleCopyJson}
      />
    </div>
  </div>
</div>
{:else}
<div class="build-workbench loading">
  <div class="loading-message">Initializing workbench...</div>
</div>
{/if}

<style>
  .build-workbench {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    /* Transparent background to show beautiful app background */
    background: transparent;
  }

  .main-layout {
    display: grid;
    grid-template-columns: 1fr auto; /* left fills, right button panel auto width */
    gap: var(--spacing-xs); /* Add small gap between content and button panel */
    width: 100%;
    height: 100%;
  }

  .left-vbox {
    min-width: 0;
    display: flex;
    flex-direction: column;
    height: 100%;
    flex: 1;
  }

  .workbench-button-panel {
    display: flex;
  }
</style>
