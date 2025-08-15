<!--
SimpleGridToggle.svelte - Minimal grid mode toggle

A clean, simple toggle for switching between diamond and box grid modes.
Replaces the overcomplicated GridModeSelector with just essential functionality.
-->
<script lang="ts">
  import type { MotionTesterState } from "../state/motion-tester-state.svelte";

  interface Props {
    state: MotionTesterState;
  }

  let { state }: Props = $props();

  function toggleGridMode() {
    const newGridType = state.gridType === "diamond" ? "box" : "diamond";
    state.setGridType(newGridType);
  }

  function handleKeyDown(event: KeyboardEvent) {
    // Space or Enter to toggle
    if (event.code === "Space" || event.code === "Enter") {
      event.preventDefault();
      toggleGridMode();
    }
    // Number keys for quick selection
    if (event.key === "1") {
      event.preventDefault();
      if (state.gridType !== "diamond") {
        state.setGridType("diamond");
      }
    }
    if (event.key === "2") {
      event.preventDefault();
      if (state.gridType !== "box") {
        state.setGridType("box");
      }
    }
  }
</script>

<div class="grid-toggle" role="group" aria-label="Grid mode toggle">
  <button
    class="toggle-btn diamond-btn {state.gridType === 'diamond'
      ? 'active'
      : ''}"
    onclick={toggleGridMode}
    onkeydown={handleKeyDown}
    aria-pressed={state.gridType === "diamond"}
    aria-label="Diamond grid mode"
    title="Switch to diamond grid (1)"
  >
    <span class="icon" aria-hidden="true">◆</span>
  </button>

  <button
    class="toggle-btn box-btn {state.gridType === 'box' ? 'active' : ''}"
    onclick={toggleGridMode}
    onkeydown={handleKeyDown}
    aria-pressed={state.gridType === "box"}
    aria-label="Box grid mode"
    title="Switch to box grid (2)"
  >
    <span class="icon" aria-hidden="true">□</span>
  </button>
</div>

<style>
  .grid-toggle {
    display: flex;
    background: rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    overflow: hidden;
  }

  .toggle-btn {
    background: transparent;
    border: none;
    color: #c7d2fe;
    padding: 8px 12px;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 40px;
    position: relative;
  }

  .toggle-btn:hover {
    background: rgba(99, 102, 241, 0.2);
    color: white;
  }

  .toggle-btn:focus {
    outline: none;
    box-shadow: inset 0 0 0 2px rgba(99, 102, 241, 0.5);
  }

  .toggle-btn.active {
    background: rgba(99, 102, 241, 0.4);
    color: white;
    box-shadow: inset 0 0 0 1px rgba(99, 102, 241, 0.6);
  }

  .icon {
    font-size: 14px;
    font-weight: bold;
  }

  .diamond-btn.active .icon {
    color: #fbbf24;
  }

  .box-btn.active .icon {
    color: #60a5fa;
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    .grid-toggle {
      border: 2px solid white;
    }

    .toggle-btn.active {
      background: white;
      color: black;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .toggle-btn {
      transition: none;
    }
  }
</style>
