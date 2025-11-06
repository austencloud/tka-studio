<script lang="ts">
  /**
   * Share Coordinator Component
   *
   * Manages share panel state and background preview generation.
   * Extracts share panel logic from CreateModule.svelte for better separation of concerns.
   *
   * Domain: Create module - Share Panel Coordination
   */

  import { createComponentLogger } from "$shared";
  import SharePanelSheet from "../../../share/components/SharePanelSheet.svelte";
  import { createShareState } from "../../../share/state";
  import { getCreateModuleContext } from "../../context";

  const logger = createComponentLogger("ShareCoordinator");

  // Get context
  const ctx = getCreateModuleContext();
  const { CreateModuleState, panelState, services } = ctx;
  const shareService = services.shareService;

  // Share state for background preview pre-rendering
  let backgroundShareState = $state<ReturnType<typeof createShareState> | null>(
    null
  );

  // Initialize background share state
  $effect(() => {
    if (shareService && !backgroundShareState) {
      backgroundShareState = createShareState(shareService);
    }
  });

  // Effect: Render share preview when sequence or options change
  // Renders both when panel is closed (pre-render) AND when panel is open (live updates)
  $effect(() => {
    if (!backgroundShareState) return;
    if (!CreateModuleState.sequenceState.currentSequence) return;

    const sequence = CreateModuleState.sequenceState.currentSequence;
    // Track options as dependency so effect re-runs when user changes share settings
    const options = backgroundShareState.options;
    // Track panel open state for logging purposes
    const isPanelOpen = panelState.isSharePanelOpen;

    // Render preview whenever sequence has beats (both panel open and closed)
    if (sequence.beats?.length > 0) {
      // Non-blocking generation - don't await
      // renderPictographToSVG now properly waits for async arrow/prop calculations
      backgroundShareState.generatePreview(sequence).catch((error) => {
        // Silent failure - preview will generate when user opens share panel
        logger.log(
          isPanelOpen
            ? "Live preview update failed:"
            : "Background preview pre-rendering skipped:",
          error
        );
      });
    }
  });

  // Event handler
  function handleClose() {
    panelState.closeSharePanel();
  }
</script>

<SharePanelSheet
  show={panelState.isSharePanelOpen}
  sequence={CreateModuleState.sequenceState.currentSequence}
  shareState={backgroundShareState}
  onClose={handleClose}
/>
