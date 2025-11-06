<script lang="ts">
  /**
   * Sequence Actions Coordinator Component
   *
   * Manages sequence transformation actions (mirror, rotate, color swap, copy JSON).
   * Extracts sequence actions logic from CreateModule.svelte for better separation of concerns.
   *
   * Domain: Create module - Sequence Transformation Coordination
   */

  import { createComponentLogger, resolve, TYPES } from "$shared";
  import SequenceActionsSheet from "../../../workspace-panel/shared/components/SequenceActionsSheet.svelte";
  import { getCreateModuleContext } from "../../context";
  import type { ISequenceTransformationService } from "../../services/contracts/ISequenceTransformationService";

  const logger = createComponentLogger("SequenceActionsCoordinator");

  // Get context
  const ctx = getCreateModuleContext();
  const { CreateModuleState, panelState } = ctx;

  // Resolve service
  const transformationService = resolve<ISequenceTransformationService>(
    TYPES.ISequenceTransformationService
  );

  // Props (only bindable props remain)
  let {
    show = $bindable(),
  }: {
    show: boolean;
  } = $props();

  // Event handlers
  function handleClose() {
    show = false;
  }

  function handleMirror() {
    const currentSequence = CreateModuleState.sequenceState.currentSequence;
    if (!currentSequence) {
      logger.warn("No sequence to mirror");
      return;
    }

    logger.log("Mirroring sequence vertically");
    const mirroredSequence = transformationService.mirrorSequence(currentSequence);
    CreateModuleState.sequenceState.setCurrentSequence(mirroredSequence);
    logger.log("✅ Sequence mirrored successfully");
  }

  function handleRotate() {
    const currentSequence = CreateModuleState.sequenceState.currentSequence;
    if (!currentSequence) {
      logger.warn("No sequence to rotate");
      return;
    }

    logger.log("Rotating sequence 90° clockwise");
    const rotatedSequence = transformationService.rotateSequence(currentSequence, 90);
    CreateModuleState.sequenceState.setCurrentSequence(rotatedSequence);
    logger.log("✅ Sequence rotated successfully");
  }

  function handleColorSwap() {
    const currentSequence = CreateModuleState.sequenceState.currentSequence;
    if (!currentSequence) {
      logger.warn("No sequence to color swap");
      return;
    }

    logger.log("Swapping sequence colors (blue ↔ red)");
    const swappedSequence = transformationService.swapColors(currentSequence);
    CreateModuleState.sequenceState.setCurrentSequence(swappedSequence);
    logger.log("✅ Sequence colors swapped successfully");
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
  {show}
  hasSequence={CreateModuleState.hasSequence}
  combinedPanelHeight={panelState.combinedPanelHeight}
  onMirror={handleMirror}
  onRotate={handleRotate}
  onColorSwap={handleColorSwap}
  onCopyJSON={handleCopyJSON}
  onClose={handleClose}
/>
