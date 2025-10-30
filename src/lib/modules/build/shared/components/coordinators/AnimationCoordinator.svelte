<script lang="ts">
  /**
   * Animation Coordinator Component
   *
   * Manages animation panel state and beat tracking during animation playback.
   * Extracts animation panel logic from BuildTab.svelte for better separation of concerns.
   *
   * Domain: Build Module - Animation Panel Coordination
   */

  import AnimationPanel from "../../../animate/components/AnimationPanel.svelte";
  import type { PanelCoordinationState } from "../../state/panel-coordination-state.svelte";
  import type { createBuildTabState as BuildTabStateType } from "../../state/build-tab-state.svelte";

  type BuildTabState = ReturnType<typeof BuildTabStateType>;

  // Props
  let {
    buildTabState,
    panelState,
    animatingBeatNumber = $bindable()
  }: {
    buildTabState: BuildTabState;
    panelState: PanelCoordinationState;
    animatingBeatNumber?: number | null;
  } = $props();

  // Event handlers
  function handleClose() {
    panelState.closeAnimationPanel();
    // Clear animating beat when panel closes
    animatingBeatNumber = null;
  }

  function handleAnimatingBeatChange(beatNumber: number) {
    animatingBeatNumber = beatNumber;
  }
</script>

<AnimationPanel
  sequence={buildTabState.sequenceState.currentSequence}
  show={panelState.isAnimationPanelOpen}
  onClose={handleClose}
  onCurrentBeatChange={handleAnimatingBeatChange}
  combinedPanelHeight={panelState.combinedPanelHeight}
/>
