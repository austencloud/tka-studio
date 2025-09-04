<script lang="ts">
  import type { Snippet } from "svelte";

  /**
   * Vertical Button Panel living inside the Workbench (right side)
   * Pure runes props + callbacks. No stores.
   */

  interface Props {
    disabled?: boolean;
    hasSelection?: boolean;
    onAddToDictionary?: () => void;
    onFullscreen?: () => void;
    onMirror?: () => void;
    onSwapColors?: () => void;
    onRotate?: () => void;
    onCopyJson?: () => void;
    onDeleteBeat?: () => void;
    onClearSequence?: () => void;
    // Optional additional render content
    renderExtra?: Snippet;
  }

  let {
    disabled = false,
    hasSelection = false,
    onAddToDictionary,
    onFullscreen,
    onMirror,
    onSwapColors,
    onRotate,
    onCopyJson,
    onDeleteBeat,
    onClearSequence,
    renderExtra,
  }: Props = $props();

  function handle(fn?: () => void) {
    if (disabled) return;
    fn?.();
  }
</script>

<div class="button-panel" aria-label="Workbench Controls">
  <!-- Dictionary & View Group -->
  <div class="button-group">
    <button
      type="button"
      class="panel-btn"
      title="Add to Dictionary"
      onclick={() => handle(onAddToDictionary)}
    >
      📚
    </button>
    <button
      type="button"
      class="panel-btn"
      title="Fullscreen"
      onclick={() => handle(onFullscreen)}
    >
      👁️
    </button>
  </div>

  <!-- Visual Separator -->
  <div class="separator"></div>

  <!-- Transform Group -->
  <div class="button-group">
    <button
      type="button"
      class="panel-btn"
      title="Mirror Sequence"
      onclick={() => handle(onMirror)}
    >
      🪞
    </button>
    <button
      type="button"
      class="panel-btn"
      title="Swap Colors"
      onclick={() => handle(onSwapColors)}
    >
      🎨
    </button>
    <button
      type="button"
      class="panel-btn"
      title="Rotate Sequence"
      onclick={() => handle(onRotate)}
    >
      🔄
    </button>
  </div>

  <!-- Visual Separator -->
  <div class="separator"></div>

  <!-- Sequence Management Group -->
  <div class="button-group">
    <button
      type="button"
      class="panel-btn"
      title="Copy JSON"
      onclick={() => handle(onCopyJson)}
    >
      📋
    </button>
    <button
      type="button"
      class="panel-btn"
      title="Delete Beat"
      disabled={!hasSelection || disabled}
      onclick={() => handle(onDeleteBeat)}
    >
      🗑️
    </button>
    <button
      type="button"
      class="panel-btn"
      title="Clear Sequence"
      onclick={() => handle(onClearSequence)}
    >
      🧹
    </button>
  </div>

  {#if renderExtra}
    {@render renderExtra()}
  {/if}
</div>

<style>
  .button-panel {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center; /* Center buttons vertically */
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    min-width: 80px;
    height: 100%; /* Take full height to enable centering */

    /* Glassmorphism panel styling with reduced opacity to avoid visual conflict */
    background: rgba(255, 255, 255, 0.04); /* Reduced from 0.08 */
    border: 1px solid rgba(255, 255, 255, 0.08); /* More subtle border */
    border-radius: 12px;
    box-shadow:
      0 4px 16px rgba(0, 0, 0, 0.08),
      0 2px 8px rgba(0, 0, 0, 0.04),
      inset 0 1px 0 rgba(255, 255, 255, 0.05); /* Reduced shadow intensity */

    /* Position relative for pseudo-element */
    position: relative;
  }

  .button-panel::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    border-radius: 12px;
    padding: 1px;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.1),
      rgba(255, 255, 255, 0.02)
    );
    mask:
      linear-gradient(#fff 0 0) content-box,
      linear-gradient(#fff 0 0);
    mask-composite: xor;
    pointer-events: none;
  }

  .button-group {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
    align-items: center;
  }

  .separator {
    width: 24px;
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.3),
      transparent
    );
    margin: var(--spacing-xs) 0;
  }

  .panel-btn {
    width: 52px;
    height: 52px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    cursor: pointer;
    font-size: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all var(--transition-normal);
    color: rgba(255, 255, 255, 0.9);
    font-weight: 500;

    /* Subtle inner shadow for depth */
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.1),
      0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .panel-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.15),
      0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .panel-btn:active:not(:disabled) {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(0);
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.2),
      0 2px 6px rgba(0, 0, 0, 0.2);
  }

  .panel-btn:disabled {
    background: rgba(200, 200, 200, 0.05);
    border-color: rgba(200, 200, 200, 0.1);
    color: rgba(255, 255, 255, 0.3);
    cursor: not-allowed;
    transform: none;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
  }
</style>
