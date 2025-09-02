<script lang="ts">
  import { resolve, TYPES } from "$lib/services/inversify/container";
  import { createBeatFrameState } from "$state";
  import { createSequenceState } from "$state";
  import { createWorkbenchState } from "$state";
  import { onMount } from "svelte";
  import ButtonPanel from "./ButtonPanel.svelte";
  import SequenceContent from "./SequenceContent.svelte";

  // Get services from DI container
  const sequenceStateService = resolve<
    import("$contracts").ISequenceStateService
  >(TYPES.ISequenceStateService);
  const beatFrameService = resolve<import("$contracts").IBeatFrameService>(
    TYPES.IBeatFrameService
  );
  const workbenchService = resolve<import("$contracts").IWorkbenchService>(
    TYPES.IWorkbenchService
  );
  const workbenchCoordinationService = resolve<
    import("$contracts").IWorkbenchCoordinationService
  >(TYPES.IWorkbenchCoordinationService);

  // Create component-scoped states
  const sequenceState = createSequenceState(sequenceStateService);
  const beatFrameState = createBeatFrameState(beatFrameService);
  const workbenchState = createWorkbenchState(
    workbenchService,
    workbenchCoordinationService,
    sequenceState,
    beatFrameState
  );

  const hasSelection = $derived(sequenceState.selectedBeatIndex >= 0);

  onMount(() => {
    workbenchState.initialize();

    // Container element is available for future use if needed
  });

  function handleDeleteBeat() {
    const idx = sequenceState.selectedBeatIndex;
    if (idx >= 0) {
      // TODO: Replace with WorkbenchBeatOperationsService.removeBeat
      // For now, use the state service directly
      sequenceState.removeBeat(idx);
    }
  }

  function handleClearSequence() {
    sequenceState.clearSequence();
  }

  function handleBeatSelected(index: number) {
    workbenchState.handleBeatClick(index);
  }

  // Advanced button actions (to be wired to services later)
  function handleAddToDictionary() {
    console.log("Add to Dictionary - to be implemented");
  }

  function handleFullscreen() {
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
    const seq = sequenceState.currentSequence;
    if (seq) {
      navigator.clipboard.writeText(JSON.stringify(seq, null, 2));
      console.log("Copied sequence JSON to clipboard");
    }
  }
</script>

<div class="workbench">
  <div class="main-layout">
    <div class="left-vbox">
      <SequenceContent {sequenceState} onBeatSelected={handleBeatSelected} />
    </div>
    <div class="workbench-button-panel">
      <ButtonPanel
        {hasSelection}
        onDeleteBeat={handleDeleteBeat}
        onClearSequence={handleClearSequence}
        onAddToDictionary={handleAddToDictionary}
        onFullscreen={handleFullscreen}
        onMirror={handleMirror}
        onSwapColors={handleSwapColors}
        onRotate={handleRotate}
        onCopyJson={handleCopyJson}
      />
    </div>
  </div>
</div>

<style>
  .workbench {
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
