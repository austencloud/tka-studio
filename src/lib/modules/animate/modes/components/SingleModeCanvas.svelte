<!--
  SingleModeCanvas.svelte
  
  Full-screen animation canvas for Single mode.
  Wraps AnimationSheetCoordinator with proper sizing and layout.
-->
<script lang="ts">
  import AnimationSheetCoordinator from "$shared/coordinators/AnimationSheetCoordinator.svelte";
  import type { SequenceData } from "$shared";

  // Props
  let {
    sequence,
    isPlaying = $bindable(),
    animatingBeatNumber = $bindable(),
  }: {
    sequence: SequenceData;
    isPlaying?: boolean;
    animatingBeatNumber?: number | null;
  } = $props();

  // Local state
  let showAnimator = $state(true);
</script>

<div class="single-mode-canvas">
  <AnimationSheetCoordinator
    {sequence}
    bind:isOpen={showAnimator}
    bind:animatingBeatNumber
    combinedPanelHeight={0}
  />
</div>

<style>
  .single-mode-canvas {
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--color-background-primary, #1a1a1a);
  }
</style>

