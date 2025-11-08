<!--
  GridModePanel.svelte - Grid Mode (2×2 Rotated Grid)

  Shows up to 4 sequences in a 2×2 grid with rotation offsets.
  Can use same sequence 4 times or different sequences.
-->
<script lang="ts">
  import type { AnimateModuleState } from "../shared/state/animate-module-state.svelte";
  import SequenceBrowserPanel from "../shared/components/SequenceBrowserPanel.svelte";

  // Props
  let {
    animateState,
  }: {
    animateState: AnimateModuleState;
  } = $props();

  const gridPositions = [
    { index: 0 as const, label: "Top-Left", icon: "fa-circle", rotation: 0 },
    { index: 1 as const, label: "Top-Right", icon: "fa-circle", rotation: 90 },
    {
      index: 2 as const,
      label: "Bottom-Left",
      icon: "fa-circle",
      rotation: 180,
    },
    {
      index: 3 as const,
      label: "Bottom-Right",
      icon: "fa-circle",
      rotation: 270,
    },
  ];

  const hasAnySequence = $derived(
    animateState.gridSequences.some((seq) => seq !== null)
  );
</script>

<div class="grid-mode-panel">
  {#if !hasAnySequence}
    <!-- Selection Prompt -->
    <div class="selection-prompt">
      <i class="fas fa-th" style="font-size: 5rem; opacity: 0.2;"></i>
      <h2>Grid Mode</h2>
      <p>Animate sequences in a 2×2 grid with rotation offsets</p>
      <button
        class="select-button"
        onclick={() => animateState.openSequenceBrowser("grid-0")}
      >
        <i class="fas fa-grid-2"></i>
        Configure Grid
      </button>
    </div>
  {:else}
    <!-- Grid View -->
    <div class="grid-view">
      <!-- Header -->
      <div class="header">
        <h3>Grid Animation</h3>
        <button
          class="reset-button"
          onclick={() => {
            animateState.setGridSequence(0, null);
            animateState.setGridSequence(1, null);
            animateState.setGridSequence(2, null);
            animateState.setGridSequence(3, null);
          }}
        >
          <i class="fas fa-redo"></i>
          Reset Grid
        </button>
      </div>

      <!-- 2×2 Grid Canvas -->
      <div class="grid-canvas">
        {#each gridPositions as pos}
          <button
            class="grid-cell"
            class:filled={animateState.gridSequences[pos.index]}
            onclick={() =>
              animateState.openSequenceBrowser(`grid-${pos.index}`)}
          >
            {#if animateState.gridSequences[pos.index]}
              <div class="cell-header">
                <span class="rotation-badge"
                  >{animateState.gridRotationOffsets[pos.index]}°</span
                >
                <div
                  class="remove-btn"
                  role="button"
                  tabindex="0"
                  aria-label="Remove sequence"
                  onclick={(e) => {
                    e.stopPropagation();
                    animateState.setGridSequence(pos.index, null);
                  }}
                  onkeydown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                      e.preventDefault();
                      e.stopPropagation();
                      animateState.setGridSequence(pos.index, null);
                    }
                  }}
                >
                  <i class="fas fa-times"></i>
                </div>
              </div>
              <div class="cell-content">
                <div class="placeholder-icon">
                  <i
                    class="fas fa-user"
                    style="transform: rotate({animateState.gridRotationOffsets[
                      pos.index
                    ]}deg);"
                  ></i>
                </div>
                <div class="sequence-name">
                  {animateState.gridSequences[pos.index]!.word || "Untitled"}
                </div>
              </div>
            {:else}
              <div class="empty-cell">
                <i class="fas fa-plus"></i>
                <span>{pos.label}</span>
              </div>
            {/if}
          </button>
        {/each}
      </div>

      <!-- Controls -->
      <div class="controls">
        <div class="playback">
          <button class="control-btn" aria-label="Play animation"
            ><i class="fas fa-play"></i></button
          >
          <button class="control-btn" aria-label="Stop animation"
            ><i class="fas fa-stop"></i></button
          >
          <button class="control-btn" aria-label="Loop animation"
            ><i class="fas fa-repeat"></i></button
          >
        </div>

        <div class="grid-settings">
          <div class="setting-group">
            <label for="grid-mode-speed"
              ><i class="fas fa-gauge"></i> Speed</label
            >
            <input
              id="grid-mode-speed"
              type="range"
              min="0.5"
              max="2"
              step="0.1"
              value={animateState.speed}
              oninput={(e) =>
                animateState.setSpeed(parseFloat(e.currentTarget.value))}
            />
            <span>{animateState.speed.toFixed(1)}x</span>
          </div>
        </div>

        <button class="export-btn">
          <i class="fas fa-download"></i>
          Export Grid
        </button>
      </div>
    </div>
  {/if}

  <SequenceBrowserPanel
    mode={animateState.browserMode}
    show={animateState.isSequenceBrowserOpen}
    onSelect={(seq) => {
      const mode = animateState.browserMode;
      if (mode === "grid-0") animateState.setGridSequence(0, seq);
      else if (mode === "grid-1") animateState.setGridSequence(1, seq);
      else if (mode === "grid-2") animateState.setGridSequence(2, seq);
      else if (mode === "grid-3") animateState.setGridSequence(3, seq);
      animateState.closeSequenceBrowser();
    }}
    onClose={animateState.closeSequenceBrowser}
  />
