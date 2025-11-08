<!--
DeleteTools.svelte - Sequence Deletion Tools

Handles sequence deletion operations like delete beat and clear sequence.
Pure presentation component that delegates to deletion services.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import type { Snippet } from "svelte";
  import { onMount } from "svelte";

  let {
    disabled = false,
    hasSelection = false,
    hasSequence = false,
    onDeleteBeat,
    onClearSequence,
    renderExtra,
  } = $props<{
    disabled?: boolean;
    hasSelection?: boolean;
    hasSequence?: boolean;
    onDeleteBeat?: () => void;
    onClearSequence?: () => void;
    renderExtra?: Snippet;
  }>();

  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleWithSelection(fn?: () => void) {
    if (disabled || !hasSelection) return;
    hapticService?.trigger("warning");
    fn?.();
  }

  function handleWithSequence(fn?: () => void) {
    if (disabled || !hasSequence) return;
    hapticService?.trigger("warning");
    fn?.();
  }
</script>

<div class="delete-tools">
  <button
    type="button"
    class="tool-btn"
    title="Delete Beat"
    disabled={!hasSelection || disabled}
    onclick={() => handleWithSelection(onDeleteBeat)}
  >
    🗑️
  </button>

  <button
    type="button"
    class="tool-btn"
    title="Clear"
    disabled={!hasSequence || disabled}
    onclick={() => handleWithSequence(onClearSequence)}
  >
    🧹
  </button>

  {#if renderExtra}
    {@render renderExtra()}
  {/if}
</div>

<style>
  .delete-tools {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xs);
  }

  .tool-btn {
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

  .tool-btn:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.15),
      0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .tool-btn:active:not(:disabled) {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(0);
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.2),
      0 2px 6px rgba(0, 0, 0, 0.2);
  }

  .tool-btn:disabled {
    background: rgba(200, 200, 200, 0.05);
    border-color: rgba(200, 200, 200, 0.1);
    color: rgba(255, 255, 255, 0.3);
    cursor: not-allowed;
    transform: none;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
  }

  /* Focus styles for accessibility */
  .tool-btn:focus-visible {
    outline: 2px solid #818cf8;
    outline-offset: 2px;
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .delete-tools {
      flex-direction: row; /* Horizontal layout on mobile */
      gap: var(--spacing-sm);
    }

    .tool-btn {
      width: 48px; /* Larger touch targets on mobile */
      height: 48px;
      font-size: 18px;
    }
  }

  /* Ultra-narrow mobile optimization */
  @media (max-width: 480px) {
    .delete-tools {
      gap: var(--spacing-xs);
    }

    .tool-btn {
      width: 44px; /* Minimum touch target size */
      height: 44px;
      font-size: 16px;
    }
  }

  /* Z Fold 6 cover screen optimization */
  @media (max-width: 320px) {
    .delete-tools {
      gap: 2px;
    }

    .tool-btn {
      width: 40px;
      height: 40px;
      font-size: 14px;
      border-radius: 8px;
    }
  }
</style>
