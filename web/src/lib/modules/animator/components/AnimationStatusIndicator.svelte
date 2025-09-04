<!--
AnimationStatusIndicator.svelte - Shows animation status and progress

Single responsibility: Display current animation state (playing/paused) and progress percentage.
No controls, no interaction - just pure status display.
-->
<script lang="ts">
  interface Props {
    isPlaying: boolean;
    progress: number;
  }

  let { isPlaying, progress }: Props = $props();

  let progressPercent = $derived(Math.round(progress * 100));
  let statusText = $derived(isPlaying ? "Playing" : "Paused");
</script>

<div class="status-indicator" role="status" aria-live="polite">
  <span
    class="status-text"
    aria-label={`Animation ${statusText} at ${progressPercent} percent`}
  >
    {statusText} • {progressPercent}%
  </span>
</div>

<style>
  .status-indicator {
    text-align: center;
  }

  .status-text {
    font-size: 12px;
    font-weight: 600;
    color: #a5b4fc;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
</style>
