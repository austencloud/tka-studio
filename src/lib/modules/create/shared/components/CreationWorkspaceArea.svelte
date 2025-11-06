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
  import type { IToolPanelMethods } from "../types/create-module-types";
  import { WorkspacePanel } from "../../workspace-panel";
  import { getCreateModuleContext } from "../context";

  // Get context
  const ctx = getCreateModuleContext();
  const { CreateModuleState, panelState, layout } = ctx;

  // Props (only presentation-specific props)
  let {
    animatingBeatNumber,
    onPlayAnimation,
    animationStateRef,
  }: {
    animatingBeatNumber: number | null;
    onPlayAnimation: () => void;
    animationStateRef?: ReturnType<IToolPanelMethods["getAnimationStateRef"]>;
  } = $props();

  // Derive values from context
  const practiceBeatIndex = $derived(panelState.practiceBeatIndex);
  const isSideBySideLayout = $derived(layout.shouldUseSideBySideLayout);
  const isMobilePortrait = $derived(layout.isMobilePortrait());
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
