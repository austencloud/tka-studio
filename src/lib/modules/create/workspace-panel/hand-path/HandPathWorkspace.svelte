<!--
HandPathWorkspace.svelte - Hand Path Drawing Workspace

Workspace area for drawing hand paths via touch gestures.
Hidden until user clicks "Start Drawing", then animates in.
Integrates with standard Workspace/ToolPanel layout.
-->
<script lang="ts">
  import { GridMode } from "$shared";
  import { slide } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import TouchableGrid from "../../construct/handpath-builder/components/TouchableGrid.svelte";
  import type { GesturalPathState } from "../../construct/handpath-builder/state";

  // Props
  let {
    pathState,
    isStarted = false,
    onSegmentComplete,
    onAdvancePressed,
    onAdvanceReleased,
  }: {
    pathState: GesturalPathState;
    isStarted: boolean;
    onSegmentComplete: (start: any, end: any) => void;
    onAdvancePressed: () => void;
    onAdvanceReleased: () => void;
  } = $props();
</script>

{#if isStarted}
  <div
    class="hand-path-workspace"
    data-testid="hand-path-workspace"
    in:slide={{ duration: 400, easing: cubicOut, axis: "y" }}
  >
    <TouchableGrid
      {pathState}
      gridMode={pathState.config?.gridMode || GridMode.DIAMOND}
      {onSegmentComplete}
      {onAdvancePressed}
      {onAdvanceReleased}
    />
  </div>
{/if}

<style>
  .hand-path-workspace {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    min-height: 0;
    width: 100%;
  }
</style>
