<!--
  MirrorModePanel.svelte - Mirror Mode (Side-by-Side Mirrored View)

  Shows one sequence alongside its mirrored version.
  Can toggle vertical/horizontal mirror axis.
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
</script>

<div class="mirror-mode-panel">
  {#if !animateState.primarySequence}
    <!-- Selection Prompt -->
    <div class="selection-prompt">
      <i class="fas fa-left-right" style="font-size: 5rem; opacity: 0.2;"></i>
      <h2>Mirror Mode</h2>
      <p>Animate one sequence side-by-side with its mirrored version</p>
      <button
        class="select-button"
        onclick={() => animateState.openSequenceBrowser("primary")}
      >
        <i class="fas fa-folder-open"></i>
        Select Sequence
      </button>
    </div>
  {:else}
    <!-- Mirror View -->
    <div class="mirror-view">
      <!-- Header -->
      <div class="header">
        <div class="sequence-info">
          <h3>{animateState.primarySequence.word || "Untitled"}</h3>
          <div class="mirror-indicator">
            <span>Original</span>
            <i class="fas fa-arrows-left-right"></i>
            <span>Mirrored ({animateState.mirrorAxis})</span>
          </div>
        </div>
        <button
          class="change-button"
          onclick={() => animateState.openSequenceBrowser("primary")}
        >
          <i class="fas fa-exchange-alt"></i>
          Change
        </button>
      </div>

      <!-- Canvas Area (Split View) -->
      <div class="canvas-split">
        <div class="canvas-half original">
          <div class="canvas-label">Original</div>
          <div class="placeholder">
            <i class="fas fa-user"></i>
          </div>
        </div>
        <div class="divider"></div>
        <div class="canvas-half mirrored">
          <div class="canvas-label">Mirrored</div>
          <div class="placeholder">
            <i class="fas fa-user" style="transform: scaleX(-1);"></i>
          </div>
        </div>
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

        <div class="mirror-settings">
          <button
            class="setting-btn"
            class:active={animateState.mirrorAxis === "vertical"}
            onclick={() => animateState.setMirrorAxis("vertical")}
          >
            <i class="fas fa-arrows-left-right"></i>
            Vertical
          </button>
          <button
            class="setting-btn"
            class:active={animateState.mirrorAxis === "horizontal"}
            onclick={() => animateState.setMirrorAxis("horizontal")}
          >
            <i class="fas fa-arrows-up-down"></i>
            Horizontal
          </button>
        </div>

        <button class="export-btn">
          <i class="fas fa-download"></i>
          Export
        </button>
      </div>
    </div>
  {/if}

  <SequenceBrowserPanel
    mode="primary"
    show={animateState.isSequenceBrowserOpen}
    onSelect={(seq) => {
      animateState.setPrimarySequence(seq);
      animateState.closeSequenceBrowser();
    }}
    onClose={animateState.closeSequenceBrowser}
  />
</div>

<style>
  .mirror-mode-panel {
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

  .mirror-view {
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

  .mirror-indicator {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    font-size: 0.875rem;
    opacity: 0.7;
    margin-top: 4px;
  }

  .canvas-split {
    flex: 1;
    display: flex;
    background: linear-gradient(
      135deg,
      rgba(20, 25, 35, 0.5) 0%,
      rgba(15, 20, 30, 0.5) 100%
    );
  }

  .canvas-half {
    flex: 1;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .canvas-label {
    position: absolute;
    top: var(--spacing-md);
    left: var(--spacing-md);
    padding: var(--spacing-xs) var(--spacing-md);
    background: rgba(0, 0, 0, 0.5);
    border-radius: var(--border-radius-sm);
    font-size: 0.75rem;
    font-weight: 600;
  }

  .placeholder {
    font-size: 5rem;
    opacity: 0.1;
  }

  .divider {
    width: 2px;
    background: linear-gradient(
      to bottom,
      transparent,
      rgba(255, 255, 255, 0.2),
      transparent
    );
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

  .mirror-settings {
    display: flex;
    gap: var(--spacing-sm);
    flex: 1;
  }

  .setting-btn {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-sm) var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-md);
    color: white;
    cursor: pointer;
    transition: all 0.2s;
  }

  .setting-btn.active {
    background: rgba(139, 92, 246, 0.3);
    border-color: rgba(139, 92, 246, 0.5);
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
