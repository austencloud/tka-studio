<script lang="ts">
  import { onMount } from 'svelte';

  // Props
  const { enabled = $bindable(false) } = $props<{
    enabled?: boolean;
  }>();

  // State
  let insets = $state({
    top: '0px',
    right: '0px',
    bottom: '0px',
    left: '0px'
  });

  // Update inset values
  function updateInsets() {
    if (typeof window === 'undefined') return;

    // Get computed values from CSS variables
    const computedStyle = getComputedStyle(document.documentElement);
    insets = {
      top: computedStyle.getPropertyValue('--safe-inset-top') || '0px',
      right: computedStyle.getPropertyValue('--safe-inset-right') || '0px',
      bottom: computedStyle.getPropertyValue('--safe-inset-bottom') || '0px',
      left: computedStyle.getPropertyValue('--safe-inset-left') || '0px'
    };
  }

  onMount(() => {
    updateInsets();

    // Update on resize and orientation change
    window.addEventListener('resize', updateInsets);
    window.addEventListener('orientationchange', updateInsets);

    return () => {
      window.removeEventListener('resize', updateInsets);
      window.removeEventListener('orientationchange', updateInsets);
    };
  });
</script>

{#if enabled}
  <div class="safe-area-visualizer">
    <!-- Top inset -->
    <div class="inset-indicator top" style="height: {insets.top};">
      <span class="inset-label">Top: {insets.top}</span>
    </div>

    <!-- Right inset -->
    <div class="inset-indicator right" style="width: {insets.right};">
      <span class="inset-label">Right: {insets.right}</span>
    </div>

    <!-- Bottom inset -->
    <div class="inset-indicator bottom" style="height: {insets.bottom};">
      <span class="inset-label">Bottom: {insets.bottom}</span>
    </div>

    <!-- Left inset -->
    <div class="inset-indicator left" style="width: {insets.left};">
      <span class="inset-label">Left: {insets.left}</span>
    </div>
  </div>
{/if}

<style>
  .safe-area-visualizer {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 10000;
  }

  .inset-indicator {
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(255, 0, 0, 0.3);
    border: 1px dashed rgba(255, 0, 0, 0.8);
    box-sizing: border-box;
    overflow: hidden;
  }

  .inset-indicator.top {
    top: 0;
    left: 0;
    width: 100%;
  }

  .inset-indicator.right {
    top: 0;
    right: 0;
    height: 100%;
  }

  .inset-indicator.bottom {
    bottom: 0;
    left: 0;
    width: 100%;
  }

  .inset-indicator.left {
    top: 0;
    left: 0;
    height: 100%;
  }

  .inset-label {
    font-size: 10px;
    color: white;
    background-color: rgba(0, 0, 0, 0.7);
    padding: 2px 4px;
    border-radius: 4px;
    white-space: nowrap;
    text-shadow: 0 0 2px black;
  }
</style>
