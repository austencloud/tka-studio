<script lang="ts">
  /**
   * Sequence Actions Coordinator Component
   *
   * Manages sequence transformation actions (mirror, rotate, color swap, copy JSON).
   * Extracts sequence actions logic from BuildTab.svelte for better separation of concerns.
   *
   * Domain: Build Module - Sequence Transformation Coordination
   */

  import { createComponentLogger } from "$shared";
  import SequenceActionsSheet from "../../../workspace-panel/shared/components/SequenceActionsSheet.svelte";
  import type { PanelCoordinationState } from "../../state/panel-coordination-state.svelte";
  import type { createBuildTabState as BuildTabStateType } from "../../state/build-tab-state.svelte";

  type BuildTabState = ReturnType<typeof BuildTabStateType>;

  const logger = createComponentLogger('SequenceActionsCoordinator');

  // Props
  let {
    buildTabState,
    panelState,
    show = $bindable()
  }: {
    buildTabState: BuildTabState;
    panelState: PanelCoordinationState;
    show: boolean;
  } = $props();

  // Event handlers
  function handleClose() {
    show = false;
  }

  function handleMirror() {
    // TODO: Implement mirror transformation
    logger.log("Mirror action triggered");
  }

  function handleRotate() {
    // TODO: Implement rotation transformation
    logger.log("Rotate action triggered");
  }

  function handleColorSwap() {
    // TODO: Implement color swap transformation
    logger.log("Color swap action triggered");
  }

  function handleCopyJSON() {
    if (!buildTabState.sequenceState.currentSequence) return;
    navigator.clipboard.writeText(
      JSON.stringify(buildTabState.sequenceState.currentSequence, null, 2)
    );
    logger.log("Sequence JSON copied to clipboard");
  }
</script>

<SequenceActionsSheet
  {show}
  hasSequence={buildTabState.hasSequence}
  combinedPanelHeight={panelState.combinedPanelHeight}
  onMirror={handleMirror}
  onRotate={handleRotate}
  onColorSwap={handleColorSwap}
  onCopyJSON={handleCopyJSON}
  onClose={handleClose}
/>
