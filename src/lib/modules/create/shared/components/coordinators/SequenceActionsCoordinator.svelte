<script lang="ts">
  /**
   * Sequence Actions Coordinator Component
   *
   * Manages sequence transformation actions (mirror, rotate, color swap, copy JSON).
   * Extracts sequence actions logic from CreateModule.svelte for better separation of concerns.
   *
   * Domain: Create module - Sequence Transformation Coordination
   */

  import { createComponentLogger } from "$shared";
  import SequenceActionsSheet from "../../../workspace-panel/shared/components/SequenceActionsSheet.svelte";
  import { getCreateModuleContext } from "../../context";

  const logger = createComponentLogger("SequenceActionsCoordinator");

  // Get context
  const ctx = getCreateModuleContext();
  const { CreateModuleState, panelState } = ctx;

  const isSheetOpen = $derived.by(() => panelState.isSequenceActionsPanelOpen);

  // Event handlers
  function handleClose() {
    logger.log("SequenceActionsCoordinator closing sequence actions panel");
    panelState.closeSequenceActionsPanel();
  }

  // Debug effect to track sheet visibility
  $effect(() => {
    logger.log(
      "SequenceActionsCoordinator sheet state changed:",
      panelState.isSequenceActionsPanelOpen
    );
  });

  async function handleMirror() {
    const currentSequence = CreateModuleState.sequenceState.currentSequence;
    if (!currentSequence) {
      logger.warn("No sequence to mirror");
      return;
    }

    logger.log("Mirroring sequence vertically (including start position)");
    await CreateModuleState.sequenceState.mirrorSequence();
    logger.log("✅ Sequence mirrored and saved successfully");
  }

  async function handleRotate() {
    const currentSequence = CreateModuleState.sequenceState.currentSequence;
    if (!currentSequence) {
      logger.warn("No sequence to rotate");
      return;
    }

    logger.log("Rotating sequence 90° clockwise (including start position)");
    await CreateModuleState.sequenceState.rotateSequence("clockwise");
    logger.log("✅ Sequence rotated and saved successfully");
  }

  async function handleColorSwap() {
    const currentSequence = CreateModuleState.sequenceState.currentSequence;
    if (!currentSequence) {
      logger.warn("No sequence to color swap");
      return;
    }

    logger.log(
      "Swapping sequence colors (blue ↔ red, including start position)"
    );
    await CreateModuleState.sequenceState.swapColors();
    logger.log("✅ Sequence colors swapped and saved successfully");
  }

  async function handleReverse() {
    const currentSequence = CreateModuleState.sequenceState.currentSequence;
    if (!currentSequence) {
      logger.warn("No sequence to reverse");
      return;
    }

    logger.log("Reversing sequence (playing backwards)");
    await CreateModuleState.sequenceState.reverseSequence();
    logger.log("✅ Sequence reversed and saved successfully");
  }

  function handleCopyJSON() {
    if (!CreateModuleState.sequenceState.currentSequence) return;
    navigator.clipboard.writeText(
      JSON.stringify(CreateModuleState.sequenceState.currentSequence, null, 2)
    );
    logger.log("Sequence JSON copied to clipboard");
  }
</script>

<SequenceActionsSheet
  show={isSheetOpen}
  hasSequence={CreateModuleState.hasSequence}
  combinedPanelHeight={panelState.combinedPanelHeight}
  onMirror={handleMirror}
  onRotate={handleRotate}
  onColorSwap={handleColorSwap}
  onReverse={handleReverse}
  onCopyJSON={handleCopyJSON}
  onClose={handleClose}
/>
