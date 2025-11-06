<script lang="ts">
  /**
   * Creation Workspace Area
   *
   * Wrapper for the actual workspace panel when a creation method has been selected.
   * Provides fade transitions and padding for the button panel at the bottom.
   *
   * Extracted from CreateModule to reduce component size.
   *
   * Domain: Create module - Workspace presentation
   */

  import { fade } from "svelte/transition";
  import WorkspacePanel from "../../../workspace-panel/core/WorkspacePanel.svelte";
  import type { createCreateModuleState as CreateModuleStateType } from "../state/create-module-state.svelte";
  import type { IToolPanelMethods } from "../types/create-module-types";

  type CreateModuleState = ReturnType<typeof CreateModuleStateType>;

  // Props
  let {
    CreateModuleState,
    practiceBeatIndex,
    animatingBeatNumber,
    isSideBySideLayout,
    isMobilePortrait,
    onPlayAnimation,
    animationStateRef,
  }: {
    CreateModuleState: CreateModuleState;
    practiceBeatIndex: number | null;
    animatingBeatNumber: number | null;
    isSideBySideLayout: boolean;
    isMobilePortrait: boolean;
    onPlayAnimation: () => void;
    animationStateRef: ReturnType<IToolPanelMethods["getAnimationStateRef"]>;
  } = $props();
</script>

<!-- Layout 2: Actual workspace when method is selected -->
<div
  class="workspace-panel-wrapper"
  in:fade={{ duration: 400, delay: 200 }}
  out:fade={{ duration: 300 }}
>
  <WorkspacePanel
    sequenceState={CreateModuleState.sequenceState}
    createModuleState={CreateModuleState}
    {practiceBeatIndex}
    {animatingBeatNumber}
    {isSideBySideLayout}
    {isMobilePortrait}
    {onPlayAnimation}
    {animationStateRef}
  />
</div>

<style>
  /* Workspace panel wrapper (Layout 2) */
  .workspace-panel-wrapper {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding-bottom: 80px; /* Space for button panel at bottom */
  }
</style>
