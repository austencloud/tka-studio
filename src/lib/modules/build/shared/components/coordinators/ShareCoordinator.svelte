<script lang="ts">
  /**
   * Share Coordinator Component
   *
   * Manages share panel state and background preview generation.
   * Extracts share panel logic from BuildTab.svelte for better separation of concerns.
   *
   * Domain: Build Module - Share Panel Coordination
   */

  import { createComponentLogger } from "$shared";
  import SharePanelSheet from "../../../share/components/SharePanelSheet.svelte";
  import type { IShareService } from "../../../share/services/contracts";
  import { createShareState } from "../../../share/state";
  import type { PanelCoordinationState } from "../../state/panel-coordination-state.svelte";
  import type { createBuildTabState as BuildTabStateType } from "../../state/build-tab-state.svelte";

  type BuildTabState = ReturnType<typeof BuildTabStateType>;

  const logger = createComponentLogger('ShareCoordinator');

  // Props
  let {
    buildTabState,
    panelState,
    shareService
  }: {
    buildTabState: BuildTabState;
    panelState: PanelCoordinationState;
    shareService: IShareService;
  } = $props();

  // Share state for background preview pre-rendering
  let backgroundShareState = $state<ReturnType<typeof createShareState> | null>(null);

  // Initialize background share state
  $effect(() => {
    if (shareService && !backgroundShareState) {
      backgroundShareState = createShareState(shareService);
    }
  });

  // Effect: Background pre-render share preview when sequence exists
  // This makes the share panel instantly show preview on first open
  $effect(() => {
    if (!backgroundShareState) return;
    if (!buildTabState.sequenceState.currentSequence) return;

    const sequence = buildTabState.sequenceState.currentSequence;

    // Only pre-render if sequence has beats
    if (sequence.beats?.length > 0) {
      // Non-blocking background generation - don't await
      backgroundShareState.generatePreview(sequence).catch((error) => {
        // Silent failure - preview will generate when user opens share panel
        logger.log("Background preview pre-rendering skipped:", error);
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
  sequence={buildTabState.sequenceState.currentSequence}
  onClose={handleClose}
/>