</div>

<style>
  .grid-mode-panel {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
  }

  .selection-prompt {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: var(--spacing-lg);
  }

  .select-button {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-md) var(--spacing-xl);
    background: linear-gradient(135deg, #ec4899, #8b5cf6);
    border: none;
    border-radius: var(--border-radius-lg);
    color: white;
    font-weight: 600;
    cursor: pointer;
  }

  .grid-view {
    display: flex;
    flex-direction: column;
    height: 100%;
  }

  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  }

  .grid-canvas {
    flex: 1;
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 2px;
    background: rgba(255, 255, 255, 0.1);
    padding: 2px;
  }

  .grid-cell {
    position: relative;
    background: linear-gradient(
      135deg,
      rgba(20, 25, 35, 0.8) 0%,
      rgba(15, 20, 30, 0.8) 100%
    );
    border: 2px solid rgba(255, 255, 255, 0.1);
    cursor: pointer;
    transition: all 0.2s;
    overflow: hidden;
  }

  .grid-cell:hover {
    border-color: rgba(236, 72, 153, 0.5);
    transform: scale(1.02);
  }

  .grid-cell.filled {
    border-color: rgba(16, 185, 129, 0.3);
  }

  .cell-header {
    position: absolute;
    top: var(--spacing-sm);
    left: var(--spacing-sm);
    right: var(--spacing-sm);
    display: flex;
    justify-content: space-between;
    z-index: 1;
  }

  .rotation-badge {
    padding: 4px 8px;
    background: rgba(139, 92, 246, 0.3);
    border: 1px solid rgba(139, 92, 246, 0.5);
    border-radius: var(--border-radius-sm);
    font-size: 0.75rem;
    font-weight: 600;
  }

  .remove-btn {
    width: 24px;
    height: 24px;
    background: rgba(239, 68, 68, 0.3);
    border: 1px solid rgba(239, 68, 68, 0.5);
    border-radius: 50%;
    color: white;
    cursor: pointer;
  }

  .cell-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: var(--spacing-md);
  }

  .placeholder-icon {
    font-size: 4rem;
    opacity: 0.3;
  }

  .sequence-name {
    font-weight: 600;
    font-size: 0.875rem;
  }

  .empty-cell {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: var(--spacing-sm);
    opacity: 0.3;
  }

  .empty-cell i {
    font-size: 3rem;
  }

  .controls {
    display: flex;
    gap: var(--spacing-xl);
    padding: var(--spacing-lg);
    background: rgba(255, 255, 255, 0.05);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }

  .playback {
    display: flex;
    gap: var(--spacing-sm);
  }

  .control-btn {
    width: 44px;
    height: 44px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    color: white;
    cursor: pointer;
  }

  .grid-settings {
    flex: 1;
  }

  .setting-group {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    max-width: 300px;
  }

  .setting-group label {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    font-size: 0.875rem;
  }

  .setting-group input {
    flex: 1;
  }

  .export-btn {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-lg);
    background: linear-gradient(135deg, #10b981, #059669);
    border: none;
    border-radius: var(--border-radius-md);
    color: white;
    font-weight: 600;
    cursor: pointer;
  }
</style>
